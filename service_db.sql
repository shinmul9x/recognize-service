-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='TRADITIONAL,ALLOW_INVALID_DATES';

-- -----------------------------------------------------
-- Schema recognize_service
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Schema recognize_service
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `recognize_service` DEFAULT CHARACTER SET utf8 ;
USE `recognize_service` ;

-- -----------------------------------------------------
-- Table `recognize_service`.`token_list`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `recognize_service`.`token_list` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `token` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `recognize_service`.`device_name`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `recognize_service`.`device_name` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(45) NOT NULL,
  `token_id` INT NULL,
  `device_id` INT NULL,
  `authenticity` TINYINT(1) NULL,
  PRIMARY KEY (`id`),
  INDEX `fk_device_name_token_list_idx` (`token_id` ASC),
  CONSTRAINT `fk_device_name_token_list`
    FOREIGN KEY (`token_id`)
    REFERENCES `recognize_service`.`token_list` (`id`)
    ON DELETE SET NULL
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `recognize_service`.`data`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `recognize_service`.`data` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `amplitude` FLOAT NOT NULL,
  `frequency` INT NULL,
  `device_name_id` INT NOT NULL,
  PRIMARY KEY (`id`),
  INDEX `fk_table1_device_name1_idx` (`device_name_id` ASC),
  CONSTRAINT `fk_table1_device_name1`
    FOREIGN KEY (`device_name_id`)
    REFERENCES `recognize_service`.`device_name` (`id`)
    ON DELETE CASCADE
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
