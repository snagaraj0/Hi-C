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
from operator import add
import logging

start = time.time()
conf = SparkConf().setAppName("SparkHDFSTEST")
conf = conf.set('spark.submit.deploymode', "cluster")
conf = conf.set('spark.executor.memory', '4G').set('spark.driver.memory', '100G').set("spark.cores.max", "165")
#conf = conf.set("spark.dynamicAllocation.enabled", "true").set("spark.dynamicAllocation.minExecutors","5").set("spark.dynamicAllocation.initialExecutors", "5").set("spark.dynamicAllocation.maxExecutors","5")
sc = SparkContext.getOrCreate(conf=conf)
#sc._jsc.hadoopConfiguration().set("fs.defaultFS", "hdfs://greg-hn:9000")
print(sc.getConf().getAll())


logging.basicConfig(filename='single.log', filemode='w', format='%(name)s - %(message)s')
test_input = sys.argv[1]

subprocess.call(["hdfs", "dfs", "-mkdir", "-p", "/user/data"])
subprocess.call(["hdfs", "dfs", "-put", test_input, "/user/data" ])
#subprocess.call(["hdfs", "dfs", "-put", o_input, "/user/data" ])

test_input = test_input.split('/')
test_len = len(test_input) - 1
end_input = test_input[test_len]

st = sys.argv[3]
filestr= st
print(filestr)

input_file = "hdfs:/user/data/" + end_input
print(input_file)

# label each line with its positional number
text_input = (sc.textFile(input_file)).zipWithIndex()

test = text_input.take(10))
logging.debug(test)
# map every 4 strings under the same read number

map_text_input = text_input.map(lambda read: (math.floor(read[1]/4), read[0]))
test = map_text_input.take(10)
logging.debug(test)

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
test = read_map.take(20))
logging.debug(test)


# Sort by the line number and then grab all the values associated with that line number
readsRDD = read_map.sortByKey().values()
bowtie_index = sys.argv[2]

#starts bowtie with parameters to bowtie index.
alignment_pipe = readsRDD.pipe("/s1/snagaraj/bowtie2/bowtie2 --no-sq --no-hd -x " + bowtie_index + " -")

def create_sam(output):
    try:
       file = open(filestr, "a+")
       for alignment in output:
           file.write(alignment + '\n')
       file.close()
    except Exception as ex:
       print(ex)


check=alignment_pipe.getNumPartitions()
logging.debug("Number of partitions:" + str(check))

# Write partitions to SAM file
aligned_output = alignment_pipe.foreachPartition(lambda output: create_sam(output))
end = time.time()
logging.info("Runtime: " + str(end-start))
sc.stop()
