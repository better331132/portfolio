drop procedure if exists sp_prof_rec;
delimiter $$
create procedure sp_prof_rec(_sq tinyint)
begin
    declare _isdone boolean default False;
    declare _popu smallint;
    declare _like smallint;
    declare _acount smallint;
    declare _prof varchar(31);
    declare _likeratio decimal(5);
    declare _aratio decimal(5);
    declare _totpoint smallint;

    declare cur_prof cursor for
		select concat(max(p.name) , '(', max(j.name), ')') prof, max(j.students) students, max(p.likecnt) likecnt, count(*) acount 
		  from Enroll e inner join Grade g on g.enroll = e.id
				 	    inner join Subject j on e.subject = j.id
                        inner join Prof p on j.prof = p.id
		  where (g.midterm+finalterm)/2 >= 80
          group by p.id;


    declare continue handler
        for not found set _isdone = True;

    drop table if exists t_prof_ranking;

    create temporary table t_prof_ranking (
        prof varchar(31) default '',
        like_ratio decimal(5) default 0,
        a_ratio decimal(5) default 0,
        total_point smallint default 0
    );
        
    open cur_prof;
    
    loop1: LOOP
        FETCH cur_prof into _prof, _popu, _like, _acount;
        
        set _prof = _prof;
        set _likeratio = (_like/_popu)*100;
        set _aratio = (_acount/_popu)*100;
        set _totpoint = (_likeratio/_aratio)*100;
        
        insert into t_prof_ranking(prof,like_ratio,a_ratio,total_point) values(_prof, _likeratio, _aratio, _totpoint);
        
        IF _isdone THEN
            LEAVE loop1;
        END IF;
    
    END LOOP loop1;
    
    close cur_prof;
    
    select prof '교수명(해당과목명)', like_ratio '호감표시비율(단위:%)', a_ratio '수강생A학점비율(단위:%)', total_point '선호도총계' 
      from t_prof_ranking order by total_point desc limit _sq;
    
end $$
delimiter ;

call sp_prof_rec(9);
