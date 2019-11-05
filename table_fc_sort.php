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
			<div class = "inactif"><a href="plot_menu.php">ScatterPlot</a></div>
			<div class = "actif"><a href="table_fc_sort.php">Count table</a></div>
			<div class = "inactif"><a href="about.php">About</a></div>
		</div>
		<div class = "contenu">
		
			<!-- parameters -->
			<div>
				<div style="float:left;width:125px;height:50px;text-align:center;line-height:50px;border-bottom:groove"><a href="table_exprs_sort.php">Counts</a></div>
				<div style="float:left;width:125px;height:50px;text-align:center;line-height:50px;border:groove;border-bottom:none">Fold-change</div>
			</div>
			<div style="clear:both"></div>
			<div style="float:left;width:250px;height:800px;border:groove;border-top:none">
				<form method="post" action="table_fc_sort.php">
					<p style="text-align:center">Fold-change</p>
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
					<ul style="list-style-type:none">Scale
						<li><input type="radio" name="scale" value="log" checked>log</li>
						<li><input type="radio" name="scale" value="linear" >linear</li>
					</ul>
					<ul style="list-style-type:none">Normalized counts
						<li><input type="radio" name="norm" value="yes" checked>Yes</li>
						<li><input type="radio" name="norm" value="no">No</li>
					</ul>
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
						for ($s = 1; $s <= 2; $s++){
							echo "<ul style=\"list-style-type:none\">Sample $s\n";
							echo "<li><SELECT name=\"sample$s\" size=1>\n";
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
							echo "</SELECT>\n";
							echo "</li>\n";
							echo "</ul>\n";
						}							
					?>
					<ul style="list-style-type:none">
						<li><input type="submit" value="See table"></li>
					</ul>
				</form>	
					
			</div>
	
			<!-- table -->
			<?php

			$sample1="";
			$sample2="";

			if(isset($_POST['sample1']) && isset($_POST['sample2'])){
				$sample1=$_POST['sample1'];
				$sample2=$_POST['sample2'];	
			}

			if($sample1 != "" && $sample2 != ""){
			
				$Types=$_POST['Types'];
				$scale=$_POST['scale'];
				$norm=$_POST['norm'];
				$which_samples=$sample1 . "," . $sample2;
			
				echo "<div class = \"count_table\" style=\"float:left;width:calc(100% - 280px);height:800px\">\n";
				echo "<table>\n";

			# Table header
				echo "<thead>\n";
				echo "<tr>\n";
			
			# for sorting			
				echo "<form method=\"post\" action=\"table_fc_sort.php\">\n";
				echo "<input type=\"hidden\" name=\"sample1\" value=\"$sample1\">\n";
				echo "<input type=\"hidden\" name=\"sample2\" value=\"$sample2\">\n";
				echo "<input type=\"hidden\" name=\"Types\" value=\"$Types\">\n";
				echo "<input type=\"hidden\" name=\"scale\" value=\"$scale\">\n";
				echo "<input type=\"hidden\" name=\"norm\" value=\"$norm\">\n";							
						
				echo "<th>Chr</th><th>Type</th><th>Start</th><th>Stop</th><th>Strand</th><th>ID</th><th>Name</th><th>Parent</th><th>gene</th>";
				for($i=0; $i < 2; $i++){
					echo "<th>";
					echo "<div style=\"float:left;height:100%;width:90%\">";
					if($scale == "log"){
						echo "log2 <br/>";
					}
					if($i==0){
						echo $sample1 . "/<br/> " . $sample2;
					} else {
						echo $sample2 . "/<br/> " . $sample1;
					}
					echo "</div>";
					echo "<div style=\"float:left;height:100%;width:10%\">";
					echo "<button class=\"button_sort\" type=\"submit\" name=\"sort_up\" value=\"" . $i . "\">\n";
					echo "<img src=\"images/button_up.png\" alt=\"up\" height=\"20\" width=\"15\"/>\n";
					echo "</button>\n";
					echo "<br/>";
					echo "<button class=\"button_sort\" type=\"submit\" name=\"sort_down\" value=\"" . $i . "\">\n";
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
						$sort_by="-1";
						$sort_sens="none";
					}
				}	
				
				echo "</form>\n";
						
				echo "\n";

				echo "</tr>\n";
				echo "</thead>\n";
				echo "<tbody>\n";
				
				$res=exec("/home/ugo/TOOLS/miniconda2/bin/python2.7 count_table.py \"fc\" $which_samples $Types \"readcount\" $scale $norm $sort_by $sort_sens");
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
