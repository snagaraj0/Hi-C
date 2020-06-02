# SparkMap

## Installation

SparkMap requires the following dependencies to run:
- The [bowtie2](http://bowtie-bio.sourceforge.net/bowtie2/index.shtml) mapper
- Python 3.7 with numpy(> 1.16.4), progressbar2(>3.50.1) , pydoop( > 2.0.0), py4j(> 0.10.7), pyinstaller(>3.6), python-utils(>2.4.0)
- Apache Spark ( > 2.4.3) with findspark( > 1.3.0)
- Hadoop (> 3.1.2)
- Unix sorting. Install GNU core utilities if running on MacOS.

It is also recommended that you run SparkMap in Linux and on a compute cluster.

To download SparkMap, make sure you have the appropriate permissions and then follow these instructions.

First, download the HiC-Pipeline repository as a tarball and  then untar with the following commands.

```
wget https://github.com/snagaraj0/SparkMap/tarball/master
tar -xzvf SparkMap.tar.gz
```
or

```
curl -L  https://github.com/snagaraj0/SparkMap/tarball/master 
tar -xzvf SparkMap.tar.gz
```

Next, configure your system to make the dependencies accessible.

Add these user specific configurations to your .bash_profile.

|                | CONFIGURATIONS                                                                |
|----------------|-------------------------------------------------------------------------------|
| PATH           | ADD SPARKMAP INSTALLATION FOLDER AND LOCATIONS OF SPARK AND HADOOP TO PATH    |                              
| PYTHONPATH     | PATH TO PYTHON3.7                                                             |                 
| JAVA_HOME      | PATH TO JAVA JDK FOR HADOOP                                                   |                            
| HADOOP_CONF_DIR| $HADOOP_HOME:/etc/hadoop                                                      |                        
| SPARK_HOME     | PATH TO SPARK INSTALLATION                                                    |                          
| LD_LIBRARY_PATH| $HADOOP_HOME:/lib/native:$LD_LIBRARY_PATH                                     |                               
|  HADOOP_HOME   | PATH TO HADOOP INSTALLTION                                                    |


Add these user specific configurations to your .bashrc


|                   | CONFIGURATIONS                                                                |
|-------------------|-------------------------------------------------------------------------------|
| PATH              | ADD $HADOOP_HOME/bin and $HADOOP_HOME/sbin to PATH                            |                              
| HADOOP_MAPRED_HOME| $HADOOP_HOME                                                                  |                 
| HADOOP_COMMON_HOME| $HADOOP_HOME                                                                  |                            
| HADOOP_HDFS_HOME  | $HADOOP_HOME                                                                  |                        
| YARN_HOME         | $HADOOP_HOME                                                                  |                                     
| HADOOP_HOME       | PATH TO HADOOP INSTALLTION                                                    |



## USAGE GUIDELINES

### Getting a Reference Genome and Fastq/FASTA files

Skip this step if you already have a Reference Genome and Fastq/FASTA paired-end reads from an experiment. Otherwise, continue if you are using data from online.
Input: Can start with an SRA format (if using online data), but convert to Fastq or fasta file types using fastq dump.
Ex: Fastq-dump --split-files --fasta {Accession #}

Find a Bowtie2 index online(widely available) as a reference genome or use bowtie2-builder(not recommended).

### Install Bowtie2 as an executable in the same directory as your input FASTQ file/files.

### Starting Hadoop and Spark

In order to use Hadoop Distributed File System(HDFS), run start-all.sh in the $HADOOP_HOME/sbin directory to start all Hadoop Daemons.

Start the Spark Driver by running start-all.sh in the $SPARK_HOME/sbin directory to start the Spark master and all Spark workers.

### Running SparkMap in single-end mode

1) Edit bowtie.sh file with parameters in the following format:

python BowtieSpark.py Full_path_to_fastq_file  Full_path_to_bowtie2_index Full_path_to_sam_file Memory_to_Executor(in GB) Driver_Memory(in GB) Max_cores_for_process

See sample bowtie.sh file for an example.

2) Run "chmod +x bowtie.sh" to give permissions

3) Run ./bowtie.sh to run Spark as an interactive process or run "nohup ./bowtie.sh" to run Spark as a background process.


### Running SparkMap in paired-end mode

1) Edit bowtie1.sh file with parameters in the following format:

python BowtieSpark.py Full_path_to_fastq_file_1 Full_path_to_fastq_file_2 Full_path_to_bowtie2_index Full_path_to_sam_file Memory_to_Executor(in GB) Driver_Memory(in GB) Max_cores_for_process

See sample bowtie1.sh file for an example.

2) Run "chmod +x bowtie1.sh" to give permissions

3) Run ./bowtie1.sh to run Spark as an interactive process or run "nohup ./bowtie.sh" to run Spark as a background process.

### CONVERTER shell script usage

Use CONVERTER.sh for single-end/locally aligned SAM files and CONVERT_pair.sh for paired-end SAM files. These scripts are useful to create  interactions data(Hi-C) in the form:

Chr1 pos1 direction1(0 or 16 for Watson/Crick strand) Chr2 pos2 direction2

Input: Pass SAM file name
Output: A file called output_alignment.dat


Rename this file after the shell script runs if you would like.

