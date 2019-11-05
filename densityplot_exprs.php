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
			<div style="text-align:center;float:left;width:100%;height:50px;line-height:50px;border-bottom:groove">Density plot</div>
			<div style="float:left;width:250px;padding:10px;border-right:groove;height:780px">    <!-- paramètres density plot -->             		
				<?php
					$names=file("data/description_data.tab");
					$i=0;
					$samples = array();
					$groups = array();
					foreach($names as $name){
					   if($i != 0){
					     $l=explode("\t", $name);
					     array_push($samples, $l[1]);
					     array_push($groups, $l[6]);
					   }
					   $i=$i+1;
					}
					$groups=array_unique($groups);
					echo "<form method=\"post\" action=\"densityplot_exprs.php\">\n";
					echo "<ul style=\"list-style-type:none;padding-left:10px\">Sample\n";
					echo "<li><SELECT name=\"sample\" size=1>\n";
					echo "<OPTION>\n";
					foreach($groups as $g){
						$i=0;
						foreach($names as $name) {
							if($i != 0){
					   			$l=explode("\t", $name);
					   			$ig=$l[6];
					     			$n=$l[1];
					     			if($ig == $g){
					       				echo "<OPTION>$n\n";
					     			}
					   		} 
					   		$i=$i+1;
					  	}
						echo "<OPTION>$g\n";
					}
					echo "</SELECT></li>\n";
					echo "</ul>\n";			
				?>
                	
               	<ul style="list-style-type:none;padding-left:10px;margin-top:50px">Count type
					<li><input type="radio" name="count_type" value="densities" checked>Densities</li>
                	<li><input type="radio" name="count_type" value="readcount">Read counts</li>
				</ul>
                	
                <ul style="list-style-type:none;padding-left:10px;margin-top:50px">Normalized data
					<li><input type="radio" name="norm" value="True" checked>Yes</li>
                	<li><input type="radio" name="norm" value="False">No</li>
				</ul>
					
				<ul style="list-style-type:none;padding-left:100px;margin-top:50px">
					<li><input type="submit" value="Submit"></li>
					</ul>
				</form>		
			</div> <!-- close volet -->
						<?php
			# sample names
  				if(isset($_POST['sample'])){
    				$sample=$_POST['sample'];
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
				if (isset($_POST['sample'])){
					$res = exec("/home/ugo/TOOLS/miniconda2/bin/python2.7 kde.py \"exprs\" $sample $count_type $norm");
						echo "<div id=\"density\"></div>";
							echo "
							<script>
							var res = $res;
							var data = res[0];
							var layout = res[1];
							Plotly.newPlot('density', data, layout, {displaylogo: false, modeBarButtonsToRemove : ['select2d','lasso2d','zoomIn2d','zoomOut2d','autoScale2d','hoverClosestCartesian','hoverCompareCartesian','toggleHover','toggleSpikelines']});
							</script>";
  				} else {
						echo "<div id=\"density\"></div>";
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
