
export type Priority = "urgent" | "high" | "normal" | "low";

export interface Ticket {
  ticket_id: string;
  priority: Priority;
  created_at: string;
  resolved_at?: string | null;
}

export interface SLAResult {
  ticket_id: string;
  breached: boolean;
  elapsed_hours: number;
  hours_over: number;
}

export const SLA_HOURS: Record<Priority, number> = {
  urgent: 4,
  high: 8,
  normal: 24,
  low: 72,
};

export function checkSLA(
  ticket: Ticket,
  at: string = new Date().toISOString(),
): SLAResult {
  const start = new Date(ticket.created_at).getTime();
  const end = new Date(ticket.resolved_at || at).getTime();

  if (!Number.isFinite(start) || !Number.isFinite(end)) {
    throw new Error("Invalid ticket date");
  }

  if (end < start) {
    throw new Error("Check time cannot be before ticket creation");
  }

  const elapsed = (end - start) / (1000 * 60 * 60);
  const target = SLA_HOURS[ticket.priority];

  return {
    ticket_id: ticket.ticket_id,
    breached: elapsed > target,
    elapsed_hours: Number(elapsed.toFixed(2)),
    hours_over: Number(Math.max(0, elapsed - target).toFixed(2)),
  };
}
