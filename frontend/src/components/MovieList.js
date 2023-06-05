import React, { useState, useEffect } from "react";
import { useQuery } from "@apollo/client";
import { GET_ALL_MOVIES } from "../query/query";

function MovieList() {
  const [selectallMovies, setSelectAllMovies] = useState({});

  const {
    loading: allMoviesLoading,
    error: allMoviesError,
    data: allMoviesData,
  } = useQuery(GET_ALL_MOVIES);

  const handleMovieClick = (id) => {
    console.log(id);
  };

  useEffect(() => {
    if (allMoviesData) {
      setSelectAllMovies(allMoviesData);
    }
  }, [allMoviesData]);

  return (
    <div>
      <h1>All Movies</h1>
      {allMoviesError && <p>Somethings went wrong {allMoviesError.message}</p>}
      {allMoviesLoading && !allMoviesError ? (
        <p>Loading movies...</p>
      ) : (
        <ul>
          {selectallMovies?.allMovies?.map((movie) => (
            <li key={movie.id} onClick={() => handleMovieClick(movie.id)}>
              {movie.title} ({movie.year})
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}

export default MovieList;
