import { api, database } from "npm:@nitric/sdk";

const mainApi = api("main");
const namesDb = database("names").ref();

// Serve static files
mainApi.get("/", async (ctx) => {
  const content = await Deno.readFile("./public/index.html");
  ctx.res.headers["Content-Type"] = "text/html";
  ctx.res.body = content;
  return ctx;
});

// Create a new name list
mainApi.post("/api/lists", async (ctx) => {
  const { name } = await ctx.req.json();
  const userId = ctx.security?.subject || 1; // TODO: Get actual user ID from auth

  const result = await namesDb.query(
    "INSERT INTO name_lists (user_id, name) VALUES ($1, $2) RETURNING id",
    [userId, name],
  );

  ctx.res.body = { id: result.rows[0].id };
  return ctx;
});

// Add a name to a list
mainApi.post("/api/names", async (ctx) => {
  const { listId, name } = await ctx.req.json();

  const result = await namesDb.query(
    "INSERT INTO names (list_id, name) VALUES ($1, $2) RETURNING id",
    [listId, name],
  );

  ctx.res.body = { id: result.rows[0].id };
  return ctx;
});

// Get names from a list
mainApi.get("/api/lists/:listId/names", async (ctx) => {
  const listId = ctx.req.params.listId;

  const result = await namesDb.query(
    "SELECT name, rank FROM names WHERE list_id = $1 ORDER BY rank DESC",
    [listId],
  );

  ctx.res.body = result.rows;
  return ctx;
});
