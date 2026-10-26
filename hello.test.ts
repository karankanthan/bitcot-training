import { describe, expect, it } from "vitest";

describe("hello world", () => {
  it("runs a typed test", () => {
    const greeting: string = "hello" + " " + "world";
    expect(greeting).toBe("hello world");
  });
});