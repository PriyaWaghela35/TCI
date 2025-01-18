CREATE DATABASE TestDB;

show databases;
use TestDB;
CREATE table users(
id INT auto_increment primary key,
name varchar(100) not null,
email_id varchar(100)
);
CREATE table  employee (empid INT primary key,name varchar(100) not null,email_id varchar(100),job_role varchar(100));

show tables;
select * from employee;
insert into employee(empid,name,email_id,job_role) Values(2001,'Priya Wagehla','priyawaghela35@gmail.com', 'Engineer');
insert into employee(empid,name,email_id,job_role) Values(2002,'Priya Sharma','priyasharma@gmail.com', 'HR');
insert into employee(empid,name,email_id,job_role) Values(2003,'Tiya Wagehla','tiyawaghela35@gmail.com', 'CA');
insert into employee(empid,name,email_id,job_role) Values(2004,'Tiya Wagehla','tiya@gmail.com', 'BBA');
insert into employee(empid,name,email_id,job_role) Values(2005,'miya kapoor','miyakapoor69@gmail.com', 'MBA');
insert into employee(empid,name,email_id,job_role) Values(2008,'jiya Wagehla','jiyawaghela99@gmail.com', 'A');
alter table employee add column contact bigint;
update employee SET contact = 9876543210 where empid=2001;
update employee SET contact = 9876543210 where empid=2002;

delete from employee where empid=2004;
DROP TABLE if exists employee;
DROP TABLE if exists users;
show databases;
drop database TestDB;
