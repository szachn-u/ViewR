<?php
	session_start()
?>

<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">

<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="fr" lang="fr">


    <head>
        
        <?php
			$title = isset($_SESSION["TITLE"]) ? $_SESSION["TITLE"] : "viewR";
			echo "<title>$title</title>\n";
        ?>
        
        <!-- <title>SensR</title> -->
        
        <meta http-equiv="Content-Type" content="text/html; charset=utf-8"/>
        
        <link rel="stylesheet" media="screen" href="https://fontlibrary.org//face/liberation-sans" type="text/css"/>
        
        <link rel="stylesheet" media="screen" type="text/css" title="Design" href="design.css"/>
        
        <style>
			
			body{
				font-family:'LiberationSansRegular';
				font-weight: normal;
				font-style:normal;
			}
				
        </style>
        
        <script src="functions.js"></script>
        
        <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
        
    </head>
    
    <body style="min-height:800px">
        
        <!-- header -->
        <div>
            
			<!-- <img src="../images/logo_sensr_v2.png" style="margin-left:auto;margin-right:auto;height:150px;display:block" alt="SensR"/> -->
            
            <?php
				if(isset($_SESSION["IMAGE2"])){
					$img = $_SESSION["IMAGE2"];
					echo "<img src=\"$img\" style=\"margin-left:auto;margin-right:auto;height:150px;display:block\">\n";
				} else {
					echo "<img src=\"no_image\" style=\"margin-left:auto;margin-right:auto;height:150px;display:block\" alt=\"viewR\">\n";

				}
			?>

        </div>
        
        <!-- <div style="height:calc(100% - 150px)"> -->
        <div style="width:100%;min-height:625px"> <!-- content -->
            <?php
            
            include 'functions.php';
            
            #### set config parameters
            
            #if(!isset($_SESSION["DESCRIPTION_DATA"])){
                
            #    setConfig();
                
            #}
            
            #### set visu parameters
            
            #var_dump($_POST);
            
            setVisuParam(isset($_POST["sampleToAdd"]));
            
            if(isset($_POST["removeSample"])){
				
				removeSampleToSession($_POST["removeSample"]);
				
			} else {
				
				if(isset($_POST["sampleToAdd"])){
					
					addSampleToSession();
					
				}
				
				setVisuParam(isset($_POST["sampleToAdd"]));
				
			}
            
            if(isset($_POST["types_to_show"])){
                
                $_SESSION["TYPES_TO_SHOW"] = $_POST["types_to_show"];
                
            } elseif(isset($_POST["menuTypeSetInput"])){
				
				unset($_SESSION["TYPES_TO_SHOW"]);
				
			}
			
			if(isset($_POST["collapse_transcripts"])){
				if($_POST["collapse_transcripts"] == "yes"){
					$_SESSION["SHOW_TRANSCRIPT_NAME"] = "no";
					$_SESSION["COLLAPSE_TRANSCRIPTS"] = "yes";
				} else {
					$_SESSION["SHOW_TRANSCRIPT_NAME"] = "yes";
					$_SESSION["COLLAPSE_TRANSCRIPTS"] = "no";
				}
			}
            
            #if(isset($_POST["menuTypeSetInput"])){
			#	var_dump($_POST["menuTypeSetInput"]);
			#}
			
			#if(isset($_SESSION["TYPES_TO_SHOW"])){
			#	var_dump($_SESSION["TYPES_TO_SHOW"]);
			#}
            
            # query on genomic location :
            # posted array "seeCoverage" takes 2 values : "coord" or "gene_name" 
            #   "coord" : "chromosome" and "coord" are also posted, containing chromosome name and genomic coordinates (start-stop)
            #   "gene_name" : "gene_name" is posted, containing pattern to search in annotation - should be 3 characters minimum
            # _if on coverage page, genomic location are store in "prev_coord" (hidden input), in the form chr:start-stop, used to stay on the same page if error in new coordinates given 
            
            if(isset($_POST["seeCoverage"])){
                
                # on coverage page
                if(isset($_POST["prev_coord"])){
                    
                    $tmp = explode(":", $_POST["prev_coord"]);
                    
                    $chr = $tmp[0];
                    
                    $start = explode("-", $tmp[1])[0];
                    
                    $stop = explode("-", $tmp[1])[1];
                    
                    # new coordinates given
                    if($_POST["seeCoverage"] == "coord"){
                        
                        # check if coordinates given are valid
                        $checkCoord = checkCoord($chr = $_POST["chromosome"], $coord = $_POST["coord"]);
                        
                        $checkedCoord = $checkCoord[0];
                        
                        $errorCoord = $checkCoord[1];
                        
                        if(!$errorCoord){
                            
                            $chr = $_POST["chromosome"];
                            
                            $start = (int)$checkedCoord[0];
                            
                            $stop = (int)$checkedCoord[1];
                            
                        }
                        
                        printCoverage($chr = $chr, $start = $start, $stop = $stop);
                    
                    # new gene name given    
                    } else if ($_POST["seeCoverage"] == "gene_name"){
                                                
                        $gene_name = $_POST["gene_name"];
                        
                        # check if gene is in annotation
                        if (strlen($gene_name) < 2){
                            
                            printCoverage($chr = $chr, $start = $start, $stop = $stop);
                            
                        } else {
                            
                            $geneArray = getGeneCoordFromIndex($ID = $gene_name);
                            
                            if(sizeof($geneArray["Chr"]) == 0){
                                
                                printCoverage($chr = $chr, $start = $start, $stop = $stop);
                                
                            } else if(sizeof($geneArray["Chr"]) == 1){
                                
                                $start = ((int)$geneArray["Start"][0] - 2000) < 1 ? 1 : (int)$geneArray["Start"][0] - 2000;
                                
                                $stop = ((int)$geneArray["Stop"][0] + 2000) > $_SESSION["CHR_SIZE"][$geneArray["Chr"][0]] ? $_SESSION["CHR_SIZE"][$geneArray["Chr"][0]] : (int)$geneArray["Stop"][0] + 2000;
                                
                                printCoverage($chr = $geneArray["Chr"][0], $start = $start, $stop = $stop);                                
                                
                            } else if(sizeof($geneArray["Chr"]) > 1){
                                
                                printTableGeneSelection($geneArray, $gene_name);
                                
                            }
                        
                        }
                        
                    }
                    
                # on menu page, query genomic location
                } else {
                    
                    # coordinates given
                    if($_POST["seeCoverage"] == "coord"){
                        
                        # check if coordinates given are valid
                        $checkCoord = checkCoord($chr = $_POST["chromosome"], $coord = $_POST["coord"]);
                        
                        $checkedCoord = $checkCoord[0];
                        
                        $errorCoord = $checkCoord[1];
                        
                        if(!$errorCoord){
                            
                            $chr = $_POST["chromosome"];
                            
                            $start = (int)$checkedCoord[0];
                            
                            $stop = (int)$checkedCoord[1];
                            
                            printCoverage($chr = $chr, $start = $start, $stop = $stop);

                        } else {
                            
                            printCoverageMenuPage();
                            
                        }
                        
                    
                    # new gene name given    
                    } else if ($_POST["seeCoverage"] == "gene_name"){
                                                
                        $gene_name = $_POST["gene_name"];
                        
                        # check if gene is in annotation
                        if (strlen($gene_name) < 2){
                            
                            printCoverageMenuPage();
                            
                        } else {
                            
                            $geneArray = getGeneCoordFromIndex($ID = $gene_name);
                            
                            if(sizeof($geneArray["Chr"]) == 0){
                                
                                printCoverageMenuPage();
                                
                            } else if(sizeof($geneArray["Chr"]) == 1){
                                
                                $start = ((int)$geneArray["Start"][0] - 2000) < 1 ? 1 : (int)$geneArray["Start"][0] - 2000;
                                
                                $stop = ((int)$geneArray["Stop"][0] + 2000) > $_SESSION["CHR_SIZE"][$geneArray["Chr"][0]] ? $_SESSION["CHR_SIZE"][$geneArray["Chr"][0]] : (int)$geneArray["Stop"][0] + 2000;
                                
                                printCoverage($chr = $geneArray["Chr"][0], $start = $start, $stop = $stop);
                                
                            } else if(sizeof($geneArray["Chr"]) > 1){
                                
                                printTableGeneSelection($geneArray, $gene_name);
                                
                            }
                        
                        }
                        
                    }
                    
                }
                
            # on menu page, no query on genomic location
            } else {
                
                printCoverageMenuPage();
                
            }
            
            ?>
            
        </div> <!-- close contenu -->
        
        <div style="clear:both;width:calc(100% - 40px);margin:0 20px 0 20px;text-align:center"><hr></div>
        
        <div style="width:90%;height:5%;margin:0 5% 0 5%;text-align:right">
            
            <p>Visualization by <a href="https://github.com/szachn-u/ViewR">ViewR</a></p>
        
        </div>
        
    </body>
    
</html>

