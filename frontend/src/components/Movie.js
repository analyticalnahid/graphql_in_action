import { useState, useEffect } from "react";
import { useQuery } from "@apollo/client";
import { GET_ALL_MOVIES, GET_MOVIE_BY_ID } from "../query/query";

function Movie() {
  const [allMovies, setAllMovies] = useState([]);
  const [selectedMovie, setSelectedMovie] = useState(null);

  const { loading: allMoviesLoading, data: allMoviesData } =
    useQuery(GET_ALL_MOVIES);
  const { loading: movieByIdLoading, data: movieByIdData } = useQuery(
    GET_MOVIE_BY_ID,
    {
      variables: { id: selectedMovie },
      skip: !selectedMovie,
    }
  );

  useEffect(() => {
    if (allMoviesData) {
      setAllMovies(allMoviesData.allMovies);
    }
  }, [allMoviesData]);

  const handleMovieClick = (id) => {
    setSelectedMovie(id);
  };

  return (
    <div>
      <h1>All Movies</h1>
      {allMoviesLoading ? (
        <p>Loading movies...</p>
      ) : (
        <ul>
          {allMovies.map((movie) => (
            <li key={movie.id} onClick={() => handleMovieClick(movie.id)}>
              {movie.title} ({movie.year}) - Directed by {movie.director.name}
            </li>
          ))}
        </ul>
      )}

      <h2>Selected Movie</h2>
      {movieByIdLoading ? (
        <p>Loading movie...</p>
      ) : movieByIdData && movieByIdData.movie ? (
        <div>
          <h3>{movieByIdData.movie.title}</h3>
          <p>Year: {movieByIdData.movie.year}</p>
          <p>Director: {movieByIdData.movie.director.name}</p>
        </div>
      ) : (
        <p>No movie selected.</p>
      )}
    </div>
  );
}

export default Movie;
