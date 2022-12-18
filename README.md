## PPCM - Phylogeny Pipeline CheckM based

Requirements: 
checkm [conda install -c bioconda checkm-genome]
RAxML [symlink], 
Mafft [conda install -c bioconda mafft], 
Trimal [conda install -c bioconda trimal]
PPCM scripts [this repo]

### Steps

#### Step 1 - get genomes (fna) (in e.g. input_bins)

#### Step 2 - get marker genes

e.g. 

```sh
checkm taxon_set domain Bacteria Markerset_Bacteria.txt
checkm analyze Markerset_Bacteria.txt input_bins out_checkm -t10
checkm qa Markerset_Bacteria.txt out_checkm -o 9 -t 10 > out_checkm.fasta
```

#### Step 3 - make tree

```sh
ppcm.sh -i input_bins/ -t 5 -m Markerset_Bacteria_subset.txt -f out_checkm.fasta -o ppcm_out
```

