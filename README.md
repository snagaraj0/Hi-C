# HicPipeline
Workflow for Hi-C

# Getting a Reference Genome and Fastq/FASTA files

Skip this step if you already have a Reference Genome and Fastq/FASTA paired-end reads from an experiment. Otherwise, continue if you are using data from online.
Input: Can start with an SRA format (if using online data), but convert to Fastq or fasta file types using fastq dump.
Ex: Fastq-dump --split-files --fasta {Accession #}

Find a Bowtie2 index online(widely available) as a reference genome or use bowtie2-builder(not recommended).

# Running Bowtie2 to create SAM files

Make sure to run Bowtie2 as an end to end aligner, rather than in paired-read alignment! This is due to the format of the shell-script which extracts information later on in the workflow.

Example: bowtie2 -x [path to index] [options] -S [name of preferred .sam file output] [fastq_1 file]
         bowtie2 -x [path to index] [options] -S [name of preferred .sam file output] [fastq_2 file]



# CONVERTER shell script usage

Input: Follow example given when prompted.

Output: A file called output_alignment.dat 
You can rename this file after the shell script runs if you would like. You can do this through the mv command in terminal or by physically renaming the file in its directory if you are running this on a standalone computer.



# Fragment Assignment Script usage

Input Format Example : 
Directory Path:/s1/snagaraj/project_env/Homo_sapiens/UCSC/hg18/Sequence/Chromosomes
Enzyme: HindIII
Alignment File after conversion through CONVERTER: /s1/snagaraj/project_env/alignment_1.dat

Make sure all these inputs are separated with a single comma and there is NO SPACE after each comma.

Output: The output will be the name of the alignment file.assigned. So in my example, the output file would be in the directory /s1/snagaraj/project_env and would be alignment_1.dat.assigned.

