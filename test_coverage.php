<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="fr" lang="fr">
	<head>
		<title>Browser python</title>
	<meta http-equiv="Content-Type" content="text/html; charset=utf-8"/>
	<link rel="stylesheet" media="screen" type="text/css" title="Design" href="design.css"/>
	<script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
	</head>
	<body>
		<div class = "header">General Title</div>
		<div class = "onglet">
        		<div class = "inactif"><a href="main.php">Main</a></div>
			<div class = "actif"><a href="coverage.php">Coverage</a></div>
			<div class = "inactif"><a href="plot_menu.php">Plots</a></div>
			<div class = "inactif"><a href="table_exprs_sort.php">Count table</a></div>
			<div class = "inactif"><a href="about.php">About</a></div>
		</div>
		<div class = "contenu" style="min-height:800px">
			<?php

				$chr="chr01";
				$start=30000;
				$stop=50000;
				#$samples="WT.G1.A238,xrn1.G1.4,WT.G1.1,rad50set1.G1.A237,xrn1.G1.3,xrn1.G1.1,rad50.G1.A237";
				#$visu="heatmap,heatmap,heatmap,heatmap,heatmap,heatmap,heatmap";
				#$scale="log,log,log,log,log,log,log";
				#$libType="stranded,stranded,stranded,stranded,stranded,stranded,stranded";
				#$norm="True,True,False,False,True,True,True";
				
				$samples="xrn1.G1.4,xrn1.G1.4,xrn1.G1.A238";
				$visu="fill,fill,fill";
				$scale="log,log,log";
				$libType="stranded,stranded,unstranded";
				$norm="True,True,True";
				
			# show coverage and annot
				$res=exec("/home/ugo/TOOLS/miniconda2/bin/python coverage.py $chr $start $stop $samples $visu $scale $libType $norm");
				
				$tmp = json_decode($res);
				
				$window_height=$tmp[2] . "px";
				
				echo "<div id=\"coverage\" style=\"height:$window_height;\"></div>\n"; 
  				
  				echo "
  				
  				<script>\n
      					var tmp = $res;\n
      					var data = tmp[0];\n
      					var layout = tmp[1];\n
      					Plotly.plot('coverage', data, layout, {staticPlot: true});\n
				</script>\n";
			?>
		</div> <!-- close contenu -->
		<div class = "footer">
		<p>January 17 2019<br>
		Version 0.0</p>
		</div>
	</body>
</html>
