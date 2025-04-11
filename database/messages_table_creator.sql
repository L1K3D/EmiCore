CREATE TABLE messages (
    id INTEGER PRIMARY KEY,
    sender_id INTEGER,
    receiver_id INTEGER,
    content TEXT,
    send_at TIMESTAMP DEFAULT NOW(),
    status TEXT,
    FOREIGN KEY (sender_id) REFERENCES users(id),
    FOREIGN KEY (receiver_id) REFERENCES users(id)
)       