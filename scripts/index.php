<?php
    
    include 'functions.php';
    session_start();
    #session_unset();
    $id = setConfig();
    $title = isset($_SESSION[$id]["TITLE"]) ? $_SESSION[$id]["TITLE"] : "viewR";
    
    echo "<!DOCTYPE html PUBLIC \"-//W3C//DTD XHTML 1.0 Strict//EN\" \"http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd\">\n";
    echo "<html xmlns=\"http://www.w3.org/1999/xhtml\" xml:lang=\"fr\" lang=\"fr\">\n";
    
    echo "    <head>\n";
        
    echo "        <title>$title</title>\n";
    
    echo "        <link rel=\"stylesheet\" media=\"screen\" href=\"https://fontlibrary.org//face/liberation-sans\" type=\"text/css\"/>\n";
    echo "        <link rel=\"stylesheet\" media=\"screen\" type=\"text/css\" title=\"Design\" href=\"design.css\"/>\n";
    
    echo "        <meta http-equiv=\"Content-Type\" content=\"text/html; charset=utf-8\"/>\n";
    
    echo "        <style>";
    echo "            body{\n";
    echo "                font-family:'LiberationSansRegular';\n";
    echo "                font-weight: normal;\n";
    echo "                font-style:normal;\n";
    echo "            }\n";
    echo "        </style>\n";
    
    echo "    </head>\n";
    
    echo "    <body style=\"width:100%;margin:0\">\n";
    
    echo "        <div style=\"width:90%;height:100%;margin:0% 5% 10% 5%\">\n";
    
    if(isset($_SESSION[$id]["IMAGE1"])){
        $img = $_SESSION[$id]["IMAGE1"];
        echo "            <img src=\"$img\" style=\"margin-top:5%;margin-bottom:5%;margin-left:auto;margin-right:auto;display:block\">\n";
    } else {
        echo "            <img src=\"no_image\" style=\"margin-top:5%;margin-bottom:5%;margin-left:auto;margin-right:auto;display:block\" alt=\"viewR\">\n";
    }
    
    echo "        </div>\n";
    
    echo "        <div style=\"clear:both;width:90%;margin:0 5% 0 5%\"></div>\n";
    
    echo "        <div style=\"margin:10% 10% 20% 10%\">\n";
    
    echo "        <form method=\"post\" action=\"coverage.php\">\n";
    
    echo "        <input type=\"hidden\" name=\"sessid\" value=\"$id\">\n";
    
    if(isset($_SESSION[$id]["USER_GUIDE"])){
        
        $guide = $_SESSION[$id]["USER_GUIDE"];
        echo "            <div style=\"width:47%;float:left;text-align:right;font-size:35px\">\n";
        echo "            <a href=\"$guide\" download>User Guide</a>\n";
        echo "            </div>\n";
        echo "            <div style=\"width:6%;float:left;text-align:center;font-size:35px\">|</div> \n";
        echo "            <div style=\"width:47%;float:left;text-align:left;font-size:35px\">\n";
        echo "            <button class=\"button_nav\" type=\"submit\" style=\"font-size:35px\">Start</button>\n";
        #echo "            <a style=\"color:black;text-decoration: none\" href=\"coverage.php\">Start</a>\n";
        echo "            </div>\n";
        
    } else {
        
        echo "            <div style=\"width:95%;float:left;text-align:center;font-size:35px\">\n";
        echo "            <button class=\"button_nav\" type=\"submit\" style=\"font-size:35px\">Start</button>\n";
        #echo "            <a style=\"color:black;text-decoration: none\" href=\"coverage.php\">Start</a>\n";
        echo "            </div>\n";
        
    }
    
    echo "    </form>\n";
    
    echo "        </div>\n"; 
    
    echo "        <div style=\"clear:both;width:90%;margin:0 5% 0 5%\"></div>\n";
    
    echo "        <div style=\"width:90%;height:20%;margin:2% 5% 2% 5%;text-align:center\">\n";
    echo "            If you use this viewer for your research, please quote Szachnowski et al.";
    echo "        </div>\n";
    
    echo "        <div style=\"clear:both;width:90%;margin:0 5% 0 5%\"><hr></div>\n";
    
    echo "        <div style=\"width:90%;height:5%;margin:0 5% 0 5%;text-align:right\">\n";
    echo "            <p>Visualization by <a href=\"https://github.com/szachn-u/ViewR\">ViewR</a></p>\n";
    echo "        </div>\n";
    
    echo "    </body>\n";
    
    echo "</html>\n";
    
?>

