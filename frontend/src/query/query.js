import {
  ApolloClient,
  InMemoryCache,
  createHttpLink,
  gql,
  concat,
  ApolloLink,
} from "@apollo/client";
import Cookies from "js-cookie";

const httpLink = createHttpLink({
  uri: "http://localhost:8000/graphql/",
  credentials: "same-origin",
});

const csrfMiddleware = new ApolloLink((operation, forward) => {
  operation.setContext(({ headers = {} }) => ({
    headers: {
      ...headers,
      "X-CSRFTOKEN": Cookies.get("csrftoken"),
    },
  }));

  return forward(operation);
});

export const client = new ApolloClient({
  link: concat(csrfMiddleware, httpLink),
  cache: new InMemoryCache(),
});

export const GET_ALL_MOVIES = gql`
  query {
    allMovies {
      id
      title
      year
    }
  }
`;

export const GET_MOVIE_BY_ID = gql`
  query ($id: Int!) {
    movie(id: $id) {
      id
      title
      year
    }
  }
`;

export default client;
