<?php
	require_once("header.php");

	$txtRaw = file_get_contents("resources/turns.txt");

	$pieces = explode("\n\n",$txtRaw);

	$textList = array();
	$catList = array();

	foreach ($pieces as $msg) {
		$pieceLine = explode("\t",$msg);
		$txt = $pieceLine[0];
		$textList[] = $txt;
		$preds = $pieceLine[1];
		$catList[] = $preds;
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