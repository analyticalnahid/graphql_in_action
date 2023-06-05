# Graphene Auth

Here is an example structure for client-side queries and mutations using Relay and Graphene. It demonstrates how to perform CRUD operations and incorporate authentication in a GraphQL API.

## Structure Overview

The client-side structure includes queries and mutations for various operations. Below is an overview of the available queries and mutations:

## Table of Contents

- [Queries](#queries)
- [Mutation](#mutation)
- [Pagination](#pagination)
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

## Mutation

#### Register
```bash
mutation SingupAccount{
  register(
    email:"skywalker@email.com",
    username:"skywalker",
    password1: "qlr4nq3f3",
    password2:"qlr4nq3f3"
  ) {
    success,
    errors,
    token,
    refreshToken
  }
}

```

#### VerifyAccount
```bash
mutation {
  verifyAccount(
    token:"eyJ1c2VybmFtZSI6InNreXdhbGtlciIsImFjdGlvbiI6ImFjdGl2YXRpb24ifQ:1itC5A:vJhRJwBcrNxvmEKxHrZa6Yoqw5Q",
  ) {
    success, errors
  }
}

```

#### ObtainJSONWebToken (Login)
```bash
mutation {
  tokenAuth(
    # username or email
    email: "skywalker@email.com"
    password: "123456super"
  ) {
    success,
    errors,
    token,
    refreshToken,
    unarchiving,
    user {
      id,
      username
    }
  }
}

```

#### SendPasswordResetEmail (Forget Password)
```bash
mutation {
  sendPasswordResetEmail(
    email: "skywalker@email.com"
  ) {
    success,
    errors
  }
}

```

#### PasswordReset (After Activation Link)
```bash
mutation {
  passwordReset(
    token: "1eyJ1c2VybmFtZSI6InNreXdhbGtlciIsImFjdGlvbiI6InBhc3N3b3JkX3Jlc2V0In0:1itExL:op0roJi-ZbO9cszNEQMs5mX3c6s",
    newPassword1: "supersecretpassword",
    newPassword2: "supersecretpassword"
  ) {
    success,
    errors
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

## Introspection Schema
```bash
./manage.py --out schema.json

GRAPHENE = {
    'SCHEMA': 'tutorial.quickstart.schema',
    'SCHEMA_OUTPUT': 'data/schema.json',  # defaults to schema.json,
    'SCHEMA_INDENT': 2,  # Defaults to None (displays all data on a single line)
}
```



## Contributing

Contributions to this project are welcome. If you find any issues or have suggestions for improvements, feel free to open an issue or submit a pull request. Please make sure to follow the code of conduct.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more information.
