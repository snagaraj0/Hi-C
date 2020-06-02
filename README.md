# SparkMap

## Installation

HiC-Pipeline requires the following dependencies to run:
- The [bowtie2](http://bowtie-bio.sourceforge.net/bowtie2/index.shtml) mapper
- Python 3.7 with matplotlib(> 3.1.1), numpy(> 1.16.4), pandas(> 0.25.0), bio( > 0.1.0),  biopython( > 1.74)
- Apache Spark ( > 2.4.3) with findspark( > 1.3.0)
- Hadoop (> 3.1.2)
- Unix sorting. Install GNU core utilities if running on MacOS.

It is also recommended that you run HiC-Pipeline in Linux and on a compute cluster.

To download HiC-Pipeline, make sure you have the appropriate permissions and then follow these instructions.

First, download the HiC-Pipeline repository as a tarball and then untar with the following commands.

```
wget https://github.com/snagaraj0/HiC-Pipeline/tarball/master
tar -xzvf HiC-Pipeline.tar.gz
```
or

```
curl -L  https://github.com/snagaraj0/HiC-Pipeline/tarball/master 
tar -xzvf HiC-Pipeline.tar.gz
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

### Bowtie2 creates SAM files as a single-end or paired-end aligner

Single-End: bowtie2 -x [path to index] [options] [fastq file] -S [name of preferred .sam file output] 
Paired-End: bowtie2 -x [path to index] [options] -1 [fastq_1 file] -2 [fastq_2 file] -S [name of preferred .sam file output]

### Starting Hadoop and Spark

In order to use Hadoop Distributed File System(HDFS), run start-all.sh in the $HADOOP_HOME/sbin directory to start all Hadoop Daemons.

Start the Spark Driver by running start-all.sh in the $SPARK_HOME/sbin directory to start the Spark master and all Spark workers.


### CONVERTER shell script usage

Input: Follow example given when prompted.
Output: A file called output_alignment.dat

You can rename this file after the shell script runs if you would like. You can do this through the mv command in terminal or by physically renaming the file in its directory if you are running this on a standalone computer.


