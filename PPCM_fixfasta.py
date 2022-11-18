!#/usr/bin/python3

import sys

fastafile = sys.argv[1]

seen_genomes=[]

outfile=open("report_fixfasta.txt",'w')

outfile.write("Duclicated genes\n")


printing=True


file=open(fastafile, 'r')
for line in file:
	line=line.strip()
	if ">" in line:
		genomeid=line.split()[0][1:]
		if genomeid in seen_genomes:
			outfile.write(genomeid+"\n")
			printing=False
		else:
			print (">"+genomeid)
			seen_genomes.append(genomeid)
			printing=True
	elif(printing):
		print (line)
				
			