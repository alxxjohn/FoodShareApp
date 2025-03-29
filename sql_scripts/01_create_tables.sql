
CREATE TABLE IF NOT EXISTS users (
    userId UUID PRIMARY KEY NOT NULL,
    email TEXT UNIQUE NOT NULL,
    username TEXT NOT NULL,
    firstname TEXT,
    lastname TEXT,
    salt TEXT NOT NULL,
    password TEXT NOT NULL,
    tos_accepted BOOLEAN NOT NULL DEFAULT TRUE,
    tos_accepted_date TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    last_login TIMESTAMP,
    bad_login_attempt TIMESTAMP,
    bad_login_count INTEGER,
    account_locked BOOLEAN NOT NULL DEFAULT FALSE,
    account_verified BOOLEAN DEFAULT TRUE,
    account_verified_at TIMESTAMP,
    company_name TEXT,
    address TEXT,
    city TEXT,
    state TEXT,
    zipCode TEXT,
    phone TEXT,
    is_business BOOLEAN NOT NULL DEFAULT FALSE,
    is_admin BOOLEAN NOT NULL DEFAULT FALSE,

    CONSTRAINT unique_email UNIQUE (email)
);


CREATE TABLE IF NOT EXISTS business (
    business_id UUID PRIMARY KEY,
    company_name TEXT NOT NULL,
    address TEXT NOT NULL,
    city TEXT NOT NULL,
    state TEXT NOT NULL,
    zipCode TEXT NOT NULL,
    lat TEXT,
    lng TEXT,
    is_foodbank BOOLEAN NOT NULL DEFAULT FALSE,
    assoc_user UUID NOT NULL REFERENCES users(userid) 
);