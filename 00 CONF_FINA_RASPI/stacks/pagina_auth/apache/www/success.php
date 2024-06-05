<?php
session_start();
if (!isset($_SESSION['username'])) {
    header("Location: index.php");
    exit();
}
?>

<!DOCTYPE html>
<html>
<head>
    <title>Login Successful</title>
</head>
<body>
    <h1>Welcome, <?php echo $_SESSION['username']; ?>!</h1>
    <form method="post" action="script.php">
        <input type="submit" value="Run Python Script">
    </form>
    <form action="http://192.168.1.11:5001">
        <input type="submit" value="Dockge">
    </form>
    </form>
        <form method="post" action="./log.php">
        <label for="fecha">Fecha (YYYY-MM-DD):</label>
        <input type="date" id="fecha" name="fecha">
        <input type="submit" value="Filtrar">
    </form>
</body>
</html>
