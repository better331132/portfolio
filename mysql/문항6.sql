drop procedure if exists sp_top3_grade;
DELIMITER $$
CREATE PROCEDURE sp_top3_grade()
begin
    declare _isdone boolean default False;
    declare _avr decimal(5);
	declare _subject varchar(10);
    declare _tier varchar(10);
    declare _grade decimal(5);


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
        grade1 decimal(5) default 0,
        tier2 varchar(10) default '',
        grade2 decimal(5) default 0,
        tier3 varchar(10) default '',
        grade3 decimal(5) default 0
    );
        
    open cur_avrs ;
    
    loop1: LOOP
        FETCH cur_avrs into _subject, _tier, _avr;
        set _subject = _subject;
        set _grade = _avr;
        set _tier = _tier;

        if not exists (select * from t_grade where subject = _subject) then
            insert into t_grade(subject, tier1, grade1) value(_subject, _tier, _grade);
            
		elseif exists (select * from t_grade where tier2 = '') then
		    update t_grade set tier2 = _tier, grade2 = _grade where subject = _subject;
            
		elseif exists (select * from t_grade where tier3 = '') then
			update t_grade set tier3 = _tier, grade3 = _grade where subject = _subject;
            
        end if;
        
		IF _isdone THEN
            LEAVE loop1;
        END IF;

    END LOOP loop1;
    
    close cur_avrs;
    
    select subject '과목명', tier1 '1등', grade1 '점수', tier2 '2등', grade2 '점수', tier3 '3등', grade3 '점수'
      from t_grade;
    
end$$
DELIMITER ;
call sp_top3_grade();