#Example using Bowtie2
python SingleSpark.py /s1/snagaraj/project_env/SRR639031_1.fastq file:///s1/snagaraj/single 20G 100G 100 2 "/s1/snagaraj/bowtie2/bowtie2 --no-hd --no-sq -x /s1/snagaraj/Homo_sapiens/UCSC/hg19/Sequence/Bowtie2Index/genome -" 

#Example using STAR
python SingleSpark.py /s1/snagaraj/project_env/SRR639031_1.fastq file:///s1/snagaraj/single 20G 100G 100 2 "/s1/snagaraj/hisat2/hisat2 --no-hd --no-sq -p 50 -x /s1/snagaraj/grch38/genome" 

#$1 $2 $3
