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

logging.basicConfig(filename='pair.log', filemode='w', level=logging.INFO)

#Uncomment to document time
#start = time.time()
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

# label each line with its positional number
text_input = (sc.textFile(input_file)).zipWithIndex()
text_input1 = (sc.textFile(input_file1)).zipWithIndex()
test = text_input.take(10)
logging.info(test)

# map every 4 strings under the same read number
map_text_input = text_input.map(lambda read: (math.floor(read[1]/4), read[0]))
map_text_input1 = text_input1.map(lambda read: (math.floor(read[1]/4), read[0]))
test = map_text_input.take(20)
logging.info(test)

logging.info(test)

combineRDD = reads.join(reads1)
test = combineRDD.take(20)
logging.info(test)

# Sort by the line number and then grab all the values associated with that line number
val_combineRDD = combineRDD.sortByKey().values()
test = val_combineRDD.first()
logging.info(test)

#starts bowtie with parameters to bowtie index.
alignment_pipe = combinedRDD.pipe(bowtie_exec + "bowtie2 " + options + " -x " + bowtie_index + " --interleaved " + " -") 
test = alignment_pipe.take(20)
logging.info(test)

check=alignment_pipe.getNumPartitions()
logging.info("Number of partitions:" + str(check))

# Write partitions to SAM file

end = time.time()
logging.info("Runtime: " + str(end-start))
sc.stop()
