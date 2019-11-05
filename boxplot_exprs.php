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
			<div class = "inactif"><a href="coverage.php">Coverage</a></div>
			<div class = "actif"><a href="plot_menu.php">Plots</a></div>	
			<div class = "inactif"><a href="table_exprs_sort.php">Count table</a></div>		
			<div class = "inactif"><a href="about.php">About</a></div>
		</div>
		<div class = "contenu">
			<div style="text-align:center;float:left;width:100%;height:50px;line-height:50px;border-bottom:groove">Boxplot</div>
			<div style="float:left;width:250px;padding:10px;border-right:groove;height:780px">    <!-- paramètres boxplot --> 
				<form method="post" action="boxplot_exprs.php">
				<ul style="list-style-type:none;padding-left:10px;margin-top:50px">Samples
					<li><input type="radio" name="sample_type" value="main" checked>Mains</li>
                	<li><input type="radio" name="sample_type" value="replicates">replicates</li>
				</ul>
			            		
				<ul style="list-style-type:none;padding-left:10px;margin-top:50px">Group by
					<li><input type="radio" name="group_by" value="Samples" checked>Sample</li>
                	<li><input type="radio" name="group_by" value="Types">Type</li>
				</ul>
                	
               	<ul style="list-style-type:none;padding-left:10px;margin-top:50px">Count type
					<li><input type="radio" name="count_type" value="densities" checked>Densities</li>
                	<li><input type="radio" name="count_type" value="readcount">Read counts</li>
				</ul>
                	
                <ul style="list-style-type:none;padding-left:10px;margin-top:50px">Normalized data
					<li><input type="radio" name="norm" value="True" checked>Yes</li>
                	<li><input type="radio" name="norm" value="False">No</li>
				</ul>
					
				<ul style="list-style-type:none;padding-left:100px;margin-top:50px">
					<li><input type="submit" name="get_boxplot" value="Submit"></li>
					</ul>
				</form>		
			</div> 
			<?php
			# sample type
				if(isset($_POST['sample_type'])){
    				$sample_type=$_POST['sample_type'];
  				}
			# group by
  				if(isset($_POST['group_by'])){
    				$group_by=$_POST['group_by'];
  				}
  			#count type
  				if (isset($_POST['count_type'])){
					$count_type=$_POST['count_type'];
				}
			# norm
				if (isset($_POST['norm'])){
					$norm=$_POST['norm'];
				} 

			# get coverage and annot
				if (isset($_POST['get_boxplot'])){
					$res = exec("/home/ugo/TOOLS/miniconda2/bin/python2.7 boxplot.py \"exprs\" $sample_type $group_by $count_type $norm");
						echo "<div id=\"boxplot\"></div>";
							echo "
							<script>
							var res = $res;
							var data = res[0];
							var layout = res[1];
							Plotly.newPlot('boxplot', data, layout, {displaylogo: false, modeBarButtonsToRemove : ['select2d','lasso2d','zoomIn2d','zoomOut2d','autoScale2d','hoverClosestCartesian','hoverCompareCartesian','toggleHover','toggleSpikelines']});
							</script>";
  				} else {
						echo "<div id=\"boxplot\"></div>";
							echo "
							<script>
							var data = [{x:[0],
										y:[0],
    									showlegend : false }];
    						var layout = {margin : {l: 50, r: 25, b: 50, t: 25}};
							Plotly.newPlot('density', data, layout, {displaylogo: false, modeBarButtonsToRemove : ['select2d','lasso2d','zoomIn2d','zoomOut2d','autoScale2d','hoverClosestCartesian','hoverCompareCartesian','toggleHover','toggleSpikelines']});
							</script>";
  				}
			?>
		</div> <!-- close contenu -->
		<div class="footer" style="border-top:groove">
		<p>January 17 2019<br>
		Version 0.0</p>
		</div>
	</body>
</html>
