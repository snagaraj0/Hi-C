# SparkMap

## Installation

SparkMap requires the following dependencies to run:
- Any mapper that can be installed as a local executable and read input through stdin, such as [bowtie2](http://bowtie-bio.sourceforge.net/bowtie2/index.shtml) for single-end mapping
- Any mapper that can be installed as a local executable and read input through stdin and supports interleaved fastq files for paired-end mapping
- Python 3.7 with numpy(> 1.16.4), progressbar2(>3.50.1) , pydoop( > 2.0.0), py4j(> 0.10.7), pyinstaller(>3.6), python-utils(>2.4.0)
- Apache Spark ( > 2.4.3) with findspark( > 1.3.0)
- Hadoop (> 3.1.2)
- Unix sorting. Install GNU core utilities if running on MacOS.

It is also recommended that you run SparkMap in Linux and on a compute cluster.

To download SparkMap, make sure you have the appropriate permissions and then follow these instructions.

First, download the SparkMap repository as a tarball and  then untar with the following commands.

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

1) Edit run.sh file with parameters in the following format:

python SingleSpark.py Full_path_to_sam_directory Memory_to_Executor(in GB) Driver_Memory(in GB) Max_cores_for_process Mapper_specific_options

See sample singlespark.sh file for an example.

2) Run "chmod +x singlespark.sh" to give permissions

3) Run ./singlespark.sh to run Spark as an interactive process or run "nohup ./singlespark.sh" to run Spark as a background process.

4) Go into your local output directory and run ``` cat * > combined_sam_file ``` to combine the blocks into a single file.


### Running SparkMap in paired-end mode

1) Edit bowtie.sh file with parameters in the following format:

python pairspark.py Full_path_to_sam_directory Memory_to_Executor(in GB) Driver_Memory(in GB) Max_cores_for_process Mapper_specific_options

See sample pairspark.sh file for an example.

2) Run "chmod +x pairspark.sh" to give permissions

3) Run ./pairspark.sh to run Spark as an interactive process or run "nohup ./pairspark.sh" to run Spark as a background process.

4) Go into your local output directory and run ``` cat * > combined_sam_file ``` to combine the blocks into a single file.

### Validation Scripts

1) Valid_reads.sh/.py- Used to create new SAM files with only mapped reads. Can only used for single-end mapping.

2) Reorder.sh/.py - Used to create new SAM files that are ordered according to read ID. Can only be used for single-end mapping.

3) Alternatively, use the [SAMtools](http://www.htslib.org/doc/samtools-sort.html) sort to sort by chromosome position or by read number.

### Interactions shell script usage

Use Interactions.sh for single-end/locally aligned SAM files and CONVERT_pair.sh for paired-end SAM files. These scripts are useful to create  interactions data(Hi-C) in the form:

Chr1 pos1 direction1(0 or 16 for Watson/Crick strand) Chr2 pos2 direction2

Input: Pass input SAM file name and output text file name 

### Misc.

If you ask for a header for the SAM file, run  ```awk '!seen[$0]++' orig_file_name > new_file_name ``` to eliminate duplicates.

