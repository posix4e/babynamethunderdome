import { api } from "npm:@nitric/sdk";

const mainApi = api("main");

mainApi.get("/hello", (ctx) => {
  ctx.res.body = { message: "Hello, World!" };
  return ctx;
});
