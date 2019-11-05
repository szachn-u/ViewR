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
			<div class = "inactif"><a href="plot_menu.php">Plots</a></div>
			<div class = "actif"><a href="table_exprs_sort.php">Count table</a></div>
			<div class = "inactif"><a href="about.php">About</a></div>
		</div>
		<div class = "contenu">
		
			<!-- parameters -->
			<div>
				<div style="float:left;width:125px;height:50px;text-align:center;line-height:50px;border:groove;border-bottom:none">Counts</div>
				<div style="float:left;width:125px;height:50px;text-align:center;line-height:50px;border-bottom:groove"><a href="table_fc.php">Fold-change</a></div>
			</div>
			<div style="clear:both"></div>
			<div style="float:left;width:250px;height:800px;border:groove;border-top:none">
				<form method="post" action="table_exprs_sort.php">
				<ul style="list-style-type:none">Samples
					<li><input type="radio" name="which_samples" value="main" checked>Main</li>
					<li><input type="radio" name="which_samples" value="replicates">Replicates</li>
				</ul>
				<ul style="list-style-type:none">Type(s)
					<li>
					<SELECT name="Types">
						<OPTION>all
					<?php
					$count_file=file("data/counts_raw_short.tab");
					$i=0;
					$all_types=array();
					foreach($count_file as $line){
						if($i != 0){
							$line=explode("\t", $line);
							array_push($all_types, $line[1]);
						}
						$i=$i+1;
					}
					$Types=array_unique($all_types, SORT_STRING);
			
					foreach($Types as $Type){
						echo "	<OPTION>" . $Type . "\n";
					} 
					?>
					</SELECT>
					</li>
				</ul>
				<ul style="list-style-type:none">Count Type
					<li><input type="radio" name="count_type" value="readcount" checked>Readcount</li>
					<li><input type="radio" name="count_type" value="densities">Densities</li>
				</ul>
				<ul style="list-style-type:none">Normalized counts
					<li><input type="radio" name="norm" value="True" checked>Yes</li>
					<li><input type="radio" name="norm" value="False">No</li>
				</ul>
				<ul style="list-style-type:none">
					<li><input type="submit" name="get_table" value="See table"></li>
				</ul>
				</form>
			</div>
	
			<!-- table -->
			<?php

			if(isset($_POST['get_table'])){
			
				$Types=$_POST['Types'];
				$count_type=$_POST['count_type'];
				$which_samples=$_POST['which_samples'];
				$norm=$_POST['norm'];
			
				echo "<div class = \"count_table\" style=\"float:left;width:calc(100% - 280px);height:800px\">\n";
				echo "<table>\n";

			# get description data
				$description_file=file("data/description_data.tab");
				$all_groups = array();
				$all_samples = array();
				$all_coeff = array();
				$i=0;
			# /!\ 1st line of description data file not red
				foreach($description_file as $line){
					if($i!=0){
						$line=explode("\t", $line);
						$all_groups[] = $line[6];
						$all_samples[] = $line[1];
						$all_coeff[] = $line[2];
					}
					$i=$i+1;
				}
				
			# sample selection
				if ($which_samples == "main"){
					$samples= array_unique($all_groups);
				} else {
					$samples= $all_samples;
				}
				sort($samples);
				

			# Table header
				echo "<thead>\n";
				echo "<tr>\n";
			
			# for sorting			
				echo "<form method=\"post\" action=\"table_exprs_sort.php\">\n";
				echo "<input type=\"hidden\" name=\"which_samples\" value=\"$which_samples\">\n";
				echo "<input type=\"hidden\" name=\"Types\" value=\"$Types\">\n";
				echo "<input type=\"hidden\" name=\"count_type\" value=\"$count_type\">\n";
				echo "<input type=\"hidden\" name=\"norm\" value=\"$norm\">\n";						
				echo "<input type=\"hidden\" name=\"get_table\" value=\"See table\">\n";		
						
				echo "<th>Chr</th><th>Type</th><th>Start</th><th>Stop</th><th>Strand</th><th>ID</th><th>Name</th><th>Parent</th><th>gene</th>";
				foreach($samples as $s){
					echo "<th>";
					echo "<div style=\"float:left;height:100%;width:90%\">";
					echo $s . "<br/>" . $count_type;
#					echo "<br/>";
					echo "</div>";
					echo "<div style=\"float:left;height:100%;width:10%\">";
					echo "<button class=\"button_sort\" type=\"submit\" name=\"sort_up\" value=\"" . $s . "\">\n";
					echo "<img src=\"images/button_up.png\" alt=\"up\" height=\"20\" width=\"15\"/>\n";
					echo "</button>\n";
					echo "<br/>";
					echo "<button class=\"button_sort\" type=\"submit\" name=\"sort_down\" value=\"" . $s . "\">\n";
					echo "<img src=\"images/button_down.png\" alt=\"down\" height=\"20\" width=\"15\"/>\n";
					echo "</button>\n";
					echo "</div>";
					echo "</th>";	
				}
				
				if(isset($_POST['sort_up'])){	
					$sort_by=$_POST['sort_up'];
					$sort_sens="up";
				} else {
					if(isset($_POST['sort_down'])){
						$sort_by=$_POST['sort_down'];
						$sort_sens="down";
					} else {
						$sort_by="none";
						$sort_sens="none";
					}
				}	
				
				echo "</form>\n";
						
				echo "\n";

				echo "</tr>\n";
				echo "</thead>\n";
				echo "<tbody>\n";
				
				$res=exec("/home/ugo/TOOLS/miniconda2/bin/python2.7 count_table.py \"exprs\" $which_samples $Types $count_type \"linear\" $norm $sort_by $sort_sens");
				$table = json_decode($res);
				
				for($i = 0; $i < sizeof($table); $i++){
					echo "<tr>";
					for($j = 0; $j < sizeof($table[0]); $j++){
						echo "<td>" . $table[$i][$j] . "</td>";
					}
					echo "</tr>\n";
				}
				
				echo "</tbody>\n";
				echo "</table>\n"; # close table
				echo "</div>\n"; # close count_table div
			}
					
			?>
		</div> <!-- close contenu -->
		<div class = "footer">
		<p>January 17 2019<br>
		Version 0.0</p>
		</div>
	</body>
</html>
