# ViewR

ViewR is a Web browser for NGS data exploration, that allows the vizualisation of any read coverage across the genome (RNA-seq, ChIP-seq, etc), along with the corresponding gene annotation.

## How It Works

ViewR is designed to take coverage data as [bigWig](https://genome.ucsc.edu/goldenPath/help/bigWig.html) files and annotation as [gtf](https://www.ensembl.org/info/website/upload/gff.html) file.  
It runs with [Apache](https://httpd.apache.org/) on Ubuntu, and requires php and python3, with [pyBigWig](https://github.com/deeptools/pyBigWig) and [pytabix](https://github.com/slowkow/pytabix) libraries.  
A php script produce the interface, a python script extract coverage values and genes coordinates requested, and the [Plotly](https://plotly.com/javascript/) graphical library generate the graphs.  

## Browser Compatibilities

| Chrome | Firefox | 
| ------ | ------- |
| ✔      | ✔       |

## Installation

### 1. Clone the repository
```
git clone https://github.com/szachn-u/ViewR.git
```
### 2. Edit description file
Edit **description.tsv** in the viewR/script/ directory, a tab separated file with one sample per line:  
 - file_f : path to the bigWig file for the reads one the forward strand (or all reads, if the library is unstranded, e.g. like ChIP-seq).  
 - file_r : path to the bigWig file for the reads one the reverse strand (for strand-specific libraries only).  
 - replicate_name : short name for the sample.  
 - cond_name : condition of the sample.  
 - norm_coeff : normalisation factor. The coverage will be **multiplied** by this value if normalized data are asked.  

### 3. Run config.sh script
```
cd ViewR/scripts
./conf.sh --annot my_annot.gtf --genome_info genome_info.tsv --pyhton_path python3
```
- my_annot.gtf should be in gtf format, with gene_id, gene_type and gene_name in the attribute column (9th)
- genome_info.tsv is a tab separated file, without header, with chromosome names (as in bigWig files) and chromosome sizes

### 4. Copy the viewR directory in /var/www/html
```
cd ../../
sudo cp -r viewR/ /var/www/html/
sudo chmod -R +x /var/www/html/viewR   # to allow execution of the scripts
```

