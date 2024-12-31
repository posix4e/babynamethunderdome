import { api, sql } from "npm:@nitric/sdk";
import { compare, hash } from "https://deno.land/x/bcrypt@v0.4.1/mod.ts";
import * as postgres from "https://deno.land/x/postgres@v0.17.0/mod.ts";

// Initialize the API and database
const authApi = api("main");
const authDb = sql("auth", {
  migrations: "file://migrations/auth",
});

// Helper function to create a database client
async function createDbClient() {
  const connString = await authDb.connectionString();

  // Parse connection string to get required parameters
  const url = new URL(connString);
  const params = {
    database: url.pathname.slice(1), // Remove leading slash
    hostname: url.hostname,
    port: parseInt(url.port || "5432"),
    user: url.username,
    password: url.password,
  };

  return new postgres.Client(params);
}

// Initialize the database schema
const dbClient = await createDbClient();
await dbClient.connect();

// Create users table if it doesn't exist
await dbClient.queryObject`
  CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
  );
`;

await dbClient.end();

// Register endpoint
authApi.post("/register", async (ctx) => {
  const { username, password } = await ctx.req.json();

  // Validate input
  if (!username || !password) {
    ctx.res.status = 400;
    ctx.res.body = { error: "Username and password are required" };
    return ctx;
  }

  try {
    // Hash the password
    const passwordHash = await hash(password);

    // Connect to database
    const client = await createDbClient();
    await client.connect();

    try {
      // Insert the user
      await client.queryObject`
        INSERT INTO users (username, password_hash)
        VALUES (${username}, ${passwordHash})
      `;

      ctx.res.status = 201;
      ctx.res.body = { message: "User registered successfully" };
    } catch (_error) {
      // Check for unique constraint violation
      if (_error.message?.includes("unique constraint")) {
        ctx.res.status = 409;
        ctx.res.body = { error: "Username already exists" };
      } else {
        ctx.res.status = 500;
        ctx.res.body = { error: "Internal server error" };
      }
    } finally {
      await client.end();
    }
  } catch (_error) {
    ctx.res.status = 500;
    ctx.res.body = { error: "Internal server error" };
  }

  return ctx;
});

// Login endpoint
authApi.post("/login", async (ctx) => {
  const { username, password } = await ctx.req.json();

  // Validate input
  if (!username || !password) {
    ctx.res.status = 400;
    ctx.res.body = { error: "Username and password are required" };
    return ctx;
  }

  try {
    // Connect to database
    const client = await createDbClient();
    await client.connect();

    try {
      // Get user from database
      const result = await client.queryObject<{
        id: number;
        username: string;
        password_hash: string;
      }>`
        SELECT id, username, password_hash
        FROM users
        WHERE username = ${username}
      `;

      const user = result.rows[0];

      // Check if user exists and password matches
      if (!user || !(await compare(password, user.password_hash))) {
        ctx.res.status = 401;
        ctx.res.body = { error: "Invalid username or password" };
        return ctx;
      }

      // Create a session (you might want to use a session store or JWT in production)
      ctx.res.body = {
        message: "Login successful",
        user: {
          id: user.id,
          username: user.username,
        },
      };
    } finally {
      await client.end();
    }
  } catch (_error) {
    ctx.res.status = 500;
    ctx.res.body = { error: "Internal server error" };
  }

  return ctx;
});

// Protected endpoint example
authApi.get("/me", async (ctx) => {
  // In a real application, you would validate a session token or JWT here
  const authHeader = ctx.req.headers.get("authorization");

  if (!authHeader) {
    ctx.res.status = 401;
    ctx.res.body = { error: "Authentication required" };
    return ctx;
  }

  // For now, we'll just check if the user exists
  const username = authHeader.replace("Bearer ", "");

  try {
    // Connect to database
    const client = await createDbClient();
    await client.connect();

    try {
      const result = await client.queryObject<{
        id: number;
        username: string;
        created_at: Date;
      }>`
        SELECT id, username, created_at
        FROM users
        WHERE username = ${username}
      `;

      const user = result.rows[0];
      if (!user) {
        ctx.res.status = 401;
        ctx.res.body = { error: "Invalid authentication" };
        return ctx;
      }

      ctx.res.body = {
        user: {
          id: user.id,
          username: user.username,
          created_at: user.created_at,
        },
      };
    } finally {
      await client.end();
    }
  } catch (_error) {
    ctx.res.status = 500;
    ctx.res.body = { error: "Internal server error" };
  }

  return ctx;
});
