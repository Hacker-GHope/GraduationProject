'创建数据库'
create database house;
'创建数据表表'
create table city(
    -> id int auto_increment not null primary key,
    -> title varchar(128),
    -> local varchar(128),
    -> details varchar(128),
    -> price varchar(64),
    -> img varchar(256),
    -> link varchar(256)
    -> )engine=innodb
    -> charset=utf8;