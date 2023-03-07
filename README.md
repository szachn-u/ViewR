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

## Install

This is the file structure of the program:

/var/www/html/viewR/
<ul>
    <li>index.html (for redirection)</li>
    <li>scripts/ (for redirection)
        <ul><li>description.tsv (to edit)</li>
            <li>config.txt (to edit)</li>
            <li>php, python, css and js scripts (do not change)</li>
        </ul>
    </li>
    <li>bw/ (directory to store bigWig files)</li>
    <li>annot/
        <ul>
            <li>annot.gtf.gz (gtf file, to edit)</li>
            <li>annot.gtf.gz.tbi (gtf file index, to edit)</li>
            <li>gene_names.tsv.gz (gene name index, to edit)</li>
            <li>gene_types.txt (list of gene types, to edit)</li>
            <li>chr_size.tsv (chromosome sizes, to edit)</li>
        </ul>
    </li>
    <li>images/
        <ul>
            <li>fleche_droite_1.png (do not change)</li>
            <li>fleche_gauche_1.png (do not change)</li>
            <li>welcome.png (do not change)</li>
            <li>header.png (do not change)</li>
        </ul>
    </li>
</ul>

