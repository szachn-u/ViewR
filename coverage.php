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
			
			# initialize variables
			$gene = "";
			$chr = "";
			$start = -3;
			$stop = -2;
			$visu = "";
			$samples = [];
			$scale = "";
			$libType = "";
			$norm = "";
			$maxSignal = 0;
			$chr_size = -1;
			
			# for search by gene name
			$chrs = [];
			$Types = [];
			$starts = [];
			$stops = [];
			$IDs = [];
			$genes = [];
			$Parents = [];
			$i_gene = -1;
			
			# search by gene name 
			if (isset($_POST['gene_name'])) {
				$gene = $_POST['gene_name'];
			}
				
			if($gene != "") {
				$file=file("data/annotation.gff");
				$i_gene = 0;
				
				foreach($file as $line){
				        $line=explode("\t", $line);
					$tmp=explode(";",$line[8]);
					$matches=preg_grep("/^(ID=)?(gene=)?(Parent=)?$gene(,)?$/i", $tmp);	
					if(sizeof($matches) > 0){
						$chrs[$i_gene] = $line[0];
						$Types[$i_gene] = $line[2];
						$starts[$i_gene] = $line[3];
						$stops[$i_gene] = $line[4];
						$strands[$i_gene] = $line[6];
						$tmp_=preg_grep("/ID=/", $tmp);
						if(sizeof($tmp_) > 0){
							$IDs[$i_gene] = str_replace("ID=","",implode("", $tmp_));
						} else {
							$IDs[$i_gene] = ".";
						}
						$tmp_=preg_grep("/gene=/", $tmp);
						if(sizeof($tmp_) > 0){
							$genes[$i_gene] = str_replace("gene=","",implode("", $tmp_));
						} else {
							$genes[$i_gene] = ".";
						}
						$tmp_=preg_grep("/Parent=/", $tmp);
						if(sizeof($tmp_) > 0){
							$Parents[$i_gene] = str_replace("Parent=","",implode("", $tmp_));
						} else {
							$Parents[$i_gene] = ".";
						}
						$i_gene = $i_gene + 1; 
					}	
				}
				if($i_gene == 1){
					$chr = $chrs[0];
					$start = $starts[0];
					$stop = $stops[0];
					$coord = $start."-".$stop;
					$chr_list=file("data/chr_sizes.tab");
					foreach($chr_list as $line){
						$i_line = explode("\t", $line);
						$i_chr = $i_line[0];
						if ($i_chr == $chr) {
						$chr_size = (int)$i_line[1];
						}
					}
				}		
			} else if (isset($_POST['chromosome'])) {
			# genomic coordinates 
			# chromosome
				$chr=$_POST['chromosome'];
				$chr_list=file("data/chr_sizes.tab");
				foreach($chr_list as $line){
					$i_line = explode("\t", $line);
					$i_chr = $i_line[0];
					if ($i_chr == $chr) {
						$chr_size = (int)$i_line[1];
					}
				}
				# coordinates
				if(isset($_POST['coord'])){ 
					$coord = $_POST['coord'];
					if($coord != ""){
						$split = explode("-",$coord);
                       				# check coord validity
                               			if (count($split) == 2){
							$start = (int)$split[0];
							if(!is_numeric($start)){
								$start = 0;
							}
							$stop = (int)$split[1];
							if(!is_numeric($stop)){
								$stop = 0;
							}
						}							
					} 
				}
			}
			
			# visu type
			if(isset($_POST['visu'])){
				$visu = $_POST['visu'];
			}
			# sample names
			if(isset($_POST['samples'])){
				$samples=implode(",", $_POST['samples']);
			} 
			# scale
			if(isset($_POST['scale'])){
				$scale=$_POST['scale'];
			}
			# library type
			if(isset($_POST['library'])){
				$libType=$_POST['library'];
			}
			# normalized or raw data
			if(isset($_POST['norm'])){
				$norm = $_POST['norm'];
			}
			# max signal value
			$maxSignal=65987;

			# if wrong coordinates on browser
			if(isset($_POST['prev_coord']) && (($start == 0) || ($start > $chr_size) || ($stop < $start) || ($stop > $chr_size))){
				if($i_gene == -1){
					$prev_coord = $_POST['prev_coord'];
					$split = explode("-",$prev_coord);
					$start = $split[0];
					$stop = $split[1];
					echo"<div class=\"warning\" style=\"clear:both\">\n";
					echo "Genomic coordinates should be given in this form : start-stop<br/>\n";
					echo "with start < stop, within chromosome limits<br/>\n";
					echo "For $chr, limits are 1-$chr_size\n";
					echo"</div>\n";
				} else if ($i_gene == 0){
					$prev_coord = $_POST['prev_coord'];
					$split = explode("-",$prev_coord);
					$chr = $split[0];
					$start = $split[1];
					$stop = $split[2];
					echo"<div class=\"warning\" style=\"clear:both\">\n";
					echo "Gene $gene not found\n";
					echo"</div>\n";					
				}

			}
			
			# if several gene names found

			if (!empty($samples) && $i_gene > 1) {
				echo "<table>\n";
					echo "<thead>\n";
						echo "<tr>\n";
							echo "<th>Chr</th><th>Type</th><th>Start</th><th>Stop</th><th>Strand</th><th>ID</th><th>gene</th><th>Parent</th>\n";
						echo "</tr>\n";
					echo "</thead>\n";
					echo "<tbody>\n";
					for ($j = 0; $j <= ($i_gene-1); $j++){
						echo "</tr>\n";
							echo "<td>$chrs[$j]</td><td>$Types[$j]</td><td>$starts[$j]</td><td>$stops[$j]</td><td>$strands[$j]</td><td>$IDs[$j]</td><td>$genes[$j]</td><td>$Parents[$j]</td>\n";
							echo "<td>\n";
							echo "<form method=\"post\" action=\"coverage.php\">\n";
							# chr
							$chr = $chrs[$j];
							echo "<input type=\"hidden\" name=\"chromosome\" value=\"$chr\">\n";
							# coord
							$coord = $starts[$j]."-".$stops[$j];
							echo "<input type=\"hidden\" name=\"coord\" value=\"$coord\">\n";
							# samples
							echo "<input type=\"hidden\" name=\"samples[]\" value=\"$samples\">\n";
							# visu
							echo "<input type=\"hidden\" name=\"visu\" value=\"$visu\">\n";		
							# scale
							echo "<input type=\"hidden\" name=\"scale\" value=\"$scale\">\n";
							# library type
							echo "<input type=\"hidden\" name=\"library\" value=\"$libType\">\n";
							# normalized or raw data
							echo "<input type=\"hidden\" name=\"norm\" value=\"$norm\">\n";
							# submit
							echo "<input type=\"submit\" value=\"See\">\n";
							echo "</form>\n";
						echo "</td>\n";
					echo "</tr>\n";
					}
			 		echo "</tbody>\n";
				echo "</table>\n"; 
			# if valid coordinates
			} else if (!empty($samples) && ($start >= 1) && ($start < $chr_size) && ($stop <= $chr_size) && ($start < $stop)) {

			# navigate
			# back
                                if($start > 1){				
					echo "<div class = \"navigateur\" style=\"float:left;width:25%\">\n";
					echo "<form method=\"post\" action=\"coverage.php\">\n";
					# chr
					echo "<input type=\"hidden\" name=\"chromosome\" value=\"$chr\">\n";
					# new coord (start or stop - ((stop+start)/2))
					$span=(int)(($stop-$start)/2);
					$start_before=(int)$start-$span;
					$stop_before=(int)$stop-$span;
					if($start_before < 1){
						$start_before = 1;
						$stop_before = $span*2+1;
					}
					$coord_before=$start_before."-".$stop_before;
					echo "<input type=\"hidden\" name=\"coord\" value=\"$coord_before\">\n";
					# samples
					echo "<input type=\"hidden\" name=\"samples[]\" value=\"$samples\">\n";
					# visu
					echo "<input type=\"hidden\" name=\"visu\" value=\"$visu\">\n";		
					# scale
					echo "<input type=\"hidden\" name=\"scale\" value=\"$scale\">\n";
					# library type
					echo "<input type=\"hidden\" name=\"library\" value=\"$libType\">\n";
					# normalized or raw data
					echo "<input type=\"hidden\" name=\"norm\" value=\"$norm\">\n";
					# submit
					echo "<button class=\"button_nav\" type=\"submit\">\n";
					echo "<img src=\"images/fleche_gauche_1.png\" alt=\"Before\" height=\"80\" width=\"140\"/>\n";
					echo "</button>\n";
					echo "</form>\n";
					echo "</div>\n";
                                } else {
					echo "<div class = \"navigateur\" style=\"float:left;width:25%\">\n";
					echo "</div>\n";
				}

			# enter new coord
				echo "<div class = \"navigateur_coord\" style=\"float:left;width:50%\">\n";
				echo "<form method=\"post\" action=\"coverage.php\">\n";
				# chr
				echo "<SELECT name=\"chromosome\">\n";
				$chr_list=file("data/chr_sizes.tab");
				foreach($chr_list as $line){
					$i_chr=explode("\t", $line);
					$i_chr=$i_chr[0];
					echo "<OPTION value=\"$i_chr\">$i_chr\n";
				}
				echo "</SELECT>";
				# coord
				echo "<input type=\"text\" name=\"coord\">\n";
				# previous coord
				if($start > 0 & $stop > 1 & $start < $stop & $start < $chr_size & $stop <= $chr_size){
					$prev_coord=$chr."-".$start."-".$stop;
					echo "<input type=\"hidden\" name=\"prev_coord\" value=\"$prev_coord\">\n";
				}
				# visu
				echo "<input type=\"hidden\" name=\"visu\" value=\"$visu\">\n";
				# samples
				echo "<input type=\"hidden\" name=\"samples[]\" value=\"$samples\">\n";		
				# scale
				echo "<input type=\"hidden\" name=\"scale\" value=\"$scale\">\n";
				# library type
				echo "<input type=\"hidden\" name=\"library\" value=\"$libType\">\n";
				# normalized or raw data
				echo "<input type=\"hidden\" name=\"norm\" value=\"$norm\">\n";
				# max signal value
				echo "<input type=\"submit\" value=\"Submit\">\n";
				echo "</form>\n";
				echo "</div>\n";

			# forward
				if($start < $chr_size && $stop < $chr_size){
					echo "<div class = \"navigateur\" style=\"float:left;width:25%\">\n";
					echo "<form method=\"post\" action=\"coverage.php\">\n";
					# chr
					echo "<input type=\"hidden\" name=\"chromosome\" value=\"$chr\">\n";
					# new coord (start or stop + ((stop+start)/2))
					$span=(int)(($stop-$start)/2);
					$start_after=(int)$start+$span;
					$stop_after=(int)$stop+$span;
					if($stop_after > $chr_size){
						$start_after = $chr_size - $span*2;
						$stop_after = $chr_size;
					}
					$coord_after=$start_after."-".$stop_after;
					echo "<input type=\"hidden\" name=\"coord\" value=\"$coord_after\">\n";
					# samples
					echo "<input type=\"hidden\" name=\"samples[]\" value=\"$samples\">\n";
					# visu
					echo "<input type=\"hidden\" name=\"visu\" value=\"$visu\">\n";		
					# scale
					echo "<input type=\"hidden\" name=\"scale\" value=\"$scale\">\n";
					# library type
					echo "<input type=\"hidden\" name=\"library\" value=\"$libType\">\n";
					# normalized or raw data
					echo "<input type=\"hidden\" name=\"norm\" value=\"$norm\">\n";
					# submit
					echo "<button class=\"button_nav\" type=\"submit\">\n";
					echo "<img src=\"images/fleche_droite_1.png\" alt=\"After\" height=\"80\" width=\"140\"/>\n";
					echo "</button>\n";
					echo "</form>\n";
					echo "</div>\n";
				} else {
					echo "<div class = \"navigateur\" style=\"float:left;width:25%\">\n";
					echo "</div>\n";
				}

			# show coverage and annot
				$res=exec("/home/ugo/TOOLS/miniconda2/bin/python2.7 coverage.py $chr $start $stop $samples $visu $scale $libType $norm $maxSignal");
				$tmp = json_decode($res);
				$window_height=$tmp[2];
				echo "<div id=\"coverage\" style=\"height:$tmp[2]px;\"></div>\n"; 
  				echo "
  				<script>\n
      					var tmp = $res;\n
      					var data = tmp[0];\n
      					var layout = tmp[1];\n
      					Plotly.plot('coverage', data, layout, {staticPlot: true});\n
				</script>\n";

			# change visu parameters (volet)
				echo "<div id=\"volet_clos\">\n";
				echo "<div id=\"volet\">\n";
				echo "<form method=\"post\" action=\"coverage.php\">\n";
				echo "<input type=\"hidden\" name=\"chromosome\" value=\"$chr\">\n";
				echo "<input type=\"hidden\" name=\"coord\" value=\"$coord\">\n";
				echo "<input type=\"hidden\" name=\"samples[]\" value=\"$samples\">\n";
                		echo "<p>Visu type\n";
				echo "<SELECT name=\"visu\">\n";
				echo "<OPTION>heatmap\n";
				echo "<OPTION>lines\n";
				echo "<OPTION>fill\n";
				echo "</SELECT>\n";
				echo "</p>\n";
				echo "<p>Library Type\n";
				echo "<SELECT name=\"library\">\n";
				echo "<OPTION>unstranded\n";
				echo "<OPTION>standard\n";
				echo "<OPTION>inverse\n";
				echo "</SELECT>\n";
				echo "</p>\n";
                		echo "<p>Scale\n";
				echo "<input type=\"radio\" name=\"scale\" value=\"log\" checked>log2\n";
				echo "<input type=\"radio\" name=\"scale\" value=\"linear\">linear\n";
				echo "</p>\n";
                		echo "<p>Normalized data\n";
				echo "<input type=\"radio\" name=\"norm\" value=\"True\" checked>Yes\n";
                		echo "<input type=\"radio\" name=\"norm\" value=\"False\">No<br/>\n";
				echo "</p>\n";
				echo "<p>\n";
				echo "<input type=\"submit\" value=\"Submit\"><br/>\n";
				echo "</p>\n";
				echo "</form>\n";	
				echo "<a href=\"#volet\" class=\"ouvrir\" aria-hidden=\"true\">Parameters</a>\n";
				echo "<a href=\"#volet_clos\" class=\"fermer\" aria-hidden=\"true\">Parameters</a>\n";
				echo "</div>\n"; # close volet
				echo "</div>\n"; # close volet_clos

			# show count table
				echo "<div class = \"count_table\" style=\"float:left;height:600px;margin-left:140px;margin-right:100px;width:calc(100% - 240px)\">\n";
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

			# get count table file
				$count_file=file("data/counts_raw.tab");
				$i=0;
				$samples= explode(",",$samples);
				foreach($count_file as $line){
			# /!\ 1st line of count file should be header
					if($i==0){
						echo "<tr>\n";
			# print table 1st line
						echo "<th>Chr</th><th>Type</th><th>Start</th><th>Stop</th><th>Strand</th><th>ID</th><th>Name</th><th>Parent</th><th>gene</th>";
						foreach($samples as $s){
							echo "<th>";
							echo $s . " densities";
							echo "</th>";		
						}
						echo "\n";

			# get count table header
						$table_header=explode("\t", $line);
						echo "</tr>\n";

					} else {

						$line=explode("\t", $line);

						if($line[0] == $chr and $start < $line[3] and $stop > $line[2]){
							echo "<tr>\n";
							# annot
							echo "<td>";
							echo implode("</td><td>",array_slice($line,0,9));
							echo "</td>";
							foreach($samples as $s){
								echo "<td>";
								if(array_search($s, $all_samples) !== FALSE){	
									$i_sample=$s." readcount";
									$sample_index=array_search($i_sample, $table_header);
									$val=$line[$sample_index];

									#normalize data
									if($norm == "True"){
										$val=$val*$all_coeff[array_search($s, $all_samples)];
									}

									# get densities (read/nt)
									$l=$line[3]-$line[2]+1;
									$val=$val/$l;	
								} else {
									$val=0;
									# get samples associated to group
									$which_samples=array_keys($all_groups, $s);
									$nb_samples=0;
	
									foreach($which_samples as $which_sample){
										$i_sample=$all_samples[$which_sample]. " readcount";
										$sample_index=array_search($i_sample, $table_header);
										$i_val=$line[$sample_index];

										# normalize data
										if($norm=="True"){
											$i_val=$i_val*$all_coeff[$which_sample];
										}
										$val=$val+$i_val;
										$nb_samples=$nb_samples+1;
									}

									# get samples mean
									$val=$val/$nb_samples;

									# get densities (read/nt)
									$l=$line[3]-$line[2]+1;
									$val=$val/$l;
								}
								# get scientific notation
								$power = ($val % 10) - 1;
								if($power < -2 or $power > 2){
        								$val=round(($val / pow(10, $power)), 3) . "e" . $power;
								} else {
									$val=round($val, 3);
								}
								echo $val;
								echo "</td>";
							}				
							echo "</tr>\n";
						}

					}	
					$i=$i+1;
				}	
				echo "</table>\n"; # close table
				echo "</div>\n"; # close count_table div
				echo "<div style=\"clear:both;height:20px\"></div>";	
			} else {
			# set parameters and coord
				echo "<form method=\"post\" action=\"coverage.php\">\n";
			# samples
				if (empty($samples) && isset($_POST['coord'])){
					echo "<div class=\"hr\"><font color=\"red\">SAMPLE SELECTION</font></div>\n";
				} else {
					echo "<div class=\"hr\">Sample selection</div>\n";
				}

				$names=file("data/description_data.tab");
				$i=0;
				$groups = array();
				foreach($names as $name){
				   if($i != 0){
				     $l=explode("\t", $name);
				     array_push($groups, $l[6]);
				   }
				   $i=$i+1;
				}
				$groups=array_unique($groups);
				$j=1;
				foreach($groups as $g){
					echo "<div style=\"float:left;width:20%\">\n";
					$i=0;
					echo "<ul style=\"list-style-type:none\">\n";
					echo "<li><input type=\"checkbox\" name=\"samples[]\" value=\"$g\">$g<br/></li>\n";
					foreach($names as $name) {
						if($i != 0){
							$line=explode("\t", $name);
							$i_group=$line[6];
							$i_name=$line[1];
							if($i_group == $g){
								echo "<li><input type=\"checkbox\" name=\"samples[]\" value=\"$i_name\">$i_name</li>\n";
				     			}
				   		} 
					$i=$i+1;
				  	}
				  	echo "</ul>\n";
					echo "</div>\n";
					$j = $j+1;
					if(fmod($j,5) == 1){
						echo "<div style=\"clear:both;width:100%;height:20px\"></div>\n";
					}
				}
				echo "<div style=\"clear:both;width:100%\"></div>";
				echo "<div class=\"hr\">Display option</div>\n";
			# visu type
				echo "<div style=\"float:left;width:25%;text-align:center;height:100px\">\n";
                		echo "<p>Select visualization type</p>\n";
				echo "<SELECT name=\"visu\">\n";
				echo "<OPTION>heatmap\n";
				echo "<OPTION>lines\n";
				echo "<OPTION>fill\n";
				echo "</SELECT>\n";
				echo "</div>\n";
			# lib type
				echo "<div style=\"float:left;width:25%;text-align:center;height:100px\">\n";
				echo "<p>Select library type</p>\n";
				echo "<SELECT name=\"library\">\n";
				echo "<OPTION>unstranded\n";
				echo "<OPTION>standard\n";
				echo "<OPTION>inverse\n";
				echo "</SELECT>\n";
				echo "</div>\n";
			# scale
				echo "<div style=\"float:left;width:25%;text-align:center;height:100px\">\n";
                		echo "<p>Select scale</p>\n";
				echo "<input type=\"radio\" name=\"scale\" value=\"log\" checked>log2\n";
				echo "<input type=\"radio\" name=\"scale\" value=\"linear\">linear\n";
				echo "</div>\n";
			#normalization
				echo "<div style=\"float:left;width:25%;text-align:center;height:100px\">\n";
                		echo "<p>Normalized data</p>\n";
				echo "<input type=\"radio\" name=\"norm\" value=\"True\" checked>Yes\n";
                		echo "<input type=\"radio\" name=\"norm\" value=\"False\">No<br/>\n";
				echo "<br/>\n";
				echo "</div>\n";
				# search by genomic coordinate 
			
			# genomic coordinates
				echo "<div style=\"clear:both;width:100%\"></div>";
				echo "<div class=\"hr\">Select genomic region</div>\n";
			
			# chromosome
				echo "<div style=\"float:left;width:33%;text-align:center;height:100px\">\n";
				echo "<p>Select genomic coordinates (start-stop)</p>\n";
				echo "<SELECT name=\"chromosome\">\n";
				$chr_list=file("data/chr_sizes.tab");
					foreach($chr_list as $line){
						$i_chr=explode("\t", $line);
						$i_chr=$i_chr[0];
						echo "<OPTION value=\"$i_chr\">$i_chr\n";
					}
				echo "</SELECT>\n";				
			# coord
				echo "<input type=\"text\" name=\"coord\">\n";
				#if (($start == 0) || ($start > $chr_size) || ($stop > $chr_size) || ($start >= $stop)){
					#echo"<div class=\"warning\" style=\"clear:both;width:25%\">\n";
				#	echo "Genomic coordinates should be given in this form : start-stop<br/>\n";
				#	echo "with start < stop, within chromosome limits<br/>\n";
				#	echo "For $chr, limits are 1-$chr_size\n";
					#echo"</div>\n";	
				#}
				echo "</div>\n";
			# search gene name
				echo "<div style=\"float:left;width:33%;text-align:center;height:100px\">\n";
				echo "<p>Enter gene name</p>\n";
				echo "<input type=\"text\" name=\"gene_name\">\n";
				#if ($i_gene == 0) {
				#	echo"<div class=\"warning\" style=\"clear:both;width:25%\">\n";
				#	echo "Gene $gene not found\n";
				#	echo"</div>\n";					 
				#}
				echo "</div>\n";
				# if gene not found
				#if ($i_gene == 0) {
				#	echo"<div class=\"warning\" style=\"clear:both;width:25%\">\n";
				#	echo "Gene $gene not found\n";
				#	echo"</div>\n";					 
				# if coordinates given are wrong format or outside chromosome 
				#} else if (($start == 0) || ($start > $chr_size) || ($stop > $chr_size) || ($start >= $stop)){
				#	echo"<div class=\"warning\" style=\"clear:both;width:25%\">\n";
				#	echo "Genomic coordinates should be given in this form : start-stop<br/>\n";
				#	echo "with start < stop, within chromosome limits<br/>\n";
				#	echo "For $chr, limits are 1-$chr_size\n";
				#	echo"</div>\n";	
				#}
			# submit
				echo "<div style=\"float:left;width:33%;height:100px;text-align:center;line-height:140px\">\n";
				echo "<div><input type=\"submit\" value=\"GO!\"></div>\n";
				echo "</div>\n";
				echo "</form>\n";
				echo "<div style =\"clear:both;width:100%;height:25px\"></div>\n";					
			}
			?>
		</div> <!-- close contenu -->
		<div class = "footer">
		<p>January 17 2019<br>
		Version 0.0</p>
		</div>
	</body>
</html>
