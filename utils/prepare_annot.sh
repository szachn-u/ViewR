#!/bin/bash

if ! command -v bedtools &> /dev/null
then
	echo "  prepare_annot.sh"
    echo "    bedtools could not be found"
    echo "    please see https://bedtools.readthedocs.io/en/latest/content/installation.html for installation"
    exit
fi

if ! command -v tabix &> /dev/null
then
	echo "  prepare_annot.sh"
    echo "    tabix could not be found"
    echo "    please see https://github.com/samtools/htslib for installation"
    exit
fi

if ! command -v bgzip &> /dev/null
then
	echo "  prepare_annot.sh"
    echo "    bgzip could not be found"
    echo "    please see https://github.com/samtools/htslib for installation"
    exit
fi

if (( $# != 4 )); 
then 
	echo -en "  prepare_annot.sh\n    usage :\n      ./prepare_annot.sh  [-h] --annot  GTF_FILE --out_prefix  OUT_PREFIX\n"
	exit
fi

while (( $# != 0 ));
	do
	case $1 in
		-h) echo -en "  prepare_annot.sh\n    usage :\n      ./prepare_annot.sh  [-h] --annot  GTF_FILE --out_prefix  OUT_PREFIX\n"; exit;;
		--annot_in) shift; annot_in=$1; if [[ ! -s "$annot_in" ]]; then echo "  file $annot_in is empty or does not exists"; echo -e "  prepare_annot.sh\n    usage :\n      ./prepare_annot.sh  [-h] --annot  GTF_FILE --out_prefix  OUT_PREFIX\n"; exit; fi; shift;;
		--out_prefix) shift; out_prefix=$1; shift;;
		*) echo -en "  prepare_annot.sh\n    unexpected argument : \"$1\"\n    usage :\n      ./prepare_annot.sh  [-h] --annot  GTF_FILE --out_prefix  OUT_PREFIX\n"; exit;;
	esac
done

annot_out="${out_prefix}.gtf.gz"
gene_names="${out_prefix}.names.tsv.gz"
gene_types="${out_prefix}.types.txt"

echo "  prepare_annot.sh will create 3 files:"
echo "    - $annot_out"
echo "    - $gene_names"
echo "    - $gene_types"

out_dir=$(dirname "$out_prefix")
if [[ ! -d "$out_dir" ]];
then
	echo "  create $out_dir"
	mkdir "$out_dir"
fi

# make annot index
if (( $(echo "$annot" | grep -E ".gz$") ));
then
	zcat "$annot_in" | bedtools sort -i stdin | bgzip > "$annot_out"
else
	bedtools sort -i "$annot_in" | bgzip > "$annot_out"
fi
tabix "$annot_out"

# make gene name index
zcat "$annot_out" | grep -P "\tgene\t" | awk -F"\t" 'OFS="\t"{
	n=split($9, a, ";")
	tmp=""
	gene_id=""
	gene_type=""
	gene_name=""
	for(i = 1; i <= n; i++){
		if(a[i] ~ /gene_id/){tmp = a[i]; gsub("gene_id", "", tmp); gsub("\"", "", tmp); gsub(" ", "", tmp); gene_id = tmp}
		if(a[i] ~ /gene_type/){tmp = a[i]; gsub("gene_type", "", tmp); gsub("\"", "", tmp); gsub(" ", "", tmp); gene_type = tmp}
		if(a[i] ~ /gene_name/){tmp = a[i]; gsub("gene_name", "", tmp); gsub("\"", "", tmp); gsub(" ", "", tmp); gene_name = tmp}
		tmp=""
	}
	print gene_id, $2, gene_type, $4, $5, $6, $7, $8, $1, gene_id, gene_name
}' | gzip > "$gene_names"

# make gene type list
zcat "$gene_names" | cut -f3 | sort | uniq > "$gene_types"
