import { assertEquals } from "https://deno.land/std/testing/asserts.ts";
import { api } from "npm:@nitric/sdk";

const mainApi = api("main");

Deno.test("Create name list", async () => {
  const ctx = {
    req: {
      json: async () => await Promise.resolve({ name: "Test List" }),
    },
    res: {},
    security: { subject: 1 },
  };

  const response = await mainApi.post("/api/lists")(ctx);
  assertEquals(typeof response.res.body.id, "number");
});

Deno.test("Add name to list", async () => {
  const ctx = {
    req: {
      json: async () => await Promise.resolve({ listId: 1, name: "John" }),
    },
    res: {},
  };

  const response = await mainApi.post("/api/names")(ctx);
  assertEquals(typeof response.res.body.id, "number");
});

Deno.test("Get names from list", async () => {
  const ctx = {
    req: {
      params: { listId: "1" },
    },
    res: {},
  };

  const response = await mainApi.get("/api/lists/:listId/names")(ctx);
  assertEquals(Array.isArray(response.res.body), true);
});
