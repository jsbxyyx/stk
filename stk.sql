create database istock default character set utf8mb4 collate utf8mb4_general_ci;

create table stock_all(
    id int primary key auto_increment,
    code varchar(20) not null,
    name varchar(20) not null,
    gmt_create datetime not null,
    unique key `uk_code` (`code`)
);

create table stock_kline(
    `id` int primary key auto_increment,
    `date` varchar(20) not null,
    `code` varchar(20) not null,
    `open` double(20, 2) not null,
    `close` double(20, 2) not null,
    `high` double(20, 2) not null,
    `low` double(20, 2) not null,
    `volume` double(20, 2) not null,
    `turnover` double(20, 2) not null,
    `amplitude` double(20, 2) not null,
    `change_rate` double(20, 2) not null,
    `change_amount` double(20, 2) not null,
    `turnover_rate` double(20, 2) not null,
    unique key `uk_date_code` (`date`, `code`)
);
