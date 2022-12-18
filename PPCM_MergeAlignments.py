#!/Users/hakondahle/miniconda3/bin/python

#!/export/dahlefs/apps/miniconda3/envs/checkm/bin/python3

import sys

def get_list(filename):
	out=[]
	file=open(filename,'r')
	for line in file:
		line=line.strip()
		out.append(line)
	return(out)
	


def set_params(sysargv):
	out={"id_file":"", "threshold":0, "genomes_file":""}
	if "-i" in sys.argv:
		pos=sys.argv.index("-i")
		out["id_file"]=sys.argv[pos+1]
	if "-t" in sys.argv:
		pos=sys.argv.index("-t")
		out["threshold"]=int(sys.argv[pos+1])
	if "-g" in sys.argv:
		pos=sys.argv.index("-g")
		out["genomes_file"]=sys.argv[pos+1]
	return(out)

def get_algnlength(fileid):
	c=0
	file=open("trimal_mafft_fixfasta_"+fileid+".fasta",'r')
	for line in file:	
		if (c > 2):
			continue
		elif (">" in line):
			c+=1
			if c==2:
				return(l)
			else:
				l=0
		else:
			line=line.strip()
			l+=len(line)
	return(l)		

def populate_genomeinfo(genomeinfo, fileid):
	algn_length=get_algnlength(fileid)
	sys.stderr.write("LEN "+fileid+" "+str(algn_length)+"\n")
	seen_genomes=[]
	file=open("trimal_mafft_fixfasta_"+fileid+".fasta",'r')
	for line in file:
		line=line.strip()
		if ">" in line:
			genome=line[1:]
			genomeinfo[genome]["num_seen"]+=1
			seen_genomes.append(genome)
		else:
			genomeinfo[genome]["seq"]+=line
	## fill in gaps
	for genome in genomeinfo:
		if genome not in seen_genomes:
			genomeinfo[genome]["seq"]+="-"*algn_length
	
	return(genomeinfo)

def get_genomeinfo(ids,genome_names):
	out={}
	for genome in genome_names:
		out[genome]={"seq":"","num_seen":0}
	for i in ids:
		out=populate_genomeinfo(out,i)
	return (out)

def print_concatenaded(genomeinfo, threshold):
	for genome in genomeinfo:
		if genomeinfo[genome]["num_seen"] < threshold:
			ns=genomeinfo[genome]["num_seen"]
			sys.stderr.write(genome+" NOT INCLUDED " + str(ns)+"\n")
		else:
			print(">"+genome)
			print(genomeinfo[genome]["seq"])	

def check_genomeinfo(genomeinfo):
	maxlen=0
	minlen=100000000000
	for genome in genomeinfo:
		length=len(genomeinfo[genome]["seq"])
		if (length < minlen):
			minlen=length
			mingenome=genome
		if (length > maxlen):
			maxlen=length
			maxgenome=genome
	sys.stderr.write(maxgenome+" "+str(maxlen)+"\n")
	sys.stderr.write(mingenome+" "+str(minlen)+"\n")
		
		


# dictionary of parameters
sysargv=sys.argv
params=set_params(sysargv)

# list of genomes (e.g. GCOO67)
genome_names=get_list(params["genomes_file"])

# list of markers, e.g PF001.5
markers = get_list(params["id_file"])

# dictionary of concatenated sequences and times seen
genomeinfo=get_genomeinfo(markers,genome_names)

# check genomeinfo
check=True
if(check):
	check_genomeinfo(genomeinfo)

	

# print concatenated sequences
print_concatenaded(genomeinfo, params["threshold"])
	
