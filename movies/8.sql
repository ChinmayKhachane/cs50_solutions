SELECT NAME FROM people
JOIN movies ON stars.movie_id=movies.id
JOIN stars ON stars.person_id=people.id
WHERE movies.title="Toy Story";