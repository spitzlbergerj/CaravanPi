-- phpMyAdmin SQL Dump
-- version 5.2.1deb1
-- https://www.phpmyadmin.net/
--
-- Host: localhost:3306
-- Erstellungszeit: 14. Mrz 2024 um 17:28
-- Server-Version: 10.11.6-MariaDB-0+deb12u1
-- PHP-Version: 8.2.7

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Datenbank: `CaravanPiValues`
--

-- --------------------------------------------------------

--
-- Tabellenstruktur für Tabelle `ausrichtung`
--

CREATE TABLE `ausrichtung` (
  `sensor_id` varchar(50) NOT NULL,
  `zeitstempel` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  `aktuell_x` float NOT NULL,
  `aktuell_y` float NOT NULL,
  `aktuell_z` float NOT NULL,
  `toleranz_x` float NOT NULL,
  `toleranz_y` float NOT NULL,
  `letztes_x` float DEFAULT NULL,
  `vorletztes_x` float DEFAULT NULL,
  `differenz_hinten_links` int(11) NOT NULL,
  `differenz_hinten_rechts` int(11) NOT NULL,
  `differenz_vorne_links` int(11) NOT NULL,
  `differenz_vorne_rechts` int(11) NOT NULL,
  `differenz_zentral_links` int(11) NOT NULL,
  `differenz_zentral_rechts` int(11) NOT NULL,
  `differenz_deichsel` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Tabellenstruktur für Tabelle `batterymanagement`
--

CREATE TABLE `batterymanagement` (
  `sensor_id` varchar(20) NOT NULL,
  `zeitstempel` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  `spannung_main` float(15,3) NOT NULL,
  `spannung_zelle1` float(15,3) NOT NULL,
  `spannung_zelle2` float(15,3) NOT NULL,
  `spannung_zelle3` float(15,3) NOT NULL,
  `spannung_zelle4` float(15,3) NOT NULL,
  `kapazitaet` float(15,3) NOT NULL,
  `temperatur` float(15,3) NOT NULL,
  `ladezyklen` int(11) NOT NULL,
  `strom` float(15,3) NOT NULL,
  `status` int(11) NOT NULL,
  `status_binary` binary(16) NOT NULL,
  `status_text` varchar(150) NOT NULL,
  `SoC` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;


-- --------------------------------------------------------

--
-- Tabellenstruktur für Tabelle `gasfuellgrad`
--

CREATE TABLE `gasfuellgrad` (
  `sensor_id` varchar(20) NOT NULL,
  `zeitstempel` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  `gewicht` float(10,0) NOT NULL,
  `fuellgrad` float(10,0) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;


-- --------------------------------------------------------

--
-- Tabellenstruktur für Tabelle `gassensor`
--

CREATE TABLE `gassensor` (
  `sensor_id` varchar(20) NOT NULL,
  `zeitstempel` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  `parts_per_million` int(11) NOT NULL,
  `alarm` tinyint(1) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Tabellenstruktur für Tabelle `klimasensor`
--

CREATE TABLE `klimasensor` (
  `sensor_id` varchar(20) NOT NULL,
  `zeitstempel` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  `temperatur` float(10,2) NOT NULL,
  `luftdruck` float(10,2) NOT NULL,
  `luftfeuchtigkeit` float(10,2) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;


-- --------------------------------------------------------

--
-- Tabellenstruktur für Tabelle `raspberrypi`
--

CREATE TABLE `raspberrypi` (
  `sensor_id` varchar(20) NOT NULL,
  `zeitstempel` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  `cpu_temp` float(15,2) NOT NULL,
  `gpu_temp` float(15,2) NOT NULL,
  `cpu_usage` float(15,2) NOT NULL,
  `ram_usage` float(15,2) NOT NULL,
  `disk_usage` float(15,2) NOT NULL,
  `net_traffic` float(15,2) NOT NULL,
  `process_count` float(15,2) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Tabellenstruktur für Tabelle `spannung`
--

CREATE TABLE `spannung` (
  `sensor_id` varchar(20) NOT NULL,
  `zeitstempel` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  `spannung` float(15,3) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Tabellenstruktur für Tabelle `tankfuellgrad`
--

CREATE TABLE `tankfuellgrad` (
  `sensor_id` varchar(20) NOT NULL,
  `zeitstempel` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  `fuellgrad` float(10,0) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Tabellenstruktur für Tabelle `temperatursensor`
--

CREATE TABLE `temperatursensor` (
  `sensor_id` varchar(50) NOT NULL,
  `zeitstempel` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  `temperatur` float(10,2) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Daten für Tabelle `temperatursensor`
--


--
-- Indizes der exportierten Tabellen
--

--
-- Indizes für die Tabelle `ausrichtung`
--
ALTER TABLE `ausrichtung`
  ADD UNIQUE KEY `SensorId_Zeitstempel` (`sensor_id`,`zeitstempel`);

--
-- Indizes für die Tabelle `batterymanagement`
--
ALTER TABLE `batterymanagement`
  ADD UNIQUE KEY `SensorId_Zeitstempel` (`sensor_id`,`zeitstempel`);

--
-- Indizes für die Tabelle `gasfuellgrad`
--
ALTER TABLE `gasfuellgrad`
  ADD UNIQUE KEY `SensorId_Zeitstempel` (`sensor_id`,`zeitstempel`);

--
-- Indizes für die Tabelle `gassensor`
--
ALTER TABLE `gassensor`
  ADD UNIQUE KEY `SensorId_Zeitstempel` (`sensor_id`,`zeitstempel`);

--
-- Indizes für die Tabelle `klimasensor`
--
ALTER TABLE `klimasensor`
  ADD UNIQUE KEY `SensorId_Zeitstempel` (`sensor_id`,`zeitstempel`);

--
-- Indizes für die Tabelle `raspberrypi`
--
ALTER TABLE `raspberrypi`
  ADD UNIQUE KEY `SensorId_Zeitstempel` (`sensor_id`,`zeitstempel`);

--
-- Indizes für die Tabelle `spannung`
--
ALTER TABLE `spannung`
  ADD UNIQUE KEY `SensorId_Zeitstempel` (`sensor_id`,`zeitstempel`);

--
-- Indizes für die Tabelle `tankfuellgrad`
--
ALTER TABLE `tankfuellgrad`
  ADD UNIQUE KEY `SensorId_Zeitstempel` (`sensor_id`,`zeitstempel`);

--
-- Indizes für die Tabelle `temperatursensor`
--
ALTER TABLE `temperatursensor`
  ADD UNIQUE KEY `SensorId_Zeitstempel` (`sensor_id`,`zeitstempel`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
