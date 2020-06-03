import sys
reads_seen = set() # holds reads already seen
file = open(sys.argv[1], "r")
outfile = open(sys.argv[2] , "w")
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
          error.write(line)
            
file.close()
outfile.close()
