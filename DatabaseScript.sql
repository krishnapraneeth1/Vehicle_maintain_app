-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema mydb
-- -----------------------------------------------------
-- -----------------------------------------------------
-- Schema vehicle_service_db
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Schema vehicle_service_db
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `vehicle_service_db` DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci ;
USE `vehicle_service_db` ;

-- -----------------------------------------------------
-- Table `vehicle_service_db`.`roles`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `vehicle_service_db`.`roles` (
  `roleid` INT NOT NULL AUTO_INCREMENT,
  `rolename` ENUM('user', 'mechanic', 'admin') NOT NULL,
  PRIMARY KEY (`roleid`),
  UNIQUE INDEX `rolename` (`rolename` ASC) VISIBLE)
ENGINE = InnoDB
AUTO_INCREMENT = 4
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `vehicle_service_db`.`user`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `vehicle_service_db`.`user` (
  `userid` INT NOT NULL AUTO_INCREMENT,
  `firstname` VARCHAR(100) NOT NULL,
  `lastname` VARCHAR(100) NOT NULL,
  `email` VARCHAR(255) NOT NULL,
  `password` VARCHAR(255) NOT NULL,
  `phoneno` VARCHAR(15) NULL DEFAULT NULL,
  `address1` VARCHAR(255) NULL DEFAULT NULL,
  `city` VARCHAR(100) NULL DEFAULT NULL,
  `state` VARCHAR(100) NULL DEFAULT NULL,
  `zipcode` VARCHAR(10) NULL DEFAULT NULL,
  `roleid` INT NOT NULL,
  PRIMARY KEY (`userid`),
  UNIQUE INDEX `email` (`email` ASC) VISIBLE,
  INDEX `roleid` (`roleid` ASC) VISIBLE,
  CONSTRAINT `user_ibfk_1`
    FOREIGN KEY (`roleid`)
    REFERENCES `vehicle_service_db`.`roles` (`roleid`)
    ON DELETE CASCADE
    ON UPDATE CASCADE)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `vehicle_service_db`.`services`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `vehicle_service_db`.`services` (
  `serviceid` INT NOT NULL AUTO_INCREMENT,
  `servicename` VARCHAR(255) NOT NULL,
  `typeofvehicle` VARCHAR(50) NOT NULL,
  PRIMARY KEY (`serviceid`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `vehicle_service_db`.`mechanics`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `vehicle_service_db`.`mechanics` (
  `mechid` INT NOT NULL AUTO_INCREMENT,
  `serviceid` INT NOT NULL,
  `userid` INT NOT NULL,
  `firstname` VARCHAR(100) NOT NULL,
  `lastname` VARCHAR(100) NOT NULL,
  `email` VARCHAR(255) NOT NULL,
  `password` VARCHAR(255) NOT NULL,
  `phoneno` VARCHAR(15) NULL DEFAULT NULL,
  `address1` VARCHAR(255) NULL DEFAULT NULL,
  `city` VARCHAR(100) NULL DEFAULT NULL,
  `state` VARCHAR(100) NULL DEFAULT NULL,
  `zipcode` VARCHAR(10) NULL DEFAULT NULL,
  `approval_status` ENUM('Pending', 'Approved', 'Rejected') NOT NULL DEFAULT 'Pending',
  PRIMARY KEY (`mechid`),
  UNIQUE INDEX `email` (`email` ASC) VISIBLE,
  INDEX `userid` (`userid` ASC) VISIBLE,
  INDEX `serviceid` (`serviceid` ASC) VISIBLE,
  CONSTRAINT `mechanics_ibfk_1`
    FOREIGN KEY (`userid`)
    REFERENCES `vehicle_service_db`.`user` (`userid`)
    ON DELETE CASCADE,
  CONSTRAINT `mechanics_ibfk_2`
    FOREIGN KEY (`serviceid`)
    REFERENCES `vehicle_service_db`.`services` (`serviceid`)
    ON DELETE CASCADE)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `vehicle_service_db`.`appointments`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `vehicle_service_db`.`appointments` (
  `appointmentid` INT NOT NULL AUTO_INCREMENT,
  `userid` INT NOT NULL,
  `mechid` INT NOT NULL,
  `appointmentdate` DATE NOT NULL,
  `appointmenttime` TIME NOT NULL,
  `status` ENUM('Pending', 'In Progress', 'Completed') NOT NULL,
  `typeofvehicle` VARCHAR(50) NOT NULL,
  PRIMARY KEY (`appointmentid`),
  INDEX `userid` (`userid` ASC) VISIBLE,
  INDEX `mechid` (`mechid` ASC) VISIBLE,
  CONSTRAINT `appointments_ibfk_1`
    FOREIGN KEY (`userid`)
    REFERENCES `vehicle_service_db`.`user` (`userid`)
    ON DELETE CASCADE,
  CONSTRAINT `appointments_ibfk_2`
    FOREIGN KEY (`mechid`)
    REFERENCES `vehicle_service_db`.`mechanics` (`mechid`)
    ON DELETE CASCADE)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `vehicle_service_db`.`mechanic_businesses`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `vehicle_service_db`.`mechanic_businesses` (
  `business_id` INT NOT NULL AUTO_INCREMENT,
  `mechid` INT NOT NULL,
  `business_name` VARCHAR(255) NOT NULL,
  `service_id` INT NOT NULL,
  `zip_code` VARCHAR(10) NOT NULL,
  `service_type` VARCHAR(255) NOT NULL,
  `vehicle_type` VARCHAR(255) NOT NULL,
  `approval_status` ENUM('Pending', 'Approved', 'Rejected') NULL DEFAULT 'Pending',
  PRIMARY KEY (`business_id`),
  INDEX `mechid` (`mechid` ASC) VISIBLE,
  INDEX `service_id` (`service_id` ASC) VISIBLE,
  CONSTRAINT `mechanic_businesses_ibfk_1`
    FOREIGN KEY (`mechid`)
    REFERENCES `vehicle_service_db`.`mechanics` (`mechid`)
    ON DELETE CASCADE,
  CONSTRAINT `mechanic_businesses_ibfk_2`
    FOREIGN KEY (`service_id`)
    REFERENCES `vehicle_service_db`.`services` (`serviceid`)
    ON DELETE CASCADE)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Data for table `vehicle_service_db`.`services`
-- -----------------------------------------------------
INSERT INTO `vehicle_service_db`.`services` (`serviceid`, `servicename`, `typeofvehicle`) VALUES
(1, 'Oil Change', 'Cars'),
(2, 'Tire Replacement', 'Cars'),
(3, 'Brake Service', 'Cars'),
(4, 'Engine Tune-up', 'Cars'),
(5, 'Wheel Alignment', 'Cars'),
(6, 'General Checkup', 'Cars'),
(7, 'Oil Change', 'Bikes'),
(8, 'Tire Replacement', 'Bikes'),
(9, 'Engine Service', 'Bikes'),
(10, 'Oil Change', 'Trucks'),
(11, 'Tire Replacement', 'Trucks'),
(12, 'Engine Service', 'Trucks');

SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
