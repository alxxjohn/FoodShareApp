
--  users table -- 

CREATE TABLE users (
    uuid TEXT PRIMARY KEY NOT NULL,
    email TEXT UNIQUE NOT NULL,
    username TEXT NOT NULL,
    firstname TEXT ,
    lastname TEXT ,
    salt TEXT NOT NULL,
    password TEXT NOT NULL,
    tos_accepted BOOLEAN NOT NULL,
    tos_accepted_date DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    last_login DATETIME,
    bad_login_attempt DATETIME,
    bad_login_count INTEGER,
    account_locked BOOLEAN NOT NULL DEFAULT 0,
    account_verified BOOLEAN DEFAULT 1,
    account_verified_at DATETIME,
    company_name TEXT,
    address TEXT,
    city TEXT,
    state TEXT,
    zip TEXT,
    phone TEXT,
    is_business BOOLEAN NOT NULL DEFAULT 0,
    is_admin BOOLEAN NOT NULL DEFAULT 0,


    PRIMARY KEY (uuid),
    CONSTRAINT unique_email UNIQUE (email)

);



-- todo add business and foodbanks table table -- 
---- ideally this should connect to a uuid in the users table  if user is_business --





-- todo add donations table -- 














