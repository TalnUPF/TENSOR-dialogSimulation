<?php
	require_once("header.php");

	$chatId = explode("_", $_GET['chatId'])[0];
	$txtRaw = file_get_contents("resources/topicsPerUser/".$_GET['chatId']);
	$pieces = explode("\n",$txtRaw);

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

	error_reporting(E_ALL);
	ini_set('display_errors', 1);

	$host = 'localhost';
	$db   = 'chatEval';
	$user = 'root';
	$pass = 'pany8491';

	$options = [
	    PDO::ATTR_ERRMODE            => PDO::ERRMODE_EXCEPTION,
	    PDO::ATTR_DEFAULT_FETCH_MODE => PDO::FETCH_ASSOC,
	    PDO::ATTR_EMULATE_PREPARES   => false,
	];
	$dsn = "mysql:host=$host;dbname=$db;";
	try {
	     $pdo = new PDO($dsn, $user, $pass, $options);
	} catch (\PDOException $e) {
	     throw new \PDOException($e->getMessage(), (int)$e->getCode());
	}

	$sql = "SELECT block_id, Q1,Q2 FROM `results` WHERE `date`='".$chatId."'";
	$stmt= $pdo->prepare($sql);
	$stmt->execute();
	$result = $stmt->fetchAll(PDO::FETCH_ASSOC);

	$aggregatedResults = array();
	$totalResults = array();
	$totalResults["Q1"] = 0;
	$totalResults["Q2"] = 0;
	
	$total = 0;

	foreach($result as $row)
	{
		if(!array_key_exists($row["block_id"],$aggregatedResults))
		{
			$aggregatedResults[$row["block_id"]]["Q1"]["positive"] = 0;
			$aggregatedResults[$row["block_id"]]["Q1"]["negative"] = 0;
			$aggregatedResults[$row["block_id"]]["Q2"]["positive"] = 0;
			$aggregatedResults[$row["block_id"]]["Q2"]["negative"] = 0;
		}
		$total++;
		$totalResults["Q1"]+=$row["Q1"];
		$totalResults["Q2"]+=$row["Q2"];

		if($row["Q1"] == 0)
		{
			$aggregatedResults[$row["block_id"]]["Q1"]["negative"]++;
		}
		if($row["Q2"] == 0)
		{
			$aggregatedResults[$row["block_id"]]["Q2"]["negative"]++;
		}
		if($row["Q1"] == 1)
		{
			$aggregatedResults[$row["block_id"]]["Q1"]["positive"]++;
		}
		if($row["Q2"] == 1)
		{
			$aggregatedResults[$row["block_id"]]["Q2"]["positive"]++;
		}
	}
	echo "<div class='generalResults'>";
	echo "<h2>"."Q1 Accuracy ".$totalResults["Q1"] / $total."</h2>";
	echo "<h2>"."Q2 Accuracy ".$totalResults["Q2"] / $total."</h2>";
	echo "</div>";
?>
	<div class="tableDiv table-responsive table-striped">
		<table class="header-fixed table">
		  <thead class="thead-dark">
		    <tr class="row chatMsg">
		      <th class="col-md-6">Block</th>
		      <th class="col-md-2">Topic</th>
		      <th class="col-md-2">Results Q1</th>
		      <th class="col-md-2">Results Q2</th>
		    </tr>
		  </thead>
<?php
	$i=0;
	$AZRA = "[--[azra]--]";
	$JAWAD = "[--[jawad]--]";
	while($i<count($textList))
	{
		
?>

		<tr class="row chatMsg">

			<td class="col-md-6">
<?php
				$textElem = trim($textList[$i]);
				$pieces = explode(" ",$textElem);
				$j = 0;
				$acumMsg = "";
				while($j < count($pieces))
				{
					$token = $pieces[$j];
					if($token == $AZRA)
					{
						echo "<span class='azraText'>".$acumMsg."</span> ||";
						$acumMsg = "";
					}
					else if ($token == $JAWAD)
					{
						echo "<span class='jawadText'>".$acumMsg."</span> ||";
						$acumMsg = "";
					}
					else
					{
						$acumMsg.=" ".$token;
					}
					$j++;
				}
?>			
			</td>
			<td class="col-md-2">
<?php
				echo $catList[$i];
?>			
			</td>

			<td class="col-md-2">
				  <div>
				  	<?php 
				  		$acc = $aggregatedResults[$i]["Q1"]["positive"] / ($aggregatedResults[$i]["Q1"]["positive"] + $aggregatedResults[$i]["Q1"]["negative"]);
				  		echo $aggregatedResults[$i]["Q1"]["positive"]." positive votes<br/>"; 
				  		echo $aggregatedResults[$i]["Q1"]["negative"]." negative votes<br/>"; 
				  		echo number_format($acc, 3, '.', ',');
				  	?>
				  </div>
				  
			</td>
			<td class="col-md-2">
				  <div>
				  	<?php 
				  		$acc = $aggregatedResults[$i]["Q2"]["positive"] / ($aggregatedResults[$i]["Q2"]["positive"] + $aggregatedResults[$i]["Q2"]["negative"]);
				  		echo $aggregatedResults[$i]["Q2"]["positive"]." positive votes<br/>"; 
				  		echo $aggregatedResults[$i]["Q2"]["negative"]." negative votes<br/>"; 
				  		echo number_format($acc, 3, '.', ',');
				  	?>
				  </div>
				  
			</td>
		</tr>
<?php
		$i++;
	}
?>
		</table>
	</div>

</form>