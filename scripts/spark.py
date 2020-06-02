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

logging.basicConfig(filename='pair.log', filemode='w', format='%(name)s - %(message)s')
start = time.time()
conf = SparkConf().setAppName("SparkHDFSTEST")
conf = conf.set('spark.submit.deploymode', "cluster")
conf = conf.set('spark.executor.memory', exec_mem).set('spark.driver.memory', driver_mem).set("spark.cores.max", max_cores)
sc = SparkContext.getOrCreate(conf=conf)
print(sc.getConf().getAll())


test_input = sys.argv[1]
o_input = sys.argv[2]

subprocess.call(["hdfs", "dfs", "-mkdir", "-p", "/user"])
subprocess.call(["hdfs", "dfs", "-mkdir", "-p", "/user/data"])
subprocess.call(["hdfs", "dfs", "-put", test_input, "/user/data" ])
subprocess.call(["hdfs", "dfs", "-put", o_input, "/user/data" ])

test_input = test_input.split('/')
end_input = test_input[len(test_input) - 1]

o_input = o_input.split('/')
end_o_input = o_input[len(o_input)- 1]

st = sys.argv[4]
filestr= st
print(filestr)

input_file = "hdfs:/user/data/" + end_input
print(input_file)

input_file1 = "hdfs:/user/data/" + end_o_input
print(input_file1)

# label each line with its positional number
text_input = (sc.textFile(input_file)).zipWithIndex()
text_input1 = (sc.textFile(input_file1)).zipWithIndex()
test = raw_input.take(10)
logging.debug(test)

# map every 4 strings under the same read number
map_text_input = text_input.map(lambda read: (math.floor(read[1]/4), read[0]))
map_text_input1 = text_input1.map(lambda read: (math.floor(read[1]/4), read[0]))
test = map_text_input.take(20)
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
    

reads = map_text_input.groupByKey().mapValues(lambda read: create(read))
reads1 = map_text_input1.groupByKey().mapValues(lambda read: create(read))
test = reads.take(20)
logging.debug(test)

combineRDD = reads.join(reads1)
print(combineRDD.take(20))

# Sort by the line number and then grab all the values associated with that line number
val_combineRDD = combineRDD.sortByKey().values()
test = val_combineRDD.first()
logging.debug(test)

bowtie_index = sys.argv[3]
combinedRDD = val_combineRDD.map(lambda x: x[0] + x[1])
test= combinedRDD.take(20)
logging.debug(test[0])

#starts bowtie with parameters to bowtie index.
alignment_pipe = combinedRDD.pipe(filestr + "/bowtie2 " + options + " -x " + bowtie_index + " --interleaved " + " -") 
test = alignment_pipe.take(20)
logging.debug(test)


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
