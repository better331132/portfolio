drop procedure if exists sp_top1_grade;
DELIMITER $$
CREATE PROCEDURE sp_top1_grade()
begin
    declare _isdone boolean default False;
    declare _avr tinyint;
	declare _subject varchar(10);
    declare _tier1 varchar(10);
    declare _grade1 tinyint;
    declare _tier2 varchar(10);
    declare _grade2 tinyint;
    declare _tier3 varchar(10);
    declare _grade3 tinyint;

    declare cur_avrs cursor for
        select j.name, s.name, v.avr from v_grade_enroll v inner join Student s on v.student = s.id
														   inner join Subject j on v.subject = j.id
		 order by j.name, v.avr desc;

    declare continue handler
        for not found set _isdone = True;

    drop table if exists t_grade;

    create temporary table t_grade (
		subject varchar(10) default '',
        tier1 varchar(10) default '',
        grade1 tinyint default 0,
        tier2 varchar(10) default '',
        grade2 tinyint default 0,
        tier3 varchar(10) default '',
        grade3 tinyint default 0
    );
        
    open cur_avrs ;
    
    loop1: LOOP
        FETCH cur_avrs into _subject, _tier1, _avr;
        set _subject = _subject;
        set _tier1 = _tier1;
        set _grade1 = floor(_avr);
		        
        insert into t_grade(subject, tier1, grade1) value(_subject, _tier1, _grade1);
        
		IF _isdone THEN
            LEAVE loop1;
        END IF;

    END LOOP loop1;
    
    close cur_avrs;
    
    select * from t_grade;
    
end$$
DELIMITER ;
call sp_top1_grade();
