-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema recognize_service
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Schema recognize_service
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `recognize_service` DEFAULT CHARACTER SET utf8 ;
USE `recognize_service` ;

-- -----------------------------------------------------
-- Table `recognize_service`.`user`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `recognize_service`.`user` (
  `id` INT(11) NOT NULL AUTO_INCREMENT,
  `username` VARCHAR(45) NOT NULL,
  `password` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`id`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8;


-- -----------------------------------------------------
-- Table `recognize_service`.`home`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `recognize_service`.`home` (
  `id` INT NOT NULL,
  `home_name` VARCHAR(45) NULL,
  `user_id` INT(11) NOT NULL,
  PRIMARY KEY (`id`),
  INDEX `fk_home_user1_idx` (`user_id` ASC),
  CONSTRAINT `fk_home_user1`
    FOREIGN KEY (`user_id`)
    REFERENCES `recognize_service`.`user` (`id`)
    ON DELETE CASCADE
    ON UPDATE CASCADE)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `recognize_service`.`room`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `recognize_service`.`room` (
  `id` INT NOT NULL,
  `room_name` VARCHAR(45) NULL,
  `home_id` INT NOT NULL,
  PRIMARY KEY (`id`),
  INDEX `fk_room_home1_idx` (`home_id` ASC),
  CONSTRAINT `fk_room_home1`
    FOREIGN KEY (`home_id`)
    REFERENCES `recognize_service`.`home` (`id`)
    ON DELETE CASCADE
    ON UPDATE CASCADE)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `recognize_service`.`device`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `recognize_service`.`device` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `device_id` VARCHAR(45) NOT NULL,
  `device_type` VARCHAR(45) NOT NULL,
  `name` VARCHAR(45) NOT NULL DEFAULT 'No Device',
  `device_name` VARCHAR(45) NOT NULL,
  `operation_status` TINYINT NOT NULL DEFAULT 0,
  `start_at` TIME NOT NULL,
  `room_id` INT NULL,
  PRIMARY KEY (`id`),
  INDEX `fk_device_room1_idx` (`room_id` ASC),
  CONSTRAINT `fk_device_room1`
    FOREIGN KEY (`room_id`)
    REFERENCES `recognize_service`.`room` (`id`)
    ON DELETE SET NULL
    ON UPDATE CASCADE)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `recognize_service`.`history_deivice`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `recognize_service`.`history_deivice` (
  `id` INT NOT NULL,
  `name` VARCHAR(45) NOT NULL,
  `start_at` TIME NOT NULL,
  `end_at` TIME NOT NULL,
  `device_id` INT NOT NULL,
  PRIMARY KEY (`id`),
  INDEX `fk_characteristic_device1_idx` (`device_id` ASC),
  CONSTRAINT `fk_characteristic_device1`
    FOREIGN KEY (`device_id`)
    REFERENCES `recognize_service`.`device` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `recognize_service`.`data`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `recognize_service`.`data` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `at` TIME NOT NULL,
  `device_id` INT NOT NULL,
  PRIMARY KEY (`id`),
  INDEX `fk_data_device1_idx` (`device_id` ASC),
  CONSTRAINT `fk_data_device1`
    FOREIGN KEY (`device_id`)
    REFERENCES `recognize_service`.`device` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
