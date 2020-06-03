#!/bin/bash

# Script for processing sam files and create a single file containing all necessary information from the output of an alignment

#  condense sam file
awk '{print $1,$3,$4,$2,$5;}' $1 > p1.sam.0
awk '{print $1,$3,$4,$2,$5;}' $2 > p2.sam.0
 
# Sort according to read id
sort -V -k1 p1.sam.0 > p1.sam.0.sorted
sort -V -k1 p2.sam.0 > p2.sam.0.sorted


paste p1.sam.0.sorted p2.sam.0.sorted > p1_p2_merged
awk '{if($1 eq $6 && $5>= 30 && $10 >= 30 && substr($2,1,3) == "chr" && substr($7,1,3) == "chr" && $3 ~ /^[0-9]+$/ && $8 ~ /^[0-9]+$/) print $2,$3,$4,$7,$8,$9}'  p1_p2_merged  > $3


#for ((i=0; i< $total; i++)); do
#    sed "${i}q;d" align_1.da > a.txt 
#    SUB=$(echo $1 | cut -c1-3 a.txt)
#    echo $SUB;
#    awk '{if($SUB eq "chr") print $1,$2,$3,$4,$5,$6}' a.txt >> align_1.dat
#done 
