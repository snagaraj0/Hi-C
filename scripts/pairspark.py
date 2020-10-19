import findspark
findspark.init()
from pyspark import SparkConf, SparkContext, TaskContext, SparkFiles
import math
import os
import time
from pyspark.sql import SQLContext
import subprocess
import sys
import pydoop.hdfs as hdfs
import logging

test_input = sys.argv[1]
o_input = sys.argv[2]
direc_path = sys.argv[3]
exec_mem = sys.argv[4]
driver_mem = sys.argv[5]
max_cores = sys.argv[6]
exec_instances = sys.argv[7]
options = sys.argv[8]

logging.basicConfig(filename='pairspark.log', filemode='w', level=logging.INFO)
conf = SparkConf().setAppName("SparkHDFSTEST")
conf = conf.set('spark.submit.deploymode', "cluster")
conf = conf.set('spark.executor.memory', exec_mem).set('spark.driver.memory', driver_mem).set("spark.cores.max", max_cores).set("spark.executor.instances", exec_instances)
sc = SparkContext.getOrCreate(conf=conf)
sc.setLogLevel("ERROR")
logging.info(sc.getConf().getAll())

subprocess.call(["hdfs", "dfs", "-mkdir", "-p", "/user"])
subprocess.call(["hdfs", "dfs", "-mkdir", "-p", "/user/data"])
subprocess.call(["hdfs", "dfs", "-put", test_input, "/user/data" ])
subprocess.call(["hdfs", "dfs", "-put", o_input, "/user/data" ])

test_input = test_input.split('/')
end_input = test_input[len(test_input) - 1]

o_input = o_input.split('/')
end_o_input = o_input[len(o_input)- 1]

logging.info(direc_path)

input_file = "hdfs:/user/data/" + end_input
print(input_file)

input_file1 = "hdfs:/user/data/" + end_o_input
print(input_file1)

#Uncomment to document time
start = time.time()
# create key-value pair with (read on line, line number)
zipped_input = (sc.textFile(input_file)).zipWithIndex()
zipped_input1 = (sc.textFile(input_file1)).zipWithIndex()

add = zipped_input.keyBy(lambda x: math.floor(x[1]/4))
add1 = zipped_input1.keyBy(lambda x: math.floor(x[1]/4))

logging.info("Zipped FastQ 1", add.takeOrdered(4))
logging.info("Zipped FastQ 2", add1.takeOrdered(4))

add = zipped_input.keyBy(lambda x: math.floor(x[1]/4))
add1 = zipped_input1.keyBy(lambda x: math.floor(x[1]/4))

# Combine all strings with the same key together 
def joining_func(line):
    sort_tup = sorted(line[1], key = lambda x: x[1])
    return (line[0],'\n'.join([y[0] for y in sort_tup]))

rdd_add = add.groupByKey().map(joining_func)
rdd_add1 = add1.groupByKey().map(joining_func)

#Join (key, value) pairs for both mates together
combineRDD = rdd_add.join(rdd_add1)
logging.info("Joined FastQ zips", combineRDD.takeOrdered(8))
rdd_add.unpersist()
rdd_add1.unpersist()

#Map Paired-end mates together into one entry
combinedRDD = combineRDD.mapValues(lambda x: x[0] + "\n"+ x[1]).values()
logging.info(combineRDD.take(20))

#starts mapper with parameters to index and options.
try:
  alignment_pipe = combinedRDD.pipe(options)
except:
  print("Could not perform mapping. Check syntax of mapper options")

logging.info(alignment_pipe.take(20))
logging.info("Number of partitions:" + str(alignment_pipe.getNumPartitions()))

# Write partitions to SAM file
alignment_pipe.saveAsTextFile(direc_path)

#Uncomment for process timing
#
end = time.time()
logging.info("Runtime: " + str(end-start))
sc.stop()
