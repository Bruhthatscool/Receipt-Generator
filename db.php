<?php
$host = "localhost";
$user = "root";   // default user in XAMPP
$pass = "";       // default password is empty
$db   = "donations_db";  // the database you just created

$conn = new mysqli($host, $user, $pass, $db);

if ($conn->connect_error) {
    die("Connection failed: " . $conn->connect_error);
}
?>
