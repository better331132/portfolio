select e.last_name, e.salary, d.department_name
 from employees e inner join departments d on e.department_id = d.department_id
 where e.salary < (select avg(salary) from employees where department_id = 80)
   and d.department_name = 'Marketing';