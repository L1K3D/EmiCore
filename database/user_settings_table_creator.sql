CREATE TABLE user_settings (
    id INTEGER PRIMARY KEY,
    user_id INTEGER,
    notifications_enabled BOOLEAN,
    dark_mode BOOLEAN,
    FOREIGN KEY (user_id) REFERENCES users(id)
)       