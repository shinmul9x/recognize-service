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
  PRIMARY KEY (`id`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8;


-- -----------------------------------------------------
-- Table `recognize_service`.`token_list`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `recognize_service`.`token_list` (
  `token` TEXT NOT NULL,
  `user_id` INT(11) NOT NULL,
  PRIMARY KEY (`token`),
  INDEX `fk_token_list_user_idx` (`user_id` ASC) VISIBLE,
  CONSTRAINT `fk_token_list_user`
    FOREIGN KEY (`user_id`)
    REFERENCES `recognize_service`.`user` (`id`)
    ON DELETE CASCADE
    ON UPDATE CASCADE)
ENGINE = InnoDB;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
