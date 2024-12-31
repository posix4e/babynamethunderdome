import { assertEquals } from "https://deno.land/std@0.208.0/assert/mod.ts";

// Test data
const TEST_USER = {
  username: "testuser",
  password: "testpass123"
};

// Test server URL
const SERVER_URL = "http://localhost:8000";

Deno.test("Authentication Flow", async (t) => {
  await t.step("Register user", async () => {
    const response = await fetch(`${SERVER_URL}/register`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(TEST_USER)
    });

    assertEquals(response.status, 201);
    const data = await response.json();
    assertEquals(data.message, "User registered successfully");
  });

  await t.step("Login user", async () => {
    const response = await fetch(`${SERVER_URL}/login`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(TEST_USER)
    });

    assertEquals(response.status, 200);
    const data = await response.json();
    assertEquals(typeof data.token, "string");
  });

  await t.step("Access protected endpoint", async () => {
    // First login to get token
    const loginResponse = await fetch(`${SERVER_URL}/login`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(TEST_USER)
    });
    const { token } = await loginResponse.json();

    // Test protected endpoint
    const response = await fetch(`${SERVER_URL}/protected`, {
      headers: { "Authorization": `Bearer ${token}` }
    });

    assertEquals(response.status, 200);
    const data = await response.json();
    assertEquals(data.user, TEST_USER.username);
  });
});
