-- What's the total number of rides that took place everyday
SELECT date_trunc('day', pickup_datetime) as day, COUNT(*) FROM rides GROUP BY day ORDER BY day;

-- What is the daily average fare amount for rides with only one passenger
-- for first 7 days?
SELECT date_trunc('day', pickup_datetime)
AS day, avg(fare_amount)
FROM rides
WHERE passenger_count = 1
AND pickup_datetime < '2016-01-08'
GROUP BY day ORDER BY day;

-- How many rides of each rate type took place in the month?
SELECT rate_code, COUNT(vendor_id) AS num_trips
FROM rides
WHERE pickup_datetime < '2016-02-01'
GROUP BY rate_code
ORDER BY rate_code;

-- How many rides of each rate type took place?
-- Join rides with rates to get more information on rate_code
SELECT rates.description, COUNT(vendor_id) AS num_trips FROM rides
JOIN rates ON rides.rate_code = rates.rate_code
WHERE pickup_datetime < '2016-02-01'
GROUP BY rates.description
ORDER BY rates.description;

-- For each airport: num trips, avg trip duration, avg cost, avg tip, avg distance, min distance, max distance, avg number of passengers
SELECT rates.description, COUNT(vendor_id) AS num_trips,
   AVG(dropoff_datetime - pickup_datetime) AS avg_trip_duration, AVG(total_amount) AS avg_total,
   AVG(tip_amount) AS avg_tip, MIN(trip_distance) AS min_distance, AVG (trip_distance) AS avg_distance, MAX(trip_distance) AS max_distance,
   AVG(passenger_count) AS avg_passengers
 FROM rides
 JOIN rates ON rides.rate_code = rates.rate_code
 WHERE rides.rate_code IN (2,3) AND pickup_datetime < '2016-02-01'
 GROUP BY rates.description
 ORDER BY rates.description;

-- USEFUL MONITORING QUERIES

-- How many rides took place every 5 minutes for the first day of 2016?
-- using the TimescaleDB "time_bucket" function
SELECT time_bucket('5 minute', pickup_datetime) AS five_min, count(*)
FROM rides
WHERE pickup_datetime < '2016-01-02 00:00'
GROUP BY five_min
ORDER BY five_min;


