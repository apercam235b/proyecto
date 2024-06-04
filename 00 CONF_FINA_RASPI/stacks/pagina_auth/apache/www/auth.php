<?php
session_start();

$servername = "db";
$username = "user";
$password = "password";
$dbname = "mydb";

// Create connection
$conn = new mysqli($servername, $username, $password, $dbname);

// Check connection
if ($conn->connect_error) {
  die("Connection failed: " . $conn->connect_error);
}

$user = $_POST['username'];
$pass = $_POST['password'];

$sql = "SELECT * FROM users WHERE username='$user' AND password='$pass'";
$result = $conn->query($sql);

if ($result->num_rows > 0) {
  $_SESSION['username'] = $user;
  header("Location: success.php");
} else {
  echo "Invalid credentials";
}

$conn->close();
?>
