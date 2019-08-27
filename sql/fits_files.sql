with q0 as
(
select  intro.file_id       as intro_file_id,
        intro.heading_title as intro_heading_title,
        intro.description   as intro_description,
        file.location_id    as file_location_id,
        file.name           as file_name
from intro
join file
on intro.file_id = file.id
where
    (
         intro.heading_title ilike 'Naming convention'
         /*
         and
         (
            intro.description like '%.fits'
            or
            intro.description like '%.fits.gz'
         )
         */
    )

),

q1 as
(
select  q0.intro_description    as intro_description,
        q0.file_name            as file_name,
        location.env_id         as location_env_id,
        location.path           as location_path
from q0
join location
on q0.file_location_id = location.id
),

q2 as
(
select  q1.location_env_id      as env_id,
        q1.location_path        as path,
        q1.intro_description    as fits_name,
        q1.file_name            as html_name,
        env.variable            as variable
from q1
join env
on q1.location_env_id = env.id
)

select concat(variable,'/',path,'/',fits_name)
from q2;
