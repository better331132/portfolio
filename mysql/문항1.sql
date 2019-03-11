create view v_grade_info AS
 select s.id '학번', max(s.name) '학생명', max(s.subjects) '수강과목수', round(avg((g.midterm+finalterm)/2),2) '전과목평균점수'
   from Student s inner join Enroll e on s.id = e.student
	 			  inner join Grade g on g.enroll = e.id
   group by s.id;

select * from v_grade_info;