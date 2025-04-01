------------------------------------
------------------------------------
-- MAIN TABLES FOR THE DATABASE --- 
------------------------------------
------------------------------------


CREATE TABLE IF NOT EXISTS users (
    uuid UUID PRIMARY KEY NOT NULL,
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
    assoc_user UUID NOT NULL REFERENCES users(uuid) 
);

----------------------------------------------
----------------------------------------------
-- TABLES BELOW ARE NOT ACTIVE IN BACKEND ---
----------------------------------------------
----------------------------------------------


CREATE TABLE IF NOT EXISTS inventory
(
  foodbank_id UUID NOT NULL,
  item_id UUID PRIMARY KEY NOT NULL 
  item_name TEXT NOT NULL,
  item_qty INTEGER NOT NULL,
  date_added TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
  item_status TEXT
);


CREATE TABLE IF NOT EXISTS reservations
(
  reservation_uuid UUID PRIMARY KEY NOT NULL,
  reservation_creation_date TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
  user_uuid TEXT,
  reserve_time TIMESTAMPTZ,
  picked_up BOOLEAN,
  picked_up_time TIMESTAMPTZ,
  reservations_array JSONB[] NOT NULL,
  current_status TEXT
)

CREATE TABLE IF NOT EXISTS donations (
    donation_id UUID PRIMARY KEY NOT NULL,
    donation_creation_date TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    foodbank_id UUID NOT NULL,
    donations_array JSONB[] NOT NULL,
    CONSTRAINT fk_foodbank_id FOREIGN KEY (foodbank_id) REFERENCES business(business_id),
    CONSTRAINT fk_user_id FOREIGN KEY (user_id) REFERENCES users(uuid),
    CONSTRAINT fk_item_id FOREIGN KEY (item_id) REFERENCES inventory(item_id)
);
