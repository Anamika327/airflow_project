select
    id as order_id,
    customerId as customer_id,
    employeeId as employee_id,

    cast(orderDate as date) as order_date,
    cast(requiredDate as date) as required_date,
    cast(shippedDate as date) as shipped_date,

    shipVia as ship_via,
    freight,
    shipName as ship_name,

    shipAddress as ship_address,
    details,

    ingested_at

from {{ source('bronze', 'raw_orders') }}
