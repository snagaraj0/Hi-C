# SparkMap
A novel framework to speed up short read alignment using Apache Spark.
Currently we support:
- Any mapper that can be installed as a local executable and read input through stdin, such as [bowtie2](http://bowtie-bio.sourceforge.net/bowtie2/index.shtml), [STAR](https://physiology.med.cornell.edu/faculty/skrabanek/lab/angsd/lecture_notes/STARmanual.pdf), or [HISAT2](http://daehwankimlab.github.io/hisat2/download/) for single-end mapping
- Any mapper that can be installed as a local executable and read input through stdin and supports interleaved fastq files for paired-end mapping, such as [bowtie2](http://bowtie-bio.sourceforge.net/bowtie2/index.shtml)

SparkMap has been tested on STAR, TopHat, Bowtie2, and HISAT2.
## Installation

SparkMap requires the following dependencies to run:
- Python 3.7 with numpy(> 1.16.4), progressbar2(>3.50.1) , pydoop( > 2.0.0), py4j(> 0.10.7), pyinstaller(>3.6), python-utils(>2.4.0)
- Apache Spark ( > 2.4.3) with findspark( > 1.3.0)
- Hadoop (> 3.1.2)
- Unix sorting. Install GNU core utilities if running on MacOS.

It is also recommended that you run SparkMap in Linux and on a compute cluster.

To download SparkMap, make sure you have the appropriate permissions and then follow these instructions.

First, download the SparkMap repository as a zip file and unzip it with the following commands.

```
wget https://github.com/snagaraj0/SparkMap/master
unzip SparkMap.zip
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
Input: Can start with an SRA format (if using online data), but convert to the FastQ file type using fastq dump.
Ex: Fastq-dump --split-files --fasta {Accession #}

Find a genome index online(widely available - [bowtie2](https://support.illumina.com/sequencing/sequencing_software/igenome.html), [STAR](http://labshare.cshl.edu/shares/gingeraslab/www-data/dobin/STAR/STARgenomes/Human/GRCh38_Ensembl99_sparseD3_sjdbOverhang99/)) as a reference genome or build your own.

### Install your mapper as an executable

### Starting Hadoop and Spark

In order to use Hadoop Distributed File System(HDFS), run start-all.sh in the $HADOOP_HOME/sbin directory to start all Hadoop Daemons.

Start the Spark Driver by running start-all.sh in the $SPARK_HOME/sbin directory to start the Spark master and all Spark workers.

### Running SparkMap in single-end mode

1) Edit singlespark.sh file with parameters in the following format:

python SingleSpark.py Full_path_to_sam_directory Memory_to_Executor(in GB) Driver_Memory(in GB) Max_cores_for_process executor_instances Mapper_specific_options Mapper_name

See sample singlespark.sh file for an example.

2) Run "chmod +x singlespark.sh" to give permissions

3) Run ./singlespark.sh to run Spark as an interactive process or run "nohup ./singlespark.sh" to run Spark as a background process.

4) Go into your local output directory and run ``` cat * > combined_sam_file ``` to combine the blocks into a single file.


### Running SparkMap in paired-end mode

1) Edit pairspark.sh file with parameters in the following format:

python pairspark.py Full_path_to_sam_directory Memory_to_Executor(in GB) Driver_Memory(in GB) Max_cores_for_process executor_instances Mapper_specific_options

See sample pairspark.sh file for an example.

2) Run "chmod +x pairspark.sh" to give permissions

3) Run ./pairspark.sh to run Spark as an interactive process or run "nohup ./pairspark.sh" to run Spark as a background process.

4) Go into your local output directory and run ``` cat * > combined_sam_file ``` to combine the blocks into a single file.

### Optimization
In order to achieve the best performance, it is recommended to increase the number of executors instances you run, but keeping the amount of threads you specify in the mapper options above 1. For example, with a cluster with 165 cores across 3 nodes, an optimized run might have 55 executor instances with 3 threads specified in the mapper options. Take a look at this article for more information: https://spoddutur.github.io/spark-notes/distribution_of_executors_cores_and_memory_for_spark_application.html

### Validation Scripts

1) Valid_reads.sh/.py- Used to create new SAM files with only mapped reads. Can only used for single-end mapping.

2) Reorder.sh/.py - Used to create new SAM files that are ordered according to read ID. Can only be used for single-end mapping.

3) Alternatively, use the [SAMtools](http://www.htslib.org/doc/samtools-sort.html) sort to sort by chromosome position or by read number.

### Interactions shell script usage

Use Interactions.sh for single-end/locally aligned SAM files and CONVERT_pair.sh for paired-end SAM files. These scripts are useful to create  interactions data(Hi-C) in the form:

```Chr1 pos1 direction1(0 or 16 for Watson/Crick strand) Chr2 pos2 direction2```

Input: Pass input SAM file name and output text file name 

### Misc.

If you ask for a header for the SAM file, run  ```awk '!seen[$0]++' orig_file_name > new_file_name ``` to eliminate duplicate headers. However, we recommend generating the header separately and joining it to the mapping file as this is faster.

