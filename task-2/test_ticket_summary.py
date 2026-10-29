
import csv

from ticket_summary import summarize_tickets


def test_counts_categories_and_calculates_average(tmp_path):
    csv_file = tmp_path / "tickets.csv"

    rows = [
        {
            "ticket_id": "T1",
            "category": "Billing",
            "created_at": "2026-03-02 09:00",
            "resolved_at": "2026-03-02 11:00",
        },
        {
            "ticket_id": "T2",
            "category": "BILLING",
            "created_at": "2026-03-02 09:00",
            "resolved_at": "2026-03-02 13:00",
        },
        {
            "ticket_id": "T3",
            "category": "Login",
            "created_at": "2026-03-02 09:00",
            "resolved_at": "",
        },
    ]

    with csv_file.open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(
            file,
            fieldnames=[
                "ticket_id",
                "category",
                "created_at",
                "resolved_at",
            ],
        )
        writer.writeheader()
        writer.writerows(rows)

    result = summarize_tickets(csv_file)

    assert result["Billing"]["ticket_count"] == 2
    assert result["Billing"]["average_resolution_hours"] == 3.0
    assert result["Login"]["ticket_count"] == 1
    assert result["Login"]["average_resolution_hours"] is None


def test_missing_category_becomes_unknown(tmp_path):
    csv_file = tmp_path / "tickets.csv"
    csv_file.write_text(
        "category,created_at,resolved_at\n"
        ",2026-03-02 09:00,2026-03-02 10:00\n",
        encoding="utf-8",
    )

    result = summarize_tickets(csv_file)

    assert result["Unknown"]["ticket_count"] == 1
    assert result["Unknown"]["average_resolution_hours"] == 1.0
