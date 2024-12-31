import { assertEquals, assertNotEquals } from "https://deno.land/std@0.208.0/assert/mod.ts";

const API_URL = "http://localhost:4001";

Deno.test("Authentication Flow", async (t) => {
  const testUser = {
    username: "testuser_" + Math.random().toString(36).substring(7),
    password: "testpass123",
  };

  await t.step("Register user", async () => {
    const response = await fetch(`${API_URL}/register`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(testUser),
    });

    assertEquals(response.status, 201);
    const data = await response.json();
    assertEquals(data.message, "User registered successfully");
  });

  await t.step("Register duplicate user should fail", async () => {
    const response = await fetch(`${API_URL}/register`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(testUser),
    });

    assertEquals(response.status, 409);
    const data = await response.json();
    assertEquals(data.error, "Username already exists");
  });

  await t.step("Login with valid credentials", async () => {
    const response = await fetch(`${API_URL}/login`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(testUser),
    });

    assertEquals(response.status, 200);
    const data = await response.json();
    assertEquals(data.message, "Login successful");
    assertNotEquals(data.user.id, undefined);
    assertEquals(data.user.username, testUser.username);
  });

  await t.step("Login with invalid password", async () => {
    const response = await fetch(`${API_URL}/login`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        username: testUser.username,
        password: "wrongpassword",
      }),
    });

    assertEquals(response.status, 401);
    const data = await response.json();
    assertEquals(data.error, "Invalid username or password");
  });

  await t.step("Access protected endpoint with auth", async () => {
    const response = await fetch(`${API_URL}/me`, {
      headers: {
        Authorization: `Bearer ${testUser.username}`,
      },
    });

    assertEquals(response.status, 200);
    const data = await response.json();
    assertEquals(data.user.username, testUser.username);
  });

  await t.step("Access protected endpoint without auth", async () => {
    const response = await fetch(`${API_URL}/me`);

    assertEquals(response.status, 401);
    const data = await response.json();
    assertEquals(data.error, "Authentication required");
  });
});
