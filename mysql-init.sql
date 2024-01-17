-- MariaDB dump 10.19-11.2.2-MariaDB, for Linux (x86_64)
--
-- Host: localhost    Database: tifddb
-- ------------------------------------------------------
-- Server version	11.2.2-MariaDB-log

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

DROP TABLE IF EXISTS `camp_camper`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `camp_camper` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp(),
  `updated_at` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  `adult_or_child` varchar(255) CHARACTER SET utf8mb3 COLLATE utf8mb3_unicode_ci DEFAULT NULL,
  `first_name` varchar(255) CHARACTER SET utf8mb3 COLLATE utf8mb3_unicode_ci DEFAULT NULL,
  `last_name` varchar(255) CHARACTER SET utf8mb3 COLLATE utf8mb3_unicode_ci DEFAULT NULL,
  `email` varchar(255) CHARACTER SET utf8mb3 COLLATE utf8mb3_unicode_ci DEFAULT NULL,
  `phone` varchar(255) CHARACTER SET utf8mb3 COLLATE utf8mb3_unicode_ci DEFAULT NULL,
  `gender` varchar(255) CHARACTER SET utf8mb3 COLLATE utf8mb3_unicode_ci DEFAULT NULL,
  `age` int(11) DEFAULT NULL,
  `band` tinyint(1) NOT NULL DEFAULT 0,
  `instruments` varchar(255) CHARACTER SET utf8mb3 COLLATE utf8mb3_unicode_ci DEFAULT NULL,
  `share_housing` varchar(255) CHARACTER SET utf8mb3 COLLATE utf8mb3_unicode_ci DEFAULT NULL,
  `family_program` tinyint(1) NOT NULL DEFAULT 0,
  `certification` tinyint(1) NOT NULL DEFAULT 0,
  `certification_details` varchar(255) CHARACTER SET utf8mb3 COLLATE utf8mb3_unicode_ci DEFAULT NULL,
  `dvd` tinyint(1) NOT NULL DEFAULT 0,
  `housing_type_id` int(11) DEFAULT NULL,
  `registration_type_id` int(11) NOT NULL,
  `registration_id` int(11) DEFAULT NULL,
  `publish` tinyint(1) NOT NULL DEFAULT 0,
  `mobility` tinyint(1) NOT NULL DEFAULT 0,
  `mobility_details` varchar(255) CHARACTER SET utf8mb3 COLLATE utf8mb3_unicode_ci DEFAULT NULL,
  `diet` tinyint(1) NOT NULL DEFAULT 0,
  `diet_details` text CHARACTER SET utf8mb3 COLLATE utf8mb3_unicode_ci DEFAULT NULL,
  `medical_details` varchar(255) CHARACTER SET utf8mb3 COLLATE utf8mb3_unicode_ci DEFAULT NULL,
  `medical` tinyint(1) NOT NULL DEFAULT 0,
  `t_shirt_type_id` int(11) DEFAULT NULL,
  `free_t_shirt` tinyint(1) NOT NULL DEFAULT 0,
  `staff` tinyint(1) NOT NULL DEFAULT 0,
  `staff_position` varchar(255) CHARACTER SET utf8mb3 COLLATE utf8mb3_unicode_ci DEFAULT NULL,
  `housing_assigned` varchar(255) CHARACTER SET utf8mb3 COLLATE utf8mb3_unicode_ci DEFAULT NULL,
  `membership_years` int(11) DEFAULT NULL,
  `join_tifd` tinyint(1) NOT NULL DEFAULT 0,
  `custom_registration_price` decimal(7,2) DEFAULT NULL,
  `membership_valid_from` date DEFAULT NULL,
  `membership_valid_to` date DEFAULT NULL,
  `custom_registration_discount` decimal(7,2) DEFAULT NULL,
  `need_linen` tinyint(1) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `registration_housing_id_dc84c1e0` (`housing_type_id`),
  KEY `registration_registration_type_id_86799b59` (`registration_type_id`)
) ENGINE=InnoDB AUTO_INCREMENT=10879 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;


--
-- Table structure for table `camp_constants`
--

DROP TABLE IF EXISTS `camp_constants`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `camp_constants` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp(),
  `updated_at` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  `year` int(11) NOT NULL,
  `form_open` date DEFAULT NULL,
  `form_close` date DEFAULT NULL,
  `form_late` date DEFAULT NULL,
  `camp_start` date DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `camp_dates`
--

DROP TABLE IF EXISTS `camp_dates`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `camp_dates` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `description` varchar(255) CHARACTER SET utf8mb3 COLLATE utf8mb3_unicode_ci DEFAULT NULL,
  `date` date DEFAULT NULL,
  `slug` varchar(255) CHARACTER SET utf8mb3 COLLATE utf8mb3_unicode_ci DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `camp_housing_types`
--

DROP TABLE IF EXISTS `camp_housing_types`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `camp_housing_types` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `description` varchar(255) CHARACTER SET utf8mb3 COLLATE utf8mb3_unicode_ci NOT NULL,
  `price` decimal(7,2) NOT NULL,
  `slug` varchar(255) CHARACTER SET utf8mb3 COLLATE utf8mb3_unicode_ci DEFAULT NULL,
  `display_order` int(11) NOT NULL,
  `cart_description` varchar(255) CHARACTER SET utf8mb3 COLLATE utf8mb3_unicode_ci NOT NULL,
  `short_description` varchar(20) CHARACTER SET utf8mb3 COLLATE utf8mb3_unicode_ci DEFAULT NULL,
  `active` tinyint(4) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=24 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;


--
-- Table structure for table `camp_membershipregistrationtypes`
--

DROP TABLE IF EXISTS `camp_membershipregistrationtypes`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `camp_membershipregistrationtypes` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `description` varchar(255) NOT NULL,
  `price` decimal(7,2) NOT NULL,
  `slug` varchar(255) DEFAULT NULL,
  `display_order` int(11) NOT NULL,
  `cart_description` varchar(255) NOT NULL,
  `adult_or_child` varchar(255) DEFAULT NULL,
  `active` tinyint(4) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `idx_display` (`display_order`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `camp_prices`
--

DROP TABLE IF EXISTS `camp_prices`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `camp_prices` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `description` varchar(255) CHARACTER SET utf8mb3 COLLATE utf8mb3_unicode_ci NOT NULL,
  `price` decimal(7,2) NOT NULL,
  `slug` varchar(255) CHARACTER SET utf8mb3 COLLATE utf8mb3_unicode_ci DEFAULT NULL,
  `display_order` int(11) NOT NULL,
  `cart_description` varchar(255) CHARACTER SET utf8mb3 COLLATE utf8mb3_unicode_ci NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=30 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `camp_rebates`
--

DROP TABLE IF EXISTS `camp_rebates`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `camp_rebates` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `description` varchar(255) CHARACTER SET utf8mb3 COLLATE utf8mb3_unicode_ci NOT NULL,
  `price` decimal(7,2) NOT NULL,
  `slug` varchar(255) CHARACTER SET utf8mb3 COLLATE utf8mb3_unicode_ci DEFAULT NULL,
  `display_order` int(11) NOT NULL,
  `cart_description` varchar(255) CHARACTER SET utf8mb3 COLLATE utf8mb3_unicode_ci NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=37 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `camp_registrar_info`
--

DROP TABLE IF EXISTS `camp_registrar_info`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `camp_registrar_info` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `description` varchar(255) CHARACTER SET utf8mb3 COLLATE utf8mb3_unicode_ci DEFAULT NULL,
  `mailing_address` text CHARACTER SET utf8mb3 COLLATE utf8mb3_unicode_ci DEFAULT NULL,
  `name` varchar(255) CHARACTER SET utf8mb3 COLLATE utf8mb3_unicode_ci DEFAULT NULL,
  `email` varchar(255) CHARACTER SET utf8mb3 COLLATE utf8mb3_unicode_ci DEFAULT NULL,
  `active` tinyint(4) DEFAULT NULL,
  `registration_source` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `camp_registration`
--

DROP TABLE IF EXISTS `camp_registration`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `camp_registration` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `transaction_id` varchar(255) CHARACTER SET utf8mb3 COLLATE utf8mb3_unicode_ci DEFAULT NULL,
  `address1` varchar(255) CHARACTER SET utf8mb3 COLLATE utf8mb3_unicode_ci DEFAULT NULL,
  `city` varchar(255) CHARACTER SET utf8mb3 COLLATE utf8mb3_unicode_ci DEFAULT NULL,
  `state` varchar(255) CHARACTER SET utf8mb3 COLLATE utf8mb3_unicode_ci DEFAULT NULL,
  `zip` varchar(255) CHARACTER SET utf8mb3 COLLATE utf8mb3_unicode_ci DEFAULT NULL,
  `country` varchar(255) CHARACTER SET utf8mb3 COLLATE utf8mb3_unicode_ci DEFAULT NULL,
  `donation_bobbi_gillotti` decimal(10,2) DEFAULT NULL,
  `donation_floor_fund` decimal(10,2) DEFAULT NULL,
  `donation_live_music` decimal(10,2) DEFAULT NULL,
  `donation_tifd` decimal(10,2) DEFAULT NULL,
  `rebate_id` int(11) DEFAULT NULL,
  `payment` decimal(10,2) DEFAULT NULL,
  `camper_note` text CHARACTER SET utf8mb3 COLLATE utf8mb3_unicode_ci DEFAULT NULL,
  `auction_items` text CHARACTER SET utf8mb3 COLLATE utf8mb3_unicode_ci DEFAULT NULL,
  `session` text CHARACTER SET utf8mb3 COLLATE utf8mb3_unicode_ci DEFAULT NULL,
  `payment_type` varchar(255) CHARACTER SET utf8mb3 COLLATE utf8mb3_unicode_ci DEFAULT NULL,
  `agreecheckbox` tinyint(1) DEFAULT NULL,
  `registrar_approval_note` text CHARACTER SET utf8mb3 COLLATE utf8mb3_unicode_ci DEFAULT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp(),
  `updated_at` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  `address2` varchar(255) CHARACTER SET utf8mb3 COLLATE utf8mb3_unicode_ci DEFAULT NULL,
  `cart_total` decimal(10,2) DEFAULT NULL,
  `paypal_fee` decimal(10,2) DEFAULT NULL,
  `paypal_gross` decimal(10,2) DEFAULT NULL,
  `registration_status_id` int(11) DEFAULT NULL,
  `year` int(11) DEFAULT NULL,
  `membership_fee_gross` decimal(10,2) DEFAULT NULL,
  `late_fee` decimal(10,2) DEFAULT NULL,
  `adjustment` decimal(10,2) DEFAULT NULL,
  `email_confirmation_sent` tinyint(4) DEFAULT NULL,
  `adjustment_note` text CHARACTER SET utf8mb3 COLLATE utf8mb3_unicode_ci DEFAULT NULL,
  `postmark` date DEFAULT NULL,
  `registration_source` int(11) NOT NULL DEFAULT 0,
  `shipping_fee` decimal(10,2) DEFAULT NULL,
  `donation_camp_fund` decimal(10,2) DEFAULT NULL,
  `donation_chuck` decimal(10,2) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=11115 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `camp_registration_status`
--

DROP TABLE IF EXISTS `camp_registration_status`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `camp_registration_status` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `status` varchar(255) CHARACTER SET utf8mb3 COLLATE utf8mb3_unicode_ci DEFAULT NULL,
  `description` text CHARACTER SET utf8mb3 COLLATE utf8mb3_unicode_ci DEFAULT NULL,
  `display_order` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=12 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `camp_registration_types`
--

DROP TABLE IF EXISTS `camp_registration_types`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `camp_registration_types` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `description` varchar(255) CHARACTER SET utf8mb3 COLLATE utf8mb3_unicode_ci NOT NULL,
  `price` decimal(7,2) NOT NULL,
  `slug` varchar(255) CHARACTER SET utf8mb3 COLLATE utf8mb3_unicode_ci DEFAULT NULL,
  `display_order` int(11) NOT NULL,
  `cart_description` varchar(255) CHARACTER SET utf8mb3 COLLATE utf8mb3_unicode_ci NOT NULL,
  `adult_or_child` varchar(255) CHARACTER SET utf8mb3 COLLATE utf8mb3_unicode_ci DEFAULT NULL,
  `active` tinyint(4) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `idx_display` (`display_order`)
) ENGINE=InnoDB AUTO_INCREMENT=116 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;


--
-- Table structure for table `camp_shirt_types`
--

DROP TABLE IF EXISTS `camp_shirt_types`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `camp_shirt_types` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `cut` varchar(255) CHARACTER SET utf8mb3 COLLATE utf8mb3_unicode_ci DEFAULT NULL,
  `size` varchar(255) CHARACTER SET utf8mb3 COLLATE utf8mb3_unicode_ci DEFAULT NULL,
  `description` varchar(255) CHARACTER SET utf8mb3 COLLATE utf8mb3_unicode_ci DEFAULT NULL,
  `cart_description` varchar(255) CHARACTER SET utf8mb3 COLLATE utf8mb3_unicode_ci DEFAULT NULL,
  `display_order` int(11) DEFAULT NULL,
  `price` decimal(10,2) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=53 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `camp_templates`
--

DROP TABLE IF EXISTS `camp_templates`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `camp_templates` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `updated_at` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  `created_at` timestamp NOT NULL DEFAULT current_timestamp(),
  `template_text` text CHARACTER SET utf8mb3 COLLATE utf8mb3_unicode_ci DEFAULT NULL,
  `slug` varchar(255) CHARACTER SET utf8mb3 COLLATE utf8mb3_unicode_ci DEFAULT NULL,
  `description` varchar(255) CHARACTER SET utf8mb3 COLLATE utf8mb3_unicode_ci DEFAULT NULL,
  `display_order` int(11) DEFAULT NULL,
  `subject` varchar(255) CHARACTER SET utf8mb3 COLLATE utf8mb3_unicode_ci DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `slug` (`slug`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `membership_payments`
--

DROP TABLE IF EXISTS `membership_payments`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `membership_payments` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `registration_id` int(11) DEFAULT NULL,
  `date_recd` datetime NOT NULL DEFAULT current_timestamp(),
  `cash` tinyint(4) DEFAULT NULL,
  `check_num` varchar(25) CHARACTER SET utf8mb3 COLLATE utf8mb3_unicode_ci DEFAULT NULL,
  `net_amt` decimal(10,2) DEFAULT NULL,
  `paypal_fee` decimal(10,2) DEFAULT NULL,
  `waiting_for_deposit` tinyint(4) DEFAULT NULL,
  `who_has_possession` varchar(255) CHARACTER SET utf8mb3 COLLATE utf8mb3_unicode_ci DEFAULT NULL,
  `deposit_date` date DEFAULT NULL,
  `notes` text CHARACTER SET utf8mb3 COLLATE utf8mb3_unicode_ci DEFAULT NULL,
  `updated_at` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  `created_at` timestamp NOT NULL DEFAULT current_timestamp(),
  `pp_ipn_name` varchar(255) CHARACTER SET utf8mb3 COLLATE utf8mb3_unicode_ci DEFAULT NULL,
  `pp_ipn_email` varchar(255) CHARACTER SET utf8mb3 COLLATE utf8mb3_unicode_ci DEFAULT NULL,
  `pp_ipn_phone` varchar(255) CHARACTER SET utf8mb3 COLLATE utf8mb3_unicode_ci DEFAULT NULL,
  `payment_type` int(11) DEFAULT NULL,
  `membership_fee` decimal(10,2) DEFAULT NULL,
  `years_paid` int(11) DEFAULT NULL,
  `bobbi_fund` decimal(10,2) DEFAULT NULL,
  `floor_fund` decimal(10,2) DEFAULT NULL,
  `music_fund` decimal(10,2) DEFAULT NULL,
  `general_fund` decimal(10,2) DEFAULT NULL,
  `camp_fee` decimal(10,2) DEFAULT NULL,
  `t_shirt_fee` decimal(10,2) DEFAULT NULL,
  `dvd_fee` decimal(10,2) DEFAULT NULL,
  `membership_person_id` int(11) DEFAULT NULL,
  `legacy_memid` int(11) DEFAULT NULL,
  `camp_fund` decimal(10,2) DEFAULT NULL,
  `housing_fee` decimal(10,2) DEFAULT NULL,
  `other_fee` decimal(10,2) DEFAULT NULL,
  `late_fee` decimal(10,2) DEFAULT NULL,
  `gross_amt` decimal(10,2) DEFAULT NULL,
  `refund_amt` decimal(10,2) DEFAULT NULL,
  `shipping_fee` decimal(10,2) DEFAULT NULL,
  `pp_ipn_id` int(11) DEFAULT NULL,
  `pp_ipn_txn_id` varchar(255) CHARACTER SET utf8mb3 COLLATE utf8mb3_unicode_ci DEFAULT NULL,
  `chuck_fund` decimal(10,2) DEFAULT NULL,
  `texakolo_fund` decimal(10,2) DEFAULT NULL,
  `gfc_linens` decimal(10,2) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=10602 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;


--
-- Table structure for table `membership_paymenttypes`
--

DROP TABLE IF EXISTS `membership_paymenttypes`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `membership_paymenttypes` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `paymenttype` varchar(255) CHARACTER SET utf8mb3 COLLATE utf8mb3_unicode_ci DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `membership_person`
--

DROP TABLE IF EXISTS `membership_person`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `membership_person` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `updated_at` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  `created_at` timestamp NOT NULL DEFAULT current_timestamp(),
  `membership_address_id` int(11) DEFAULT NULL,
  `first_name` varchar(255) CHARACTER SET utf8mb3 COLLATE utf8mb3_unicode_ci DEFAULT NULL,
  `last_name` varchar(255) CHARACTER SET utf8mb3 COLLATE utf8mb3_unicode_ci DEFAULT NULL,
  `email` varchar(255) CHARACTER SET utf8mb3 COLLATE utf8mb3_unicode_ci DEFAULT NULL,
  `email2` varchar(255) CHARACTER SET utf8mb3 COLLATE utf8mb3_unicode_ci DEFAULT NULL,
  `work_phone` varchar(255) CHARACTER SET utf8mb3 COLLATE utf8mb3_unicode_ci DEFAULT NULL,
  `cell_phone` varchar(255) CHARACTER SET utf8mb3 COLLATE utf8mb3_unicode_ci DEFAULT NULL,
  `home_phone` varchar(255) CHARACTER SET utf8mb3 COLLATE utf8mb3_unicode_ci DEFAULT NULL,
  `membership_valid_from` date DEFAULT NULL,
  `membership_valid_to` date DEFAULT NULL,
  `membership_type_id` int(11) DEFAULT NULL,
  `member_since` int(11) DEFAULT NULL,
  `ok_to_publish` tinyint(4) DEFAULT NULL,
  `age` int(11) DEFAULT NULL,
  `gender` varchar(100) CHARACTER SET utf8mb3 COLLATE utf8mb3_unicode_ci DEFAULT NULL,
  `dancegroups` varchar(255) CHARACTER SET utf8mb3 COLLATE utf8mb3_unicode_ci DEFAULT NULL,
  `notes` text CHARACTER SET utf8mb3 COLLATE utf8mb3_unicode_ci DEFAULT NULL,
  `flags` varchar(255) CHARACTER SET utf8mb3 COLLATE utf8mb3_unicode_ci DEFAULT NULL,
  `email_newsletter` tinyint(4) DEFAULT NULL,
  `member_year` int(11) DEFAULT NULL,
  `legacy_pubemail1` tinyint(4) DEFAULT NULL,
  `legacy_pubemail2` tinyint(4) DEFAULT NULL,
  `legacy_agecategory` varchar(255) CHARACTER SET utf8mb3 COLLATE utf8mb3_unicode_ci DEFAULT NULL,
  `last_camp` int(11) DEFAULT NULL,
  `legacy_dob` date DEFAULT NULL,
  `registration_id` int(11) DEFAULT NULL,
  `phone` varchar(255) CHARACTER SET utf8mb3 COLLATE utf8mb3_unicode_ci DEFAULT NULL,
  `registration_type_id` int(11) DEFAULT NULL,
  `membership_years` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1847 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `membership_registration_types`
--

DROP TABLE IF EXISTS `membership_registration_types`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `membership_registration_types` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `description` varchar(255) CHARACTER SET utf8mb3 COLLATE utf8mb3_unicode_ci NOT NULL,
  `price` decimal(7,2) NOT NULL,
  `slug` varchar(255) CHARACTER SET utf8mb3 COLLATE utf8mb3_unicode_ci DEFAULT NULL,
  `display_order` int(11) NOT NULL,
  `cart_description` varchar(255) CHARACTER SET utf8mb3 COLLATE utf8mb3_unicode_ci NOT NULL,
  `adult_or_child` varchar(255) CHARACTER SET utf8mb3 COLLATE utf8mb3_unicode_ci DEFAULT NULL,
  `active` tinyint(4) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `idx_display` (`display_order`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `membership_report`
--

DROP TABLE IF EXISTS `membership_report`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `membership_report` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `title` varchar(255) CHARACTER SET utf8mb3 COLLATE utf8mb3_unicode_ci DEFAULT NULL,
  `description` text CHARACTER SET utf8mb3 COLLATE utf8mb3_unicode_ci DEFAULT NULL,
  `timestamp` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  `slug` varchar(255) CHARACTER SET utf8mb3 COLLATE utf8mb3_unicode_ci DEFAULT NULL,
  `display_order` int(11) DEFAULT NULL,
  `category` varchar(255) CHARACTER SET utf8mb3 COLLATE utf8mb3_unicode_ci DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=18 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;


--
-- Table structure for table `membership_type`
--

DROP TABLE IF EXISTS `membership_type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `membership_type` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `membertype` varchar(255) CHARACTER SET utf8mb3 COLLATE utf8mb3_unicode_ci DEFAULT NULL,
  `display_order` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=13 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

/*!40101 SET character_set_client = @saved_cs_client */;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2024-01-16 21:07:57
-- MariaDB dump 10.19-11.2.2-MariaDB, for Linux (x86_64)
--
-- Host: localhost    Database: tifddb
-- ------------------------------------------------------
-- Server version	11.2.2-MariaDB-log

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `camp_constants`
--

DROP TABLE IF EXISTS `camp_constants`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `camp_constants` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp(),
  `updated_at` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  `year` int(11) NOT NULL,
  `form_open` date DEFAULT NULL,
  `form_close` date DEFAULT NULL,
  `form_late` date DEFAULT NULL,
  `camp_start` date DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `camp_constants`
--

LOCK TABLES `camp_constants` WRITE;
/*!40000 ALTER TABLE `camp_constants` DISABLE KEYS */;
INSERT INTO `camp_constants` VALUES
(1,'2023-08-30 19:32:27','2023-08-30 19:32:27',2022,'2022-09-03','2022-11-14','2022-11-30','2022-11-24');
/*!40000 ALTER TABLE `camp_constants` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2024-01-16 21:27:09
-- MariaDB dump 10.19-11.2.2-MariaDB, for Linux (x86_64)
--
-- Host: localhost    Database: tifddb
-- ------------------------------------------------------
-- Server version	11.2.2-MariaDB-log

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `camp_dates`
--

DROP TABLE IF EXISTS `camp_dates`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `camp_dates` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `description` varchar(255) CHARACTER SET utf8mb3 COLLATE utf8mb3_unicode_ci DEFAULT NULL,
  `date` date DEFAULT NULL,
  `slug` varchar(255) CHARACTER SET utf8mb3 COLLATE utf8mb3_unicode_ci DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `camp_dates`
--

LOCK TABLES `camp_dates` WRITE;
/*!40000 ALTER TABLE `camp_dates` DISABLE KEYS */;
INSERT INTO `camp_dates` VALUES
(1,'Camp Start','2023-11-23','camp_start'),
(2,'Registration Opens','2024-01-13','form_open'),
(3,'Late fee after this date','2023-11-01','late_date'),
(4,'Last day to register','2024-12-14','form_close');
/*!40000 ALTER TABLE `camp_dates` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2024-01-16 21:27:09
-- MariaDB dump 10.19-11.2.2-MariaDB, for Linux (x86_64)
--
-- Host: localhost    Database: tifddb
-- ------------------------------------------------------
-- Server version	11.2.2-MariaDB-log

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `camp_housing_types`
--

DROP TABLE IF EXISTS `camp_housing_types`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `camp_housing_types` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `description` varchar(255) CHARACTER SET utf8mb3 COLLATE utf8mb3_unicode_ci NOT NULL,
  `price` decimal(7,2) NOT NULL,
  `slug` varchar(255) CHARACTER SET utf8mb3 COLLATE utf8mb3_unicode_ci DEFAULT NULL,
  `display_order` int(11) NOT NULL,
  `cart_description` varchar(255) CHARACTER SET utf8mb3 COLLATE utf8mb3_unicode_ci NOT NULL,
  `short_description` varchar(20) CHARACTER SET utf8mb3 COLLATE utf8mb3_unicode_ci DEFAULT NULL,
  `active` tinyint(4) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=24 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `camp_housing_types`
--

LOCK TABLES `camp_housing_types` WRITE;
/*!40000 ALTER TABLE `camp_housing_types` DISABLE KEYS */;
INSERT INTO `camp_housing_types` VALUES
(13,'Stay with another adult in a private room (private bath) - double occupancy - registering as #2 of two adults sharing room',0.00,'housing',500,'Stay with another adult in a private room (private bath) - double occupancy - registering as #2 of two adults sharing room','with other adult',1),
(14,'Stay in a cabin shared w/ other women (shared bath)',0.00,'housing',20,'Stay in a cabin shared w/ other women (shared bath)','women dorm',1),
(15,'Stay in a cabin shared w/ other men (shared bath)',0.00,'housing',30,'Stay in a cabin shared w/ other men (shared bath)','men dorm',1),
(16,'Stay in a cabin shared w/ other couples (shared bath)',0.00,'housing',40,'Stay in a cabin shared w/ other couples (shared bath)','couple dorm',1),
(17,'Stay in a cabin shared w/ other family(ies) (shared bath)',0.00,'housing',50,'Stay in a cabin shared w/ other family(ies) (shared bath)','fam dorm',1),
(18,'Free Private Cabin for Qualified Families *',0.00,'housing',60,'Free Private Cabin for Qualified Families *','free fam cabin',0),
(19,'Stay with another adult in a private room (private bath) - double occupancy - registering as #2 of two adults sharing room',0.00,'housing',400,'Stay with another adult in a private room (private bath) - double occupancy - registering as #2 of two adults sharing room','with sep reg adult',0),
(20,'Private Cabin (Shared Bath)',100.00,'housing',80,'Private Cabin (Shared Bath)','prvt cabin',0),
(21,'Stay alone in a private room (private bath) - single occupancy - one adult',100.00,'housing',90,'Stay alone in a private room (private bath) - single occupancy - one adult','prv room single',1),
(22,'Stay with another adult in a private room (private bath) - double occupancy - registering as #1 of two adults sharing room',100.00,'housing',100,'Stay with another adult in a private room (private bath) - double occupancy - registering as #1 of two adults sharing room','prv room dbl',1),
(23,'Stay in a private room (private bath) - double occupancy - list here #2 of two adults sharing room',0.00,'housing',101,'Stay in a private room (private bath) - double occupancy - list here #2 of two adults sharing room','prv room dbl2',0);
/*!40000 ALTER TABLE `camp_housing_types` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2024-01-16 21:27:09
-- MariaDB dump 10.19-11.2.2-MariaDB, for Linux (x86_64)
--
-- Host: localhost    Database: tifddb
-- ------------------------------------------------------
-- Server version	11.2.2-MariaDB-log

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `camp_prices`
--

DROP TABLE IF EXISTS `camp_prices`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `camp_prices` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `description` varchar(255) CHARACTER SET utf8mb3 COLLATE utf8mb3_unicode_ci NOT NULL,
  `price` decimal(7,2) NOT NULL,
  `slug` varchar(255) CHARACTER SET utf8mb3 COLLATE utf8mb3_unicode_ci DEFAULT NULL,
  `display_order` int(11) NOT NULL,
  `cart_description` varchar(255) CHARACTER SET utf8mb3 COLLATE utf8mb3_unicode_ci NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=30 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `camp_prices`
--

LOCK TABLES `camp_prices` WRITE;
/*!40000 ALTER TABLE `camp_prices` DISABLE KEYS */;
INSERT INTO `camp_prices` VALUES
(1,'T-Shirt',22.00,'shirt',10,'T-Shirt'),
(2,'DVD',21.00,'dvd',10,'Dance review video'),
(3,'TIFD membership - 1 year',15.00,'membership',10,'TIFD membership - 1 year'),
(27,'Late fee',25.00,'late_fee',50,'Late fee'),
(28,'Shipping',4.25,'shipping',100,'Shipping'),
(29,'Linens',15.00,'linen',120,'Linens from GFC');
/*!40000 ALTER TABLE `camp_prices` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2024-01-16 21:27:09
-- MariaDB dump 10.19-11.2.2-MariaDB, for Linux (x86_64)
--
-- Host: localhost    Database: tifddb
-- ------------------------------------------------------
-- Server version	11.2.2-MariaDB-log

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `camp_rebates`
--

DROP TABLE IF EXISTS `camp_rebates`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `camp_rebates` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `description` varchar(255) CHARACTER SET utf8mb3 COLLATE utf8mb3_unicode_ci NOT NULL,
  `price` decimal(7,2) NOT NULL,
  `slug` varchar(255) CHARACTER SET utf8mb3 COLLATE utf8mb3_unicode_ci DEFAULT NULL,
  `display_order` int(11) NOT NULL,
  `cart_description` varchar(255) CHARACTER SET utf8mb3 COLLATE utf8mb3_unicode_ci NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=37 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `camp_rebates`
--

LOCK TABLES `camp_rebates` WRITE;
/*!40000 ALTER TABLE `camp_rebates` DISABLE KEYS */;
INSERT INTO `camp_rebates` VALUES
(23,'Life membership 1 adult',-15.00,'rebate',10,'TIFD lifetime membership rebate - 1 adult'),
(24,'Life membership 2 adults',-30.00,'rebate',20,'TIFD lifetime membership rebate - 2 adults'),
(25,'Life membership 3 adults',-45.00,'rebate',30,'TIFD lifetime membership rebate - 3 adults'),
(26,'Life membership 4 adults',-60.00,'rebate',40,'TIFD lifetime membership rebate - 4 adults'),
(27,'No rebate',0.00,'no_rebate',0,'No Rebate'),
(28,'1 adult dues prepaid',-15.00,'prepaid',50,'Individual membership - dues prepaid'),
(29,'2 adults dues prepaid',-30.00,'prepaid',60,'Individual membership - 2 adults'),
(30,'3 adults dues prepaid',-45.00,'prepaid',70,'Individual membership - 3 adults'),
(31,'4 adults dues prepaid',-60.00,'prepaid',80,'Individual membership - 4 adults'),
(32,'LEGACY family rebate',-20.00,'legacy',1000,'LEGACY family rebate'),
(33,'LEGACY family rebate',-35.00,'legacy',1000,'LEGACY family rebate'),
(34,'LEGACY family rebate',-50.00,'legacy',1000,'LEGACY family rebate'),
(35,'LEGACY family rebate',-45.00,'legacy',1000,'LEGACY family rebate'),
(36,'LEGACY family rebate',-5.00,'legacy',1000,'LEGACY family rebate');
/*!40000 ALTER TABLE `camp_rebates` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2024-01-16 21:27:09
-- MariaDB dump 10.19-11.2.2-MariaDB, for Linux (x86_64)
--
-- Host: localhost    Database: tifddb
-- ------------------------------------------------------
-- Server version	11.2.2-MariaDB-log

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `camp_registration_status`
--

DROP TABLE IF EXISTS `camp_registration_status`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `camp_registration_status` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `status` varchar(255) CHARACTER SET utf8mb3 COLLATE utf8mb3_unicode_ci DEFAULT NULL,
  `description` text CHARACTER SET utf8mb3 COLLATE utf8mb3_unicode_ci DEFAULT NULL,
  `display_order` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=12 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `camp_registration_status`
--

LOCK TABLES `camp_registration_status` WRITE;
/*!40000 ALTER TABLE `camp_registration_status` DISABLE KEYS */;
INSERT INTO `camp_registration_status` VALUES
(1,'Incomplete','User has saved the first page, not the second (no agree checkbox)',10),
(2,'NotPaid','User has saved the 2nd page (confirmed alcohol policy), not selected a payment type yet',20),
(3,'Waiting for PayPal','User pushed the PayPal button and we have not yet confirmed their paypal payment',30),
(4,'Waiting for check','User pressed the check payment button and we have not yet approved their payment',40),
(5,'Registrar Approved','Registrar confirmed payment',100),
(6,'Paypal IPN confirmed','We received a successful IPN response from PayPal',60),
(7,'Paypal IPN error','Error code when something went wrong with paypal IPN (set in camp/signals.py)',NULL),
(8,'PAID via registrar','Registrar has processed payment and the registration is paid in full',50),
(9,'Imported from old DB','',NULL),
(10,'Invalid','A generic status to put registrations that would otherwise be deleted',5),
(11,'Refunded','A refund was issued from paypal',4);
/*!40000 ALTER TABLE `camp_registration_status` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2024-01-16 21:27:09
-- MariaDB dump 10.19-11.2.2-MariaDB, for Linux (x86_64)
--
-- Host: localhost    Database: tifddb
-- ------------------------------------------------------
-- Server version	11.2.2-MariaDB-log

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `camp_registration_types`
--

DROP TABLE IF EXISTS `camp_registration_types`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `camp_registration_types` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `description` varchar(255) CHARACTER SET utf8mb3 COLLATE utf8mb3_unicode_ci NOT NULL,
  `price` decimal(7,2) NOT NULL,
  `slug` varchar(255) CHARACTER SET utf8mb3 COLLATE utf8mb3_unicode_ci DEFAULT NULL,
  `display_order` int(11) NOT NULL,
  `cart_description` varchar(255) CHARACTER SET utf8mb3 COLLATE utf8mb3_unicode_ci NOT NULL,
  `adult_or_child` varchar(255) CHARACTER SET utf8mb3 COLLATE utf8mb3_unicode_ci DEFAULT NULL,
  `active` tinyint(4) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `idx_display` (`display_order`)
) ENGINE=InnoDB AUTO_INCREMENT=116 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `camp_registration_types`
--

LOCK TABLES `camp_registration_types` WRITE;
/*!40000 ALTER TABLE `camp_registration_types` DISABLE KEYS */;
INSERT INTO `camp_registration_types` VALUES
(1,'Full-time Camper',366.00,'registration',100,'Full-time Camper','adult',1),
(5,'Part-time Camper',296.00,'registration',99,'Part-time Camper','adult',1),
(6,'Non-dancer camper',296.00,'registration',98,'Non-dancer camper','adult',1),
(7,'50% Discount (TIFD admin staff)',183.00,'registration',79,'50% Discount (TIFD admin staff)','adult',1),
(8,'25% Discount (TIFD Admin Staff)',274.50,'registration',78,'25% Discount (TIFD Admin Staff)','adult',1),
(9,'Half scholarship (Bobbi Gillotti)',183.00,'registration',90,'Half scholarship (Bobbi Gillotti)','adult',1),
(10,'Full scholarship (Bobbi Gillotti)',0.00,'registration',80,'Full scholarship (Bobbi Gillotti)','adult',1),
(11,'Child camper (age 0-16)',0.00,'registration',10,'Child camper (age 0-16)','child',1),
(12,'Child Registration (age 0-16) - Part Time',0.00,'registration',10,'Child Registration (age 0-16) - Part Time','child',0),
(106,'Donation for virtual camp 2020',100.00,'registration',50,'Donation for virtual camp 2020','adult',0),
(107,'Individual Membership',15.00,'membership',10,'Individual Membership','adult',1),
(108,'Student Membership',10.00,'membership',10,'Student Membership','adult',1),
(109,'Lifetime Membership',500.00,'membership',499,'Lifetime Membership','adult',1),
(110,'Donation for virtual camp 2020',0.00,'registration',15,'Donation for virtual camp 2020','adult',0),
(111,'Donation for virtual camp 2020',50.00,'registration',40,'Donation for virtual camp 2020','adult',0),
(112,'Donation for virtual camp 2020',20.00,'registration',30,'Donation for virtual camp 2020','adult',0),
(113,'Virtual camp only - donations accepted',0.00,'registration',14,'Virtual camp only - donations accepted','adult',0),
(115,'No membership - just take me to the donations page',0.00,'membership',0,'No membership - just take me to the donations page','adult',1);
/*!40000 ALTER TABLE `camp_registration_types` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2024-01-16 21:27:09
-- MariaDB dump 10.19-11.2.2-MariaDB, for Linux (x86_64)
--
-- Host: localhost    Database: tifddb
-- ------------------------------------------------------
-- Server version	11.2.2-MariaDB-log

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `camp_shirt_types`
--

DROP TABLE IF EXISTS `camp_shirt_types`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `camp_shirt_types` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `cut` varchar(255) CHARACTER SET utf8mb3 COLLATE utf8mb3_unicode_ci DEFAULT NULL,
  `size` varchar(255) CHARACTER SET utf8mb3 COLLATE utf8mb3_unicode_ci DEFAULT NULL,
  `description` varchar(255) CHARACTER SET utf8mb3 COLLATE utf8mb3_unicode_ci DEFAULT NULL,
  `cart_description` varchar(255) CHARACTER SET utf8mb3 COLLATE utf8mb3_unicode_ci DEFAULT NULL,
  `display_order` int(11) DEFAULT NULL,
  `price` decimal(10,2) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=53 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `camp_shirt_types`
--

LOCK TABLES `camp_shirt_types` WRITE;
/*!40000 ALTER TABLE `camp_shirt_types` DISABLE KEYS */;
INSERT INTO `camp_shirt_types` VALUES
(1,NULL,NULL,'No shirt','No shirt',0,0.00),
(41,'M','XS','male size XS','T-Shirt male size XS',10,22.00),
(42,'M','S','male size S','T-Shirt male size S',20,22.00),
(43,'M','M','male size M','T-Shirt male size M',30,22.00),
(44,'M','L','male size L','T-Shirt male size L',40,22.00),
(45,'M','XL','male size XL','T-Shirt male size XL',50,22.00),
(46,'M','XXL','male size XXL','T-Shirt male size XXL',60,22.00),
(47,'F','XS','female size XS','T-Shirt female size XS',70,22.00),
(48,'F','S','female size S','T-Shirt female size S',80,22.00),
(49,'F','M','female size M','T-Shirt female size M',90,22.00),
(50,'F','L','female size L','T-Shirt female size L',100,22.00),
(51,'F','XL','female size XL','T-Shirt female size XL',110,22.00),
(52,'F','XXL','female size XXL','T-Shirt female size XXL',120,22.00);
/*!40000 ALTER TABLE `camp_shirt_types` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2024-01-16 21:27:09
-- MariaDB dump 10.19-11.2.2-MariaDB, for Linux (x86_64)
--
-- Host: localhost    Database: tifddb
-- ------------------------------------------------------
-- Server version	11.2.2-MariaDB-log

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `camp_templates`
--

DROP TABLE IF EXISTS `camp_templates`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `camp_templates` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `updated_at` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  `created_at` timestamp NOT NULL DEFAULT current_timestamp(),
  `template_text` text CHARACTER SET utf8mb3 COLLATE utf8mb3_unicode_ci DEFAULT NULL,
  `slug` varchar(255) CHARACTER SET utf8mb3 COLLATE utf8mb3_unicode_ci DEFAULT NULL,
  `description` varchar(255) CHARACTER SET utf8mb3 COLLATE utf8mb3_unicode_ci DEFAULT NULL,
  `display_order` int(11) DEFAULT NULL,
  `subject` varchar(255) CHARACTER SET utf8mb3 COLLATE utf8mb3_unicode_ci DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `slug` (`slug`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `camp_templates`
--

LOCK TABLES `camp_templates` WRITE;
/*!40000 ALTER TABLE `camp_templates` DISABLE KEYS */;
INSERT INTO `camp_templates` VALUES
(1,'2023-09-01 14:47:26','0000-00-00 00:00:00','<p>Your Texas Camp {{ now.year }} registration has been <strong>confirmed</strong>.&nbsp; This means your payment has been processed and your registration is finalized.</p>\r\n\r\n<p>Details of your registration are below.&nbsp; If you have problems or any questions about registration feel free to email registrar@tifd.org.</p>\r\n\r\n<p>Regards,</p>\r\n\r\n<p>Texas Camp {{now.year}} Registrar</p>\r\n\r\n<p>&nbsp;</p>','registration_approved','Automatically sent to a camper when registration is approved by registrar',NULL,'Your Texas Camp registration for {{now.year}} has been confirmed'),
(2,'2021-10-11 02:20:19','0000-00-00 00:00:00','<p>Thank you!</p>\r\n\r\n<p>Your registration has been received but your payment has NOT yet been processed.&nbsp; You will receive another email once payment is confirmed.</p>\r\n\r\n<p>These are the registration details that we have recorded. If there are any errors please forward this e-mail along with corrections to registrar@tifd.org.</p>','registration_received','Automatically sent to a camper when registration is received but not paid',NULL,'Your preliminary Texas Camp registration details for {{now.year}}'),
(3,'2023-09-10 01:55:51','0000-00-00 00:00:00','<p>By participating in this camp, all registrants agree to follow all state and federal laws (for example, not destroying property, not serving alcohol to minors, and not participating in illegal drug activity). Registrants also agree to follow Greene Family Camp&rsquo;s rules, and the <a href=\"https://tifd.org/code-of-conduct\">TIFD Code of Conduct</a>.</p>\r\n\r\n<p>Additionally,&nbsp;all registrants agree to review and follow the <a href=\"https://tifd.org/2023-covid-protocols/\">TIFD COVID protocols on tifd.org.</a></p>','safety_agreement','Agree form box text',NULL,'agree form'),
(4,'2020-09-30 21:06:12','0000-00-00 00:00:00','<p>All camp attendees agree to follow the <a href=\"http://www.tifd.org/code-of-conduct\">TIFD Code of Conduct</a>.</p>\r\n\r\n<p>Since this is a virtual camp, please keep the following in mind:</p>\r\n\r\n<ul>\r\n	<li>Dress appropriately when appearing on camera</li>\r\n	<li>Mute yourself when not participating</li>\r\n	<li>Make sure no offensive images are visible on screen</li>\r\n	<li>Refrain from offensive or inappropriate comments, whether delivered verbally or via chat</li>\r\n	<li>Do not offer unsolicited advice to others, either during teaching or while dancing</li>\r\n	<li>Avoid sustained or repeated disruptions during a TIFD event (for example, repeatedly unmuting your audio to interrupt the teaching)</li>\r\n</ul>\r\n\r\n<p>To view the full code of Conduct and guidelines for how they apply to virtual events, <a href=\"http://www.tifd.org/code-of-conduct\">click here</a>.</p>','safety_agreement_virtual_camp','safety_agreement_virtual_camp',NULL,'safety_agreement_virtual_camp'),
(5,'2021-10-11 02:03:08','0000-00-00 00:00:00','<p>{% load mathfilters %}</p>\r\n\r\n<p>Your TIFD membership has been <strong>confirmed</strong>.&nbsp; Details of your membership including membership expiration date are below.&nbsp; If you have any problems or have any other questions about membership feel free to email registrar@tifd.org.</p>\r\n\r\n<p>Regards,</p>\r\n\r\n<p>Texas International Folk Dancers<br />\r\n&nbsp;</p>\r\n\r\n<p>&nbsp;</p>','membership_confirmed','Sent to member after filling out the membership renewal form',NULL,'Your TIFD membership has been confirmed'),
(6,'2021-10-11 02:25:04','0000-00-00 00:00:00','<p>Thank you!</p>\r\n\r\n<p>Your TIFD membership registration has been received but your payment has NOT yet been processed.&nbsp; You will receive another email once payment is confirmed.</p>\r\n\r\n<p>These are the registration details that we have recorded. If there are any errors please forward this e-mail along with corrections to registrar@tifd.org.</p>\r\n\r\n<p>Once payment is confirmed we will send a follow-up email with your membership expiration date.</p>\r\n\r\n<p>&nbsp;</p>','membership_received','Automatically sent to a member when registration is completed',NULL,'Your preliminary TIFD membership details for {{now.year}}'),
(7,'2021-10-11 02:02:48','0000-00-00 00:00:00','<p>Thank you for the generous {{ now.year }} donation!</p>\r\n\r\n<p>Texas International Folk Dancers is a non-profit, tax-exempt corporation under 501(c)(3). This means that your membership dues and donations made to TIFD are tax deductible to the extent allowed by law.&nbsp;&nbsp; The attached receipt confirms your donation.&nbsp; If you have problems opening the attachment or have any other questions feel free to email the TIFD registrar at registrar@tifd.org</p>\r\n\r\n<p>&nbsp;</p>\r\n\r\n<p>&nbsp;</p>','donation_confirmed','Donation Tex receipt',50,'Thank you from TIFD for the {{ now.year }} donation!');
/*!40000 ALTER TABLE `camp_templates` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2024-01-16 21:27:09
-- MariaDB dump 10.19-11.2.2-MariaDB, for Linux (x86_64)
--
-- Host: localhost    Database: tifddb
-- ------------------------------------------------------
-- Server version	11.2.2-MariaDB-log

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `membership_report`
--

DROP TABLE IF EXISTS `membership_report`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `membership_report` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `title` varchar(255) CHARACTER SET utf8mb3 COLLATE utf8mb3_unicode_ci DEFAULT NULL,
  `description` text CHARACTER SET utf8mb3 COLLATE utf8mb3_unicode_ci DEFAULT NULL,
  `timestamp` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  `slug` varchar(255) CHARACTER SET utf8mb3 COLLATE utf8mb3_unicode_ci DEFAULT NULL,
  `display_order` int(11) DEFAULT NULL,
  `category` varchar(255) CHARACTER SET utf8mb3 COLLATE utf8mb3_unicode_ci DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=18 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `membership_report`
--

LOCK TABLES `membership_report` WRITE;
/*!40000 ALTER TABLE `membership_report` DISABLE KEYS */;
INSERT INTO `membership_report` VALUES
(2,'List of special diets','Vegan, Vegetarian, grouped together.','2020-11-08 19:41:32','diet',9999,'camp'),
(3,'Camp Roster','List of campers\' names and addresses','2020-11-08 19:41:32','camproster',10,'camp'),
(4,'Address Labels','','2020-11-08 19:41:32','addresslabels',9999,'camp'),
(5,'List of minor children and Family Program','List of campers in the family program','2020-11-08 19:41:32','familyprogram',9999,'camp'),
(6,'Housing Report','Housing Report','2020-11-08 19:41:32','housingreport',9999,'camp'),
(7,'Musicians','List of musicians','2020-11-08 19:41:32','musicians',30,'camp'),
(8,'Name Badges','Name Badges','2020-11-08 19:41:32','namebadges',20,'camp'),
(9,'Camp staff','List of camp staff members, positions, and disconts','2020-11-08 19:41:32','campstaff',1000,'camp'),
(10,'TIFD Members in good standing','A list of TIFD members whose memberships are valid for the selected year','2020-11-08 19:41:49','members_in_good_standing',100,'membership'),
(11,'T-shirt report','','2020-11-08 19:41:32','t-shirt',50,'camp'),
(12,'DVD report','','2020-11-08 19:41:32','dvd',50,'camp'),
(13,'Camp refund report','camp refund report','2021-10-29 20:21:17','refund',0,'camp'),
(14,'TIFD memberships set to expire','TIFD memberships set to expire','2021-11-24 21:22:22','members_expiring',101,'membership'),
(15,'Member Search','Member Search','2022-09-19 20:25:13','member_search',9999,'membership'),
(16,'Donations Report','List of paypal donations not tied to a camp/membership registration','2022-11-09 23:00:33','donations_report',102,'membership'),
(17,'GFC linens report','','2023-11-03 17:28:22','linen',500,'camp');
/*!40000 ALTER TABLE `membership_report` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

INSERT INTO auth_group VALUES(1,'registrar');
INSERT INTO auth_user_groups VALUES(1,1,1);
update camp_templates set created_at=CURRENT_TIMESTAMP;

insert into camp_registrar_info (`description`,`name`,`email`,`mailing_address`,`active`,`registration_source`) VALUES ('Description: The camp registrar','First Last camp registrar', 'registrar@camp','123 main street',TRUE, 0);
insert into camp_registrar_info (`description`,`name`,`email`,`mailing_address`,`active`,`registration_source`) VALUES ('Description: The camp registrar','First Last membership registrar', 'registrar@camp','123 main street',TRUE, 1);

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2024-01-16 21:27:09

