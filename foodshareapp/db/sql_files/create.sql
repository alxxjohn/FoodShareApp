CREATE TABLE business
(
    businessID TEXT PRIMARY KEY NOT NULL,
    company_name TEXT NOT NULL,
    address TEXT NOT NULL,
    city TEXT NOT NULL,
    state TEXT NOT NULL,
    zip TEXT NOT NULL,
    isFoodbank BOOLEAN NOT NULL DEFAULT 0,
    lat TEXT NOT NULL,
    lng TEXT NOT NULL,
    assoc_user TEXT NOT NULL
);

CREATE TABLE FoodBankInventory
(
  itemID TEXT PRIMARY KEY NOT NULL,
  foodbankID TEXT NOT NULL,
  itemName TEXT NOT NULL,
  itemQuant INTEGER NOT NULL,
  itemStatus TEXT NOT NULL
);

CREATE TABLE donations
(
    donationID TEXT PRIMARY KEY NOT NULL,
    businessID TEXT NOT NULL,
    foodbankID TEXT NOT NULL,
    donationDate DATETIME NOT NULL,
    donationWeight FLOAT NOT NULL,
    donationDolAmt FLOAT NOT NULL,
    donationsArray TEXT NOT NULL
);

CREATE TABLE users
(
    userId TEXT PRIMARY KEY NOT NULL,
    username TEXT NOT NULL,
    firstname TEXT NOT NULL,
    lastName TEXT NOT NULL,
    email TEXT NOT NULL,
    phone TEXT NOT NULL,
    salt TEXT NOT NULL,
    password TEXT NOT NULL,
    tos_accepted BOOLEAN NOT NULL DEFAULT 0,
    tos_accepted_date DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    last_login DATETIME,
    bad_login_attempt DATETIME,
    bad_login_count INTEGER,
    account_locked  BOOLEAN NOT NULL DEFAULT 0,
    account_verified BOOLEAN DEFAULT 1,
    account_verified_at DATETIME
);

CREATE TABLE reservations
(
  reservationID TEXT PRIMARY KEY NOT NULL,
  foodbankID TEXT NOT NULL,
  reservationMadeTime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  userID TEXT NOT NULL,
  itemsArray TEXT NOT NULL,
  pickupTime DATETIME NOT NULL,
  showedUP BOOLEAN NOT NULL DEFAULT 0,
  showedUPtime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  reservationStatus TEXT NOT NULL
);