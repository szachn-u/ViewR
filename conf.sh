#!/bin/bash

### functions
print_usage () {
    echo "  conf.sh"
    echo "    parameters :"
    echo "    --description     tab separated file (with header) : file_F, file_R, replicate_name, cond_name, norm_coeff"
    echo "    --annot           annotation file, in gtf format"
    echo "    --genome_info     tab separated file (no header) : chromosome names and sizes"
    echo "    --out_dir         path to brower files  (default : ./myViewR)"
    echo "    --python_path     path to python        (default : python3)"
}
export -f print_usage

### check bedtools, bgzip & tabix
if ! command -v bedtools &> /dev/null
then
    echo "  conf.sh"
    echo "    bedtools could not be found"
    echo "    please see https://bedtools.readthedocs.io/en/latest/content/installation.html for installation"
    exit
fi

if ! command -v tabix &> /dev/null
then
	echo "  conf.sh"
    echo "    tabix could not be found"
    echo "    please see https://github.com/samtools/htslib for installation"
    exit
fi

if ! command -v bgzip &> /dev/null
then
    echo "  conf.sh"
    echo "    bgzip could not be found"
    echo "    please see https://github.com/samtools/htslib for installation"
    exit
fi

### parse & check args
if (( $# > 10 )); 
then 
	print_usage
	exit
fi

description=""
annot_in=""
genome_info=""
python_path="python3"
out_dir="myViewR"

while (( $# != 0 ));
    do
    case $1 in
        -h) print_usage; exit;;
        --description) shift; description=$1; if [[ ! -s "$description" ]]; then echo "  description file $description_in is empty or does not exists"; print_usage; exit; fi; shift;;
        --annot) shift; annot_in=$1; if [[ ! -s "$annot_in" ]]; then echo "  annot file $annot_in is empty or does not exists"; print_usage; exit; fi; shift;;
        --genome_info) shift; genome_info=$1; if [[ ! -s "$genome_info" ]]; then echo "  genome info file $genome_info is empty or does not exists"; print_usage; exit; fi; shift;;
        --python_path) shift; python_path=$1; if [[ ! -s "$python_path" ]]; then echo "  python path $python_path was not found"; print_usage; exit; fi; shift;;
        --out_dir) shift; out_dir=$1; if [[ -d "$out_dir" ]]; then echo "  dir $out_dir_already exists"; print_usage; exit; fi; shift;;
        *) echo -en "  conf.sh\n    unexpected argument : \"$1\"\n"; print_usage; exit;;
    esac
done 

if [[ "$description" == "" ]]; then echo "  conf.sh"; echo "    missing description file"; print_usage; exit; fi 
if [[ "$annot_in" == "" ]]; then echo "  conf.sh"; echo "    missing annot file"; print_usage; exit; fi 
if [[ "$genome_info" == "" ]]; then echo "  conf.sh"; echo "    missing genome_info file"; print_usage; exit; fi 

### make dirs
mkdir "$out_dir"
mkdir "$out_dir/scripts" "$out_dir/annot" "$out_dir/images" "$out_dir/bw"

### prepare annotation files
annot_out="$out_dir/annot/annot.gtf.gz"
gene_names="$out_dir/annot/gene_names.tsv.gz"
gene_types="$out_dir/annot/gene_types.txt"

# make annot index
if  (( $(echo "$annot_in" | grep -Ec ".gz$") == 1 ));
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

### copy genome info 
cp "$genome_info" "$out_dir/annot/chr_size.tab"

### copy bw files in ../bw directory
cat "$description" | while read line;
do
    f1=$(echo "$line" | cut -f1)
    name_f1="$(basename $f1)"
    f2=$(echo "$line" | cut -f2)
    name_f2="$(basename $f2)"
    sample=$(echo "$line" | cut -f3)
    cond=$(echo "$line" | cut -f4)
    coeff=$(echo "$line" | cut -f5)
    
    if [[ "$f1" == "file_F" ]]; then echo "$line" > "$out_dir/scripts/description.tsv"; continue; fi
    
    if [[ ! -s "$f1" ]]; 
    then 
        echo "  file $f1 not found or empty"
        continue
    else 
        cp "$f1" "$out_dir/bw/"
    fi
    
    if [[ "$f2" != "" ]]
    then 
        if [[ ! -f "$f2" ]]
        then 
            echo "  file $f2 not found or empty"
            continue
        else 
            cp "$f2" "$out_dir/bw/"
        fi
    else
        new_f2=""
    fi
    
    echo -e "../bw/$name_f1\t../bw/$name_f2\t$sample\t$cond\t$coeff" >> "$out_dir/scripts/description.tsv"
    
done

### set config.txt file
if (( $(grep -c "PYTHON_PATH=python3" scripts/config.txt) != 1 ));
then
	cat "scripts/config.txt" | awk -v p=$python_path '{if($1 ~ /PYTHON_PATH/){print "PYTHON_PATH="p}else{print $0}}' > "$out_dir/scripts/config.txt"
fi

### copy scripts
cp "scripts/index.html" "$out_dir/"
cp "scripts/coverage.php" "$out_dir/scripts/"
cp "scripts/coverage.py" "$out_dir/scripts/"
cp "scripts/functions.php" "$out_dir/scripts/"
cp "scripts/functions.py" "$out_dir/scripts/"
cp "scripts/functions.js" "$out_dir/scripts/"
cp "scripts/design.css" "$out_dir/scripts/"
cp "scripts/index.php" "$out_dir/scripts/"

### copy images
cp "images/*" "$out_dir/images/"
