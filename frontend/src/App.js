import { ApolloProvider } from "@apollo/client";
import { client } from "./query/query";
import Movie from "./components/Movie";

function App() {
  return (
    <ApolloProvider client={client}>
      <Movie />
    </ApolloProvider>
  );
}

export default App;
