<?php

# read table from file and return an array
# in : 
# out : 

	function readTable($tableFile, $headerFirstLine, $tableColumnIndex, $columnNames, $fieldSep){
	
		# set variable if no args given
	
		if(!isset($fieldSep)){
		
			$fieldSep="\t";
		
		}

		if(!isset($headerFirstLine)){
		
			$headerFirstLine=False;
		
		}

		if(!isset($columnNames)){
		
			if($headerFirstLine){
			
				$f = fopen($tableFile, 'r');
			
				$columnNames = explode($fieldSep, fgets($f));
			
				fclose($f);
			
			} else {
			
				$f = fopen($tableFile, 'r');
			
				$ncol = count(explode($fieldSep, fgets($f)));
			
				$columnNames=range(0,(count($ncol)-1));
			
				fclose($f);
			
			}
		
		}

		if(!isset($tableColumnIndex)){
		
			$tableColumnIndex = range(0,(count($columnNames)-1));
		
		}

		# initalize table

		$table=array();
		
		$ncol=count($tableColumnIndex);
		
		for($j_col=0; $j_col < $ncol; $j_col++){
		
			$colName=$columnNames[$tableColumnIndex[$j_col]];
		
			$table[$colName] = array();

		}
	
		$i_line=0;
	
		$tableFile_=file($tableFile);
	
		foreach($tableFile_ as $line){
		
			$line=explode($fieldSep, $line);
			
			if($i_line==0 & !$headerFirstLine){
			
				for($j_col=0; $j_col < $ncol; $j_col++){
				    
				    $table[$columnNames[$tableColumnIndex[$j_col]]][] = $line[$tableColumnIndex[$j_col]];
					
				}
		
			} else {
			
				if($i_line>0){
				
					for($j_col=0; $j_col < $ncol; $j_col++){
				    	
				        $table[$columnNames[$tableColumnIndex[$j_col]]][] = $line[$tableColumnIndex[$j_col]];
			
					}
				
				}
			
			}
		
			$i_line=$i_line+1;
			
		}
		
		return $table;

	}

# get scientific notation

	function scientificNotation($val){ # from https://stackoverflow.com/questions/21416286/php-scientific-notation-format
	
		if($val != 0){
		
    		$exp = floor(log($val, 10));
    		
    		return sprintf('%.2fE%+03d', $val/pow(10,$exp), $exp);
    		
    	} else {
    	
    		return(0);
    	}
    	
    }

# printHTMLTable
# in : 
# out :

	function printHTMLTable($counts_, $countType_, $log_) {
	
		$colnames=array_keys($counts_);
	
		$nrow=count($counts_[$colnames[0]]);
	
		echo "<table>\n";
		
		# print header
		
		echo "<tr>\n";
		
		foreach($colnames as $col){
		
			echo "<th>"; 
					
			if(array_keys($colnames, $col)[0] > 8) {
					
				$colname=$col . " " .  $countType_;
						
				if($log_){
						
					$colname="log2 " . $colname;
						
				} 
					
				echo $colname;
					
			} else {
					
				echo $col;	
					
			}
					
			echo "</th>";
		
		}
		
		echo "</tr>\n";
		
		for($i_row=0; $i_row < $nrow; $i_row++){
		
			echo "<tr>\n";
		
			foreach($colnames as $col){
			
				
				echo "<td>"; 
					
				echo $counts_[$col][$i_row];
					
				echo "</td>";
			
			}
		
			echo "</tr>\n";
		
		}
		
		echo "</table>\n";
	
	}

# sortTable
# in :
# out:

# sortTable
# in :
# out:

	function sortTable($table_, $sortBy_, $sortOrder_){
	
		if(isset($sortBy_)){
	
			if(array_key_exists($sortBy_, $table_)){
		
				if(!isset($sortOrder_)){
			
					$sortOrder_="asc";
			
				}
			
				$tmp=$table_[$sortBy_];
			
				if($sortOrder_ == "asc"){
			
					asort($tmp);
			
				} else {
			
					arsort($tmp);
			
				}
		
				$rowOrder=array_keys($tmp);
		
				$tableSorted=array();
			
				foreach(array_keys($table_) as $col){
				
					$tableSorted[$col]=array();
				
					foreach($rowOrder as $i_row){
				
						$tableSorted[$col][]=$table_[$col][$i_row];
				
					}
				
				}
		
			} else {
					
				print($sortBy_ . " is not in table keys\n" );
					
				$tableSorted=$table_;
					
			}
			
		} else {
		
			$tableSorted=$table_;
			
		}
		
		return($tableSorted);
	
	}
	

# printCountTable : 
# int : 
# out :

	function getCountTable($countTableFile, $chr, $start, $stop, $descriptionDataFile, $samples, $countType, $norm, $log, $printAnnot, $sortBy, $sortOrder, $printHTMLTable, $returnTable){
	
		# get description data
		$descriptionData=readTable($tableFile=$descriptionDataFile, $headerFirstLine=True, $tableColumnIndex=array(1,2,6), $columnNames=NULL, $fieldSep="\t");
	
		# initialize variables
		if(!isset($countType)){
			
			$countType="densities";
			
		}
	
		if(!isset($norm)){
			
			$norm=True;
		}
	
		if(!isset($log)){
			
			$log=False;
		
		}
	
		if(!isset($printAnnot)){
			
			$printAnnot=True;
				
		}
	
		if(!isset($printHTMLTable)){
		
			$printHTMLTable=False;	
			
		}
	
		if(!isset($returnTable)){
		
			$returnTable=False;
		
		}
	
		# initialize count table
		$countTable=array();
		
		if($printAnnot){
			
			$colnamesAnnot=array("Chr", "Type", "Start", "Stop", "Strand", "ID", "Name", "Parent", "gene");
			
			foreach($colnamesAnnot as $col){
			
				$countTable[$col] = array();
				
			}
			
		}
	
		foreach($samples as $sample){
							
			$countTable[$sample] = array();
							
		}
	
		# get count table header
		$f = fopen($countTableFile, 'r');
			
		$headerCountTable=explode($fieldSep, fgets($f));
			
		fclose($f);
	
		# get index of sample in count table
		$sampleIndCountTable=array();
		
		foreach($samples as $sample){
				
			if(count(array_keys($headerCountTable, $sample)) != 0){	
				
				$sampleIndCountTable[$sample]=array_keys($headerCountTable, $sample);
			
			} else {
			
				$sampleIndCountTable[$sample]=array();
			
				$ind_rep=array_keys($descriptionData['group'], $sample);
				
				foreach($ind_rep as $ind){
				
					$rep=$descriptionData['sample'][$ind];
				
					$sampleIndCountTable[$sample][]=array_keys($headerCountTable, $rep)[0];
				
				}
				
			}	
						
		}

		# get index of sample in description_data
		$sampleIndDescription=array();
	
		foreach($samples as $sample){
		
			$try=array_keys($descriptionData["sample"], $sample);
	
			if(count($try) != 0){	
				
				$sampleIndDescription[$sample]=$try;
			
			} else {
			
				$sampleIndDescription[$sample]=array_keys($descriptionData["group"], $sample);
			
			}	
		
		}
	

	
	    # read file by line
		$countTableFile_=file($countTableFile);
	
		$i_line=0;
		
		foreach($countTableFile_ as $line){
		
			$line=explode("\t", $line);
		
			if($i_line != 0 & $line[0] == $chr & $line[2] <= $stop & $line[3] >= $start){ # /!\ 1st line of count file should be header
			
				if($printAnnot){
			
					foreach(range(0,count($colnamesAnnot)-1) as $i_col){
						
						
						
						$countTable[$colnamesAnnot[$i_col]][] = $line[$i_col];
				
					}
			
				}
		
				foreach($samples as $sample){
				
					if(count($sampleIndCountTable[$sample]) == 1){ # if replicate alone
				
						$val=$line[$sampleIndCountTable[$sample][0]];
				
						if($norm){
					
							$val=$val*$descriptionData['coeff'][$sampleIndDescription[$sample][0]];
					
						}
				
						if($countType == "densities"){
					
							$l=$line[3]-$line[2]+1;
							
							$val=$val/$l;
					
						}
				
					} else { # if mean of replicates
				
						$val=0;
						
						$nb_rep=count($sampleIndCountTable[$sample]);		
						
						for($i=0; $i < $nb_rep; $i++){

							$i_val=$line[$sampleIndCountTable[$sample][$i]];

							if($norm){
							
								$i_val=$i_val*$descriptionData['coeff'][$sampleIndDescription[$sample][$i]];
								
							}
							
							$val=$val+$i_val;
													
						}
						
						$val=$val/$nb_rep;		
	
						if($countType == "densities"){
						
							$l=$line[3]-$line[2]+1;
							
							$val=$val/$l;
						
						}			
				
					}
					
					if($log){
					
						$val=log($val, 2);
					
					}
					
					$countTable[$sample][] = scientificNotation($val);
					
				}
				
			}
		
			$i_line=$i_line+1;
		
		}
		
		if(isset($sortBy)){
		
			$countTable=sortTable($table_=$countTable, $sortBy_=$sortBy, $sortOrder_=$sortOrder);
		
		}
		
		if($returnTable){
		
			return($countTable);
		
		}
		
		if($printHTMLTable){
		
			printHTMLTable($counts_=$countTable, $countType_=$countType, $log_=$log);
		
		}	
	
	}

# printBrowserArrow
# in : 
# out : 

	function printBrowserArrow($chr_, $start_, $stop_, $samples_, $visu_, $scale_, $libType_, $norm_, $which){
		
		echo "<form method=\"post\" action=\"coverage.php\">\n";
		
		# chr
		echo "<input type=\"hidden\" name=\"chromosome\" value=\"$chr\">\n";
		
		# new coord (start or stop - ((stop+start)/2))
		$span=(int)(($stop_-$start_)/2);
		
		$start_before=(int)$start_-$span;
		
		$stop_before=(int)$stop_-$span;
		
		if($start_before < 1){
			
			$start_before = 1;
			
			$stop_before = $span*2+1;
		}
		
		$coord_before=$start_before."-".$stop_before;
		
		echo "<input type=\"hidden\" name=\"coord\" value=\"$coord_before\">\n";
		
		# samples
		echo "<input type=\"hidden\" name=\"samples[]\" value=\"$samples_\">\n";
		
		# visu
		echo "<input type=\"hidden\" name=\"visu\" value=\"$visu_\">\n";		
		
		# scale
		echo "<input type=\"hidden\" name=\"scale\" value=\"$scale_\">\n";
		
		# library type
		echo "<input type=\"hidden\" name=\"library\" value=\"$libType_\">\n";
		
		# normalized or raw data
		echo "<input type=\"hidden\" name=\"norm\" value=\"$norm_\">\n";
		
		# submit
		echo "<button class=\"button_nav\" type=\"submit\">\n";
		
		if($which=="left"){
		
			echo "<img src=\"images/fleche_gauche_1.png\" alt=\"Before\" height=\"80\" width=\"140\"/>\n";
		
		} else {
		
			echo "<img src=\"images/fleche_droite_1.png\" alt=\"Before\" height=\"80\" width=\"140\"/>\n";
		
		}
		
		
		echo "</button>\n";
		
		echo "</form>\n";
	
	}
	
# printBrowserCoord
# in
# out
	function printBrowserCoord(){
	
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

	}

?>


