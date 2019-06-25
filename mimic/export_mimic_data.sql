set search_path to mimiciii;


select date_trunc('month', admittime) as month, count(*) from admissions
where admittime between '2137-01-01' and '2137-12-31' group by month order by month asc;

select labevents.subject_id as id, d_labitems.label as label, d_labitems.fluid as fluid,
d_labitems.category as category, labevents.value as value, labevents.valuenum as number,
labevents.valueuom as units from labevents
inner join d_labitems on labevents.itemid = d_labitems.itemid limit 500;

Copy (select noteevents.subject_id, gender, dob, dod, chartdate, text
  from noteevents inner join patients on noteevents.subject_id=patients.subject_id limit 5)
  To '/tmp/noteevents_limit5.csv' With CSV DELIMITER ',';


%  select max(chartdate), min(chartdate) from noteevents;
%           max         |         min
%  ---------------------+---------------------
%   2210-10-01 00:00:00 | 2097-12-07 00:00:00


select chartdate, count(*) from noteevents group by chartdate;

%       chartdate      | count
% ---------------------+-------
%  2148-12-11 00:00:00 |   132


  Copy
  (select noteevents.subject_id, gender, dob, dod, chartdate, text
    from noteevents inner join patients on noteevents.subject_id=patients.subject_id
    where chartdate='2148-12-11') To '/tmp/noteevents.csv' With CSV DELIMITER ',';

    Copy
    (select noteevents.subject_id, gender, dob, dod, chartdate, text
      from noteevents inner join patients on noteevents.subject_id=patients.subject_id
      limit 5000) To '/tmp/noteevents5000.csv' With CSV DELIMITER ',';

    Copy
    (select chartevents.subject_id, gender, dob, dod, charttime,
      d_items.label, value, valuenum, valueuom, warning, error, resultstatus, stopped
      from chartevents
      inner join patients on chartevents.subject_id=patients.subject_id
      inner join d_items on chartevents.itemid=d_items.itemid
      where charttime='2148-12-11') To '/tmp/chartevents.csv' With CSV DELIMITER ',';
