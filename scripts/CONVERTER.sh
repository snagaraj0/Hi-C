#!/bin/bash

# Script to create single file with all interactions data from 2 single-end SAM files

#  extract important information from sam file
awk '{print $1,$3,$4,$2,$5;}' $1 > p1.sam.0
awk '{print $1,$3,$4,$2,$5;}' $2 > p2.sam.0
 
# Sort according to read id
sort -V -k1 p1.sam.0 > p1.sam.0.sorted
sort -V -k1 p2.sam.0 > p2.sam.0.sorted


paste p1.sam.0.sorted p2.sam.0.sorted > p1_p2_merged

#check appropriate conditions for pairing of interacting reads
awk '{if($1 eq $6 && $5>= 30 && $10 >= 30 && substr($2,1,3) == "chr" && substr($7,1,3) == "chr" && $3 ~ /^[0-9]+$/ && $8 ~ /^[0-9]+$/) print $2,$3,$4,$7,$8,$9}'  p1_p2_merged  > $3
