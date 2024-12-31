import { Application, Router } from "oak";
import { create, getNumericDate, verify } from "djwt";
import { compare, hash } from "bcrypt";

// In-memory user storage (replace with a proper database in production)
const users = new Map<string, { password: string }>();

// JWT secret key (use a proper secret management in production)
const key = await crypto.subtle.generateKey(
  { name: "HMAC", hash: "SHA-256" },
  true,
  ["sign", "verify"],
);

const router = new Router();

// Register endpoint
router.post("/register", async (ctx) => {
  const body = await ctx.request.body().value;
  const { username, password } = body;

  if (!username || !password) {
    ctx.response.status = 400;
    ctx.response.body = { error: "Username and password are required" };
    return;
  }

  if (users.has(username)) {
    ctx.response.status = 409;
    ctx.response.body = { error: "Username already exists" };
    return;
  }

  const hashedPassword = await hash(password);
  users.set(username, { password: hashedPassword });

  ctx.response.status = 201;
  ctx.response.body = { message: "User registered successfully" };
});

// Login endpoint
router.post("/login", async (ctx) => {
  const body = await ctx.request.body().value;
  const { username, password } = body;

  if (!username || !password) {
    ctx.response.status = 400;
    ctx.response.body = { error: "Username and password are required" };
    return;
  }

  const user = users.get(username);
  if (!user) {
    ctx.response.status = 401;
    ctx.response.body = { error: "Invalid credentials" };
    return;
  }

  const isValid = await compare(password, user.password);
  if (!isValid) {
    ctx.response.status = 401;
    ctx.response.body = { error: "Invalid credentials" };
    return;
  }

  // Create JWT token
  const token = await create(
    { alg: "HS256", typ: "JWT" },
    { username, exp: getNumericDate(60 * 60 * 24) }, // 24 hours expiry
    key,
  );

  ctx.response.body = { token };
});

// Protected endpoint example
router.get("/protected", async (ctx) => {
  const authHeader = ctx.request.headers.get("Authorization");
  if (!authHeader || !authHeader.startsWith("Bearer ")) {
    ctx.response.status = 401;
    ctx.response.body = { error: "No token provided" };
    return;
  }

  const token = authHeader.split(" ")[1];
  try {
    const payload = await verify(token, key);
    ctx.response.body = {
      message: "Protected data",
      user: payload.username,
    };
  } catch (error) {
    ctx.response.status = 401;
    ctx.response.body = { error: "Invalid token" };
  }
});

const app = new Application();
app.use(router.routes());
app.use(router.allowedMethods());

console.log("Server running on http://localhost:8000");
await app.listen({ port: 8000 });
