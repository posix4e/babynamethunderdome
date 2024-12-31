import { api } from "npm:@nitric/sdk";

const helloApi = api("main");
helloApi.get("/hello/:name", (ctx) => {
  const { name } = ctx.req.params;
  ctx.res.body = `Hello ${name}`;
  return ctx;
});
