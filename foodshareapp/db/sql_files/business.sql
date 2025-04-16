CREATE TABLE businesses (
    BusinessId TEXT PRIMARY KEY,
    companyName TEXT NOT NULL,
    address TEXT NOT NULL,
    city TEXT NOT NULL,
    state TEXT NOT NULL,
    zipcode TEXT NOT NULL,
    lat TEXT,
    lng TEXT,
    isFoodbank BOOLEAN NOT NULL DEFAULT 0,
    assoc_user TEXT NOT NULL
);