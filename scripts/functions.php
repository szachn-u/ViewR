<?php

## setConfig
# read config file :
# contains : PYTHON_PATH, DESCRIPTION_DATA, ANNOT_FILE, ANNOT_IS_INDEXED, ANNOT_TYPE, CHR_SIZE, TYPES_LIST
# set these variables in $_SESSION

function setConfig($file="config.txt"){
    
    foreach(file($file) as $line){
        
        $line = preg_replace('/\s+/', '', $line);
        
        if(empty($line)){
            
            continue;
            
        }
        
        $split=explode("=", $line);
        
        $name=$split[0];
        
        $value=preg_replace('/\s+/', '', $split[1]);
                
        switch($name){
            
            case "PYTHON_PATH":
                
                $_SESSION["PYTHON_PATH"] = ($value == "") ? "/usr/bin/python3" : $value;
                                
                break;
            
            case "DESCRIPTION_DATA":
                
                $description_data = array();
                
                if(file_exists($value)){
                    
                    $_SESSION["DESCRIPTION_DATA_FILE"] = $value;
                    
                    $i = 0;
                    
                    foreach(file($value) as $line_){
                        
                        if($i > 0){
                            
                            $line_ = explode("\t", $line_);
                            
                            $cond = $line_[3];
                            
                            if(!array_key_exists($cond, $description_data)){
                                
                                $description_data[$cond] = array();
                                
                            }
                            
                            array_push($description_data[$cond], $line_[2]);
                            
                        } else {
                            
                            $i = $i + 1;
                            
                        }
                        
                    }
                    
                    $_SESSION["DESCRIPTION_DATA"] = sizeof($description_data) > 0 ? $description_data : null;
                    
                } 
                
                break;
            
            case "SCRIPTS_DIR":
                
                if (file_exists($value)){
                    
                    $_SESSION["SCRIPTS_DIR"] = $value;
                    
                }
                
                break;
            
            case "ANNOT_FILE":
                
                if(file_exists($value)){
                    
                    $_SESSION["ANNOT_FILE"] = $value;
                    
                }
                
                break;
            
            case "ANNOT_IS_INDEXED":
                
                $_SESSION["ANNOT_IS_INDEXED"] = filter_var($value, FILTER_VALIDATE_BOOLEAN);
                
                break;
            
            case "CHR_SIZE":
                
                $chr_sizes = array();
                
                if(file_exists($value)){
                                        
                    foreach(file($value) as $line_){
                        
                        $split_line_ = explode("\t", $line_);
                        
                        $chr_name = $split_line_[0];
                        $chr_size = (int)$split_line_[1];
                        
                        $chr_sizes[$chr_name] = $chr_size;
                        
                    }
                    
                } 
                
                $_SESSION["CHR_SIZE"] = sizeof($chr_sizes) > 0 ? $chr_sizes : null;
                
                break;
            
            case "ANNOT_NAME_INDEX":
                
                if(file_exists($value)){
                    
                    $_SESSION["ANNOT_NAME_INDEX"] = $value;
                    
                }
                
                break;
            
            case "ANNOT_GENE_TYPES_LIST":
                
                if(file_exists($value)){
                    
                    $types_in_annot = array();
                    
                    foreach(file($value) as $line_){
                        
                        $splitLine = explode("\t", $line_);
                        
                        if(sizeof($splitLine) == 1){
                            
                            $t = str_replace(array("\r", "\n", ), '', $line_);
                            
                            if(!array_key_exists("noClass", $types_in_annot) && ( $t != "")){
                                
                                $types_in_annot["noClass"] = array();
                                
                            }
                            
                            if($t != ""){
								array_push($types_in_annot["noClass"], $t); 
                            }
                            
                        } else if (sizeof($splitLine) == 2){
                            
                            $class = $splitLine[0];
                            $t = str_replace(array("\r", "\n"), '', $splitLine[1]);
                            
                            if(( $t != "" ) or ( $class != "" )){
								if(!array_key_exists($splitLine[0], $types_in_annot)){
									
									$types_in_annot[$splitLine[0]] = array();
									
								}
								
								array_push($types_in_annot[$splitLine[0]], $t);
                            }
                        }
                        
                    }
                    
                    if (sizeof($types_in_annot) != 0){
						$_SESSION["ANNOT_GENE_TYPES_LIST"] = $types_in_annot;
						if(array_key_exists("noClass", $types_in_annot)){
							$tmp = $types_in_annot["noClass"];
							sort($tmp);
							$_SESSION["ANNOT_GENE_TYPES_LIST"]["noClass"] = $tmp;
						}
                    }
                }
                
                break;
            
            case "IMAGE1":
                
                if(file_exists($value)){
                    
                    $_SESSION["IMAGE1"] = $value;
                    
                }
                
                break;
            
            case "IMAGE2":
                
                if(file_exists($value)){
                    
                    $_SESSION["IMAGE2"] = $value;
                    
                }
                
                break;
            
            case "TITLE":
                
                $_SESSION["TITLE"] = ($value == "") ? "viewR" : $value;
                
                break;
            
            case "USER_GUIDE":
                
                if(file_exists($value)){
                    
                    $_SESSION["USER_GUIDE"] = $value;
                    
                }
                
                break;
        }
        
    }
    
}

# from https://stackoverflow.com/questions/9186038/php-generate-rgb
# and https://convertingcolors.com/blog/article/convert_rgb_to_hex_with_php.html
function getColor($i){
    
    $hash = md5('color' . $i);
    $r = substr($hash, 0, 2);
    $g = substr($hash, 2, 2);
    $b = substr($hash, 4, 2);
    $sHexValue = "#" . $r . $g . $b;
    
    return($sHexValue);
}

## addSampleToSession
# add content of $_POST["sample"] (if present) to $_SESSION sample
# initialize $_SESSION["sample"] to array if not set 
function addSampleToSession(){
    
    if(!isset($_SESSION['samples'])){
        
        $_SESSION['samples'] = array();
        
    } 
    
    if(isset($_POST["sampleToAdd"])){
        if(!in_array($_POST["sampleToAdd"], $_SESSION['samples'])){
            array_push($_SESSION['samples'], $_POST["sampleToAdd"]);
        }
    }
    
}

## setVisuParam
# for parameters visu, color, lineType, libtype, scale, & norm
# initialize $_SESSION[param] to array if not set
# set $_SESSION[param] to $_POST[param] if $_POST[param] exists
# add default visu parameters to $_SESSION if addParam is true
function setVisuParam($addParam){
    
    $defaultVisuParam=array(
        "visu" => "line", 
        "lineType" => "solid",
        "libType" => "stranded",
        "scale" => "linear",
        "norm" => "yes"
    );
    
    foreach(array("visu", "lineType", "libType", "scale", "norm", "color") as $param){
        
        if(isset($_POST[$param])){
            
            if($param == "color"){
                
                $_SESSION[$param] = $_POST[$param];
                
                if($addParam){
                    
                    array_push($_SESSION[$param], getColor(count($_SESSION[$param])));
                    
                }
                
            } else {
                
                $_SESSION[$param] = $_POST[$param];
                
            }
            
        } else {
            
            if($addParam){
                
                if($param == "color"){
                    
                    $_SESSION[$param] = array(0 => getColor(0));
                    
                } else {
                    
                    $_SESSION[$param] = $defaultVisuParam[$param];
                    
                }
                
            }
            
        }
        
    }
    
}

function removeSampleToSession($i){
    
    $samples = array();
    $colors = array();
    
    for($j = 0; $j < sizeof($_SESSION["samples"]); $j++){
        
        if($j != $i){
            
            array_push($samples, $_SESSION["samples"][$j]);
            array_push($colors, $_SESSION["color"][$j]);
            
        } 
        
    }
    
    $_SESSION["samples"] = $samples;
    $_SESSION["color"] = $colors;
    
}

# printDropDownJS
function printDropdownJS(){
    
        echo "<script>\n";
        echo "  window.onclick = function(e){\n";
        echo "    var target = e.target;\n";
        echo "    var child = \"\";\n";
        echo "    if(target.className == \"dropbtnlabel\"){\n";
        echo "      var parent = target.parentElement.parentElement;\n";
        echo "      child = parent.getElementsByClassName(\"dropdown-content\")[0];\n";
        echo "      if(child.style.visibility == \"hidden\" || !child.style.visibility){";
        echo "        child.style.visibility = \"visible\";\n";
        echo "      } else {\n";
        echo "        child.style.visibility = \"hidden\";\n";
        echo "      }\n";
        echo "    }\n";
        echo "    var all_elements = document.getElementsByClassName(\"dropdown-content\");\n";
        echo "    for(var i = 0; i < all_elements.length; i++){\n";
        echo "      if(all_elements[i] != child){ all_elements[i].style.visibility = \"hidden\";}\n";
        echo "    }\n";
        echo "  };\n";
        echo "</script>\n";
    
} 

## printSampleSelector
function printSampleSelector($mainLabel, $values){
    
    echo "<div class=\"dropdown\">\n";
    echo "  <div class=\"dropbtn\"><div class=\"dropbtnlabel\" style=\"width:100%;height:100%;text-align:center\">$mainLabel</div>\n";
    echo "  </div>\n";
    echo "  <div class=\"dropdown-content\">\n";
    foreach(array_keys($values)as $k){
        $val = $values[$k][0];
        $name = $values[$k][1];
         echo "    <button type=\"submit\" name=\"sampleToAdd\" value=\"$val\">$name</button>\n";
    }
    echo "  </div>\n";
    echo "</div>\n";

}

## printAllSampleSelector
function printAllSampleSelectors(){
    
    echo "<div style=\"position:relative\">\n";
    
    $i = 1;
    
    foreach(array_keys($_SESSION["DESCRIPTION_DATA"]) as $cond){
        
        if($i == 1){
            echo "<div class=\"navbar\">\n";
        }
        
        $nRep = count($_SESSION["DESCRIPTION_DATA"][$cond]);
        if($nRep > 1){
            $sampleValues = array(array($cond, "merged"));
            foreach($_SESSION["DESCRIPTION_DATA"][$cond] as $rep){
                array_push($sampleValues, array($rep, $rep));
            }
        } else {
            $sampleValues = array(array($_SESSION["DESCRIPTION_DATA"][$cond][0], $_SESSION["DESCRIPTION_DATA"][$cond][0]));
        }
        
        printSampleSelector($cond, $sampleValues);
        
        if($i == 5){
            echo "</div>\n"; # close navbar
            $i = 0;
        }
        $i = $i + 1;
    }
    
    if($i > 1){
        
        echo "</div>\n"; # close navbar
        
    }
    echo "</div>\n";
    
}

## printColorSelection
#
function printOneSampleSelected($paramValueSelected, $label, $i){
    
    echo "<div class=\"sampleSelectedOut\" style=\"border-color:$paramValueSelected\" id=\"sample$i\">\n";
    echo "<div class=\"sampleSelectedIn\">\n";
    echo "<div class=\"sampleSelectedLabel\">";
    echo $label;
    echo "</div>\n";
    echo "<input type=\"color\" id=\"colorPicker$i\" value=\"$paramValueSelected\" name=\"color[]\"/>\n";
    echo "</div>\n";
    echo "<div class=\"sampleSelectedRemove\">\n";
    echo "<button type=\"submit\" name=\"removeSample\" value=\"$i\">X</button>\n";
    echo "</div>\n";    
    echo "</div>\n";
    
    echo "<script>
        document.getElementById(\"colorPicker$i\").addEventListener('change', (e) => {
            document.getElementById(\"sample$i\").style.borderColor = e.target.value;
        });
    </script>\n";
    
}

## printSampleSelected
#
function printSampleSelected(){
    
    echo "<div style=\"position:relative\">\n";
    
    $j = 1;
    for($i = 0; $i < sizeof($_SESSION["samples"]); $i++){
        if($j == 1){
            echo "<div class=\"navbar\">\n";
        }
        printOneSampleSelected($_SESSION["color"][$i], $_SESSION["samples"][$i], $i);
        if($j == 5){
            echo "</div>\n";
            if(count($_SESSION["color"]) != $j){
                echo "<div style=\"width:100%;height:10px\"></div>\n";
            }
            $j = 0;
        }
        $j = $j + 1;
    }
    
    if($j > 1){
        echo "</div>\n";
    }
    
    echo "</div>\n";
    
}

## printVisuSelector
#
function printVisuSelector($paramValues, $paramValueSelected, $inputName, $title){
    
    echo "<div class=\"dropdown\">\n";
    echo "  <div class=\"dropbtn\"><div class=\"dropbtnlabel\" style=\"width:100%;height:100%;text-align:center\">$title : $paramValueSelected</div>";
    echo "    <input type=\"hidden\" name=\"$inputName\" value=\"$paramValueSelected\"/>\n";
    echo "  </div>\n";
    echo "  <div class=\"dropdown-content\" id=\"$inputName\">\n";
    foreach($paramValues as $val){
         echo "    <button onclick=\"setSelectedVisu(event)\" type=\"button\" value=\"$val\">$val</button>\n";
    }
    echo "  </div>\n";
    echo "<script>\n";
    echo "    function setSelectedVisu(e){\n";
    echo "        var names = {\"visu\" : \"Visualization\", \"libType\" : \"Library type\",\"scale\" : \"Scale\",\"norm\" : \"Normalized\"};\n";
    echo "        var target = e.target;\n";
    echo "        var id = target.parentElement.id;\n";
    echo "        var dropdown = target.parentElement.parentElement;\n";
    echo "        var dropbtn = dropdown.children[0];\n";
    echo "        dropbtn.children[1].value = target.textContent;\n";
    echo "        dropbtn.children[0].textContent = names[id] + \" : \" + target.textContent;\n";
    echo "    }\n";
    echo "</script>\n";
    echo "</div>\n";
}

## printAllVisuSelectors
#
function printAllVisuSelectors(){
    
    echo "<div style=\"position:relative\">\n";
    
    echo "<div class=\"navbar\">\n";
    printVisuSelector(array("heatmap", "fill", "line"), $_SESSION["visu"], "visu", "Visualization"); 
    printVisuSelector(array("stranded", "unstranded"), $_SESSION["libType"], "libType", "Library type"); 
    printVisuSelector(array("log2", "linear"), $_SESSION["scale"], "scale", "Scale"); 
    printVisuSelector(array("yes", "no"), $_SESSION["norm"], "norm", "Normalized");
    echo "</div>\n";
    echo "</div>\n";
    
}

## printAnnotFeatureSelection
#
function printAnnotFeatureSelection($value, $is_open){
    
    # selection
    
    echo "<div style=\"position:relative;width:100%;height:20px;text-align:center\">\n";
    echo "<div style=\"float:left;position:relative;width:calc(100% / 2 - 75px);height:20px\"></div>\n";
    if($value == "all"){
        echo "<div class=\"menuTypeSet\" style=\"background-color:#6495ED;color:white\" onclick=\"setMenuType(event)\">all</div>\n";
        echo "<div class=\"menuTypeSet\" onclick=\"setMenuType(event)\">none</div>\n";
        echo "<div class=\"menuTypeSet\" onclick=\"setMenuType(event)\">select</div>\n";
    }
    if($value == "none"){
        echo "<div class=\"menuTypeSet\" onclick=\"setMenuType(event)\">all</div>\n";
        echo "<div class=\"menuTypeSet\" style=\"background-color:#6495ED;color:white\" onclick=\"setMenuType(event)\">none</div>\n";
        echo "<div class=\"menuTypeSet\" onclick=\"setMenuType(event)\">select</div>\n";
    }
    if($value == "select"){
        echo "<div class=\"menuTypeSet\" onclick=\"setMenuType(event)\">all</div>\n";
        echo "<div class=\"menuTypeSet\"onclick=\"setMenuType(event)\">none</div>\n";
        echo "<div class=\"menuTypeSet\" style=\"background-color:#6495ED;color:white\" onclick=\"setMenuType(event)\">select</div>\n";
    }
    echo "<input type=\"hidden\" name=\"menuTypeSetInput\" value=\"$value\"/>";

    echo "<script>
        function setMenuType(e){
            var target = e.target;
            if(target.className == \"menuTypeSet\"){
                var which = target.textContent;
                var p = target.parentElement;
                var elements = p.getElementsByClassName(\"menuTypeSet\");
                var menu = document.getElementsByClassName(\"geneTypeMenu\")[0];
                var input1 = document.getElementsByName(\"menuTypeSetInput\")[0];
                var input2 = document.getElementsByName(\"geneTypeMenuInput\")[0];
                for(var i = 0; i < elements.length; i++){
                    elements[i].style.backgroundColor = \"white\";
                    elements[i].style.color = \"black\";
                    if(which == \"select\"){
                        if(menu.style.display == \"none\"){ 
                            menu.style.display = \"block\";
                            input2.value = \"yes\";
                        } else { 
                            menu.style.display = \"none\";
                            input2.value = \"no\";
                        }
                    }
                    if(which == \"all\"){
                        var typeSelectors = document.getElementsByClassName(\"geneTypeSelector\");
                        for(var j = 0; j < typeSelectors.length; j++){
                            typeSelectors[j].children[0].disabled = false;
                            typeSelectors[j].style.opacity = \"1\";
                        }
                    }
                    if(which == \"none\"){
                        var typeSelectors = document.getElementsByClassName(\"geneTypeSelector\");
                        for(var j = 0; j < typeSelectors.length; j++){
                            typeSelectors[j].children[0].disabled = true;
                            typeSelectors[j].style.opacity = \"0.3\";
                        }
                    }
                }
                target.style.backgroundColor = \"#6495ED\";
                target.style.color = \"white\";
                input1.value = which;
            }
        }
    </script>\n";
    echo "</div>\n";
    if($is_open == "no"){
        echo "<div class=\"geneTypeMenu\" style=\"position:relative;display:none\">\n";
    } else {
        echo "<div class=\"geneTypeMenu\" style=\"position:relative;display:block\">\n";
    }
    echo "<input type=\"hidden\" name=\"geneTypeMenuInput\" value=\"$is_open\"/>\n";
    $i = 1;
    foreach($_SESSION["ANNOT_GENE_TYPES_LIST"]["noClass"] as $type){
        if($i == 1){
            echo "<div class=\"navbar\">\n";
        }
        if(isset($_SESSION["TYPES_TO_SHOW"])){
            if(!in_array($type, $_SESSION["TYPES_TO_SHOW"])){
                $disabled = "disabled=\"disabled\"";
                $op=0.3;
            } else {
                $disabled="";
                $op=1;
            }
        } elseif ($value == "all") {
            $disabled="";
            $op=1;
        } else {
            $disabled = "disabled=\"disabled\"";
            $op=0.3;
        }
        
        echo "<div class=\"geneTypeSelector\" style=\"opacity:$op\">\n";
        echo "<input type=\"hidden\" name=\"types_to_show[]\" value=\"$type\" $disabled/>\n";
        echo "<div style=\"position:relative;width:100%;height:100%;text-align:center\" onclick=\"setSelectedType(event)\">$type</div>\n";
        
        echo "<script>\n";
        echo "    function setSelectedType(e){\n";
        echo "        var input = document.getElementsByName(\"menuTypeSetInput\")[0];\n";
        echo "        input.value = \"select\";\n";
        echo "        var target = e.target;\n";
        echo "        input = target.parentElement.children[0];\n";
        echo "        var parent = target.parentElement;\n";
        echo "        if(input.disabled == true){\n";
        echo "          input.disabled = false;\n";
        echo "          parent.style.opacity = \"1\";\n";
        echo "        } else {\n";
        echo "          input.disabled = true;\n";
        echo "          parent.style.opacity = \"0.3\";\n";
        echo "        }\n";
        echo "        var elements = document.getElementsByClassName(\"menuTypeSet\");\n";
        echo "        for(var i = 0; i < elements.length; i++){\n";
        echo "          if(elements[i].textContent == \"select\"){\n";
        echo "            elements[i].style.backgroundColor = \"#6495ED\";\n";
        echo "            elements[i].style.color = \"white\";\n";
        echo "          } else {\n";
        echo "            elements[i].style.backgroundColor = \"white\";\n";
        echo "            elements[i].style.color = \"black\";\n";
        echo "          }\n";
        echo "        }\n";
        echo "    }\n";
        echo "</script>\n";
        
        echo "</div>\n";
        if($i == 5){
            echo "</div> <!-- close navbar -->\n";
            $i = 0;
        }
        $i = $i + 1;
    }
    if($i > 1){
        echo "</div>  <!-- close navbar -->\n";
    }
        
    echo "</div>\n";
    
}


## checkCoord
# check genomic coordinates
# chromosome should be in $_SESSION[CHR_SIZE] 
# should be given in the form (int)start-(int)stop
# start and stop should be > 0 and < chromosome size
# start should be < stop
# in : 
#  chromosome name
#  coordinates
# out : 
#  2D array :
#    (corrected) coord
#    boolean saying if there is error in coord
function checkCoord($chr, $coord){
    
    #$errorMessage = array();
    $error = False;
    
    if(is_null($chr) or !array_key_exists($chr, $_SESSION["CHR_SIZE"])){
        
        #array_push($errorMessage, "Invalid chromosome name");
        $error=true;
        
    } else {
        
        $chr_size = (int)$_SESSION["CHR_SIZE"][$chr];
        
        $split = explode("-",$coord);
        
        if (count($split) == 2){
            
            $start = (int)$split[0];
            
            $stop = (int)$split[1];
            
            if(!is_numeric($start) or !is_numeric($stop)){
                
                #array_push($errorMessage, "coordinates given should be numeric");
                $error=true;
            } else if(($start < 1 and $stop < 1) or ($start > $chr_size and $stop > $chr_size)){
                
                #array_push($errorMessage, "Coordinates are out of chromosome limits");
                $error=true;
            } else {
                
                $start = $start < 1 ? 1 : $start;
                
                $stop = $stop > $chr_size ? $chr_size : $stop; 
                
                if($start >= $stop){
                    
                    #array_push($errorMessage, "Stop should be larger than start");
                    $error=true;
                }
                
            }
            
        } else {
            
           #array_push($errorMessage, "Invalid coordinates format"); 
           $error=true; 
        }
        
    }
    
    #$errorMessage = sizeof($errorMessage) == 0 ? null : $errorMessage;
    
    $checkedCoord = array($start, $stop);
    
    #return(array($checkedCoord, $errorMessage));
    return(array($checkedCoord, $error));
}

## printBrowserCoord
# in :
#     prev_chr   : previous genomic coordinates
#     prev_start : previous genomic coordinates
#     prev_stop  : previous genomic coordinates
# out :
#     print a text box to enter (new) genomic coordinates and submit button
#     post prev_coord, chromosomme coord & seeCoverage
function printBrowserCoord($prev_chr=null,$prev_start=null, $prev_stop=null){
    
    if(!is_null($prev_chr) and !is_null($prev_start) and !is_null($prev_stop)){
        
        $prev_coord=$prev_chr.":".$prev_start."-".$prev_stop;
        
        echo "<input type=\"hidden\" name=\"prev_coord\" value=\"$prev_coord\"/>\n";
        
    }
    
    #echo "<div style=\"width:100%;height:30px;margin-top:15px\">Enter coordinates in the form start-stop\n";
    echo "<div style=\"position:relative; float:left;width:100%;height:30px;font-style:italic\">Enter coordinates (e.g. 150000-200000)\n";
        #echo "<div class=\"tooltip\">Select genomic coordinates\n";
    
        #    echo "<span class=\"tooltiptext\" style=\"width:400px\">Enter coordinates in the form start-stop</span>\n";
    
        #echo "</div>\n";
    
    echo "</div>\n";
    
    ## chr
    echo "<select name=\"chromosome\">\n";
    
    if(isset($_SESSION["CHR_SIZE"])){
        
        foreach(array_keys($_SESSION["CHR_SIZE"]) as $chr){
            
            $to_print = (!is_null($prev_chr) and $prev_chr == $chr) ? "<option selected>$chr\n" : "<option>$chr\n";
            
            echo $to_print;
            
        }
        
        echo "</select>";
    
        ## coord
        echo "<input type=\"text\" name=\"coord\"/>\n";
        
        echo "<button type=\"submit\" name=\"seeCoverage\" value=\"coord\">GO!</button>\n";
        
    } else {
        
        echo "<p>FILE CHR_SIZE IS MISSING IN CONFIG FILE, OR CANNOT BE FOUND</p>\n";
        
    }
    
}

## printBrowserGene
# print text box 
# post : 
#  prev_coord (hidden): previous coordinates  
#  gene_name : user input
#  seeCoverage : gene_name
function printBrowserGene($boxSize = null, $prev_chr=null,$prev_start=null, $prev_stop=null){
    
    #echo "<div style=\"width:100%;height:30px;margin-top:15px\">\n";
    #    echo "<div class=\"tooltip\">Gene name\n";
    #        echo "<span class=\"tooltiptext\" style=\"width:350px\">Use all or part of gene name <br>(min 3 characters)</span>\n";
    #    echo "</div>\n";
    #echo "</div>\n";
    
    echo "<div style=\"position:relative;float:left;width:100%;height:30px;font-style:italic\">Enter gene name (e.g. RRP6)\n";
    echo "</div>\n";
    
    if(!is_null($prev_chr) and !is_null($prev_start) and !is_null($prev_stop)){
        
        $prev_coord=$prev_chr.":".$prev_start."-".$prev_stop;
        
        echo "<input type=\"hidden\" name=\"prev_coord\" value=\"$prev_coord\"/>\n";
        
    }
    
    if(!is_null($boxSize)){
        
        echo "<input type=\"text\" size=\"$boxSize\" name=\"gene_name\"/>\n";
        
    } else {
        
        echo "<input type=\"text\" name=\"gene_name\"/>\n";
        
    }
    
    echo "<button type=\"submit\" name=\"seeCoverage\" value=\"gene_name\">GO!</button>\n";
    
}

## getGeneCoordFromIndex
function getGeneCoordFromIndex($ID){
    
    $res=array();
    
    foreach (array("Chr", "Type", "Start", "Stop", "Strand", "ID") as $col){
        
        $res[$col] = array();
        
    }
    
    if(file_exists($_SESSION["ANNOT_NAME_INDEX"])){
        
        $file=gzopen($_SESSION["ANNOT_NAME_INDEX"], "r");
        
        $i_gene = 0;
        
        while(!gzeof($file)){
            
            $line = gzgets($file);
            
            $line = explode("\t", $line);
            
            $is_gene_in_line = preg_grep("/".trim($ID)."/i", $line);
            
            if(count($is_gene_in_line) > 0){
                
                $res["Chr"][$i_gene] = preg_replace('/\s+/', '', $line[8]);
                $res["Type"][$i_gene] = preg_replace('/\s+/', '', $line[2]);
                $res["Start"][$i_gene] = preg_replace('/\s+/', '', $line[3]);
                $res["Stop"][$i_gene] = preg_replace('/\s+/', '', $line[4]);
                $res["Strand"][$i_gene] = preg_replace('/\s+/', '', $line[6]);
                $res["ID"][$i_gene] = preg_replace('/\s+/', '', $line[0]);
                
                if(count($line) >= 11){
                    
                    $res["name"][$i_gene] = preg_replace('/\s+/', '', trim($line[10]));
                    
                }
                
                $i_gene = $i_gene + 1;
            }
            
        }
        
        gzclose($file);
        
    } 
    
    return($res);
}

## printTableGeneSelection
# print a table with all genes found in annotation, with name matching pattern "geneName"
# for each record, print a button that post genomic coordinates (+/- 5000)
# post :
#  chr (hidden) : gene chromosome
#  coord (hidden) : gene coordinates
#  seeCoverage : coord
function printTableGeneSelection($geneArray, $geneName){
    
    $n_genes_found=count($geneArray["Chr"]);
    
    echo "<div style=\"float:left;padding-top:15px;padding-bottom:15px;text-align:center;width:100%\">\n";
    
    echo "<p><b>$n_genes_found genes</b> were found with the name/pattern <b>\"$geneName\"</b> : \n";
    
    echo "</div>\n";
    
    echo "<div class = \"count_table\" style=\"float:left;max-height:600px;margin-left:5%; margin-bottom:20px;width:90%\">\n";
    
    echo "<table>\n";
    
    echo "<tr>\n";
    
    foreach(array_keys($geneArray) as $k){
        
        echo "<th style=\"width:12.5%\">$k</th>";
        
    }
    
    echo "<th style=\"width:12.5%\">See gene</th>";
    
    echo "</tr>\n";
    
    for ($i_gene = 0; $i_gene < ($n_genes_found); $i_gene++){
        
        $Chr = $geneArray["Chr"][$i_gene];
        
        $chr_size = $_SESSION["CHR_SIZE"][$Chr];
        
        if(!is_null($chr_size)){
            
            echo "<tr>";
            
            foreach(array_keys($geneArray) as $k){
                
                if(sizeof($geneArray[$k]) > $i_gene){
                    
                    $val=$geneArray[$k][$i_gene];
                    
                } else {
                    
                    $val="";
                    
                }
                
                echo "<td style=\"width:12.5%\">$val</td>";
                
            }
            
            echo "<td style=\"width:12.5%\">";
            
            echo "<form method=\"post\" action=\"coverage.php\">\n";
            
            echo "<input type=\"hidden\" name=\"chromosome\" value=\"$Chr\">\n";
            
            ## coord
            $start = $geneArray['Start'][$i_gene] - 2000;
            
            if($start < 1){
                
                $start = 1;
                
            }
            
            $stop = $geneArray['Stop'][$i_gene] + 2000;
            
            if($stop > $chr_size){
                
                $stop = (int)$chr_size;
                
            }
            
            $coord = $start."-".$stop;
            
            echo "<input type=\"hidden\" name=\"coord\" value=\"$coord\">\n";
            
            ## submit
            echo "<button type=\"submit\" name=\"seeCoverage\" value=\"coord\">GO!</button>\n";
            
            echo "</form>\n";
            
            echo "</td>\n";
            
            echo "</tr>\n";
            
        }
        
    }
    
    echo "</table>\n";
    
    echo "</div>\n";
    
}


## printCoverageMenuPage
function printCoverageMenuPage(){
    
    echo "<div style=\"position:relative;float:left;height:25px;width:100%\"><a href=\"index.php\">&#xAB;back to main page</a></div>\n";
    
    echo "<div style=\"clear:both\"></div>\n";
    
    echo "<form id=\"myForm\" method=\"post\" action=\"coverage.php\">\n";
    
    #echo "<div style=\"position:relative;float:left;width:100%\">\n";
    echo "<button type=\"submit\" style=\"display:none\" disabled></button>\n";
    #echo "</div>\n";
    
    if(isset($_SESSION["DESCRIPTION_DATA"])){
        
        echo "<div class=\"hr\">Sample selection</div>\n";
        
        echo "<div style=\"position:relative;float:left;margin-left:20px;width:calc(100% - 20px);height:30px;font-style:italic\">\n";
        echo "Click on sample name to add to selection";
        echo "</div>\n";
        
        printAllSampleSelectors();
        
    } else {
        
        echo "<p>FILE DESCRIPTION_DATA IS MISSING IN CONFIG FILE, OR CANNOT BE FOUND</p>\n";
        
    }
    
    ## if sample selected, show visualization parameter and genomic coordinates selection 
    if(!empty($_SESSION["samples"])){
        
        echo "<div class=\"hr\">Visualization options</div>\n";
        
        ## samples selected
        
        echo "<div style=\"position:relative;float:left;margin-left:20px;width:calc(100% - 20px);height:30px;font-style:italic\">\n";
        echo "Click on sample to change color (for line visualization) and on the cross to remove it";
        echo "</div>\n";
        
        printSampleSelected();
        
        ## visu param selection
        
        echo "<div style=\"position:relative;float:left;margin:20px 0 0 20px;width:calc(100% - 20px);height:30px;font-style:italic\">\n";
        echo "Select visualization option";
        echo "</div>\n";
        
        printAllVisuSelectors();
        
        #echo "<div style=\"clear:both;width:100%;height:10px\"></div>\n";
        
        ## annotation feature selection
        if(isset($_SESSION["ANNOT_FILE"]) && isset($_SESSION["ANNOT_GENE_TYPES_LIST"])){
            
            echo "<div class=\"hr\">Gene annotation : select gene type to show\n";
            #echo "<div class=\"tooltip\">Annotation visualization selection\n";
            #echo "<span class=\"tooltiptext\" style=\"width:300px\">Select annotation features for display</span>\n";
            #echo "</div>\n";
            echo "</div>\n";
            
            $value = "all";
            if(isset($_POST["menuTypeSetInput"])){
                $value = $_POST["menuTypeSetInput"];
            }
            
            $is_open = "no";
            if(isset($_POST["geneTypeMenuInput"])){
                $is_open = $_POST["geneTypeMenuInput"];
            }
            
            printAnnotFeatureSelection($value, $is_open);
            
            echo "<div style=\"clear:both;width:100%\"></div>\n";
            
            $collapse="yes";
            
            if(isset($_SESSION["COLLAPSE_TRANSCRIPTS"])){
				if($_SESSION["COLLAPSE_TRANSCRIPTS"] == "no"){
					$collapse = "no";
				}
			}
            
            echo "<div style=\"width:100%;position:relative;float:left\">\n";
            echo "<div style=\"position:relative;width:50%;text-align:right;float:left\">collapse isoforms</div>\n";
            if($collapse=="yes"){
				echo "<div style=\"position:relative;width:5%;text-align:right;float:left\"><input type=\"radio\" name=\"collapse_transcripts\" value=\"yes\" checked>yes</div>\n";
				echo "<div style=\"position:relative;width:5%;text-align:right;float:left\"><input type=\"radio\" name=\"collapse_transcripts\" value=\"no\">no</div>\n";
			} else {
				echo "<div style=\"position:relative;width:5%;text-align:right;float:left\"><input type=\"radio\" name=\"collapse_transcripts\" value=\"yes\">yes</div>\n";
				echo "<div style=\"position:relative;width:5%;text-align:right;float:left\"><input type=\"radio\" name=\"collapse_transcripts\" value=\"no\" checked>no</div>\n";
			}
            echo "</div>\n";
            
            echo "<div style=\"clear:both;width:100%\"></div>\n";
        }
        
        #echo "<div style=\"clear:both;width:100%\"></div>\n";
        
        ## genomic coordinates
        
        echo "<div class=\"hr\">Genomic location</div>\n";
        
        echo "<div style=\"position:relative;height:75px;width:100%;margin-bottom:25px\">\n";
        
        echo "<div style=\"position:relative;float:left;width:50%;text-align:center\">\n";
        printBrowserCoord();
        echo "</div>\n";
        
        echo "<div style=\"position:relative;float:left;width:50%;text-align:center\">\n";
        printBrowserGene();
        echo "</div>\n";
        
        echo "</div>\n"; 
        
    }
    
    printDropdownJS();
    
    echo "</form>\n";
    
    echo "<script>\n";
    echo " document.getElementById(\"myForm\").onkeypress = function(event) {\n";
    echo "   var key = e.charCode || e.keyCode || 0;\n";
    echo "   if (key == 13) {\n";
    echo "     alert(\"No Enter!\");\n";
    echo "     e.preventDefault();\n";
    echo "   }\n";
    echo " }\n";
    echo "</script>\n";
}

## printBrowserArrow
## in :
##     chr_     : chromosome - previous genomic coordinates
##     chrsize_ : chromosome size
##     start_   : start - previous genomic coordinates
##     stop_    : stop - previous genomic coordinates
##     samples_ : samples names - for form
##     visu_    : visu type - for form
##     scale_   : log? - for form
##     libType_ : library type ((un)stranded) - for form
##     norm_    : normalized ? - for form
##     which    : left or right. Go left or rightward along genome?
## out : 
##     print browser arrow to navigate along genome, and give hidden form
function printBrowserArrow($chr_, $start_, $stop_, $which){
    
    $span=(int)(($stop_-$start_+1)/2);
    
    $chr_size = $_SESSION["CHR_SIZE"][$chr_];
    
    ## set new coord : add half window width
    if($which=="left"){
        
        $start_new=(int)$start_-$span;
        
        if($start_new < 1){
            
            $start_new = 1;
            
        } 
        
        $stop_new=(int)$start_new+($span*2);
        
    } else {
        
        $stop_new=(int)$stop_+$span;
        
        if($stop_new > $chr_size){
            
            $stop_new = $chr_size;
        }
        
        $start_new=(int)$stop_new-($span*2);
        
    }
    
    $coord_new=$start_new."-".$stop_new;
    
    echo "<form method=\"post\" action=\"coverage.php\">\n";
    
    ## chr
    echo "<input type=\"hidden\" name=\"chromosome\" value=\"$chr_\">\n";
    
    ## coord
    echo "<input type=\"hidden\" name=\"coord\" value=\"$coord_new\">\n";
    
    ## submit
    
    if($which=="left"){
    
		echo "<button class=\"button_nav\" style=\"position:relative;float:right\" type=\"submit\" name=\"seeCoverage\" value=\"coord\">\n";
		
        echo "<img src=\"../images/fleche_gauche_1.png\" alt=\"Before\" height=\"50px\" width=\"90px\"/>\n";
        
    } else {
        
        echo "<button class=\"button_nav\" style=\"position:relative;float:left\" type=\"submit\" name=\"seeCoverage\" value=\"coord\">\n";

        
        echo "<img src=\"../images/fleche_droite_1.png\" alt=\"After\" height=\"50px\" width=\"90px\"/>\n";
        
    }
    
    echo "</button>\n";
    
    echo "</form>\n";
    
}


## printBrowserZoom
function printBrowserZoom($chr_, $start_, $stop_, $zoom){
    
    $span=(int)($stop_ - $start_-1);
    
    $chr_size = $_SESSION["CHR_SIZE"][$chr_];
    
    $spanFrac=round($span/4);
    
    if (($span > 2) or ($span < $chr_size)) {
        
        ## set new coord
        if($zoom=="in"){ ##  divide window by 2
            
            $start_new=(int)$start_ + $spanFrac;
            
            $stop_new=(int)$stop_ - $spanFrac;
            
            if (($stop_new - $start_new) < 2){
                
                $stop_new = $start_new + 2;
                
            }
            
        } else if($zoom == "out"){ ##  multiply window by 2
            
            $start_new=(int)$start_ - $spanFrac;
            
            if($start_new < 1){
                
                $start_new = 1;
                
            }
            
            $stop_new = (int)$stop_ + $spanFrac;
            
            if($stop_new > $chr_size){
                
                $stop_new = $chr_size;
                
            }
            
        }
        
        $coord_new=$start_new."-".$stop_new;
        
        echo "<form method=\"post\" action=\"coverage.php\">\n";
        
        ## chr
        echo "<input type=\"hidden\" name=\"chromosome\" value=\"$chr_\">\n";
        
        ## coord
        echo "<input type=\"hidden\" name=\"coord\" value=\"$coord_new\">\n";
        
        ## submit
        echo "<div style=\"position:relative;float:left;width:30%\">";
        if($zoom=="in"){

            echo "<button style=\"height:25px;width:15px;position:relative;float:left;border:none;padding:0px\" type=\"submit\" value=\"coord\" name=\"seeCoverage\">+</button>\n";
            
        } else {
            
            echo "<button style=\"height:25px;width:15px;position:relative;float:right;border:none;padding:0px\" type=\"submit\" value=\"coord\" name=\"seeCoverage\">-</button>\n";
            
        }
        echo "</div>\n";
        
        echo "</form>\n";
        
    }
    
}

## printHTMLTable : print table HTML format
## 
## in : 
## out :
##     table HTML format
function printHTMLTable($table, $isHeader) {
    
    echo "<table>\n";
    
    $i_line = 0;
    
    foreach($table as $line){
        
        echo "<tr>";
        
        $tag = ($i_line == 0 and $isHeader) ? ("th") : ("td");
            
        foreach(explode(",", $line) as $col){
            
            echo "<$tag>$col</$tag>";
            
        }
        
        echo "</tr>\n";
        
    }
    
    echo "</table>\n";
    
}


## printCoverage
function printCoverage($chr, $start, $stop){ 
    
    echo "<div style=\"position:relative;float:left;height:25px;width:100%\"><a href=\"coverage.php\">&#xAB;back to menu</a></div>\n";
    
    ## navbar 1
    echo "<div style=\"position:relative;float:left;height:75px;width:100%\">\n";
    
    ## new coordinates
    echo "<div class = \"navigateur_coord\" style=\"position:relative;float:left;width:40%;margin-left:10%;height:100%;text-align:center\">\n";
    
    echo "<form method=\"post\" action=\"coverage.php\">\n";
    
    printBrowserCoord($chr, $start, $stop);
    
    echo "</form>\n";
    
    echo "</div>\n";
    
    ## new gene name
    echo "<div class = \"navigateur_coord\" style=\"position:relative;float:left;width:40%;margin-right:10%;height:100%;text-align:center\">\n";
    
    echo "<form method=\"post\" action=\"coverage.php\">\n";
    
    printBrowserGene($boxSize = 15, $prev_chr = $chr, $prev_start = $start, $prev_stop = $stop);
    
    echo "</form>\n";
    
    echo "</div>\n";
	
    echo "</div>\n"; ## end navbar1
    
    echo "<div style=\"clear:both;width:100%\">\n";
    
    echo "<hr style=\"color:#A0A0A0\">\n";
    
    echo "</div>\n";
	
	## navbar 2
	
	echo "<div style=\"position:relative;float:left;height:50px;width:100%\">\n";
	
    ## to go left 
    echo "<div style=\"position:relative;float:left;width:35%;height:100%\">\n";
    
    if($start > 1){
        
        printBrowserArrow($chr_=$chr, $start_=$start, $stop_=$stop, $which="left");
        
    }
    
    echo "</div>\n";
	
    ## zoom & genomic location
    echo "<div style=\"position:relative;float:left;height:50px;width:30%\">\n";
    
		printBrowserZoom($chr_=$chr, $start_=$start, $stop_=$stop, $zoom="out");
    
		echo "<div style=\"position:relative;float:left;height:25px;width:30%;text-align:center\">Zoom</div>\n";
    
		printBrowserZoom($chr_=$chr, $start_=$start, $stop_=$stop, $zoom="in");
    
		echo "<div style=\"position:relative;float:left;height:20px;padding-top:5px;width:100%;text-align:center\">$chr : $start - $stop</div>\n";
    
    echo "</div>\n";

    ## to go right
    
    echo "<div style=\"position:relative;float:left;width:35%;height:100%\">\n";
    
    if($start < $_SESSION["CHR_SIZE"][$chr] && $stop < $_SESSION["CHR_SIZE"][$chr]){
        
        printBrowserArrow($chr_=$chr, $start_=$start, $stop_=$stop, $which="right");
        
    }
    echo "</div>\n";
    
    echo "</div>\n"; ## end navbar2
    
    ## show coverage and annot
    
    $samples=implode(",", $_SESSION['samples']);
    
    $visu=$_SESSION['visu'];
    
    $scale=$_SESSION['scale'];
    
    $libType=$_SESSION['libType'];
    
    $norm=$_SESSION['norm'];
    
    $color=implode(",", $_SESSION['color']);
    
    $lineType=$_SESSION['lineType'];
    
    $pythonPath=$_SESSION['PYTHON_PATH'];
    
    #$scriptDir=$_SESSION['SCRIPTS_DIR'];
    
    $annotFile=$_SESSION['ANNOT_FILE'];
    
    $descriptionDataFile=$_SESSION['DESCRIPTION_DATA_FILE'];
    
    $types_to_show = isset($_SESSION['TYPES_TO_SHOW']) ? implode(",", $_SESSION['TYPES_TO_SHOW']) : "";
    
    $show_transcript_name = "no";
	$collapse_transcripts = "yes";
	
    if(isset($_SESSION["COLLAPSE_TRANSCRIPTS"])){
		
		$show_transcript_name = $_SESSION["SHOW_TRANSCRIPT_NAME"];
		$collapse_transcripts = $_SESSION["COLLAPSE_TRANSCRIPTS"];
		
	} 
	
	#$show_transcript_name = isset($_SESSION["SHOW_TRANSCRIPT_NAME"]) ? $_SESSION["SHOW_TRANSCRIPT_NAME"] : "no";
    #$collapse_transcripts =  isset($_SESSION["COLLAPSE_TRANSCRIPTS"]) ? $_SESSION["COLLAPSE_TRANSCRIPTS"] : "yes";
    
    # protect variables
    $chr = escapeshellarg($chr);
    $start = escapeshellarg($start);
    $stop = escapeshellarg($stop);
    $samples = escapeshellarg($samples);
    $visu = escapeshellarg($visu);
    $scale = escapeshellarg($scale);
    $libType = escapeshellarg($libType);
    $norm = escapeshellarg($norm);
    $color = escapeshellarg($color);
    $lineType = escapeshellarg($lineType);
    $annotFile = escapeshellarg($annotFile);
    $descriptionDataFile = escapeshellarg($descriptionDataFile);
    $types_to_show = escapeshellarg($types_to_show);
    $show_transcript_name = escapeshellarg($show_transcript_name);
    $collapse_transcripts = escapeshellarg($collapse_transcripts);
    
    #echo "$pythonPath coverage.py --chr=$chr --start=$start --stop=$stop --samples=\"$samples\" --visu=\"$visu\" --scale=\"$scale\" --libType=\"$libType\" --norm=\"$norm\" --color=\"$color\" --lineType=\"$lineType\" --annot=$annotFile --description_data=$descriptionDataFile --types_to_show=\"$types_to_show\" --show_transcript_name=$show_transcript_name --collapse_transcripts=$collapse_transcripts";
    
    #$res=exec("$pythonPath $scriptDir/coverage.py --chr=$chr --start=$start --stop=$stop --samples=\"$samples\" --visu=\"$visu\" --scale=\"$scale\" --libType=\"$libType\" --norm=\"$norm\" --color=\"$color\" --lineType=\"$lineType\" --annot=$annotFile --description_data=$descriptionDataFile --types_to_show=\"$types_to_show\" --show_transcript_name=$show_transcript_name --collapse_transcripts=$collapse_transcripts");
    $res=exec("$pythonPath coverage.py --chr=$chr --start=$start --stop=$stop --samples=\"$samples\" --visu=\"$visu\" --scale=\"$scale\" --libType=\"$libType\" --norm=\"$norm\" --color=\"$color\" --lineType=\"$lineType\" --annot=$annotFile --description_data=$descriptionDataFile --types_to_show=\"$types_to_show\" --show_transcript_name=$show_transcript_name --collapse_transcripts=$collapse_transcripts");
    
    if (count(json_decode($res)) == 3){
        
        $window_height=json_decode($res)[2] . "px";
        
    } else {
                
        $window_height="200px";
        
    }
    
    echo "<div id=\"coverage\" style=\"height:$window_height;\"></div>\n";
    
    echo "
        <script>
            var tmp = $res;
            var data = tmp[0];
            var layout = tmp[1];
            Plotly.newPlot('coverage', data, layout, {modeBarButtonsToRemove: ['zoom2d', 'pan2d', 'select2d', 'lasso2d','zoomIn2d','zoomOut2d','autoScale2d','resetScale2d','hoverClosestCartesian','hoverCompareCartesian','toggleSpikelines']});
        </script>";
    
    # print count table
    #$countFile = $_SESSION["COUNT_FILE"];
        
    #$countFileIndex = $_SESSION["COUNT_FILE_IS_INDEXED"] ? "TRUE" : "FALSE";
    
    #echo "<div style=\"clear:both;width:100%\"></div>\n";
    
    #echo "<div class = \"count_table\">\n";
    
    #$res = exec("$pythonPath $scriptDir/print_count_table.py --countFile=$countFile --indexed=$countFileIndex --descriptionDataFile=$descriptionDataFile --chr=$chr --start=$start --stop=$stop --samples=\"$samples\" --norm=\"$norm\" --scale=\"$scale\"");
    
    #var_dump($res);
    
    #printHTMLTable(json_decode($res),True);
    
    echo "</div>\n";
    
}


?>




