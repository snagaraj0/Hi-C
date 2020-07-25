#Example using Bowtie2
python SingleSpark.py /s1/snagaraj/project_env/SRR639031_1.fastq file:///s1/snagaraj/single 20G 100G 100 "/s1/snagaraj/bowtie2/bowtie2 --no-hd --no-sq -x /s1/snagaraj/Homo_sapiens/UCSC/hg19/Sequence/Bowtie2Index/genome -" 

#Example using STAR
python SingleSpark.py /s1/snagaraj/project_env/SRR639031_1.fastq file:///s1/snagaraj/single 20G 100G 100  "/s1/snagaraj/STAR/STAR --runMode alignReads --readFilesIn /dev/stdin --readFilesType Fastx SE --genome-Dir /s1/snagaraj/star --outStd SAM"

#$1 $2 $3
