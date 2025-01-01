# Baby Name Thunderdome

A collaborative baby name selection platform built with Deno and Nitric. Help parents choose the
perfect name through a fun and interactive voting system.

## Features

- **For Parents**:
  - Create and manage lists of potential baby names
  - Invite friends and family to participate in name selection
  - View voting results and rankings
  - Secure account management

- **For Friends & Family**:
  - Easy-to-use voting interface
  - Compare names in head-to-head matchups
  - No account required for voting
  - Share feedback on name choices

- **Technical Features**:
  - Secure user authentication with JWT
  - Persistent data storage
  - RESTful API design
  - Rate limiting and security measures

## Prerequisites

1. **Required Tools**:
   - Deno v2.1.4 or later
   - Node.js v18.x or later
   - Nitric CLI v0.1.0 or later

2. **Installation**:
   ```bash
   # Install Deno
   curl -fsSL https://deno.land/x/install/install.sh | sh

   # Install Node.js (using nvm)
   curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.0/install.sh | bash
   nvm install 18
   nvm use 18

   # Install Nitric CLI
   npm install -g @nitric/cli
   ```

## Development

1. **Start the Development Server**:
   ```bash
   nitric start
   ```
   The server will be available at http://localhost:8000

2. **Code Formatting**:
   ```bash
   deno fmt
   ```

3. **Linting**:
   ```bash
   deno lint
   ```

## API Endpoints

### Authentication

```http
# Register New Parent Account
POST /auth/register
Content-Type: application/json
{
  "email": "parent@example.com",
  "password": "secure_password",
  "name": "Parent Name"
}

# Login
POST /auth/login
Content-Type: application/json
{
  "email": "parent@example.com",
  "password": "secure_password"
}
```

### Name Management

```http
# Add Names to List
POST /names
Authorization: Bearer <token>
Content-Type: application/json
{
  "names": ["Name1", "Name2", "Name3"]
}

# Get Voting Results
GET /names/results
Authorization: Bearer <token>
```

### Voting

```http
# Get Name Pair for Voting
GET /vote/<voting_id>

# Submit Vote
POST /vote/<voting_id>
Content-Type: application/json
{
  "winner": "Name1",
  "loser": "Name2"
}
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
   - Follow the code style guidelines
   - Add tests for new features
   - Run existing tests
4. Submit a pull request

## Security Considerations

- All endpoints require appropriate authentication
- Rate limiting is implemented on all routes
- Input validation and sanitization
- Secure password hashing
- HTTPS required in production
- Environment-based configuration

## License

[MIT License](LICENSE)
