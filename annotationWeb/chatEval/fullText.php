<?php
	require_once("header.php");

	$chatId = $_GET['chatId'];
	$txtRaw = file_get_contents("resources/turns/".$chatId);

	$pieces = explode("\n\n",$txtRaw);

	$textList = array();
	$catList = array();

	foreach ($pieces as $msg) 
	{
		$textList[] = $msg;
	}
	$i=0;
?>
	<div class="table-responsive chatConversation">
		<table class="table table-striped">
<?php
	while($i<count($textList))
	{
?>

		<tr class="chatMsg">
			<td>
<?php	
			echo $textList[$i];
			$i++;
?>		</td>
		</tr>
<?php
	}
?>
		</table>
	</div>