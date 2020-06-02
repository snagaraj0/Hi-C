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

start = time.time()
conf = SparkConf().setAppName("SparkHDFSTEST")
conf = conf.set('spark.submit.deploymode', "cluster")
conf = conf.set('spark.executor.memory', '4G').set('spark.driver.memory', '100G').set("spark.cores.max", "165")
#conf = conf.set("spark.dynamicAllocation.enabled", "true").set("spark.dynamicAllocation.minExecutors","5").set("spark.dynamicAllocation.initialExecutors", "5").set("spark.dynamicAllocation.maxExecutors","5")
#conf = conf.set('spark.executor.instances', '5')
sc = SparkContext.getOrCreate(conf=conf)
#sc._jsc.hadoopConfiguration().set("fs.defaultFS", "hdfs://greg-hn:9000")
print(sc.getConf().getAll())



test_input = sys.argv[1]
o_input = sys.argv[2]
'''
temp = 0
head = ""
with open(test_input) as file:
   for line in file:
        if(temp == 4):
           break;
        head+=line
        temp = temp + 1
print(len(head))
'''
#subprocess.call(["hdfs", "dfs", "-mkdir", "-p", "/user/data"])
subprocess.call(["hdfs", "dfs", "-put", test_input, "/user/data" ])
subprocess.call(["hdfs", "dfs", "-put", o_input, "/user/data" ])

test_input = test_input.split('/')
end_input = test_input[len(test_input) - 1]

o_input = o_input.split('/')
end_o_input = o_input[len(o_input)- 1]

st = sys.argv[4]
filestr="/s1/snagaraj/project_env/" + st
print(filestr)

input_file = "hdfs:/user/data/" + end_input
print(input_file)

input_file1 = "hdfs:/user/data/" + end_o_input
print(input_file1)

# creates tuples with format (string, line number)
raw_input = (sc.textFile(input_file)).zipWithIndex()
raw_input1 = (sc.textFile(input_file1)).zipWithIndex()
print(raw_input.take(10))

# create tuple with format (read number, dna)
map_raw_input = raw_input.map(lambda read: (math.floor(read[1]/4), read[0]))
map_raw_input1 = raw_input1.map(lambda read: (math.floor(read[1]/4), read[0]))
temp = map_raw_input.take(20)
print(temp)

# add 4 strings in each read
def readcreation(reads):
    temp = 0
    line = ""
    line1 = ""
    line2 = ""
    line3 = ""
    for read in reads:
        if  temp == 0:
            line = read 
        elif temp == 1:
            line1 = read
        elif temp == 2:
            line2 = read
        else:
            line3 = read
        temp = temp+1
    return "%s\n%s\n%s\n%s\n"  % (line, line1, line2, line3)

reads = map_raw_input.groupByKey().mapValues(lambda read: readcreation(read))
reads1 = map_raw_input1.groupByKey().mapValues(lambda read: readcreation(read))
#print(reads.take(20))

combineRDD = reads.join(reads1)
print(combineRDD.take(20))

# Sort by line # and get reads corresponding to each
#readsRDD = reads.sortByKey().values()
#readsRDD1 = reads1.sortByKey().values() 
val_combineRDD = combineRDD.sortByKey().values()
num_reads = val_combineRDD.count()
print(num_reads)
print(val_combineRDD.first())
#print("p2",readsRDD1.take(20))
bowtie_index = sys.argv[3]
combinedRDD = val_combineRDD.map(lambda x: x[0] + x[1])
test= combinedRDD.take(20)
print(test[0])
#test.saveAsTextFile("/s1/snagaraj/project_env/temp.txt")

#alignment_pipe = readsRDD.pipe("/s1/snagaraj/bowtie2/bowtie2 --quiet --local --very-sensitive-local -x " + bowtie_index + " -")
alignment_pipe = combinedRDD.pipe("/s1/snagaraj/bowtie2/bowtie2 --no-hd --no-sq -x " + bowtie_index + " --interleaved " + " -") 
#alignment_pipe = combinedRDD.pipe("/s1/snagaraj/project_env/run.sh " + bowtie_index)

#alignmentRDD =combinedRDD.pipe("/s1/snagaraj/project_env/run.py " + bowtie_index)
print(alignment_pipe.take(20))


def create(output):
    try:
       file = open(filestr, "a+")
       for alignment in output:
           file.write(alignment + '\n')
       file.close()
    except Exception as ex:
       print(ex)


check=alignment_pipe.getNumPartitions()
print(check)
aligned_output = alignment_pipe.foreachPartition(lambda x: create(x))
end = time.time()
temp_file = open("time.txt", 'a+')
temp_file.write("Runtime: " + str(end-start))
temp_file.close()
sc.stop()
