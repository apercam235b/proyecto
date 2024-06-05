<?php
session_start();
if (!isset($_SESSION['username'])) {
    header("Location: index.php");
    exit();
}
?>

<html>
<body>
<?php

$FechaFiltro = $_POST["fecha"] ;

$archivo = fopen("log.txt","r") or die ("no se puede abrir");
while(!feof($archivo)) {
        $linea = fgets($archivo);
        if (strpos($linea,$FechaFiltro)===0){
                echo $linea."<br>";
        }
}
fclose($archivo);
?>

</body>
</html>
