<?php
include "db.php";  // include the database connection

header("Content-Type: application/json"); // tell browser we’re sending JSON

if (isset($_GET['query'])) {
    $query = $_GET['query'];
    
    // Prepare statement to prevent SQL injection
    $stmt = $conn->prepare("SELECT Donor_ID, Name, Mobile_no, Location 
                            FROM donor_details 
                            WHERE Name LIKE CONCAT('%', ?, '%')
                            LIMIT 10");
    $stmt->bind_param("s", $query);
    $stmt->execute();
    $result = $stmt->get_result();
    
    $donors = [];
    while ($row = $result->fetch_assoc()) {
        $donors[] = $row;
    }
    
    echo json_encode($donors);
} else {
    echo json_encode([]); // return empty array if no query
}
?>
