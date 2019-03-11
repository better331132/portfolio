-- 문항 1
create table Student(
  id int unsigned NOT NULL AUTO_INCREMENT primary key,
  name varchar(31) NOT NULL,
  tel varchar(31),
  email varchar(31),
  birth date,
  addr varchar(31),
  gender bit(1)
);
desc Student;

create table Prof(
	id int unsigned not null auto_increment primary key,
    name varchar(31) not null,
    likecnt int not null
);
desc Prof;

create table Subject(
	id int unsigned not null auto_increment primary key,
    name varchar(31) not null,
    prof int unsigned,
    constraint foreign key fk_prof(prof) references Prof(id)
    on delete set null
);
desc Subject;

create table Enroll(
	id int unsigned not null auto_increment primary key,
    student int unsigned,
    subject int unsigned,
    constraint foreign key fk_subject(subjects) references Subject(id)
    on delete cascade,
    constraint foreign key fk_student(students) references Student(id)
    on delete cascade
);
desc Enroll;