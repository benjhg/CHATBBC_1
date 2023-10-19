-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema global_chat
-- -----------------------------------------------------
DROP SCHEMA IF EXISTS `global_chat` ;

-- -----------------------------------------------------
-- Schema global_chat
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `global_chat` ;
USE `global_chat` ;

-- -----------------------------------------------------
-- Table `global_chat`.`users`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `global_chat`.`users` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `username` VARCHAR(255) NOT NULL,
  `email` VARCHAR(255) NOT NULL,
  `password` VARCHAR(255) NOT NULL,
  `alias` VARCHAR(255) NOT NULL,
  `created_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE INDEX (`email` ASC) VISIBLE);


-- -----------------------------------------------------
-- Table `global_chat`.`games`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `global_chat`.`games` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `title` VARCHAR(255) NOT NULL,
  `genre` VARCHAR(255) NULL DEFAULT NULL,
  `created_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`));


-- -----------------------------------------------------
-- Table `global_chat`.`messages`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `global_chat`.`messages` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `content` TEXT NOT NULL,
  `user_id` INT NULL DEFAULT NULL,
  `sent_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  INDEX (`user_id` ASC) VISIBLE,
  CONSTRAINT ``
    FOREIGN KEY (`user_id`)
    REFERENCES `global_chat`.`users` (`id`));


-- -----------------------------------------------------
-- Table `global_chat`.`user_games`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `global_chat`.`user_games` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `users_id` INT NOT NULL,
  `games_id` INT NOT NULL,
  PRIMARY KEY (`id`),
  INDEX `fk_user_games_users1_idx` (`users_id` ASC) VISIBLE,
  INDEX `fk_user_games_games1_idx` (`games_id` ASC) VISIBLE,
  CONSTRAINT `fk_user_games_users1`
    FOREIGN KEY (`users_id`)
    REFERENCES `global_chat`.`users` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_user_games_games1`
    FOREIGN KEY (`games_id`)
    REFERENCES `global_chat`.`games` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION);


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;