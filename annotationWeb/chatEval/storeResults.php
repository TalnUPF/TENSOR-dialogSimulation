<?php
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
	
	$results = array();

	foreach($_POST as $key => $answer)
	{
		$pieces = explode("_",$key);
		$questionId = $pieces[0];
		$block_id = $pieces[1];
		
		if(!array_key_exists($block_id,$results))
		{
			$results[$block_id] = array();
		}

		$results[$block_id][$questionId] = intval($answer);
		
	}

	foreach($results as $block => $dictAns)
	{
		$sql = "INSERT INTO `results` (`block_id`, Q1, Q2) VALUES (?,?,?)";
		$stmt= $pdo->prepare($sql);
		$stmt->execute([$block, $dictAns["Q1"], $dictAns["Q2"]]);
	}

	require_once("header.php");

	echo "<div class='thankYou'>";
	echo "<h1>STORED RESULTS!</h1>";
	echo "<br/>";
	echo "<h2>Thank you!</h2></div>";

?>