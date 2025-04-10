CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,
    role TEXT DEFAULT 'simple',
    company_id INTEGER,
    interests TEXT[],
    profile_photo TEXT,
    availability TEXT[],
    FOREIGN KEY (company_id) REFERENCES companies(id)
)