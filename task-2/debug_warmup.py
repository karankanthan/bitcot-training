# Bug: delta.seconds ignored complete days, so longer ticket durations were calculated incorrectly.
# Fix: delta.total_seconds() includes the full elapsed time; the sample output confirms the fix.
from datetime import datetime

FMT = "%Y-%m-%d %H:%M"


def _parse(ts):
    return datetime.strptime(ts, FMT)


'''def _hours_between(start, end):
    delta = _parse(end) - _parse(start)
    return delta.seconds / 3600'''

def _hours_between(start, end):
    delta = _parse(end) - _parse(start)
    return delta.total_seconds() / 3600


def breach_report(tickets, sla_hours):
    breached = []
    total = 0.0
    counted = 0
    for t in tickets:
        if not t.get("resolved_at"):
            continue
        hours = _hours_between(t["created_at"], t["resolved_at"])
        total += hours
        counted += 1
        if hours > sla_hours[t["priority"]]:
            breached.append(t["ticket_id"])
    average = total / counted if counted else 0.0
    return {"breached": breached, "average_hours": round(average, 2), "counted": counted}


if __name__ == "__main__":
    sla = {"urgent": 4, "high": 8, "normal": 24, "low": 72}
    sample = [
        {"ticket_id": "A", "priority": "urgent", "created_at": "2026-03-02 09:00", "resolved_at": "2026-03-02 12:00"},
        {"ticket_id": "B", "priority": "normal", "created_at": "2026-03-02 09:00", "resolved_at": "2026-03-03 11:00"},
        {"ticket_id": "C", "priority": "high", "created_at": "2026-03-02 09:00", "resolved_at": "2026-03-02 19:00"},
        {"ticket_id": "D", "priority": "low", "created_at": "2026-03-02 09:00", "resolved_at": ""},
    ]
    print(breach_report(sample, sla))

