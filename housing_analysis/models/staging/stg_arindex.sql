with source as (
    select * from {{ source('raw', 'arindex_negyedev') }}
),

renamed as (
    select
        idoszak,
        ev::integer as ev,
        negyedev,
        osszevont_index::float as osszevont_index,
        tiszta_haszn::float as tiszta_ar_haszn,
        tiszta_uj::float as tiszta_ar_uj
    from source
    where ev is not null
      and negyedev not in ('nan', 'NaT')
)

select * from renamed