#Example using Bowtie2
pipenv run python SingleSpark.py single 20G 100G 100 25G "/s1/snagaraj/Homo_sapiens/UCSC/hg19/Sequence/Bowtie2Index/genome--no-hd --no-sq" 

#Example using STAR
pipenv run python SingleSpark.py STAR /s1/snagaraj/project_env/SRR639031_1.fastq /s1/snagaraj/Homo_sapiens/UCSC/hg19/Sequence/Bowtie2Index/genome /s1/snagaraj/project_env/single.sam "--genome-Dir " 4G 100G 100 25G

#$1 $2 $3
