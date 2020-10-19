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

fq_input = sys.argv[1]
direc_path = sys.argv[2]
exec_mem = sys.argv[3]
driver_mem = sys.argv[4]
max_cores = sys.argv[5]
exec_instances = sys.argv[6]
options = sys.argv[7]

conf = SparkConf().setAppName("SingleSparkAligner")
conf = conf.set('spark.submit.deploymode', "cluster")
conf = conf.set('spark.executor.memory', exec_mem).set('spark.driver.memory', driver_mem).set("spark.cores.max", max_cores).set("spark.executor.instances", exec_instances)
sc = SparkContext.getOrCreate(conf=conf)
sc.setLogLevel("ERROR")
logging.basicConfig(filename='singlespark.log', filemode='w', level=logging.INFO)
logging.getLogger().setLevel(logging.INFO)
logging.info(sc.getConf().getAll())

subprocess.call(["hdfs", "dfs", "-mkdir", "-p", "/user"])
subprocess.call(["hdfs", "dfs", "-mkdir", "-p", "/user/data"])
subprocess.call(["hdfs", "dfs", "-put", fq_input, "/user/data" ])

filestr = direc_path
logging.info(filestr)
    
fq_input = fq_input.split('/')
test_len = len(fq_input) - 1
end_input = fq_input[test_len]

input_file = "hdfs:/user/data/" + end_input
print(input_file)

# Uncomment for process timing
start = time.time()
# create key-value pair with (read on line, line number)
zipped_input = (sc.textFile(input_file)).zipWithIndex()

add = zipped_input.keyBy(lambda x: math.floor(x[1]/4))
logging.info("Zipped FastQ", add.takeOrdered(4))

# Combine all strings with the same key together
def joining_func(line):
    sort_tup = sorted(line[1], key = lambda x: x[1])
    return '\n'.join([y[0] for y in sort_tup])

#Group all lines with the same Key and join them together by their original position in the file
rdd_add = add.groupByKey().map(joining_func)
logging.info("Grouped and Joined Output", rdd_add.takeOrdered(4))

#starts mapper with parameters to index and options.
try:
    alignment_pipe = rdd_add.pipe(options)
except:
    print("Could not perform mapping. Check syntax of mapper options")
logging.info("Mapper Output", alignment_pipe.take(4))

logging.info("Number of Partitions:", alignment_pipe.getNumPartitions())
logging.info("Number of Reads:", alignment_pipe.count())

#Collecting output and maintaining parallelization while writing to local file
alignment_final.saveAsTextFile(direc_path)

#Uncomment if you want to record process timing
end = time.time()
temp_file = open("time.txt", 'w+')
temp_file.write("Runtime: " + str(end-start))
temp_file.close()
sc.stop()
