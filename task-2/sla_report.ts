
import { readFileSync } from "node:fs";
import { resolve } from "node:path";
import { checkSLA, type Priority } from "./sla";

const csvPath = resolve(
  process.argv[2] ?? resolve(__dirname, "tickets.csv"),
);

const csv = readFileSync(csvPath, "utf-8");
const lines = csv.trim().split(/\r?\n/);

if (lines.length < 2) {
  console.log("No ticket records found.");
  process.exit(0);
}

const headers = lines[0].split(",").map((header) => header.trim());
const column = (name: string) => headers.indexOf(name);

const idIndex = column("ticket_id");
const createdIndex = column("created_at");
const resolvedIndex = column("resolved_at");
const priorityIndex = column("priority");
const statusIndex = column("status");

if ([idIndex, createdIndex, resolvedIndex, priorityIndex, statusIndex].some((i) => i < 0)) {
  throw new Error("CSV is missing a required column.");
}

const targets: Record<Priority, number> = {
  urgent: 4,
  high: 8,
  normal: 24,
  low: 72,
};

const now = new Date();
let checked = 0;
let breached = 0;

for (const line of lines.slice(1)) {
  const fields = line.split(",").map((value) => value.trim());
  if (fields.length !== headers.length) continue;

  const ticketId = fields[idIndex];
  const priority = fields[priorityIndex].toLowerCase() as Priority;
  const createdAt = fields[createdIndex];
  const resolvedAt = fields[resolvedIndex];
  const status = fields[statusIndex].toLowerCase();

  if (!(priority in targets) || !createdAt) continue;

  const isResolved =
    status === "resolved" || status === "closed" || Boolean(resolvedAt);

  const ticket = {
    ticket_id: ticketId,
    priority,
    created_at: createdAt.replace(" ", "T") + (createdAt.endsWith("Z") ? "" : "Z"),
    resolved_at: isResolved && resolvedAt
      ? resolvedAt.replace(" ", "T") + (resolvedAt.endsWith("Z") ? "" : "Z")
      : undefined,
  };

  try {
    const result = checkSLA(ticket, now.toISOString());
    checked++;

    if (result.breached) {
      breached++;
      console.log(
        `${ticketId}: BREACHED — ${result.hours_over} hours over SLA ` +
        `(${result.elapsed_hours} elapsed hours; target ${targets[priority]} hours)`,
      );
    }
  } catch {
    console.warn(`${ticketId}: skipped due to invalid dates`);
  }
}

console.log(`\nTickets checked: ${checked}`);
console.log(`Tickets breaching SLA: ${breached}`);
