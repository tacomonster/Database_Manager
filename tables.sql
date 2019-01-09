CREATE TABLE contacts (
     contact_id INTEGER PRIMARY KEY AUTOINCREMENT,
     first_name TEXT NOT NULL,
     last_name TEXT NOT NULL,
     email TEXT NOT NULL,
     phone TEXT NOT NULL
);

CREATE TABLE ig_user (
     ig_id INTEGER PRIMARY KEY AUTOINCREMENT,
     username TEXT,
     followers INTEGER,
     posts INTEGER,
     following INTEGER
);
