# ViewR

ViewR is a Web browser for NGS data exploration, that allows the vizualisation of any read coverage across the genome (RNA-seq, ChIP-seq, etc), along with the corresponding gene annotation.

# How It Works

ViewR is designed to take coverage data as [bigWig](https://genome.ucsc.edu/goldenPath/help/bigWig.html) files and annotation as [gtf](https://www.ensembl.org/info/website/upload/gff.html) file.
It runs with [Apache](https://httpd.apache.org/) on Ubuntu, and requires php and python3, with [pyBigWig](https://github.com/deeptools/pyBigWig) and [pytabix](https://github.com/slowkow/pytabix) libraries.
