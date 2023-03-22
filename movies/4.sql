SELECT COUNT(movies.id) from movies
JOIN ratings ON movies.id = ratings.movie_id
WHERE rating = 10;