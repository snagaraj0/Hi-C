import sys
reads_seen = set() # holds reads already seen
file = open(sys.argv[1], "r")
outfile = open(sys.argv[2] , "w")
debug = open("outr.sam", "w")
error = open("error.sam", "w")
temp=0

read_temp = file.readline().strip().split()[0]
liner = read_temp.split(":")[0]
for line in file:
    line_split = line.split()
    try:
        if len(line_split[2]) > 3:
             outfile.write(line)
        else:
             continue
    except: 
        continue
          #error.write(line)
'''
for line in file:
    line_split = line.split()
    read_id = line_split[0]
    outfile.write(line)
    reads_seen.add(read_id)
    if(read_id[1:] == "PG"):
       break;

for line in file:
    line_split = line.split()
    read_id = line_split[0]
    keep = True
    #print(temp)
    for i in range(11, len(line_split)):
        if(len(line_split[i].split(":")) != 3):
           keep = False
    if read_id not in reads_seen and keep and len(line_split) > 10:
       if len(line_split[9]) == len(line_split[10]) and len(line_split[2]) > 3:
           outfile.write(line)
          #print(line_split[2])
           reads_seen.add(read_id)

'''
file.close()
outfile.close()
