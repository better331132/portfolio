drop trigger if exists tr_addclub_ranleader;
Delimiter //
create trigger tr_addclub_ranleader
	after insert on Club For Each Row
BEGIN
    insert into Clubmember(name, student, level) select New.id, (select student from Clubmember where level = 0 order by rand() limit 1), 2;
     
END //

delimiter ;


