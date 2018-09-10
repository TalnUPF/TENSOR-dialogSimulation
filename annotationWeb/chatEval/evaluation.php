<?php
	require_once("header.php");

	$txtRaw = file_get_contents("resources/forWeb.out");

	$pieces = explode("\n\n",$txtRaw);

	$textList = array();
	$catList = array();

	foreach ($pieces as $msg) {
		$pieceLine = explode("\t",$msg);
		$txt = $pieceLine[0];
		if($txt!=""){
			$textList[] = $txt;
			$preds = $pieceLine[1];
			$catList[] = $preds;
		}		
	}

?>
<form action="storeResults.php" method="POST">

	<div class="tableDiv table-responsive table-striped">
		<table class="header-fixed table">
		  <thead class="thead-dark">
		    <tr class="row chatMsg">
		      <th class="col-md-1">ID</th>
		      <th class="col-md-5">Block</th>
		      <th class="col-md-2">Topic</th>
		      <th class="col-md-2">Q1</th>
		      <th class="col-md-2">Q2</th>
		    </tr>
		  </thead>
<?php
	$i=0;
	while($i<count($textList))
	{
?>

		<tr class="row chatMsg">

			<td class="col-md-1">
<?php
				echo $i;
?>	
			</td>
			<td class="col-md-5">
<?php
				echo $textList[$i];
?>			
			</td>
			<td class="col-md-2">
<?php
				echo $catList[$i];
?>			
			</td>

			<td class="col-md-2">
				  <div>
				  	Does this block make sense?
				  </div>
				  <input type="radio" name="Q1_<?php echo $i;?>" value="1"  checked="checked" /> Yes<br/>
				  <input type="radio" name="Q1_<?php echo $i;?>" value="0"/> No <br/>
			</td>
			<td class="col-md-2">
				  <div>
				  	Does this topic classification sense?
				  </div>
				  <input type="radio" name="Q2_<?php echo $i;?>" value="1"  checked="checked" /> Yes<br>
				  <input type="radio" name="Q2_<?php echo $i;?>" value="0"/> No
			</td>
		</tr>
<?php
		$i++;
	}
?>
		</table>
	</div>
	<div class="submitButton">
		<input class="btn btn-danger" type="submit" value="Store Answers">
	</div>
</form>