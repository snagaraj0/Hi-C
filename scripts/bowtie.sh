#Example using Bowtie2
pipenv run python SingleSpark.py bowtie2 /s1/snagaraj/project_env/SRR639031_1.fastq /s1/snagaraj/Homo_sapiens/UCSC/hg19/Sequence/Bowtie2Index/genome /s1/snagaraj/project_env/single.sam "--no-hd --no-sq" 4G 100G 100

#Example using STAR
pipenv run python SingleSpark.py STAR /s1/snagaraj/project_env/SRR639031_1.fastq /s1/snagaraj/Homo_sapiens/UCSC/hg19/Sequence/Bowtie2Index/genome /s1/snagaraj/project_env/single.sam "--genome-Dir " 4G 100G 100

#$1 $2 $3
