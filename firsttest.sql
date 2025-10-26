create database m;
use m;
-- drop table mani;
create table mani(
depid INTEGER primary key,
depname VARCHAR(12));
insert into mani(depid,depname) values(11,'mani');
insert into mani(depid,depname) values(12,'mani1');
insert into mani(depid,depname) values(13,'mani2');
insert into mani(depid,depname) values(14,'mani3');
select * from mani;
create table emp(
empid integer primary key,
empname varchar(12),
depid integer ,
foreign key(depid) references mani(depid)
);
INSERT INTO mani (depid, depname) VALUES (11, 'Science');

insert into emp(empid,empname,depid) values(1,'math',11);
insert into emp(empid,empname,depid) values(2,'math',12);
insert into emp(empid,empname,depid) values(3,'math',13);
select * from emp
join mani using(depid);
INSERT INTO mani(depid, depname)
VALUES
(15, 'mani3'),
(16, 'mani3');
select *
from emp
full join  mani ;


