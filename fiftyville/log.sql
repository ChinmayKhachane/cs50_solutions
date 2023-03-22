SELECT description FROM crime_scene_reports WHERE year = 2021 AND month = 7 AND day = 28 AND street = "Humphrey Street";
-- Get information on crime

SELECT transcript FROM interviews WHERE year = 2021 AND month = 7 AND day = 28 AND transcript LIKE "&bakery%";
-- Check for info at interviews, where 4 transcripts show up

SELECT name FROM people JOIN bakery_security_logs ON bakery_security_logs.license_plate = people.license_plate
WHERE year = 2021 AND month = 7 AND day = 28 AND hour = 10 AND minute >= 15 AND minute <= 25 and activity = "exit";
-- Get names of suspects based on license plate

SELECT name FROM people
JOIN bank_accounts ON people.id = bank_accounts.person_id
JOIN atm_transactions ON bank_accounts.account_number = atm_transactions.account_number
WHERE atm_location = "Leggett Street" AND transaction_type = "withdraw" AND year = 2021 AND month = 7 AND day = 28;
-- Get names of suspects based on atm_transcations that took place

SELECT name FROM people
JOIN passengers ON people.passport_number = passengers.passport_number
WHERE passenger.flight_id = (SELECT id FROM flights WHERE year = 2021 AND month = 7 AND day = 29 AND origin_airport_id =
(SELECT id FROM airports WHERE city = "Fiftyville") ORDER BY hour,minute LIMIT 1);
--Get names of suspects from earliest flight originating from Fiftyville

SELECT city FROM airports
WHERE id = (SELECT destination_airport_id FROM flights WHERE year = 2021 AND month = 7 AND day = 29 AND origin_airport_id = (SELECt id FROM airports WHERE city = "Fiftyville")
ORDER BY hour,minute LIMIT 1);
--Get destination of all possible suspects

SELECT name FROM people
JOIN phone_calls ON phone_calls.caller = people.phone_number
WHERE year = 2021 AND month = 7 AND day = 28 AND duration < 60;
-- Get names of phone calls on the fateful day that lasted less than a minute

SELECT name FROM people
JOIN phone_calls ON phone_calls.receiver = people.phone_number
WHERE year = 2021 AND month = 7 AND day = 28 AND duration < 60 AND caller = (SELECT phone_number FROM people WHERE name = "Bruce");
--Get name of Bruce accomplice