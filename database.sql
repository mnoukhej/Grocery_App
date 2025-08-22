

-- Porducts Table --------------------------------------------------------
CREATE TABLE `gs`.`products` (
  `product_id` INT NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(45) NOT NULL,
  `uom_id` INT NOT NULL,
  `price_per_unit` DOUBLE NOT NULL,
  PRIMARY KEY (`product_id`));

-- Porducts Table --------------------------------------------------------
ALTER TABLE `gs`.`products` 
ADD INDEX `fk_uom_id_idx` (`uom_id` ASC) VISIBLE;
;
ALTER TABLE `gs`.`products` 
ADD CONSTRAINT `fk_uom_id`
  FOREIGN KEY (`uom_id`)
  REFERENCES `gs`.`uom` (`uom_id`)
  ON DELETE NO ACTION
  ON UPDATE RESTRICT;



-- Product Table --
INSERT INTO `gs`.`products` (`product_id`, `name`, `uom_id`, `price_per_unit`) VALUES ('1', 'Toothpaste', '1', '30');





-- Units of Measurement Table -----------------------------------------
CREATE TABLE `gs`.`uom` (
  `uom_id` INT NOT NULL,
  `uom_name` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`uom_id`));

INSERT INTO `gs`.`uom` (`uom_id`, `uom_name`) VALUES ('1', 'Each');
INSERT INTO `gs`.`uom` (`uom_id`, `uom_name`) VALUES ('2', 'Kg');



-- Orders--------------------------------------------------------
CREATE TABLE `gs`.`orders` (
  `order_id` INT NOT NULL AUTO_INCREMENT,
  `customer_name` VARCHAR(45) NOT NULL,
  `total` DOUBLE NOT NULL,
  `datatime` DATETIME NOT NULL,
  PRIMARY KEY (`order_id`));











  CREATE TABLE `gs`.`order_details` (
  `order_id` INT NOT NULL,
  `product_id` INT NOT NULL,
  `quality` DOUBLE NOT NULL,
  `total_price` DOUBLE NOT NULL,
  PRIMARY KEY (`order_id`),
  INDEX `fk_product_id_idx` (`product_id` ASC) VISIBLE,
  CONSTRAINT `fk_order_id`
    FOREIGN KEY (`order_id`)
    REFERENCES `gs`.`orders` (`order_id`)
    ON DELETE NO ACTION
    ON UPDATE RESTRICT,
  CONSTRAINT `fk_product_id`
    FOREIGN KEY (`product_id`)
    REFERENCES `gs`.`products` (`product_id`)
    ON DELETE NO ACTION
    ON UPDATE RESTRICT);
