drop function if exists f_student_avr;
delimiter //
create function f_student_avr(sid tinyint) RETURNS decimal(5,2)
BEGIN
	RETURN (select avg((g.midterm+g.finalterm)/2) '전과목평균점수'
			 from Student s inner join Enroll e on e.student = s.id
							inner join Grade g on g.enroll = e.id
             where s.id = sid);
END //

delimiter ;

