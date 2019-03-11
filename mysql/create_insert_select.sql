-- 문항 6
create table Grade(
	id int not null auto_increment primary key,
    midterm varchar(3),
    finalterm varchar(3),
    enroll int unsigned,
    constraint foreign key fk_enroll(enroll) references Enroll(id)
    on delete set null
);

insert into Grade(enroll, midterm, finalterm) select id, (100- ceil(rand()*45)), (100 - ceil(rand()*45)) from Enroll order by id ;
-- 1
select j.name as '과목명', 
	   s.name as '학생명', 
       g.midterm as '중간', 
       g.finalterm as '기말', 
       g.midterm+finalterm as '총점', 
       (g.midterm+finalterm)/2 as '평균',
       (case when (g.midterm+finalterm)/2 > 90 then 'A'
		     when (g.midterm+finalterm)/2 > 80 then 'B'
             when (g.midterm+finalterm)/2 > 70 then 'C'
             when (g.midterm+finalterm)/2 > 60 then 'D'
             else 'F' end) as '학점'
 from Enroll e inner join Student s on e.student = s.id
               inner join Subject j on e.subject = j.id
               inner join Grade g on e.id = g.enroll order by j.name;

-- 2
select j.name as '과목명',
       avg((g.midterm+finalterm)/2) as '과목평균',
       count(*) as '총 학생수'
 from Enroll e inner join Student s on e.student = s.id
               inner join Subject j on e.subject = j.id
               inner join Grade g on e.id = g.enroll
group by j.name
order by j.name;

-- 3
select s.name as '학생명',
       count(*) as '과목수',
       sum(g.midterm+finalterm) as '총점',
       avg((g.midterm+finalterm)/2) as '평균',
       (case when avg((g.midterm+finalterm)/2) > 80 then 'A'
			when avg((g.midterm+finalterm)/2) > 75 then 'B'
            when avg((g.midterm+finalterm)/2) > 72 then 'C'
            when avg((g.midterm+finalterm)/2) > 70 then 'D'
            else 'F' end) as '평점'
 from Enroll e inner join Student s on e.student = s.id
               inner join Subject j on e.subject = j.id
               inner join Grade g on e.id = g.enroll
 group by s.name
 order by s.name;