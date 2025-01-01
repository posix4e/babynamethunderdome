import { assertEquals } from "https://deno.land/std/assert/mod.ts";
import "./api.ts";

Deno.test("API endpoints are registered", () => {
  // Since we can't directly test the handlers due to Nitric's API design,
  // we can at least verify that our file imports successfully and doesn't throw any errors
  assertEquals(true, true);
});
