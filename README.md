# Hi-C
Workflow for Hi-C

Getting a Reference Genome and Fastq/FASTA files

Skip this step if you already have a Reference Genome and Fastq/FASTA paired-end reads from an experiment. Otherwise, continue if you are using data from online.
Input: Can start with an SRA format (if using online data), but convert to Fastq or fasta file types using fastq dump.
Ex: Fastq-dump --split-files --fasta {Accession #}

Make sure to have a copy in the FASTA format if you do not have a bowtie2 index for that reference genome as Bowtie2 only accepts FASTA files in its bowtie2 indexer.

Running Bowtie2 to create SAM files




