CREATE TABLE feedbacks (
    id INTEGER PRIMARY KEY,
    meeting_id INTEGER,
    user_id INTEGER,
    score INTEGER CHECK (score BETWEEN 1 AND 5),
    comment TEXT,
    FOREIGN KEY (meeting_id) REFERENCES meetings(id),
    FOREIGN KEY (user_id) REFERENCES users(id)
)       