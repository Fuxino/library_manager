-- MariaDB dump 10.17  Distrib 10.4.8-MariaDB, for Linux (x86_64)
--
-- Host: raspi    Database: Library
-- ------------------------------------------------------
-- Server version	10.4.7-MariaDB-log

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Position to start replication or point-in-time recovery from
--

-- CHANGE MASTER TO MASTER_LOG_FILE='raspi-bin.000010', MASTER_LOG_POS=6857;

--
-- GTID to start replication from
--

-- SET GLOBAL gtid_slave_pos='0-1-284';

--
-- Current Database: `Library`
--

CREATE DATABASE /*!32312 IF NOT EXISTS*/ `Library` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci */;

USE `Library`;

--
-- Table structure for table `Authors`
--

DROP TABLE IF EXISTS `Authors`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Authors` (
  `Id` int(11) NOT NULL AUTO_INCREMENT,
  `Name` varchar(64) COLLATE utf8mb4_unicode_ci NOT NULL,
  `Gender` varchar(2) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `Nationality` varchar(64) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `BirthYear` int(11) DEFAULT NULL,
  `DeathYear` int(11) DEFAULT NULL,
  PRIMARY KEY (`Id`),
  UNIQUE KEY `Name` (`Name`)
) ENGINE=InnoDB AUTO_INCREMENT=311 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `Books`
--

DROP TABLE IF EXISTS `Books`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Books` (
  `Id` int(11) NOT NULL AUTO_INCREMENT,
  `ISBN` varchar(13) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `Title` varchar(256) COLLATE utf8mb4_unicode_ci NOT NULL,
  `Author` int(11) NOT NULL,
  `OtherAuthors` text COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `Publisher` int(11) DEFAULT NULL,
  `Series` int(11) DEFAULT NULL,
  `Language` varchar(64) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `Year` int(11) DEFAULT NULL,
  `Pages` int(11) DEFAULT NULL,
  `Category` varchar(64) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `Owner` varchar(7) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `Type` varchar(7) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  PRIMARY KEY (`Id`),
  UNIQUE KEY `ISBN` (`ISBN`),
  KEY `Author` (`Author`),
  KEY `Publisher` (`Publisher`),
  KEY `Series` (`Series`),
  CONSTRAINT `Books_ibfk_1` FOREIGN KEY (`Author`) REFERENCES `Authors` (`Id`) ON UPDATE CASCADE,
  CONSTRAINT `Books_ibfk_2` FOREIGN KEY (`Publisher`) REFERENCES `Publishers` (`Id`) ON UPDATE CASCADE,
  CONSTRAINT `Books_ibfk_3` FOREIGN KEY (`Series`) REFERENCES `Series` (`Id`) ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=576 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `Publishers`
--

DROP TABLE IF EXISTS `Publishers`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Publishers` (
  `Id` int(11) NOT NULL AUTO_INCREMENT,
  `Name` varchar(64) COLLATE utf8mb4_unicode_ci NOT NULL,
  PRIMARY KEY (`Id`),
  UNIQUE KEY `Name` (`Name`)
) ENGINE=InnoDB AUTO_INCREMENT=189 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `Series`
--

DROP TABLE IF EXISTS `Series`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Series` (
  `Id` int(11) NOT NULL AUTO_INCREMENT,
  `Name` varchar(64) COLLATE utf8mb4_unicode_ci NOT NULL,
  `Author` int(11) DEFAULT NULL,
  PRIMARY KEY (`Id`),
  UNIQUE KEY `Name` (`Name`,`Author`),
  KEY `Author` (`Author`),
  CONSTRAINT `Series_ibfk_1` FOREIGN KEY (`Author`) REFERENCES `Authors` (`Id`) ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=72 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2019-09-21  7:54:49
