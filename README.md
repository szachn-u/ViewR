# ViewR

ViewR is a browser-based tool for NGS data exploration.  
It can display images of read coverage across the genome from any "omic" data (RNA-seq, ChIP-seq, etc), along with the corresponding gene annotation.

#### How It Works

All the data are on the server side. It takes coverage data as [bigWig](https://genome.ucsc.edu/goldenPath/help/bigWig.html) files and annotation as [gtf](https://www.ensembl.org/info/website/upload/gff.html) file. It runs with [Apache](https://httpd.apache.org/) on Ubuntu, and requires [php](https://www.php.net/) and [python3](https://www.python.org/), with [pyBigWig](https://github.com/deeptools/pyBigWig) and [pytabix](https://github.com/slowkow/pytabix) libraries. It makes also use of the [Plotly](https://plotly.com/javascript/) graphical library.

#### Browser Compatibilities

| Chrome | Firefox | 
| ------ | ------- |
| ✔      | ✔       |

## Installation

#### 1. Clone the repository
```
git clone https://github.com/szachn-u/ViewR.git
```
#### 2. Edit description file
Edit **description.tsv**, a tab separated file, with header, one sample per line:  
 - file_F : path to the bigWig file for the reads from the forward strand (or all reads, if the library is unstranded, e.g. like ChIP-seq).  
 - file_R : path to the bigWig file for the reads from the reverse strand (for strand-specific libraries only).  
 - replicate_name : short name for the sample.  
 - cond_name : condition of the sample.  
 - norm_coeff : normalisation factor. The coverage will be **multiplied** by this value if normalized data are asked.  
  
#### 3. Run config.sh script
```
cd ViewR
# requires bedtools and htslib to be installed
./conf.sh --description /path/to/description.tsv --annot my_annot.gtf --genome_info genome_info.tsv --out_dir /path/to/myViewR --python_path /path/to/python
```
- **description.tsv**, the file edited previously
- **my_annot.gtf** should be in gtf format, with gene_id, gene_type and gene_name in the attribute column (9th)
- **genome_info.tsv** is a tab separated file, without header, with chromosome names (as in bigWig files) and chromosome sizes
- **/path/to/myViewR**, the directory to store your ViewR files
- **/path/to/python** refers to your python, with pybigWig and pytabix installed
  
#### 4. Copy the output of ./conf.sh on the server
```
sudo cp -r /path/to/myViewR/ /var/www/html/
sudo chmod -R +x /var/www/html/myViewR   # to allow execution of the scripts
```
#### 5. Launch ViewR
You can access your ViewR by typing **localhost/myViewR** in the adress bar of your web browser
  
### Authors
Ugo Szachnowski <ugo.szachnowski@hotmail.fr>
