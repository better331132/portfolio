-- 문항 4
select * from Dept;

create table Dept(
  id int unsigned not null auto_increment primary key,
  name varchar(31) not null,
  prof int unsigned,
  student int unsigned,
  constraint foreign key fk_Dept_Prof(prof) references Prof(id) on delete set null,
  constraint foreign key fk_Dept_Student(student) references Student(id) on delete set null
);
desc Dept;

select * from Dept;
start transaction;
insert into Dept(name, prof) values("수학과", ceil(rand()*100));
insert into Dept(name, prof) values("경제학과", ceil(rand()*100));
insert into Dept(name, prof) values("기계공학과", ceil(rand()*100));
insert into Dept(name, prof) values("통계학과", ceil(rand()*100));
insert into Dept(name, prof) values("국어국문학과", ceil(rand()*100));
commit;

ALTER TABLE Student
ADD COLUMN dept INT UNSIGNED NULL AFTER gender,
ADD INDEX fk_Student_Dept_idx (dept ASC);
;
ALTER TABLE Student
ADD CONSTRAINT fk_Student_Dept
  FOREIGN KEY (dept)
  REFERENCES Dept (id)
  ON DELETE SET NULL;

update Student set dept = ceil(rand()*5);


update Dept d inner join Student s on d.id = s.dept set d.student = s.id;