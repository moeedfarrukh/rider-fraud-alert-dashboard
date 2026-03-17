import os
import random
import sqlite3
from datetime import datetime, timedelta

from flask import Flask, redirect, render_template, request, url_for


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "data", "fraud_dashboard.db")
SCHEMA_PATH = os.path.join(BASE_DIR, "data", "schema.sql")

app = Flask(__name__)


def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def initialize_database():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    with open(SCHEMA_PATH, "r", encoding="utf-8") as schema_file:
        conn.executescript(schema_file.read())
    conn.commit()
    conn.close()


def seed_data_if_needed():
    conn = get_connection()
    rider_count = conn.execute("SELECT COUNT(*) AS count FROM riders").fetchone()["count"]
    if rider_count > 0:
        conn.close()
        return

    random.seed(42)
    now = datetime.utcnow()
    cities = ["Karachi", "Lahore", "Islamabad", "Rawalpindi"]
    signup_channels = ["organic", "paid_social", "referral", "seo"]
    payment_methods = ["card", "wallet", "cash"]
    fraud_types = [
        "promo_abuse",
        "payment_fraud",
        "location_spoofing",
        "refund_abuse",
        "account_takeover",
    ]
    analysts = ["Ayesha", "Hamza", "Sana", "Bilal"]

    suspicious_riders = set(random.sample(range(1, 101), 18))

    for rider_id in range(1, 101):
        created_at = now - timedelta(days=random.randint(10, 180))
        city = random.choice(cities)
        channel = random.choice(signup_channels)
        status = "active"
        conn.execute(
            """
            INSERT INTO riders (rider_id, created_at, city, signup_channel, status)
            VALUES (?, ?, ?, ?, ?)
            """,
            (rider_id, created_at.isoformat(), city, channel, status),
        )

        device_count = random.randint(1, 2) if rider_id not in suspicious_riders else random.randint(3, 6)
        for _ in range(device_count):
            first_seen = created_at + timedelta(days=random.randint(0, 20))
            last_seen = now - timedelta(days=random.randint(0, 3))
            rooted = 1 if (rider_id in suspicious_riders and random.random() < 0.55) else 0
            conn.execute(
                """
                INSERT INTO devices (rider_id, first_seen_ts, last_seen_ts, rooted_flag)
                VALUES (?, ?, ?, ?)
                """,
                (rider_id, first_seen.isoformat(), last_seen.isoformat(), rooted),
            )

        login_count = random.randint(8, 20) if rider_id in suspicious_riders else random.randint(3, 12)
        for _ in range(login_count):
            login_ts = now - timedelta(days=random.randint(0, 30), hours=random.randint(0, 23))
            ip = f"10.{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}"
            geo_lat = 24.8 + random.random() * 10
            geo_lon = 67.0 + random.random() * 8
            success = 1 if random.random() > (0.25 if rider_id in suspicious_riders else 0.08) else 0
            conn.execute(
                """
                INSERT INTO logins (rider_id, ip, geo_lat, geo_lon, ts, success)
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                (rider_id, ip, geo_lat, geo_lon, login_ts.isoformat(), success),
            )

    trip_id = 1
    payment_id = 1
    refund_id = 1
    for rider_id in range(1, 101):
        trip_count = random.randint(15, 45) if rider_id in suspicious_riders else random.randint(6, 26)
        for _ in range(trip_count):
            start_ts = now - timedelta(days=random.randint(0, 35), hours=random.randint(0, 23))
            duration_min = random.randint(8, 45)
            end_ts = start_ts + timedelta(minutes=duration_min)
            distance = round(random.uniform(1.5, 18.0), 2)
            fare = round(max(120, distance * random.uniform(40, 110)), 2)

            if rider_id in suspicious_riders:
                promo_amount = round(fare * random.uniform(0.2, 0.75), 2) if random.random() < 0.55 else 0
            else:
                promo_amount = round(fare * random.uniform(0.1, 0.3), 2) if random.random() < 0.2 else 0

            status = "completed" if random.random() > 0.07 else "cancelled"
            driver_id = random.randint(2000, 2400)

            conn.execute(
                """
                INSERT INTO trips (
                    trip_id, rider_id, driver_id, fare, promo_amount, distance_km, start_ts, end_ts, status
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    trip_id,
                    rider_id,
                    driver_id,
                    fare,
                    promo_amount,
                    distance,
                    start_ts.isoformat(),
                    end_ts.isoformat(),
                    status,
                ),
            )

            success = 1 if random.random() > (0.35 if rider_id in suspicious_riders else 0.08) else 0
            chargeback = 1 if (rider_id in suspicious_riders and random.random() < 0.25) else 0
            method = random.choice(payment_methods)
            conn.execute(
                """
                INSERT INTO payments (payment_id, rider_id, trip_id, amount, method, success, chargeback_flag, ts)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    payment_id,
                    rider_id,
                    trip_id,
                    fare - promo_amount,
                    method,
                    success,
                    chargeback,
                    end_ts.isoformat(),
                ),
            )

            if rider_id in suspicious_riders and random.random() < 0.38:
                refund_amount = round((fare - promo_amount) * random.uniform(0.3, 1.0), 2)
                reason = random.choice(["duplicate_charge", "service_issue", "trip_not_taken"])
                conn.execute(
                    """
                    INSERT INTO refunds (refund_id, rider_id, trip_id, amount, reason, ts)
                    VALUES (?, ?, ?, ?, ?, ?)
                    """,
                    (refund_id, rider_id, trip_id, refund_amount, reason, (end_ts + timedelta(hours=2)).isoformat()),
                )
                refund_id += 1

            payment_id += 1
            trip_id += 1

    # Seed historical analyst actions for realism.
    alert_seeds = random.sample(list(suspicious_riders), 12)
    for rider_id in alert_seeds:
        action = random.choice(["monitor", "temporary_block", "escalate"])
        outcome = random.choice(["confirmed_fraud", "pending_review", "false_positive"])
        analyst = random.choice(analysts)
        conn.execute(
            """
            INSERT INTO analyst_actions (alert_id, analyst_id, action, action_ts, outcome_label, notes)
            VALUES (NULL, ?, ?, ?, ?, ?)
            """,
            (
                analyst,
                action,
                (now - timedelta(days=random.randint(1, 10))).isoformat(),
                outcome,
                "Seeded historical action",
            ),
        )

    conn.commit()
    conn.close()


def refresh_alerts():
    conn = get_connection()
    conn.execute("DELETE FROM alerts")
    conn.execute(
        """
        WITH rider_metrics AS (
            SELECT
                r.rider_id,
                r.city,
                COALESCE(SUM(CASE WHEN p.success = 0 THEN 1 ELSE 0 END), 0) AS failed_payments_30d,
                COALESCE(SUM(CASE WHEN p.chargeback_flag = 1 THEN 1 ELSE 0 END), 0) AS chargebacks_30d,
                COALESCE(COUNT(DISTINCT d.device_id), 0) AS devices_count,
                COALESCE(SUM(CASE WHEN d.rooted_flag = 1 THEN 1 ELSE 0 END), 0) AS rooted_devices,
                COALESCE(COUNT(DISTINCT l.ip), 0) AS unique_ips_30d,
                COALESCE(SUM(CASE WHEN l.success = 0 THEN 1 ELSE 0 END), 0) AS failed_logins_30d,
                COALESCE(SUM(t.promo_amount), 0) AS promo_used_30d,
                COALESCE(SUM(CASE WHEN ref.refund_id IS NOT NULL THEN ref.amount ELSE 0 END), 0) AS refund_amount_30d,
                COALESCE(SUM(t.fare), 0) AS gross_fare_30d
            FROM riders r
            LEFT JOIN trips t
                ON r.rider_id = t.rider_id
                AND t.start_ts >= datetime('now', '-30 day')
            LEFT JOIN payments p
                ON p.trip_id = t.trip_id
            LEFT JOIN refunds ref
                ON ref.trip_id = t.trip_id
            LEFT JOIN devices d
                ON d.rider_id = r.rider_id
            LEFT JOIN logins l
                ON l.rider_id = r.rider_id
                AND l.ts >= datetime('now', '-30 day')
            GROUP BY r.rider_id, r.city
        ),
        scored AS (
            SELECT
                rider_id,
                city,
                failed_payments_30d,
                chargebacks_30d,
                devices_count,
                rooted_devices,
                unique_ips_30d,
                failed_logins_30d,
                promo_used_30d,
                refund_amount_30d,
                gross_fare_30d,
                MIN(
                    100,
                    (
                        failed_payments_30d * 4 +
                        chargebacks_30d * 10 +
                        CASE WHEN devices_count >= 4 THEN 20 ELSE devices_count * 2 END +
                        rooted_devices * 6 +
                        CASE WHEN unique_ips_30d >= 8 THEN 10 ELSE unique_ips_30d END +
                        failed_logins_30d * 2 +
                        CASE
                            WHEN gross_fare_30d > 0 THEN (promo_used_30d / gross_fare_30d) * 40
                            ELSE 0
                        END +
                        CASE
                            WHEN gross_fare_30d > 0 THEN (refund_amount_30d / gross_fare_30d) * 60
                            ELSE 0
                        END
                    )
                ) AS risk_score
            FROM rider_metrics
        )
        INSERT INTO alerts (rider_id, fraud_type, risk_score, estimated_loss, priority_score, created_ts, status)
        SELECT
            s.rider_id,
            CASE
                WHEN chargebacks_30d >= 2 THEN 'payment_fraud'
                WHEN refund_amount_30d > promo_used_30d AND refund_amount_30d > 500 THEN 'refund_abuse'
                WHEN promo_used_30d > 900 THEN 'promo_abuse'
                WHEN failed_logins_30d >= 5 AND unique_ips_30d >= 6 THEN 'account_takeover'
                ELSE 'location_spoofing'
            END AS fraud_type,
            ROUND(s.risk_score, 2) AS risk_score,
            ROUND((chargebacks_30d * 350 + refund_amount_30d + promo_used_30d * 0.4), 2) AS estimated_loss,
            ROUND((s.risk_score * (chargebacks_30d * 350 + refund_amount_30d + promo_used_30d * 0.4)) / 100, 2) AS priority_score,
            datetime('now') AS created_ts,
            CASE WHEN s.risk_score >= 70 THEN 'open' ELSE 'monitor' END AS status
        FROM scored s
        WHERE s.risk_score >= 35
        """
    )
    conn.commit()
    conn.close()


@app.route("/")
def queue():
    refresh_alerts()
    conn = get_connection()
    min_risk = request.args.get("min_risk", default=35, type=int)
    fraud_type = request.args.get("fraud_type", default="")
    city = request.args.get("city", default="")
    status = request.args.get("status", default="")

    query = """
        SELECT
            a.alert_id,
            a.rider_id,
            r.city,
            a.fraud_type,
            a.risk_score,
            a.estimated_loss,
            a.priority_score,
            a.status,
            a.created_ts
        FROM alerts a
        JOIN riders r ON r.rider_id = a.rider_id
        WHERE a.risk_score >= ?
    """
    params = [min_risk]

    if fraud_type:
        query += " AND a.fraud_type = ?"
        params.append(fraud_type)
    if city:
        query += " AND r.city = ?"
        params.append(city)
    if status:
        query += " AND a.status = ?"
        params.append(status)

    query += " ORDER BY a.priority_score DESC, a.risk_score DESC"
    alerts = conn.execute(query, params).fetchall()

    summary = conn.execute(
        """
        SELECT
            COUNT(*) AS total_alerts,
            ROUND(AVG(risk_score), 2) AS avg_risk,
            ROUND(SUM(estimated_loss), 2) AS est_loss,
            ROUND(SUM(CASE WHEN status = 'open' THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 1) AS open_ratio
        FROM alerts
        """
    ).fetchone()

    headline_row = conn.execute(
        """
        SELECT
            SUM(CASE WHEN risk_score >= 80 THEN 1 ELSE 0 END) AS high_risk_alerts,
            SUM(CASE WHEN status = 'blocked' THEN 1 ELSE 0 END) AS blocked_riders
        FROM alerts
        """
    ).fetchone()

    severity_row = conn.execute(
        """
        SELECT
            SUM(CASE WHEN risk_score >= 80 THEN 1 ELSE 0 END) AS high_count,
            SUM(CASE WHEN risk_score BETWEEN 60 AND 79.99 THEN 1 ELSE 0 END) AS medium_count,
            SUM(CASE WHEN risk_score < 60 THEN 1 ELSE 0 END) AS low_count
        FROM alerts
        """
    ).fetchone()

    total_for_severity = (
        (severity_row["high_count"] or 0)
        + (severity_row["medium_count"] or 0)
        + (severity_row["low_count"] or 0)
    ) or 1

    severity = {
        "high_count": severity_row["high_count"] or 0,
        "medium_count": severity_row["medium_count"] or 0,
        "low_count": severity_row["low_count"] or 0,
        "high_pct": round((severity_row["high_count"] or 0) * 100.0 / total_for_severity, 1),
        "medium_pct": round((severity_row["medium_count"] or 0) * 100.0 / total_for_severity, 1),
        "low_pct": round((severity_row["low_count"] or 0) * 100.0 / total_for_severity, 1),
    }

    fraud_type_mix = conn.execute(
        """
        SELECT
            fraud_type,
            COUNT(*) AS cnt
        FROM alerts
        GROUP BY fraud_type
        ORDER BY cnt DESC
        LIMIT 5
        """
    ).fetchall()

    total_fraud = sum(row["cnt"] for row in fraud_type_mix) or 1
    fraud_type_mix = [
        {"fraud_type": row["fraud_type"], "cnt": row["cnt"], "pct": round(row["cnt"] * 100.0 / total_fraud, 1)}
        for row in fraud_type_mix
    ]

    cities = conn.execute("SELECT DISTINCT city FROM riders ORDER BY city").fetchall()
    fraud_types = conn.execute("SELECT DISTINCT fraud_type FROM alerts ORDER BY fraud_type").fetchall()
    conn.close()

    return render_template(
        "queue.html",
        alerts=alerts,
        summary=summary,
        headline=headline_row,
        severity=severity,
        fraud_type_mix=fraud_type_mix,
        cities=cities,
        fraud_types=fraud_types,
        filters={"min_risk": min_risk, "fraud_type": fraud_type, "city": city, "status": status},
    )


@app.route("/rider/<int:rider_id>")
def rider_detail(rider_id):
    conn = get_connection()
    rider = conn.execute("SELECT * FROM riders WHERE rider_id = ?", (rider_id,)).fetchone()
    if rider is None:
        conn.close()
        return redirect(url_for("queue"))

    risk_snapshot = conn.execute(
        """
        SELECT fraud_type, risk_score, estimated_loss, priority_score, status, created_ts
        FROM alerts
        WHERE rider_id = ?
        ORDER BY created_ts DESC
        LIMIT 1
        """,
        (rider_id,),
    ).fetchone()

    trips = conn.execute(
        """
        SELECT trip_id, fare, promo_amount, distance_km, start_ts, status
        FROM trips
        WHERE rider_id = ?
        ORDER BY start_ts DESC
        LIMIT 10
        """,
        (rider_id,),
    ).fetchall()
    payments = conn.execute(
        """
        SELECT payment_id, amount, method, success, chargeback_flag, ts
        FROM payments
        WHERE rider_id = ?
        ORDER BY ts DESC
        LIMIT 10
        """,
        (rider_id,),
    ).fetchall()
    refunds = conn.execute(
        """
        SELECT refund_id, amount, reason, ts
        FROM refunds
        WHERE rider_id = ?
        ORDER BY ts DESC
        LIMIT 10
        """,
        (rider_id,),
    ).fetchall()
    devices = conn.execute(
        """
        SELECT device_id, rooted_flag, first_seen_ts, last_seen_ts
        FROM devices
        WHERE rider_id = ?
        ORDER BY last_seen_ts DESC
        """,
        (rider_id,),
    ).fetchall()
    actions = conn.execute(
        """
        SELECT aa.action_id, aa.alert_id, aa.analyst_id, aa.action, aa.outcome_label, aa.notes, aa.action_ts
        FROM analyst_actions aa
        LEFT JOIN alerts a ON a.alert_id = aa.alert_id
        WHERE a.rider_id = ?
        ORDER BY aa.action_ts DESC
        LIMIT 20
        """,
        (rider_id,),
    ).fetchall()
    conn.close()

    return render_template(
        "rider_detail.html",
        rider=rider,
        risk_snapshot=risk_snapshot,
        trips=trips,
        payments=payments,
        refunds=refunds,
        devices=devices,
        actions=actions,
    )


@app.post("/alerts/<int:alert_id>/action")
def take_action(alert_id):
    action = request.form.get("action", "monitor")
    analyst = request.form.get("analyst", "Unassigned")
    notes = request.form.get("notes", "").strip()
    outcome = request.form.get("outcome", "pending_review")

    status_map = {
        "allow": "closed",
        "monitor": "monitor",
        "temporary_block": "blocked",
        "escalate": "open",
    }
    status = status_map.get(action, "monitor")

    conn = get_connection()
    conn.execute("UPDATE alerts SET status = ? WHERE alert_id = ?", (status, alert_id))
    conn.execute(
        """
        INSERT INTO analyst_actions (alert_id, analyst_id, action, action_ts, outcome_label, notes)
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        (alert_id, analyst, action, datetime.utcnow().isoformat(), outcome, notes),
    )
    conn.commit()
    conn.close()
    return redirect(url_for("queue"))


@app.route("/actions")
def actions():
    conn = get_connection()
    records = conn.execute(
        """
        SELECT
            aa.action_id,
            aa.alert_id,
            aa.analyst_id,
            aa.action,
            aa.outcome_label,
            aa.notes,
            aa.action_ts,
            a.rider_id,
            a.fraud_type
        FROM analyst_actions aa
        LEFT JOIN alerts a ON a.alert_id = aa.alert_id
        ORDER BY aa.action_ts DESC
        LIMIT 100
        """
    ).fetchall()
    conn.close()
    return render_template("actions.html", records=records)


def bootstrap():
    initialize_database()
    seed_data_if_needed()
    refresh_alerts()


if __name__ == "__main__":
    bootstrap()
    app.run(debug=True)
