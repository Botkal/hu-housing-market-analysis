with source as (
    select * from {{ source('raw', 'atlagár_regio_telepulestipus') }}
),

renamed as (
    select
        regio,
        telepulestipus,
        lakastipus,
        idoszak,
        atlagár_mFt::float as atlagár_mFt
    from source
    where atlagár_mFt is not null
      and regio not in ('nan', 'Régió')
)

select * from renamed