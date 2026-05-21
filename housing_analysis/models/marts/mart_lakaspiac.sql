with arindex as (
    select * from {{ ref('stg_arindex') }}
),

telepulestipus as (
    select * from {{ ref('stg_atlagar_telepulestipus') }}
),

budapest as (
    select
        idoszak,
        atlagár_mFt as budapest_atlagár_mFt
    from telepulestipus
    where regio = 'Budapest'
      and telepulestipus = 'főváros'
      and lakastipus = 'Használt lakások'
),

orszagos as (
    select
        idoszak,
        avg(atlagár_mFt) as orszagos_atlagár_mFt
    from telepulestipus
    where lakastipus = 'Használt lakások'
    group by idoszak
),

fejer as (
    select
        idoszak,
        atlagár_mFt as fejer_atlagár_mFt
    from telepulestipus
    where regio = 'Fejér'
      and lakastipus = 'Használt lakások'
),

final as (
    select
        a.idoszak,
        a.ev,
        a.negyedev,
        a.osszevont_index,
        a.tiszta_ar_haszn,
        a.tiszta_ar_uj,
        b.budapest_atlagár_mFt,
        o.orszagos_atlagár_mFt,
        f.fejer_atlagár_mFt
    from arindex a
    left join budapest b on a.idoszak = b.idoszak
    left join orszagos o on a.idoszak = o.idoszak
    left join fejer f on a.idoszak = f.idoszak
)

select * from final