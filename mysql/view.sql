create view v_enroll_student AS
 select e.*, s.name
 from Enroll e inner join Student s on e.student = s.id;

desc v_enroll_student;

show create view v_enroll_student;

select * from v_enroll_student order by id;

update v_enroll_student set name = '뷰수정' where id = 1;

select * from information_schema.views
		where table_schema = 'betterdb';

-- view : Try This
-- 1)
create view v_grade_enroll AS
 select j.id, count(*) from Enroll e inner join Grade g on e.id = g.enroll
                                     inner join Subject j on e.subject = j.id
 group by j.id;

select * from v_grade_enroll;

create view v_info AS
 select s.id '학번', s.name '이름', j.id '과목번호', j.name '과목이름', g.midterm '중간', g.finalterm '기말', g.midterm+finalterm '총점', (g.midterm+finalterm)/2 '평균',
	  (case when (g.midterm+finalterm)/2 > 90 then 'A'
		     when (g.midterm+finalterm)/2 > 80 then 'B'
             when (g.midterm+finalterm)/2 > 70 then 'C'
             when (g.midterm+finalterm)/2 > 60 then 'D'
             else 'F' end) '학점'
  from Enroll e inner join Student s on e.student = s.id
                inner join Subject j on e.subject = j.id
				inner join Grade g on e.id = g.enroll; 

select * from v_info where 과목이름 = '수리통계' order by 평균 desc;

 select s.id '학번', s.name '이름', j.id '과목번호', j.name '과목이름', g.midterm '중간', g.finalterm '기말', g.midterm+finalterm '총점', (g.midterm+finalterm)/2 '평균',
	  (case when (g.midterm+finalterm)/2 > 90 then 'A'
		     when (g.midterm+finalterm)/2 > 80 then 'B'
             when (g.midterm+finalterm)/2 > 70 then 'C'
             when (g.midterm+finalterm)/2 > 60 then 'D'
             else 'F' end) '학점'
  from Enroll e inner join Student s on e.student = s.id
                inner join Subject j on e.subject = j.id
				inner join Grade g on e.id = g.enroll; 