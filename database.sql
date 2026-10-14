-- Create Database
CREATE DATABASE IF NOT EXISTS `gs`;
USE `gs`;

-- Units of Measurement Table -----------------------------------------
CREATE TABLE IF NOT EXISTS `gs`.`uom` (
  `uom_id` INT NOT NULL AUTO_INCREMENT,
  `uom_name` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`uom_id`)
);

INSERT INTO `gs`.`uom` (`uom_id`, `uom_name`) VALUES (1, 'Each'), (2, 'Kg')
ON DUPLICATE KEY UPDATE `uom_name` = VALUES(`uom_name`);

-- Products Table -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `gs`.`product` (
  `product_id` INT NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(45) NOT NULL,
  `uom_id` INT NOT NULL,
  `price_per_unit` DOUBLE NOT NULL,
  PRIMARY KEY (`product_id`),
  INDEX `fk_uom_id_idx` (`uom_id` ASC) VISIBLE,
  CONSTRAINT `fk_uom_id`
    FOREIGN KEY (`uom_id`)
    REFERENCES `gs`.`uom` (`uom_id`)
    ON DELETE NO ACTION
    ON UPDATE RESTRICT
);

-- View for compatibility if queries reference `products`
CREATE OR REPLACE VIEW `gs`.`products` AS SELECT * FROM `gs`.`product`;

-- Initial Product Record
INSERT INTO `gs`.`product` (`product_id`, `name`, `uom_id`, `price_per_unit`) VALUES (1, 'Toothpaste', 1, 30)
ON DUPLICATE KEY UPDATE `name` = VALUES(`name`), `uom_id` = VALUES(`uom_id`), `price_per_unit` = VALUES(`price_per_unit`);

-- Orders Table -------------------------------------------------------
CREATE TABLE IF NOT EXISTS `gs`.`orders` (
  `order_id` INT NOT NULL AUTO_INCREMENT,
  `customer_name` VARCHAR(45) NOT NULL,
  `total` DOUBLE NOT NULL,
  `datetime` DATETIME NOT NULL,
  PRIMARY KEY (`order_id`)
);

-- Order Details Table ------------------------------------------------
CREATE TABLE IF NOT EXISTS `gs`.`order_details` (
  `order_detail_id` INT NOT NULL AUTO_INCREMENT,
  `order_id` INT NOT NULL,
  `product_id` INT NOT NULL,
  `quantity` DOUBLE NOT NULL,
  `total_price` DOUBLE NOT NULL,
  PRIMARY KEY (`order_detail_id`),
  INDEX `fk_order_id_idx` (`order_id` ASC) VISIBLE,
  INDEX `fk_product_id_idx` (`product_id` ASC) VISIBLE,
  CONSTRAINT `fk_order_id`
    FOREIGN KEY (`order_id`)
    REFERENCES `gs`.`orders` (`order_id`)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
  CONSTRAINT `fk_product_id`
    FOREIGN KEY (`product_id`)
    REFERENCES `gs`.`product` (`product_id`)
    ON DELETE NO ACTION
    ON UPDATE RESTRICT
);
