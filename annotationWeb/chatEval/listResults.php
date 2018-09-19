<?php

	require_once("header.php");


	$files = scandir('./resources/topicsPerUser/');
	echo "<div id='mainContainer'>";
	echo "<h1>Chat Conversations</h1><br/>";

	foreach ($files as $file) 
	{
		if ($file != '.' && $file != '..') 
	    {
	    	$files_in_directory = scandir($file);
			$items_count = count($files_in_directory);
			echo "<div class='link'><a href='results.php?chatId=".$file."'>".$file."</a></div>";
		}
	}	

?>