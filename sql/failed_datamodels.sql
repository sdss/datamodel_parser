with pq as
(
select location.env_id as env_id, location.path, file.name, file.status
from file
join location
on file.location_id = location.id
where file.status = 'failed' or file.status = 'pending'
),
ppq as
(
select env.variable, pq.path, pq.name, pq.status
from pq
join env
on pq.env_id = env.id
)

select concat('parse_html -l error -v --path datamodel/files/',variable,'/',path,'/',name)
from ppq;

