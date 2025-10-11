<?php
include "db.php";

header("Content-Type: application/json");

if ($_SERVER["REQUEST_METHOD"] === "POST") {
    $name = trim($_POST['name']);
    $phone = trim($_POST['phone']);
    $location = trim($_POST['location']);
    $email = isset($_POST['email']) ? trim($_POST['email']) : null;
    $address = isset($_POST['address']) ? trim($_POST['address']) : null;

    if (empty($name) || empty($phone) || empty($location)) {
        echo json_encode(["success" => false, "message" => "Required fields missing"]);
        exit;
    }

    $stmt = $conn->prepare("INSERT INTO donor_details (Name, Mobile_no, Mail, Address, Location)
                            VALUES (?, ?, ?, ?, ?)");
    $stmt->bind_param("sssss", $name, $phone, $email, $address, $location);

    if ($stmt->execute()) {
        echo json_encode([
            "success" => true,
            "Donor_ID" => $conn->insert_id,
            "Name" => $name
        ]);
    } else {
        echo json_encode(["success" => false, "message" => "Database error"]);
    }

    $stmt->close();
} else {
    echo json_encode(["success" => false, "message" => "Invalid request method"]);
}
?>

