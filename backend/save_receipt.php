<?php
include "db.php";

if (isset($_POST['submit'])) {
    $name     = $_POST['name'];
    $date     = $_POST['date'];
    $amount   = $_POST['amount'];
    $paytype  = $_POST['paytype'];
    $category = $_POST['category'];

    $stmt = $conn->prepare("INSERT INTO receipts (Donor_Name, Amount, Date, Category, Payment_type) VALUES (?, ?, ?, ?, ?)");
    $stmt->bind_param("sdsss", $name, $amount, $date, $category, $paytype);

    if ($stmt->execute()) {
        $last_id = $conn->insert_id;
        // header("Location: receipt.php?id=$last_id");
        // exit;
        echo "Donation saved successfully. Receipt ID: $last_id";
    } else {
        echo "Error: " . $stmt->error;
    }
}
?>
