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

options = sys.argv[5]
exec_mem = sys.argv[6]
driver_mem = sys.argv[7]
max_cores = sys.argv[8]

start = time.time()
conf = SparkConf().setAppName("SparkHDFSTEST")
conf = conf.set('spark.submit.deploymode', "cluster")
conf = conf.set('spark.executor.memory', exec_mem).set('spark.driver.memory', driver_mem).set("spark.cores.max", max_cores)
sc = SparkContext.getOrCreate(conf=conf)
print(sc.getConf().getAll())

logging.basicConfig(filename='single.log', filemode='w', level=logging.INFO)
logging.getLogger().setLevel(logging.INFO)
mapper = sys.argv[1]
test_input = sys.argv[2]

subprocess.call(["hdfs", "dfs", "-mkdir", "-p", "/user/data"])
subprocess.call(["hdfs", "dfs", "-put", test_input, "/user/data" ])

test_input = test_input.split('/')
test_len = len(test_input) - 1
end_input = test_input[test_len]

st = sys.argv[4]
filestr= st
logging.info(filestr)

bowtie_exec_index = filestr.rfind("/")
bowtie_exec = ""
for i in range(bowtie_exec_index + 1):
    bowtie_exec += filestr[i]

input_file = "hdfs:/user/data/" + end_input
print(input_file)

# label each line with its positional number
text_input = (sc.textFile(input_file)).zipWithIndex()

test = text_input.take(10)
logging.info(test)
# map every 4 strings under the same read number

map_text_input = text_input.map(lambda read: (math.floor(read[1]/4), read[0]))
test = map_text_input.take(10)
logging.info(test)

# Combine all strings with same read number together
def create(reads):
    temp = 0
    line_str = ""
    for read in reads:
        if(temp % 4 == 0 and temp/4 == 1):
            break
        else:
            line_str += read + '\n'
            temp = temp + 1
    return line_str


read_map = map_text_input.groupByKey().mapValues(lambda read: create(read))
test = read_map.take(20)
logging.info(test)


# Sort by the line number and then grab all the values associated with that line number
readsRDD = read_map.sortByKey().values()
bowtie_index = sys.argv[3]

#starts bowtie with parameters to bowtie index.
alignment_pipe = readsRDD.pipe(bowtie_exec + "bowtie2 " + options + " -x " + bowtie_index + " -")

def create_sam(output):
    try:
       file = open(filestr, "a+")
       for alignment in output:
           file.write(alignment + '\n')
       file.close()
    except Exception as ex:
       print(ex)


check=alignment_pipe.getNumPartitions()
logging.info("Number of partitions:" + str(check))

# Write partitions to SAM file
aligned_output = alignment_pipe.foreachPartition(lambda output: create_sam(output))
end = time.time()
logging.info("Runtime: " + str(end-start))
sc.stop()
