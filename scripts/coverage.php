<?php
    
    session_start();
    
    include 'functions.php';
    
    if(!isset($_POST["sessid"])){
        $id = setConfig();
    } else {
        $id = $_POST["sessid"];
    }
    
    echo "<!DOCTYPE html PUBLIC \"-//W3C//DTD XHTML 1.0 Transitional//EN\" \"http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd\">\n";
    
    echo "<html xmlns=\"http://www.w3.org/1999/xhtml\" xml:lang=\"fr\" lang=\"fr\">\n";

    echo "<head>\n";
    
    #$title = isset($_SESSION[$id]["TITLE"]) ? $_SESSION[$id]["TITLE"] : "viewR";
    echo "    <title>Genome Browsers</title>\n";
    
    echo "    <meta http-equiv=\"Content-Type\" content=\"text/html; charset=utf-8\"/>\n";
    
    echo "    <link rel=\"stylesheet\" media=\"screen\" href=\"https://fontlibrary.org//face/liberation-sans\" type=\"text/css\"/>\n";
    echo "    <link rel=\"stylesheet\" media=\"screen\" type=\"text/css\" title=\"Design\" href=\"../design.css\"/>\n";
    
    echo "    <style>\n";
    echo "        body{\n";
    echo "            font-family:'LiberationSansRegular';\n";
    echo "            font-weight: normal;\n";
    echo "            font-style:normal;\n";
    echo "        }\n";
    echo "    </style>\n";
    
    echo "    <script src=\"functions.js\"></script>\n";
    echo "    <script src=\"https://cdn.plot.ly/plotly-latest.min.js\"></script>\n";
    
    echo "</head>\n";
    
    echo "<body style=\"min-height:800px\">\n";

    echo "    <div style=\"background-color:green;color:white;text-align:center;height:70px;padding:1px 0px 1px 0px\">\n";
    
    $title = isset($_SESSION[$id]["TITLE"]) ? $_SESSION[$id]["TITLE"] : "";
    echo "<h1>" . $title . "</h1>\n";
    
    #if(isset($_SESSION[$id]["IMAGE2"])){
    #    $img = $_SESSION[$id]["IMAGE2"];
    #    echo "<img src=\"$img\" style=\"margin-left:auto;margin-right:auto;height:150px;display:block\">\n";
    #} else {
    #    echo "<img src=\"no_image\" style=\"margin-left:auto;margin-right:auto;height:150px;display:block\" alt=\"viewR\">\n";
    #}
    
    echo "    </div>\n";
    echo "    <div style=\"width:100%;min-height:625px\">\n"; # <!-- content -->
    
    #### set visu parameters
    
    ##
    if(isset($_POST["SAMPLE_TYPE"]) && isset($_SESSION[$id]["SAMPLE_TYPE"])){
        
        if($_POST["SAMPLE_TYPE"] != $_SESSION[$id]["SAMPLE_TYPE"]){
            
            $_SESSION[$id]['samples'] = array();
            
            foreach(array_keys($_SESSION[$id]["DESCRIPTION_DATA"]) as $cond){
                if($_POST["SAMPLE_TYPE"] == "condition"){
                    array_push($_SESSION[$id]['samples'], $cond);
                    setVisuParam($id = $id, $addParam = True, $visu = $_SESSION[$id]["DEFAULT_VISU"], $lineType = $_SESSION[$id]["DEFAULT_LINETYPE"], $libType = $_SESSION[$id]["DEFAULT_LIBTYPE"], $scale = $_SESSION[$id]["DEFAULT_SCALE"], $norm = $_SESSION[$id]["DEFAULT_NORM"]);
                } elseif($_POST["SAMPLE_TYPE"] == "replicates") {
                    foreach($_SESSION[$id]["DESCRIPTION_DATA"][$cond] as $rep){
                        array_push($_SESSION[$id]['samples'], $rep);
                        setVisuParam($id = $id, $addParam = True, $visu = $_SESSION[$id]["DEFAULT_VISU"], $lineType = $_SESSION[$id]["DEFAULT_LINETYPE"], $libType = $_SESSION[$id]["DEFAULT_LIBTYPE"], $scale = $_SESSION[$id]["DEFAULT_SCALE"], $norm = $_SESSION[$id]["DEFAULT_NORM"]);
                    }
                }
            }
            
            $_SESSION[$id]["color"] = array();
            for($i = 0; $i < count($_SESSION[$id]['samples']); $i++){
                array_push($_SESSION[$id]["color"], getColor($i));
            }
            
            $_SESSION[$id]["SAMPLE_TYPE"] = $_POST["SAMPLE_TYPE"];
            
        }
        
    }
    
    ##
    
    setVisuParam($id = $id, isset($_POST["sampleToAdd"]));
    
    if(isset($_POST["removeSample"])){
        removeSampleToSession($id = $id, $_POST["removeSample"]);
    } else {
        if(isset($_POST["sampleToAdd"])){
            addSampleToSession($id = $id);
        }
        setVisuParam($id = $id, isset($_POST["sampleToAdd"]));
    }
    
    if(isset($_POST["types_to_show"])){
        $_SESSION[$id]["TYPES_TO_SHOW"] = $_POST["types_to_show"];
    } elseif(isset($_POST["menuTypeSetInput"])){
        unset($_SESSION[$id]["TYPES_TO_SHOW"]);
    }
    
    if(isset($_POST["collapse_transcripts"])){
        if($_POST["collapse_transcripts"] == "yes"){
            $_SESSION[$id]["SHOW_TRANSCRIPT_NAME"] = "no";
            $_SESSION[$id]["COLLAPSE_TRANSCRIPTS"] = "yes";
        } else {
            $_SESSION[$id]["SHOW_TRANSCRIPT_NAME"] = "yes";
            $_SESSION[$id]["COLLAPSE_TRANSCRIPTS"] = "no";
        }
     }
     
     # query on genomic location :
     # posted array "seeCoverage" takes 2 values : "coord" or "gene_name" 
     #   "coord" : "chromosome" and "coord" are also posted, containixng chromosome name and genomic coordinates (start-stop)
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
                $checkCoord = checkCoord($id = $id, $chr = $_POST["chromosome"], $coord = $_POST["coord"]);
                $checkedCoord = $checkCoord[0];
                $errorCoord = $checkCoord[1];
                
                if(!$errorCoord){
                    $chr = $_POST["chromosome"];
                    $start = (int)$checkedCoord[0];
                    $stop = (int)$checkedCoord[1];
                }
                
                printCoverage($id = $id, $chr = $chr, $start = $start, $stop = $stop);
                
            # new gene name given    
            } else if ($_POST["seeCoverage"] == "gene_name"){
                
                $gene_name = $_POST["gene_name"];
                
                # check if gene is in annotation
                if (strlen($gene_name) < 2){
                    
                    printCoverage($id = $id, $chr = $chr, $start = $start, $stop = $stop);
                
                } else {
                    
                    $geneArray = getGeneCoordFromIndex($id = $id, $gene_id = $gene_name);
                    
                    if(sizeof($geneArray["Chr"]) == 0){
                        
                        printCoverage($id = $id, $chr = $chr, $start = $start, $stop = $stop);
                    
                    } else if(sizeof($geneArray["Chr"]) == 1){
                        
                        $start = ((int)$geneArray["Start"][0] - 2000) < 1 ? 1 : (int)$geneArray["Start"][0] - 2000;
                        $stop = ((int)$geneArray["Stop"][0] + 2000) > $_SESSION[$id]["CHR_SIZE"][$geneArray["Chr"][0]] ? $_SESSION[$id]["CHR_SIZE"][$geneArray["Chr"][0]] : (int)$geneArray["Stop"][0] + 2000;
                        printCoverage($id = $id, $chr = $geneArray["Chr"][0], $start = $start, $stop = $stop);                                
                    
                    } else if(sizeof($geneArray["Chr"]) > 1){
                        
                        printTableGeneSelection($id = $id, $geneArray, $gene_name);
                    
                    }
                }
            }
            
        # on menu page, query genomic location
        } else {
            
            # coordinates given
            if($_POST["seeCoverage"] == "coord"){
                
                # check if coordinates given are valid
                $checkCoord = checkCoord($id = $id, $chr = $_POST["chromosome"], $coord = $_POST["coord"]);
                $checkedCoord = $checkCoord[0];
                $errorCoord = $checkCoord[1];
                
                if(!$errorCoord){
                    
                    $chr = $_POST["chromosome"];
                    $start = (int)$checkedCoord[0];
                    $stop = (int)$checkedCoord[1];
                    printCoverage($id = $id, $chr = $chr, $start = $start, $stop = $stop);
                    
                } else {
                    
                    printCoverageMenuPage($id = $id);
                
                }
                
            # new gene name given    
            } else if ($_POST["seeCoverage"] == "gene_name"){
                
                $gene_name = $_POST["gene_name"];
                # check if gene is in annotation
                
                if (strlen($gene_name) < 2){
                    
                    printCoverageMenuPage($id = $id);
                
                } else {
                    
                    $geneArray = getGeneCoordFromIndex($id = $id, $gene_id = $gene_name);
                    
                    if(sizeof($geneArray["Chr"]) == 0){
                        
                        printCoverageMenuPage($id = $id);
                        
                    } else if(sizeof($geneArray["Chr"]) == 1){
                        
                        $start = ((int)$geneArray["Start"][0] - 2000) < 1 ? 1 : (int)$geneArray["Start"][0] - 2000;
                        $stop = ((int)$geneArray["Stop"][0] + 2000) > $_SESSION[$id]["CHR_SIZE"][$geneArray["Chr"][0]] ? $_SESSION[$id]["CHR_SIZE"][$geneArray["Chr"][0]] : (int)$geneArray["Stop"][0] + 2000;
                        printCoverage($id = $id, $chr = $geneArray["Chr"][0], $start = $start, $stop = $stop);
                            
                    } else if(sizeof($geneArray["Chr"]) > 1){
                        
                        printTableGeneSelection($id = $id, $geneArray, $gene_name);
                        
                    }
                }
            }
        }
    # on menu page, no query on genomic location
    } else {
        
        printCoverageMenuPage($id = $id);
        
    }
    
    echo "    </div>\n"; # <!-- close contenu -->
    
    echo "    <div style=\"clear:both;width:calc(100% - 40px);margin:0 20px 0 20px;text-align:center\"><hr></div>\n";
    
    echo "    <div style=\"width:90%;height:5%;margin:1% 5% 1% 5%;text-align:right\">\n";
    
    echo "    <p>A tool by Morillon Lab</p>\n";
    
    echo "    </div>\n";
    
    echo "</body>\n";
    
    echo "</html>\n";

?>
