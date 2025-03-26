CREATE TABLE reservations
(
  reservationID TEXT PRIMARY KEY NOT NULL,
  foodbankID TEXT,
  reservationMadeTime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  userID TEXT,
  itemID TEXT,
  itemsArray TEXT,
  pickupTime DATETIME,
  showedUPtime DATETIME
)

