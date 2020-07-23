#Example using Bowtie2
pipenv run python SingleSpark.py single 20G 100G 100 "/s1/snagaraj/bowtie2/bowtie2 --no-hd --no-sq -x /s1/snagaraj/Homo_sapiens/UCSC/hg19/Sequence/Bowtie2Index/genome -" 

#Example using STAR
pipenv run python SingleSpark.py STAR /s1/snagaraj/Homo_sapiens/UCSC/hg19/Sequence/Bowtie2Index/genome /s1/snagaraj/project_env/single.sam "--genome-Dir " 4G 100G 100 25G

#$1 $2 $3
