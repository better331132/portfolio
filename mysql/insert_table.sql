-- 문항 2
start transaction;
insert into Grade(enroll, midterm, finalterm) select id, (100- ceil(rand()*45)), (100 - ceil(rand()*45)) from Enroll order by id ;
commit;