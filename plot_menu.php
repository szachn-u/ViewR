<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="fr" lang="fr">
	<head>
		<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
		<link rel="stylesheet" media="screen" type="text/css" title="Design" href="design.css" />
		<script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
	</head>

	<body>
		<div class = "header">General Title</div>
		<div class = "onglet">
        	<div class = "inactif"><a href="main.php">Main</a></div>
			<div class = "inactif"><a href="coverage.php">Coverage</a></div>
			<div class = "actif"><a href="plot_menu.php">Plots</a></div>	
			<div class = "inactif"><a href="table_exprs_sort.php">Count table</a></div>	
			<div class = "inactif"><a href="about.php">About</a></div>
		</div>
		<div class = "contenu" style = "height:800px">
			<div style="float:left;width:calc(33% - 21px);text-align:center;margin:50px 10px 5px 10px;border:groove">
				<div>Scatter plot</div>
				<div><img src="images/scatter.png" height="500px" width="90%"></div>
				<div style="border-top:groove"></div>
				<a href="scatterplot.php" class="button" style="width:calc(100% - 5px)">Expression levels</a>
			</div>
			<div style="float:left;width:calc(33% - 21px);text-align:center;margin:50px 10px 5px 10px;border:groove">
				<div>Boxplot</div>
				<div><img src="images/boxplot.png" height="500px" width="90%"></div>
				<div style="border-top:groove"></div>
				<a href="boxplot_exprs.php" class="button" style="width:calc(50% - 6px)">Expression levels</a>
				<a href="boxplot_fc.php" class="button" style="width:calc(50% - 6px)">Fold-change</a>
			</div>
			<div style="float:left;width:calc(33% - 21px);text-align:center;margin:50px 10px 5px 10px;border:groove">
				<div>Density plot</div>
				<div><img src="images/density.png" height="500px" width="90%"></div>
				<div style="border-top:groove"></div>
				<a href="densityplot_exprs.php" class="button" style="width:calc(50% - 6px)">Expression levels</a>
				<a href="densityplot_fc.php" class="button" style="width:calc(50% - 6px)">Fold-change</a>
			</div>
		</div>
		<div class = "footer">
			<p>January 17 2019<br>
			Version 0.0</p>
		</div>
	</body>
</html>
