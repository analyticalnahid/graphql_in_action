# Relay CRUD and Authentication

Here is an example structure for client-side queries and mutations using Relay and Graphene. It demonstrates how to perform CRUD operations and incorporate authentication in a GraphQL API.

## Structure Overview

The client-side structure includes queries and mutations for various operations. Below is an overview of the available queries and mutations:

## Table of Contents

- [Queries](#queries)
- [Mutation](#mutations)
- [Contributing](#contributing)
- [License](#license)

## Queries

#### GetAllMovies
```bash
query GetAllMovies {
  allMovies(year_Icontains: 2025) {
    edges {
      node {
        id
        title
        year
        director {
          name
          surname
        }
      }
    }
  }
}
```

#### GetAllDirectors
```bash
query GetAllDirectors {
  allDirectors {
    edges {
      node {
        id
        name
        surname
      }
    }
  }
}

```

#### GetSingleMovie
```bash
query GetSingleMovie {
  movie(id: "TW92aWVOb2RlOjU=") {
    id
    title
    year
  }
}

```

## Mutation

#### addMovie
```bash
mutation addMovie {
  createMovie(input: {title: "Matrix 4", year: 2025}) {
    movie {
      id
      title
      year
    }
  }
}

```

#### updateMovie
```bash
mutation updateMovie {
  updateMovie(
    input: {title: "Matrix 00", movieId: "TW92aWVOb2RlOjE1", year: 2025}
  ) {
    movie {
      id
      title
      year
    }
  }
}

```

#### GetToken
```bash
mutation GetToken {
  tokenAuth(input: {username: "nahid", password: "nahid123"}) {
    token
  }
}

```

#### VerifyToken
```bash
mutation VerifyToken {
  verifyToken(
    input: {token: "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6Im5haGlkIiwiZXhwIjoxNjg1NzMyNzA4LCJvcmlnSWF0IjoxNjg1NzMyNDA4fQ.N34zbPuNfH76PxL20OGI_CoCAOnaMXCwPojrJhJrPdo"}
  ) {
    payload
  }
}

```

#### deleteToken
```bash
mutation deleteToken {
  deleteTokenCookie {
    deleted
  }
}

```
#### GetRefreshToken
```bash
mutation GetRefreshToken {
  refreshToken(
    input: {token: "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6Im5haGlkIiwiZXhwIjoxNjg1NzIxNTExLCJvcmlnSWF0IjoxNjg1NzIxMjExfQ.mk5U38LISvvIIyfxt3iU5b5fmcwJKwd_Sy9eNIWQJwA"}
  ) {
    token
  }
}
```

#### RevokeToken
```bash
mutation RevokeToken {
  revokeToken(
    input: {refreshToken: "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6Im5haGlkIiwiZXhwIjoxNjg1NzIxNTg0LCJvcmlnSWF0IjoxNjg1NzIxMjExfQ.C59fXcdq7X2ojcS79NJRruNAXa4lnXcqWO8k5zFUnPE"}
  ) {
    revoked
  }
}

```

## Pagination

```bash
query GetAllMovies {
  allMovies(first:1 after: "YXJyYXljb25uZWN0aW9uOjE=") {
    pageInfo{
      startCursor
      endCursor
      hasNextPage
      hasPreviousPage
    }
    edges {
      cursor
      node {
        id
        title
        year
        director {
          name
          surname
        }
      }
    }
  }
}

```

## Contributing

Contributions to this project are welcome. If you find any issues or have suggestions for improvements, feel free to open an issue or submit a pull request. Please make sure to follow the code of conduct.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more information.
