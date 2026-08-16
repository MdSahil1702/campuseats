-- ============================================================
-- CampusEats — Assignment 2
-- Service-owned database schema
--
-- Boundary rule: each table belongs to exactly ONE service.
-- Services only reach other services' data through contracts
-- (see Task 3), never by joining across service boundaries.
-- ============================================================


-- ============================================================
-- ACCOUNTS SERVICE
-- Owns: users, addresses
-- ============================================================

CREATE TABLE users (
    user_id    INT AUTO_INCREMENT PRIMARY KEY,
    name       VARCHAR(100)  NOT NULL,
    email      VARCHAR(150)  NOT NULL,
    UNIQUE KEY uq_users_email (email)
);

CREATE TABLE addresses (
    address_id     INT AUTO_INCREMENT PRIMARY KEY,
    user_id        INT           NOT NULL,
    address_text   VARCHAR(255)  NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(user_id)
        ON UPDATE CASCADE
        ON DELETE CASCADE,
    INDEX idx_addresses_user_id (user_id)
);


-- ============================================================
-- CATALOGUE SERVICE
-- Owns: restaurants, menus, menu_items
-- ============================================================

CREATE TABLE restaurants (
    restaurant_id  INT AUTO_INCREMENT PRIMARY KEY,
    name           VARCHAR(150)  NOT NULL
);

CREATE TABLE menus (
    menu_id         INT AUTO_INCREMENT PRIMARY KEY,
    restaurant_id   INT           NOT NULL,
    name            VARCHAR(150)  NOT NULL,
    FOREIGN KEY (restaurant_id) REFERENCES restaurants(restaurant_id)
        ON UPDATE CASCADE
        ON DELETE CASCADE,
    INDEX idx_menus_restaurant_id (restaurant_id)
);

CREATE TABLE menu_items (
    item_id    INT AUTO_INCREMENT PRIMARY KEY,
    menu_id    INT            NOT NULL,
    name       VARCHAR(150)   NOT NULL,
    price      DECIMAL(10,2)  NOT NULL CHECK (price >= 0),
    FOREIGN KEY (menu_id) REFERENCES menus(menu_id)
        ON UPDATE CASCADE
        ON DELETE CASCADE,
    INDEX idx_menu_items_menu_id (menu_id)
);


-- ============================================================
-- ORDERS SERVICE
-- Owns: carts, cart_items, orders, order_items
-- ============================================================

CREATE TABLE carts (
    cart_id    INT AUTO_INCREMENT PRIMARY KEY,
    user_id    INT           NOT NULL,
    status     VARCHAR(30)   NOT NULL,
    INDEX idx_carts_user_id (user_id)
);

CREATE TABLE cart_items (
    cart_item_id  INT AUTO_INCREMENT PRIMARY KEY,
    cart_id       INT  NOT NULL,
    item_id       INT  NOT NULL,
    quantity      INT  NOT NULL CHECK (quantity > 0),
    FOREIGN KEY (cart_id) REFERENCES carts(cart_id)
        ON UPDATE CASCADE
        ON DELETE CASCADE,
    INDEX idx_cart_items_cart_id (cart_id)
);

CREATE TABLE orders (
    order_id    INT AUTO_INCREMENT PRIMARY KEY,
    user_id     INT            NOT NULL,
    address_id  INT            NOT NULL,
    status      VARCHAR(30)    NOT NULL,
    total       DECIMAL(10,2)  NOT NULL CHECK (total >= 0),
    INDEX idx_orders_user_id (user_id),
    INDEX idx_orders_address_id (address_id)
);

CREATE TABLE order_items (
    order_item_id  INT AUTO_INCREMENT PRIMARY KEY,
    order_id       INT            NOT NULL,
    item_id        INT            NOT NULL,
    quantity       INT            NOT NULL CHECK (quantity > 0),
    price          DECIMAL(10,2)  NOT NULL CHECK (price >= 0),
    FOREIGN KEY (order_id) REFERENCES orders(order_id)
        ON UPDATE CASCADE
        ON DELETE CASCADE,
    INDEX idx_order_items_order_id (order_id)
);


-- ============================================================
-- PAYMENTS SERVICE
-- Owns: transactions, refunds
-- ============================================================

CREATE TABLE transactions (
    transaction_id  INT AUTO_INCREMENT PRIMARY KEY,
    order_id        INT            NOT NULL,
    amount          DECIMAL(10,2)  NOT NULL CHECK (amount >= 0),
    status          VARCHAR(30)    NOT NULL,
    INDEX idx_transactions_order_id (order_id)
);

CREATE TABLE refunds (
    refund_id       INT AUTO_INCREMENT PRIMARY KEY,
    transaction_id  INT            NOT NULL,
    amount          DECIMAL(10,2)  NOT NULL CHECK (amount >= 0),
    status          VARCHAR(30)    NOT NULL,
    FOREIGN KEY (transaction_id) REFERENCES transactions(transaction_id)
        ON UPDATE CASCADE
        ON DELETE CASCADE,
    INDEX idx_refunds_transaction_id (transaction_id)
);


-- ============================================================
-- DELIVERY SERVICE
-- Owns: riders, delivery_assignments
-- ============================================================

CREATE TABLE riders (
    rider_id  INT AUTO_INCREMENT PRIMARY KEY,
    name      VARCHAR(100)  NOT NULL
);

CREATE TABLE delivery_assignments (
    assignment_id  INT AUTO_INCREMENT PRIMARY KEY,
    order_id       INT          NOT NULL,
    rider_id       INT          NOT NULL,
    status         VARCHAR(30)  NOT NULL,
    FOREIGN KEY (rider_id) REFERENCES riders(rider_id)
        ON UPDATE CASCADE
        ON DELETE CASCADE,
    INDEX idx_delivery_assignments_order_id (order_id),
    INDEX idx_delivery_assignments_rider_id (rider_id)
);


-- ============================================================
-- NOTIFICATIONS SERVICE
-- Owns: notification_log
-- ============================================================

CREATE TABLE notification_log (
    notification_id  INT AUTO_INCREMENT PRIMARY KEY,
    user_id          INT           NOT NULL,
    message          VARCHAR(255)  NOT NULL,
    status           VARCHAR(30)   NOT NULL,
    INDEX idx_notification_log_user_id (user_id)
);
