CREATE TABLE IF NOT EXISTS riders (
    rider_id INTEGER PRIMARY KEY,
    created_at TEXT NOT NULL,
    city TEXT NOT NULL,
    signup_channel TEXT NOT NULL,
    status TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS trips (
    trip_id INTEGER PRIMARY KEY,
    rider_id INTEGER NOT NULL,
    driver_id INTEGER NOT NULL,
    fare REAL NOT NULL,
    promo_amount REAL NOT NULL DEFAULT 0,
    distance_km REAL NOT NULL,
    start_ts TEXT NOT NULL,
    end_ts TEXT NOT NULL,
    status TEXT NOT NULL,
    FOREIGN KEY (rider_id) REFERENCES riders(rider_id)
);

CREATE TABLE IF NOT EXISTS payments (
    payment_id INTEGER PRIMARY KEY,
    rider_id INTEGER NOT NULL,
    trip_id INTEGER NOT NULL,
    amount REAL NOT NULL,
    method TEXT NOT NULL,
    success INTEGER NOT NULL,
    chargeback_flag INTEGER NOT NULL DEFAULT 0,
    ts TEXT NOT NULL,
    FOREIGN KEY (rider_id) REFERENCES riders(rider_id),
    FOREIGN KEY (trip_id) REFERENCES trips(trip_id)
);

CREATE TABLE IF NOT EXISTS refunds (
    refund_id INTEGER PRIMARY KEY,
    rider_id INTEGER NOT NULL,
    trip_id INTEGER NOT NULL,
    amount REAL NOT NULL,
    reason TEXT NOT NULL,
    ts TEXT NOT NULL,
    FOREIGN KEY (rider_id) REFERENCES riders(rider_id),
    FOREIGN KEY (trip_id) REFERENCES trips(trip_id)
);

CREATE TABLE IF NOT EXISTS devices (
    device_id INTEGER PRIMARY KEY AUTOINCREMENT,
    rider_id INTEGER NOT NULL,
    first_seen_ts TEXT NOT NULL,
    last_seen_ts TEXT NOT NULL,
    rooted_flag INTEGER NOT NULL DEFAULT 0,
    FOREIGN KEY (rider_id) REFERENCES riders(rider_id)
);

CREATE TABLE IF NOT EXISTS logins (
    login_id INTEGER PRIMARY KEY AUTOINCREMENT,
    rider_id INTEGER NOT NULL,
    ip TEXT NOT NULL,
    geo_lat REAL NOT NULL,
    geo_lon REAL NOT NULL,
    ts TEXT NOT NULL,
    success INTEGER NOT NULL,
    FOREIGN KEY (rider_id) REFERENCES riders(rider_id)
);

CREATE TABLE IF NOT EXISTS alerts (
    alert_id INTEGER PRIMARY KEY AUTOINCREMENT,
    rider_id INTEGER NOT NULL,
    fraud_type TEXT NOT NULL,
    risk_score REAL NOT NULL,
    estimated_loss REAL NOT NULL,
    priority_score REAL NOT NULL,
    created_ts TEXT NOT NULL,
    status TEXT NOT NULL,
    FOREIGN KEY (rider_id) REFERENCES riders(rider_id)
);

CREATE TABLE IF NOT EXISTS analyst_actions (
    action_id INTEGER PRIMARY KEY AUTOINCREMENT,
    alert_id INTEGER,
    analyst_id TEXT NOT NULL,
    action TEXT NOT NULL,
    action_ts TEXT NOT NULL,
    outcome_label TEXT NOT NULL,
    notes TEXT,
    FOREIGN KEY (alert_id) REFERENCES alerts(alert_id)
);

CREATE INDEX IF NOT EXISTS idx_alerts_priority ON alerts(priority_score DESC);
CREATE INDEX IF NOT EXISTS idx_alerts_risk ON alerts(risk_score DESC);
CREATE INDEX IF NOT EXISTS idx_payments_rider_ts ON payments(rider_id, ts DESC);
CREATE INDEX IF NOT EXISTS idx_trips_rider_start ON trips(rider_id, start_ts DESC);
CREATE INDEX IF NOT EXISTS idx_refunds_rider_ts ON refunds(rider_id, ts DESC);
