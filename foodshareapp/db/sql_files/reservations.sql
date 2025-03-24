CREATE TABLE reservations
(
  reservationID TEXT PRIMARY KEY NOT NULL,
  reservationMadeTime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  foodbankID TEXT,
  itemID TEXT,
  itemName TEXT,
  userID TEXT,
  itemQty INTEGER,
  pickupTime DATETIME,
  showedUP BOOLEAN,
  showedUPtime DATETIME.
  status TEXT,
)

