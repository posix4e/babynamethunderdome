# Deno Nitric Authentication Example

This is a simple example of a Deno application with authentication using JWT
tokens.

## Features

- User registration
- User login with JWT token generation
- Protected routes using JWT authentication
- In-memory user storage (can be replaced with a database)

## Prerequisites

- Deno installed on your system

## Running the Application

1. Start the server:
   ```bash
   deno task dev
   ```

2. The server will run on http://localhost:8000

## API Endpoints

### Register User

```http
POST /register
Content-Type: application/json

{
  "username": "your_username",
  "password": "your_password"
}
```

### Login

```http
POST /login
Content-Type: application/json

{
  "username": "your_username",
  "password": "your_password"
}
```

### Access Protected Route

```http
GET /protected
Authorization: Bearer your_jwt_token
```

## Running Tests

```bash
deno test --allow-net test.ts
```

## Security Notes

This is a basic example and includes several simplifications that should not be
used in production:

1. Uses in-memory storage instead of a proper database
2. Has a hardcoded JWT secret
3. Lacks input validation and rate limiting
4. Missing proper error handling

For production use, make sure to:

1. Use a proper database
2. Implement secure secret management
3. Add input validation
4. Implement rate limiting
5. Add proper error handling
6. Use HTTPS
7. Implement password complexity requirements
