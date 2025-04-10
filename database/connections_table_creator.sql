CREATE TABLE connections (
    id INTEGER PRIMARY KEY,
    user1_id INTEGER,
    user2_id INTEGER,
    status TEXT,
    created_at TIMESTAMP DEFAULT NOW(),
    FOREIGN KEY (user1_id) REFERENCES users(id),
    FOREIGN KEY (user2_id) REFERENCES users(id)
)       