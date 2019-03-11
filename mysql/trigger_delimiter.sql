Delimiter //
create trigger tr_enroll_subject_students_delete
	before delete on Enroll For Each Row
BEGIN
    delete from Grade
     where enroll = OLD.id;
	update Subject 
		set students = 
			(select count(*) - 1 from Enroll 
             where subject = (select subject from Enroll where id = OLD.id)
             )
	where id = (select subject from Enroll where id = OLD.id);
     
END //

delimiter ;

Delimiter //
create trigger tr_enroll_student_subjects_delete
	before delete on Enroll For Each Row
BEGIN
    delete from Grade
     where enroll = OLD.id;
	update Subject 
		set subjects = 
			(select count(*) - 1 from Enroll 
             where student = (select student from Enroll where id = OLD.id)
             )
	where id = (select student from Enroll where id = OLD.id);
     
END //

delimiter ;

Delimiter //
create trigger tr_subject_classroom_insert
	after insert on Subject For Each Row
BEGIN
	update Subject
		set classroom = ceil(rand()*10 + 10)
	where id = NEW.classroom;

END //

delimiter ;

delimiter //
create trigger tr_subject_prof_null
  before insert
  on Subject for each row
BEGIN
	IF NEW.prof is null THEN
		SET NEW.porf = (select id from Prof order by rand() limit 1);
    END IF;
END //
delimiter ;