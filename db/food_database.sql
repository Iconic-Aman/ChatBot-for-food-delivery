DROP DATABASE IF EXISTS my_food_database;
CREATE DATABASE IF NOT EXISTS my_food_database;
USE my_food_database;

DROP TABLE IF EXISTS food_items;
CREATE TABLE food_items(
    item_id INT NOT NULL,
    name VARCHAR(50) DEFAULT NULL,
    price DECIMAL(6, 2) DEFAULT NULL,
    PRIMARY KEY(item_id)
);

LOCK TABLES food_items WRITE;
INSERT INTO food_items (item_id, name, price)
VALUES (1, 'Pav Bhaji', 6),
    (2, 'Chole Bhature', 7),
    (3, 'Pizza', 8),
    (4, 'Mango Lassi', 5),
    (5, 'Masala Dosa', 6),
    (6, 'Vegetable Biryani', 9),
    (7, 'Vada Pav', 4),
    (8, 'Rava Dosa', 7),
    (9, 'Samosa', 5);
UNLOCK TABLES;

DROP TABLE IF EXISTS order_tracking;
CREATE TABLE order_tracking(
    order_id INT NOT NULL,
    status VARCHAR(255) DEFAULT NULL,
    PRIMARY KEY(order_id)
);

LOCK TABLES order_tracking WRITE;
INSERT INTO order_tracking(order_id, status)
VALUES (40, 'Delivered'),
    (41, 'in Transit');
UNLOCK TABLES;

DROP TABLE IF EXISTS orders;
CREATE TABLE orders(
    order_id INT NOT NULL,
    item_id INT NOT NULL,
    quantity INT DEFAULT NULL,
    total_price DECIMAL (10, 2) DEFAULT NULL,
    PRIMARY KEY(order_id, item_id),
    FOREIGN KEY(item_id) REFERENCES food_items(item_id));

LOCK TABLES orders WRITE;
INSERT INTO orders (order_id, item_id, quantity, total_price)
VALUES (40, 1, 2, 12),
    (40, 3, 1, 8),  
    (41, 4, 3, 15),
    (41, 6, 2, 18),
    (41, 9, 4, 20);
UNLOCK TABLES;

DELIMITER ;;
CREATE FUNCTION getPriceForItem(p_item_name VARCHAR(200))
    RETURNS DECIMAL(10, 2)
    DETERMINISTIC
    /* write the function body */
BEGIN
    DECLARE v_price DECIMAL(10, 2);
    /* check if item_name exists in the table */
    IF(SELECT COUNT(*) from food_items WHERE name = p_item_name) > 0 THEN
        SELECT price INTO v_price FROM food_items WHERE name = p_item_name;
        RETURN v_price;
    ELSE
        RETURN -1;
        /* if item not present return -1 */
    END IF;
END ;;
DELIMITER ; /*Always keep a space between delimiter and semicolon */

DELIMITER ;;
CREATE FUNCTION getTotalOrderPrice(p_order_id INT)
    RETURNS DECIMAL(10, 2)
    DETERMINISTIC
BEGIN
    DECLARE v_total_price DECIMAL(10, 2);
    IF(SELECT COUNT(*) from orders WHERE order_id = p_order_id) > 0 THEN
        SELECT SUM(total_price) INTO v_total_price FROM orders WHERE order_id = p_order_id;
        RETURN v_total_price;
    ELSE
        RETURN -1;
    END IF;
END;;
DELIMITER ;

DELIMITER ;;
CREATE PROCEDURE insertOrderItem(
    IN p_food_item VARCHAR(255),
    IN p_quantity INT,
    IN p_order_id INT
)
BEGIN
    DECLARE v_item_id INT;
    DECLARE v_price DECIMAL(10, 2);
    DECLARE v_total_price DECIMAL(10, 2);
    /* Get the item_id and price for the food item */
    SET v_item_id = (SELECT item_id FROM food_items WHERE name = p_food_item);
    SET v_price = (SELECT getPriceForItem(p_food_item));

    /* Calculate the total price for the order item */
    SET v_total_price = v_price * p_quantity;
    /* Insert the order item into the orders table */
    INSERT INTO orders (order_id, item_id, quantity, total_price)
    VALUES (p_order_id, v_item_id, p_quantity, v_total_price);
END ;;
DELIMITER ;

