delimiter //
create function f_student_cnt(jname varchar(31)) RETURNS smallint
BEGIN
	RETURN (select count(*) 
			 from Subject s inner join Enroll e on e.subject = s.id
             group by s.name having s.name = jname);
END //

delimiter ;

delimiter //
create function f_subject_cnt(sname varchar(31)) RETURNS smallint
BEGIN
	RETURN (select count(*) from Enroll
			 where student = (select id from Student where name = sname limit 1));
END//
delimiter ;

select f_student_cnt('수리통계');

select * from Subject;

drop function f_student_cnt;

select name, f_student_cnt(name) '수강생 수' from Subject;
select name, f_subject_cnt(name) '과목수' from Student;
drop function f_subject_cnt;

select name, count(*) from Student group by name having count(*)>1;



select concat(name, count(*)) from Student group by name having count(*) > 1;
select * from Club;
