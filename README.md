# ViewR

ViewR is a Web browser for NGS data exploration, that allows the vizualisation of any read coverage across the genome (RNA-seq, ChIP-seq, etc), along with the corresponding gene annotation.

## How It Works

ViewR is designed to take coverage data as [bigWig](https://genome.ucsc.edu/goldenPath/help/bigWig.html) files and annotation as [gtf](https://www.ensembl.org/info/website/upload/gff.html) file.  
It runs with [Apache](https://httpd.apache.org/) on Ubuntu, and requires php and python3, with [pyBigWig](https://github.com/deeptools/pyBigWig) and [pytabix](https://github.com/slowkow/pytabix) libraries.  A php script produce the interface, a python script extract coverage values and genes coordinates requested, and the [Plolty](https://plotly.com/javascript/) graphical library generate the graphs.  

## Browser Compatibilities

| Chrome | Firefox | 
| ------ | ------- |
| ✔      | ✔       |

## Install

This is the file structure of the program:

/var/www/html/viewR
    |
    |--index.html (for redirection)
    |--scripts
        |--description.tsv
        |--config.txt
        |--index.php
        |--coverage.php
        |--functions.php
        |--coverage.py
        |--functions.py
        |--functions.js
        |--design.css
    |--bw
        |--sample1.bw
        |--sample2.bw
        |--...
    |--annot
        |--annot.gtf.gz
        |--annot.gtf.gz.tbi
        |--gene_names.tsv.gz
        |--gene_types.txt
        |--chr_size.tsv
    |--images
        |--fleche_droite_1.png
        |--fleche_gauche_1.png
        |--welcome.png
        |--header.png


