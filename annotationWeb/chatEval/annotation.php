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


<div class="topDivs" class="col-md-12">
	<h3>Annotation Guidelines</h3>
	<h4>Label descriptions:</h4>
	<b>conversation</b> -> just general chit chat. Greetings, general questions, standard stuff <br/>
	<b>suspActivities</b> -> are the participants talking about suspicious activities? <br/>
	<b>emotions</b> -> are the participants talking about their emotions? </br>
	<b>religion</b> -> are they talking about their religion? <br/>
	<b>news</b> -> generic news discussion <br/>
	<b>yijad</b> -> extremist religion discussion
</div>

<div id="export" >
	<a href="downloadAnns.php" class="btn btn-warning" role="button">Export current annotations</a>
</div>

<form action="storeAnnotations.php" method="POST">

	<div class="tableDivAnn tableDiv table-responsive table-striped">
		<table class="header-fixed table">
		  <thead class="thead-dark">
		    <tr class="row chatMsg">
		      <th class="col-md-1">ID</th>
		      <th class="col-md-8">Block</th>
		      <th class="col-md-3">Category</th>
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
			<td class="col-md-8">
<?php
				echo $textList[$i];
?>			
			</td>

			<td class="col-md-3">
				  <div align="center" class="categoryWrapper">
				  	 <label for="sel1">Pick the most fitting category:</label>
				     <select name="<?php echo $i;?>" class="form-control dropdown" id="sel1">
				          <option value="conversation">conversation</option>
						  <option value="suspActivities">suspActivities</option>
						  <option value="emotions">emotions</option>
						  <option value="religion">religion</option>
						  <option value="news">news</option>
						  <option value="yijad">yijad</option>
				      </select>
				  </div>
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