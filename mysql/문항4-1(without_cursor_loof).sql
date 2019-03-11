drop procedure if exists sp_prof_rec;
delimiter $$
create procedure sp_prof_rec(_sq tinyint)
begin

	select concat(max(p.name) , '(', max(j.name), ')') prof, 
		   max(p.likecnt) / max(j.students) like_ratio, 
           count(*) / max(j.students) a_ratio, 
           max(p.likecnt)/count(*) 총점
	  from Enroll e inner join Grade g on g.enroll = e.id
			 	    inner join Subject j on e.subject = j.id
                    inner join Prof p on j.prof = p.id
	 where (g.midterm+finalterm)/2 >= 80
     group by p.id
     order by 총점 desc limit _sq;
	
end $$
delimiter ;

call sp_prof_rec(9);
