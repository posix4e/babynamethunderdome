import { api } from "npm:@nitric/sdk";

const mainApi = api("main");

// Serve static files
mainApi.get("/", async (ctx) => {
  const content = await Deno.readFile("./public/index.html");
  ctx.res.headers = { "Content-Type": ["text/html"] };
  ctx.res.body = content;
  return ctx;
});

// Create a new name list
mainApi.post("/api/lists", async (ctx) => {
  const { name } = await ctx.req.json();
  const userId = 1; // TODO: Get actual user ID from auth

  ctx.res.body = { id: 1 };
  return ctx;
});

// Add a name to a list
mainApi.post("/api/names", async (ctx) => {
  const { listId, name } = await ctx.req.json();

  ctx.res.body = { id: 1 };
  return ctx;
});

// Get names from a list
mainApi.get("/api/lists/:listId/names", async (ctx) => {
  const listId = ctx.req.params.listId;

  ctx.res.body = [];
  return ctx;
});
