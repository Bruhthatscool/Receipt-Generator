-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Oct 10, 2025 at 08:37 PM
-- Server version: 10.4.32-MariaDB
-- PHP Version: 8.0.30

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `donations_db`
--

-- --------------------------------------------------------

--
-- Table structure for table `donation_category`
--

CREATE TABLE `donation_category` (
  `Category_ID` int(11) NOT NULL,
  `Category` varchar(100) NOT NULL,
  `Active` tinyint(1) NOT NULL DEFAULT 1
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `donation_category`
--

INSERT INTO `donation_category` (`Category_ID`, `Category`, `Active`) VALUES
(1, 'General Fund', 1),
(2, 'Disaster Relief', 1),
(3, 'Digital Mission', 0);

-- --------------------------------------------------------

--
-- Table structure for table `donor_details`
--

CREATE TABLE `donor_details` (
  `Donor_ID` int(11) NOT NULL,
  `Name` varchar(100) NOT NULL,
  `Mobile_no` varchar(15) NOT NULL,
  `Mail` varchar(100) DEFAULT NULL,
  `Address` varchar(255) DEFAULT NULL,
  `Location` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `donor_details`
--

INSERT INTO `donor_details` (`Donor_ID`, `Name`, `Mobile_no`, `Mail`, `Address`, `Location`) VALUES
(1, 'Ananya Nair', '7012374100', 'ananyanair@gmail.com', 'kochupurakkal(H),EKM', 'Ernakulam'),
(2, 'Athul ', '8129429443', 'athul@gmail.com', 'Meenadom,kottaym', 'KTYM'),
(3, 'Anna Grace', '9744085817', 'anna@gmail.com', 'kazhakkootam,TVM', 'TVM'),
(4, 'Arsha Ann', '8547949274', 'arsha@gmail.com', 'chengannur,Aleppey', 'Aleppey');

-- --------------------------------------------------------

--
-- Table structure for table `receipts`
--

CREATE TABLE `receipts` (
  `Receipt_ID` int(11) NOT NULL,
  `Donor_ID` int(11) NOT NULL,
  `Amount` decimal(10,2) NOT NULL,
  `Donation_date` date NOT NULL,
  `Category_ID` int(11) NOT NULL,
  `Payment_type` enum('cash','gpay','cheque') NOT NULL,
  `Reference_no` varchar(50) DEFAULT NULL,
  `Creation_date` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `receipts`
--

INSERT INTO `receipts` (`Receipt_ID`, `Donor_ID`, `Amount`, `Donation_date`, `Category_ID`, `Payment_type`, `Reference_no`, `Creation_date`) VALUES
(1, 1, 1500.00, '2025-10-01', 1, 'cash', 'REF001', '2025-10-10 10:03:51'),
(2, 2, 3000.00, '2025-10-02', 2, 'gpay', 'G12345', '2025-10-10 10:02:38'),
(3, 3, 2000.00, '2025-10-03', 1, 'cheque', 'CHQ789', '2025-10-10 10:02:38'),
(4, 4, 5000.00, '2025-10-04', 3, 'cash', 'REF002', '2025-10-10 10:02:38'),
(5, 2, 1000.00, '2025-10-05', 2, 'gpay', 'G67890', '2025-10-10 10:02:38');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `donation_category`
--
ALTER TABLE `donation_category`
  ADD PRIMARY KEY (`Category_ID`);

--
-- Indexes for table `donor_details`
--
ALTER TABLE `donor_details`
  ADD PRIMARY KEY (`Donor_ID`);

--
-- Indexes for table `receipts`
--
ALTER TABLE `receipts`
  ADD PRIMARY KEY (`Receipt_ID`),
  ADD KEY `Donor_ID` (`Donor_ID`),
  ADD KEY `Category_ID` (`Category_ID`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `donation_category`
--
ALTER TABLE `donation_category`
  MODIFY `Category_ID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT for table `donor_details`
--
ALTER TABLE `donor_details`
  MODIFY `Donor_ID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- AUTO_INCREMENT for table `receipts`
--
ALTER TABLE `receipts`
  MODIFY `Receipt_ID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `receipts`
--
ALTER TABLE `receipts`
  ADD CONSTRAINT `receipts_ibfk_1` FOREIGN KEY (`Donor_ID`) REFERENCES `donor_details` (`Donor_ID`),
  ADD CONSTRAINT `receipts_ibfk_2` FOREIGN KEY (`Category_ID`) REFERENCES `donation_category` (`Category_ID`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
