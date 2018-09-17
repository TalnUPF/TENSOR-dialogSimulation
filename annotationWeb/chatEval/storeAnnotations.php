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
	$idAnn = rand();
	$date = $_POST["chatId"];
	foreach($_POST as $key => $answer)
	{
		if($key!="chatId")
		{
			$sql = "INSERT INTO `annotations` (`turn_id`, annotation, `id_annotator`,`date`) VALUES (?,?,?,?)";
			$stmt= $pdo->prepare($sql);
			$stmt->execute([intval($key), $answer, $idAnn,$date]);
		}
	}

	require_once("header.php");

	echo "<div class='thankYou'>";
	echo "<h1>STORED RESULTS!</h1>";
	echo "<br/>";
	echo "<h2>Thank you!</h2></div>";

?>
