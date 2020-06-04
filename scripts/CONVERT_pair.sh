#  condense sam file
awk '{print $1,$3,$4,$2,$5;}' $1 > pr.sam

# Sort according to read id
sort -V -k1 pr.sam > pr.sam.sorted

paste -d " "  - - < pr.sam.sorted  > pr.sam.merged
awk '{if($1 eq $6 && $5>= 30 && $10 >= 30 && substr($2,1,3) == "chr" && substr($7,1,3) == "chr" && $3 ~ /^[0-9]+$/ && $8 ~ /^[0-9]+$/) print $2,$3,$4,$7,$8,$9}'  pr.sam.merged > $2


