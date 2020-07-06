CREATE VIEW cagg_rides_view WITH
(timescaledb.continuous, timescaledb.refresh_interval = '30m')
AS
SELECT vendor_id, time_bucket('1h', pickup_datetime) as day,
     count(*) total_rides,
     avg(fare_amount) avg_fare,
     max(trip_distance) as max_trip_distance,
     min(trip_distance) as min_trip_distance
FROM rides
GROUP BY vendor_id, time_bucket('1h', pickup_datetime);
