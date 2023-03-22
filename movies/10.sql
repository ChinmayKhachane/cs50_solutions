SELECT name FROM people
JOIN movies ON directors.movie_id=movies.id
JOIN directors ON directors.person_id=people.id
JOIN ratings ON ratings.movie_id=movies.id
WHERE ratings.rating >= 9;