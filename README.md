# ViewR

ViewR is a Web browser for NGS data exploration, that allows the vizualisation of any read coverage across the genome (RNA-seq, ChIP-seq, etc), along with the corresponding gene annotation.

## How It Works

ViewR is designed to take coverage data as [bigWig](https://genome.ucsc.edu/goldenPath/help/bigWig.html) files and annotation as [gtf](https://www.ensembl.org/info/website/upload/gff.html) file.  
It runs with [Apache](https://httpd.apache.org/) on Ubuntu, and requires php and python3, with [pyBigWig](https://github.com/deeptools/pyBigWig) and [pytabix](https://github.com/slowkow/pytabix) libraries.  
A php script produce the interface, a python script extract coverage values and genes coordinates requested, and the [Plolty](https://plotly.com/javascript/) graphical library generate the graphs.  

## Browser Compatibilities

| Chrome | Firefox | 
| ------ | ------- |
| ✔      | ✔       |

## Installation

1. Clone the repository
<p> git clone https://github.com/szachn-u/ViewR.git</p>
2. Edit description file
<p>In script directory, edit the "desciption.tsv" file</p>
3. Prepare annotation files
<p>Run prepare_annot.sh script, in utils directory</p>

