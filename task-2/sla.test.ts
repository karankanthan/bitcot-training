
import { describe, expect, it } from "vitest";
import { checkSLA } from "./sla";

describe("checkSLA", () => {
  it("does not breach when a ticket is resolved within the target", () => {
    const result = checkSLA(
      {
        ticket_id: "T1",
        priority: "urgent",
        created_at: "2026-03-02T09:00:00Z",
        resolved_at: "2026-03-02T12:00:00Z",
      },
      "2026-03-02T13:00:00Z",
    );

    expect(result.breached).toBe(false);
    expect(result.elapsed_hours).toBe(3);
    expect(result.hours_over).toBe(0);
  });

  it("does not breach exactly at the SLA limit", () => {
    const result = checkSLA(
      {
        ticket_id: "T2",
        priority: "urgent",
        created_at: "2026-03-02T09:00:00Z",
        resolved_at: "2026-03-02T13:00:00Z",
      },
      "2026-03-02T14:00:00Z",
    );

    expect(result.breached).toBe(false);
    expect(result.hours_over).toBe(0);
  });

  it("reports how many hours the ticket exceeded its SLA", () => {
    const result = checkSLA(
      {
        ticket_id: "T3",
        priority: "urgent",
        created_at: "2026-03-02T09:00:00Z",
      },
      "2026-03-02T14:30:00Z",
    );

    expect(result.breached).toBe(true);
    expect(result.elapsed_hours).toBe(5.5);
    expect(result.hours_over).toBe(1.5);
  });

  it("uses the correct target for a low-priority ticket", () => {
    const result = checkSLA(
      {
        ticket_id: "T4",
        priority: "low",
        created_at: "2026-03-02T09:00:00Z",
      },
      "2026-03-05T10:00:00Z",
    );

    expect(result.breached).toBe(true);
    expect(result.hours_over).toBe(1);
  });

  it("rejects invalid dates", () => {
    expect(() =>
      checkSLA(
        {
          ticket_id: "T5",
          priority: "normal",
          created_at: "not-a-date",
        },
        "2026-03-02T12:00:00Z",
      ),
    ).toThrow("Invalid ticket date");
  });
});
