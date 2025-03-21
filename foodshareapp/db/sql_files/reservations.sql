CREATE TABLE reservations
(
  reservationID TEXT PRIMARY KEY NOT NULL,
  reservationMadeTime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  foodbankID TEXT,
  itemID TEXT,
  userID TEXT,
  itemQuant INTEGER,
  pickupTime DATETIME,
  showedUP TEXT,
  showedUPtime DATETIME
)

