<?php

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

$sql = "SELECT turn_id, annotation, id_annotator FROM `annotations`";
$stmt= $pdo->prepare($sql);
$stmt->execute();
$result = $stmt->fetchAll(PDO::FETCH_ASSOC);

$strFile = "";
foreach ($result as $dictAnn) 
{
		$line = $dictAnn["id_annotator"]."&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;".$textList[$dictAnn["turn_id"]]."&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;".$dictAnn["annotation"]."<br/>";
		$strFile.=$line;
}

echo $strFile;

?>