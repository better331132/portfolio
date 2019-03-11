-- 각 과목 교수이름
select j.*, p.name as "prof.name"
 from Subject j inner join Profs p
 on j.profs = p.id;
 
-- 동아리 전체 목록에 리더 이름 함께 출력
select c.*, s.name as "Club leader"
 from Club c inner join Students s on c.leader = s.id; 

-- 과목별 등록 학생수
select e.subject, max(j.name) as "subject", count(*) as "student"
 from Enroll e inner join Subject j on e.subject = j.id
 group by subject;
 
-- 역사과목의 학생목록
select s.name, s.birth
 from Enroll e inner join Student s on e.students = s.id
               inner join Subject j on e.subject = j.id
 where j.name = "생명과학";

-- 특정과목을 듣는 서울 거주 학생 목록
select j.name, s.id, s.name
 from Enroll e inner join Student s on e.students = s.id
			   inner join Subject j on e.subject = j.id
 where j.name = "수리통계" and s.addr = "서울";

-- 특정 과목을 수강중인 지역별 학생수
select j.name, s.addr, count(*)
 from Enroll e inner join Student s on e.students = s.id
			   inner join Subject j on e.subject = j.id
 where j.name = "과학철학"
 group by s.addr;

-- 과목별 학생 목록
 select * from Enroll;
 
-- 서울에 거주하는 과목별 남녀 학생수
select min(j.name) as '과목명', (case when s.gender = 0 then '여' else '남' end) as '성별', count(*) as '학생수'
 from Enroll e inner join Student s on e.student = s.id
			   inner join Subject j on e.subject = j.id
where s.addr = "서울" group by j.id, s.gender order by j.name, s.gender desc;

 


 