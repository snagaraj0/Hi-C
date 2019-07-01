# Hi-C
Workflow for Hi-C

Getting a Reference Genome and Fastq/FASTA files

Skip this step if you already have a Reference Genome and Fastq/FASTA paired-end reads from an experiment. Otherwise, continue if you are using data from online.
Input: Can start with an SRA format (if using online data), but convert to Fastq or fasta file types using fastq dump.
Ex: Fastq-dump --split-files --fasta {Accession #}

Find a Bowtie2 index online(widely available) as a reference genome or use bowtie2-builder(not recommended).

Running Bowtie2 to create SAM files

Make sure to run Bowtie2 as an end to end aligner, rather than in paired-read alignment! This is due to the format of the shell-script which extracts information later on in the workflow.

Example: bowtie2 -x [path to index] [options] -S [name of preferred .sam file output] [fastq_1 file]
         bowtie2 -x [path to index] [options] -S [name of preferred .sam file output] [fastq_2 file]




