<?php
session_start();
if (!isset($_SESSION['username'])) {
    header("Location: index.php");
    exit();
}

// Añadimos depuración para verificar la ejecución del script PHP
error_reporting(E_ALL);
ini_set('display_errors', 1);

echo "Ejecutando script de Python...<br>";

// Ejecutar el script de Python y capturar la salida
$output = shell_exec('python3 /var/www/html/script.py 2>&1');
echo "<pre>";
echo $output;
echo "</pre>";
?>
