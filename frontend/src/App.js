import { ApolloProvider } from "@apollo/client";
import MovieList from "./components/MovieList";
import client from "./query/query";

function App() {
  return (
    <ApolloProvider client={client}>
      <MovieList />
    </ApolloProvider>
  );
}

export default App;
