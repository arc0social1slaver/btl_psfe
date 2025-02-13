create schema `bookstore`;
use `bookstore`;
create table `cart`(
    `id` int primary key auto_increment,
    `user_id` int,
    `name` varchar(20),
    `price` int,
    `quality` int,
    `image` varchar(20)
);
create table `message`(
    `id` int primary key auto_increment,
    `user_id` int,
    `name` varchar(100),
    `number` varchar(12),
    `email` varchar(100),
    `message` varchar(500)
);
create table `orders`(
    `id` int primary key auto_increment,
    `user_id` int,
    `name` varchar(100),
    `number` varchar(12),
    `email` varchar(100),
    `method` varchar(50),
    `address` varchar(500),
    `total_products` varchar(1000),
    `total_price` int,
    `placed_on` varchar(50),
    `payment_status` varchar(20)
);
create table `products`(
    `id` int primary key auto_increment,
    `name` varchar(100),
    `price` int,
    `image` varchar(100)
);
create table `users`(
    `id` int primary key auto_increment,
    `name` varchar(100),
    `email` varchar(100),
    `password` varchar(100),
    `user_type` varchar(20)
);
insert into `users`(`name`,`email`,`password`,`user_type`) values
(
    'superManager','abcdefgh@gmail.com','123456789','admin'
),
(
    'superUser', 'abcdefgh@gmail.com','123456789','user'
);