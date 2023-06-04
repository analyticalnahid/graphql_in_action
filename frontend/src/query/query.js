import {
  ApolloClient,
  InMemoryCache,
  gql,
} from "@apollo/client";

export const client = new ApolloClient({
  uri: "http://localhost:8000/graphql/",
  cache: new InMemoryCache(),
});

export const GET_ALL_MOVIES = gql`
query {
  allMovies {
    id
    title
    year
    director {
      name
      surname
    }
  }
}
`;

export const GET_MOVIE_BY_ID = gql`
  query ($id: Int!) {
    movie(id: $id) {
      id
      title
      year
      director {
        name
      }
    }
  }
`;
