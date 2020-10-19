#Example using Bowtie2
python singleSpark.py /s1/snagaraj/project_env/SRR639031_1.fastq file:///s1/snagaraj/single 20G 100G 100 2 "/s1/snagaraj/bowtie2/bowtie2 --no-hd --no-sq -x /s1/snagaraj/Homo_sapiens/UCSC/hg19/Sequence/Bowtie2Index/genome -" 

#Example using HISAT2
python singleSpark.py /s1/snagaraj/project_env/SRR639031_1.fastq file:///s1/snagaraj/single 20G 100G 100 2 "/s1/snagaraj/hisat2/hisat2 --no-hd --no-sq -p 50 -x /s1/snagaraj/grch38/genome -" 

#Example using BBMAP
python singleSpark.py /s1/snagaraj/project_env/SRR639031_1.fastq file:///s1/snagaraj/single 20G 100G 100 2 "java -ea -Xmx40912m -Xms30312m -cp /s1/snagaraj/bbmap/current/align2.BBMap build=1 overwrite=true fastareadlen=500 in=stdin.fq out=stdout ref=/s1/snagaraj/Homo_sapiens/UCSC/hg19/Sequence/Bowtie2Index/genome.fa interleaved=false path=/s1/snagaraj/bbmap build=1 t=50"

#$1 $2 $3
