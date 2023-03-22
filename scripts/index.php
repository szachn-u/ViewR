<?php
	
	include 'functions.php';
	session_start();
	session_unset();
	setConfig();
?>

<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">

<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="fr" lang="fr">

    <head>
        
        <?php
			$title = isset($_SESSION["TITLE"]) ? $_SESSION["TITLE"] : "viewR";
			echo "<title>$title</title>\n";
        ?>
        
        <link rel="stylesheet" media="screen" href="https://fontlibrary.org//face/liberation-sans" type="text/css"/>
        
        <link rel="stylesheet" media="screen" type="text/css" title="Design" href="design.css"/>
        
        <meta http-equiv="Content-Type" content="text/html; charset=utf-8"/>
        
        <style>
			
			body{
				font-family:'LiberationSansRegular';
				font-weight: normal;
				font-style:normal;
				}
				
        </style>
        
    </head>
    
    <body style="width:100%;margin:0">
        
        <div style="width:90%;height:100%;margin:0% 5% 10% 5%">
            
            <?php
				if(isset($_SESSION["IMAGE1"])){
					$img = $_SESSION["IMAGE1"];
					echo "<img src=\"$img\" style=\"margin-top:5%;margin-bottom:5%;margin-left:auto;margin-right:auto;display:block\">\n";
				} else {
					echo "<img src=\"no_image\" style=\"margin-top:5%;margin-bottom:5%;margin-left:auto;margin-right:auto;display:block\" alt=\"viewR\">\n";

				}
			?>
            
            <div style="clear:both;width:90%;margin:0 5% 0 5%"></div>
        
        </div>
		
		<div style="margin:10% 10% 20% 10%">
				
				<?php
				if(isset($_SESSION["USER_GUIDE"])){
					$guide=$_SESSION["USER_GUIDE"];
					echo "<div style=\"width:47%;float:left;text-align:right;font-size:35px\">\n";
					echo "<a href=\"$guide\" download>User Guide</a>\n";
					echo "</div>\n";
					echo "<div style=\"width:6%;float:left;text-align:center;font-size:35px\">|</div> \n";
					echo "<div style=\"width:47%;float:left;text-align:left;font-size:35px\">\n";
					echo "<a style=\"color:black;text-decoration: none\" href=\"coverage.php\">Start</a>\n";
					echo "</div>\n";
				} else {
					echo "<div style=\"width:95%;float:left;text-align:center;font-size:35px\">\n";
					echo "<a style=\"color:black;text-decoration: none\" href=\"coverage.php\">Start</a>\n";
					echo "</div>\n";
				}
				
				?>
				
		</div> 
        
        <div style="clear:both;width:90%;margin:0 5% 0 5%"></div>
        
        <div style="width:90%;height:20%;margin:2% 5% 2% 5%;text-align:center">
			
			If you use this viewer for your research, please quote Szachnowski et al.
			
        </div>
        
        <div style="clear:both;width:90%;margin:0 5% 0 5%"><hr></div>
        
        <div style="width:90%;height:5%;margin:0 5% 0 5%;text-align:right">
            
            <p>Visualization by <a href="https://github.com/szachn-u/ViewR">ViewR</a></p>
        
        </div>
        
    </body>
    
</html>

