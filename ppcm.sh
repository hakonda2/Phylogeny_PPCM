#!/bin/bash

# add to PATH
export PATH=$PATH:/export/dahlefs/apps/symlinks/

# defaults
threshold=0
output_dir="ppcm_out"
bootstrapping=0

while getopts i:t:o:m:f:b: flag
do
    case "${flag}" in
        i) input_dir=${OPTARG};;
        t) threshold=${OPTARG};;
        o) output_dir=${OPTARG};;
	m) marker_file=${OPTARG};;
	f) checkm_fastafile=${OPTARG};;
	b) bootstrapping=1;;
    esac
done


echo "input_dir: $input_dir";
echo "threshold: $threshold";
echo "marker_file: $marker_file";
echo "output_dir: $output_dir";
echo "fastafile: $checkm_fastafile";
echo "bootstrapping: $bootstrapping";

### make tmp
if  [ ! -d "tmp" ] ; then
	mkdir tmp
fi

#### split into one fastafile per marker
cd tmp
while read line
	do
	grep -A1 --no-group-separator $line ../${checkm_fastafile} > ${line}.fasta
done < ../${marker_file}
cd ..


#### remove dublicates
#PATH=/export/dahlefs/work/Hakon/Phylogeny/PhylPipeline_test/scripts/:$PATH
cd tmp
while read line
	do 
	PPCM_fixfasta.py ${line}.fasta > fixfasta_${line}.fasta
done < ../${marker_file}
cd ..

### run mafft (conda install -c bioconda mafft)
cd tmp
while read line
	do
	echo "####### "${line}
	mafft-linsi fixfasta_${line}.fasta > mafft_fixfasta_${line}.fasta
done < ../${marker_file}
cd ..


### trim (conda install -c bioconda trimal)
cd tmp
while read line
	do
	echo "####### "${line}
	trimal -in  mafft_fixfasta_${line}.fasta -out trimal_mafft_fixfasta_${line}.fasta -gappyout
done < ../${marker_file}
cd ..




### get list of genomes
grep ">" tmp/trimal_mafft_fixfasta_*.fasta | sed 's/>//' | cut -f2 -d":" | sort -u > tmp/GenomeList.txt 



### concatenate alignments
cd tmp
PPCM_MergeAlignments.py -i ../Markerset_Bacteria_subset.txt -g GenomeList.txt -t ${threshold} > ConcatenatedAlgn.fasta
cd ..


### make tree
file="ConcatenatedAlgn.fasta"
cd tmp
if [ "$bootstrapping" -ne 0 ]; then
   raxmlHPC-PTHREADS -m PROTCATLG -s $file -p 12345 -x 12345 -N autoMRE -f a -n autoresult -T 14
else
   raxmlHPC-PTHREADS -m PROTCATLG -s $file -p 12345 -# 20 -n T1 -T 14
fi
cd ..

### genomeid vs species
cd tmp
ls -1 ../$input_dir | cut -f1 -d"." > t1.tmp
head -1 ../$input_dir/*.* | grep "^>" | cut -f2,3 -d" " | awk 'BEGIN{c=1}{print c$0; c=c+1}' | sed 's/ /_/g' | sed 's/\.//g' | sed 's/>/_/g' | sed 's/://g' > t2.tmp
paste t1.tmp t2.tmp > genomeid_vs_species.txt
cd ..

### move to output
if  [ ! -d $output_dir ] ; then
	mkdir $output_dir
fi
mv tmp/genomeid_vs_species.txt $output_dir 


if [ "$bootstrapping" -ne 0 ]; then
	mv tmp/RAxML* $output_dir
else
	mv tmp/RAxML*best* $output_dir
fi









