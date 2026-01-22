-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema mydb
-- -----------------------------------------------------
-- -----------------------------------------------------
-- Schema airbnb_erd
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Schema airbnb_erd
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `airbnb_erd` DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci ;
USE `airbnb_erd` ;

-- -----------------------------------------------------
-- Table `airbnb_erd`.`attribute_category`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `airbnb_erd`.`attribute_category` (
  `attribute_category_id` INT NOT NULL AUTO_INCREMENT,
  `category_name` VARCHAR(255) NOT NULL,
  PRIMARY KEY (`attribute_category_id`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `airbnb_erd`.`attribute`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `airbnb_erd`.`attribute` (
  `attribute_id` INT NOT NULL AUTO_INCREMENT,
  `attribute_category_id` INT NOT NULL,
  `attribute_name` VARCHAR(255) NOT NULL,
  `description` TEXT NULL DEFAULT NULL,
  PRIMARY KEY (`attribute_id`),
  INDEX `attribute_category_id` (`attribute_category_id` ASC) VISIBLE,
  CONSTRAINT `attribute_ibfk_1`
    FOREIGN KEY (`attribute_category_id`)
    REFERENCES `airbnb_erd`.`attribute_category` (`attribute_category_id`)
    ON DELETE CASCADE)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `airbnb_erd`.`region`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `airbnb_erd`.`region` (
  `region_id` INT NOT NULL AUTO_INCREMENT,
  `region_name` VARCHAR(255) NOT NULL,
  PRIMARY KEY (`region_id`),
  UNIQUE INDEX `uq_region_name` (`region_name` ASC) VISIBLE)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `airbnb_erd`.`country`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `airbnb_erd`.`country` (
  `country_id` INT NOT NULL AUTO_INCREMENT,
  `region_id` INT NOT NULL,
  `country_name` VARCHAR(255) NOT NULL,
  PRIMARY KEY (`country_id`),
  UNIQUE INDEX `uq_country_name` (`country_name` ASC) VISIBLE,
  INDEX `region_id` (`region_id` ASC) VISIBLE,
  CONSTRAINT `country_ibfk_1`
    FOREIGN KEY (`region_id`)
    REFERENCES `airbnb_erd`.`region` (`region_id`)
    ON DELETE CASCADE)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `airbnb_erd`.`location`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `airbnb_erd`.`location` (
  `location_id` BIGINT NOT NULL AUTO_INCREMENT,
  `country_id` INT NOT NULL,
  `city` VARCHAR(255) NOT NULL,
  `address` VARCHAR(255) NULL DEFAULT NULL,
  `location_name` VARCHAR(255) NULL DEFAULT NULL,
  `latitude` DECIMAL(10,8) NULL DEFAULT NULL,
  `longitude` DECIMAL(11,8) NULL DEFAULT NULL,
  PRIMARY KEY (`location_id`),
  INDEX `idx_country` (`country_id` ASC) VISIBLE,
  INDEX `idx_city` (`city` ASC) VISIBLE,
  CONSTRAINT `location_ibfk_1`
    FOREIGN KEY (`country_id`)
    REFERENCES `airbnb_erd`.`country` (`country_id`)
    ON DELETE CASCADE)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `airbnb_erd`.`place_type`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `airbnb_erd`.`place_type` (
  `place_type_id` INT NOT NULL AUTO_INCREMENT,
  `type_name` VARCHAR(255) NULL DEFAULT NULL,
  PRIMARY KEY (`place_type_id`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `airbnb_erd`.`property_type`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `airbnb_erd`.`property_type` (
  `property_type_id` INT NOT NULL AUTO_INCREMENT,
  `type_name` VARCHAR(255) NULL DEFAULT NULL,
  PRIMARY KEY (`property_type_id`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `airbnb_erd`.`user_account`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `airbnb_erd`.`user_account` (
  `id` BIGINT NOT NULL AUTO_INCREMENT,
  `first_name` VARCHAR(100) NOT NULL,
  `last_name` VARCHAR(100) NOT NULL,
  `email_address` VARCHAR(255) NOT NULL,
  `password_hash` VARCHAR(255) NOT NULL,
  `phone` VARCHAR(50) NULL DEFAULT NULL,
  `created_at` DATETIME NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` DATETIME NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE INDEX `email_address` (`email_address` ASC) VISIBLE,
  INDEX `idx_email` (`email_address` ASC) VISIBLE)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `airbnb_erd`.`property`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `airbnb_erd`.`property` (
  `property_id` BIGINT NOT NULL AUTO_INCREMENT,
  `location_id` BIGINT NOT NULL,
  `place_type_id` INT NOT NULL,
  `property_type_id` INT NOT NULL,
  `host_id` BIGINT NOT NULL,
  `name` VARCHAR(255) NOT NULL,
  `description` TEXT NULL DEFAULT NULL,
  `price_per_night` DECIMAL(10,2) NOT NULL,
  `number_guests` INT NOT NULL,
  `num_beds` INT NOT NULL,
  `num_bedrooms` INT NOT NULL,
  `num_bathrooms` INT NOT NULL,
  `is_guest_favourite` TINYINT(1) NULL DEFAULT '0',
  `created_at` DATETIME NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` DATETIME NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`property_id`),
  INDEX `place_type_id` (`place_type_id` ASC) VISIBLE,
  INDEX `property_type_id` (`property_type_id` ASC) VISIBLE,
  INDEX `idx_location` (`location_id` ASC) VISIBLE,
  INDEX `idx_host` (`host_id` ASC) VISIBLE,
  INDEX `idx_price` (`price_per_night` ASC) VISIBLE,
  CONSTRAINT `property_ibfk_1`
    FOREIGN KEY (`location_id`)
    REFERENCES `airbnb_erd`.`location` (`location_id`)
    ON DELETE CASCADE,
  CONSTRAINT `property_ibfk_2`
    FOREIGN KEY (`place_type_id`)
    REFERENCES `airbnb_erd`.`place_type` (`place_type_id`),
  CONSTRAINT `property_ibfk_3`
    FOREIGN KEY (`property_type_id`)
    REFERENCES `airbnb_erd`.`property_type` (`property_type_id`),
  CONSTRAINT `property_ibfk_4`
    FOREIGN KEY (`host_id`)
    REFERENCES `airbnb_erd`.`user_account` (`id`)
    ON DELETE CASCADE)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `airbnb_erd`.`bookings`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `airbnb_erd`.`bookings` (
  `booking_id` BIGINT NOT NULL AUTO_INCREMENT,
  `property_id` BIGINT NOT NULL,
  `user_id` BIGINT NOT NULL,
  `start_date` DATE NOT NULL,
  `end_date` DATE NOT NULL,
  `total_price` DECIMAL(10,2) NOT NULL,
  `status` ENUM('pending', 'confirmed', 'cancelled') NULL DEFAULT 'pending',
  `created_at` DATETIME NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`booking_id`),
  INDEX `idx_property` (`property_id` ASC) VISIBLE,
  INDEX `idx_user` (`user_id` ASC) VISIBLE,
  INDEX `idx_dates` (`start_date` ASC, `end_date` ASC) VISIBLE,
  CONSTRAINT `bookings_ibfk_1`
    FOREIGN KEY (`property_id`)
    REFERENCES `airbnb_erd`.`property` (`property_id`)
    ON DELETE CASCADE,
  CONSTRAINT `bookings_ibfk_2`
    FOREIGN KEY (`user_id`)
    REFERENCES `airbnb_erd`.`user_account` (`id`)
    ON DELETE CASCADE)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `airbnb_erd`.`guest_type`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `airbnb_erd`.`guest_type` (
  `guest_type_id` INT NOT NULL AUTO_INCREMENT,
  `type_name` VARCHAR(255) NOT NULL,
  PRIMARY KEY (`guest_type_id`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `airbnb_erd`.`booking_guests`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `airbnb_erd`.`booking_guests` (
  `booking_id` BIGINT NOT NULL,
  `guest_type_id` INT NOT NULL,
  `num_guests` INT NOT NULL,
  PRIMARY KEY (`booking_id`, `guest_type_id`),
  INDEX `guest_type_id` (`guest_type_id` ASC) VISIBLE,
  CONSTRAINT `booking_guests_ibfk_1`
    FOREIGN KEY (`booking_id`)
    REFERENCES `airbnb_erd`.`bookings` (`booking_id`)
    ON DELETE CASCADE,
  CONSTRAINT `booking_guests_ibfk_2`
    FOREIGN KEY (`guest_type_id`)
    REFERENCES `airbnb_erd`.`guest_type` (`guest_type_id`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `airbnb_erd`.`user_review`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `airbnb_erd`.`user_review` (
  `review_id` BIGINT NOT NULL AUTO_INCREMENT,
  `property_id` BIGINT NOT NULL,
  `user_id` BIGINT NOT NULL,
  `booking_id` BIGINT NULL DEFAULT NULL,
  `overall_rating` INT NOT NULL,
  `comment` TEXT NULL DEFAULT NULL,
  `created_at` DATETIME NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`review_id`),
  INDEX `idx_property` (`property_id` ASC) VISIBLE,
  INDEX `idx_user` (`user_id` ASC) VISIBLE,
  CONSTRAINT `user_review_ibfk_1`
    FOREIGN KEY (`property_id`)
    REFERENCES `airbnb_erd`.`property` (`property_id`)
    ON DELETE CASCADE,
  CONSTRAINT `user_review_ibfk_2`
    FOREIGN KEY (`user_id`)
    REFERENCES `airbnb_erd`.`user_account` (`id`)
    ON DELETE CASCADE)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `airbnb_erd`.`review_component`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `airbnb_erd`.`review_component` (
  `review_component_id` INT NOT NULL AUTO_INCREMENT,
  `component_name` VARCHAR(255) NOT NULL,
  PRIMARY KEY (`review_component_id`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `airbnb_erd`.`component_rating`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `airbnb_erd`.`component_rating` (
  `component_id` BIGINT NOT NULL AUTO_INCREMENT,
  `review_id` BIGINT NOT NULL,
  `review_component_id` INT NOT NULL,
  `rating` INT NOT NULL,
  PRIMARY KEY (`component_id`),
  INDEX `review_component_id` (`review_component_id` ASC) VISIBLE,
  INDEX `idx_review` (`review_id` ASC) VISIBLE,
  CONSTRAINT `component_rating_ibfk_1`
    FOREIGN KEY (`review_id`)
    REFERENCES `airbnb_erd`.`user_review` (`review_id`)
    ON DELETE CASCADE,
  CONSTRAINT `component_rating_ibfk_2`
    FOREIGN KEY (`review_component_id`)
    REFERENCES `airbnb_erd`.`review_component` (`review_component_id`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `airbnb_erd`.`conversation`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `airbnb_erd`.`conversation` (
  `conversation_id` BIGINT NOT NULL AUTO_INCREMENT,
  `created_at` DATETIME NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`conversation_id`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `airbnb_erd`.`conversation_participants`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `airbnb_erd`.`conversation_participants` (
  `conversation_id` BIGINT NOT NULL,
  `user_id` BIGINT NOT NULL,
  PRIMARY KEY (`conversation_id`, `user_id`),
  INDEX `user_id` (`user_id` ASC) VISIBLE,
  CONSTRAINT `conversation_participants_ibfk_1`
    FOREIGN KEY (`conversation_id`)
    REFERENCES `airbnb_erd`.`conversation` (`conversation_id`)
    ON DELETE CASCADE,
  CONSTRAINT `conversation_participants_ibfk_2`
    FOREIGN KEY (`user_id`)
    REFERENCES `airbnb_erd`.`user_account` (`id`)
    ON DELETE CASCADE)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `airbnb_erd`.`favourite`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `airbnb_erd`.`favourite` (
  `user_account_id` BIGINT NOT NULL,
  `property_id` BIGINT NOT NULL,
  PRIMARY KEY (`user_account_id`, `property_id`),
  INDEX `property_id` (`property_id` ASC) VISIBLE,
  CONSTRAINT `favourite_ibfk_1`
    FOREIGN KEY (`user_account_id`)
    REFERENCES `airbnb_erd`.`user_account` (`id`)
    ON DELETE CASCADE,
  CONSTRAINT `favourite_ibfk_2`
    FOREIGN KEY (`property_id`)
    REFERENCES `airbnb_erd`.`property` (`property_id`)
    ON DELETE CASCADE)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `airbnb_erd`.`language`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `airbnb_erd`.`language` (
  `language_id` INT NOT NULL AUTO_INCREMENT,
  `language` VARCHAR(255) NOT NULL,
  PRIMARY KEY (`language_id`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `airbnb_erd`.`payment`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `airbnb_erd`.`payment` (
  `payment_id` BIGINT NOT NULL AUTO_INCREMENT,
  `booking_id` BIGINT NOT NULL,
  `amount` DECIMAL(10,2) NOT NULL,
  `payment_date` DATETIME NULL DEFAULT NULL,
  `payment_method` VARCHAR(100) NULL DEFAULT NULL,
  `paid_at` DATETIME NULL DEFAULT NULL,
  PRIMARY KEY (`payment_id`),
  INDEX `idx_booking` (`booking_id` ASC) VISIBLE,
  CONSTRAINT `payment_ibfk_1`
    FOREIGN KEY (`booking_id`)
    REFERENCES `airbnb_erd`.`bookings` (`booking_id`)
    ON DELETE CASCADE)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `airbnb_erd`.`property_attribute`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `airbnb_erd`.`property_attribute` (
  `property_id` BIGINT NOT NULL,
  `attribute_id` INT NOT NULL,
  PRIMARY KEY (`property_id`, `attribute_id`),
  INDEX `attribute_id` (`attribute_id` ASC) VISIBLE,
  CONSTRAINT `property_attribute_ibfk_1`
    FOREIGN KEY (`property_id`)
    REFERENCES `airbnb_erd`.`property` (`property_id`)
    ON DELETE CASCADE,
  CONSTRAINT `property_attribute_ibfk_2`
    FOREIGN KEY (`attribute_id`)
    REFERENCES `airbnb_erd`.`attribute` (`attribute_id`)
    ON DELETE CASCADE)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `airbnb_erd`.`property_images`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `airbnb_erd`.`property_images` (
  `image_id` BIGINT NOT NULL AUTO_INCREMENT,
  `property_id` BIGINT NOT NULL,
  `image_url` VARCHAR(500) NOT NULL,
  `image_order` INT NULL DEFAULT '0',
  PRIMARY KEY (`image_id`),
  INDEX `idx_property` (`property_id` ASC) VISIBLE,
  CONSTRAINT `property_images_ibfk_1`
    FOREIGN KEY (`property_id`)
    REFERENCES `airbnb_erd`.`property` (`property_id`)
    ON DELETE CASCADE)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `airbnb_erd`.`roles`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `airbnb_erd`.`roles` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `name` ENUM('host', 'guest', 'admin') NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE INDEX `uq_role_name` (`name` ASC) VISIBLE)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `airbnb_erd`.`user_language`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `airbnb_erd`.`user_language` (
  `user_language_id` BIGINT NOT NULL AUTO_INCREMENT,
  `user_id` BIGINT NOT NULL,
  `language_id` INT NOT NULL,
  PRIMARY KEY (`user_language_id`),
  INDEX `language_id` (`language_id` ASC) VISIBLE,
  INDEX `idx_user` (`user_id` ASC) VISIBLE,
  CONSTRAINT `user_language_ibfk_1`
    FOREIGN KEY (`user_id`)
    REFERENCES `airbnb_erd`.`user_account` (`id`)
    ON DELETE CASCADE,
  CONSTRAINT `user_language_ibfk_2`
    FOREIGN KEY (`language_id`)
    REFERENCES `airbnb_erd`.`language` (`language_id`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `airbnb_erd`.`user_roles`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `airbnb_erd`.`user_roles` (
  `id` BIGINT NOT NULL AUTO_INCREMENT,
  `user_id` BIGINT NOT NULL,
  `role_id` INT NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE INDEX `uq_user_role` (`user_id` ASC, `role_id` ASC) VISIBLE,
  INDEX `role_id` (`role_id` ASC) VISIBLE,
  CONSTRAINT `user_roles_ibfk_1`
    FOREIGN KEY (`user_id`)
    REFERENCES `airbnb_erd`.`user_account` (`id`)
    ON DELETE CASCADE,
  CONSTRAINT `user_roles_ibfk_2`
    FOREIGN KEY (`role_id`)
    REFERENCES `airbnb_erd`.`roles` (`id`)
    ON DELETE CASCADE)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
