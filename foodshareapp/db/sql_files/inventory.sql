CREATE TABLE inventory
(
  foodbankID TEXT PRIMARY KEY NOT NULL,
  itemID INTEGER NOT NULL,
  itemName TEXT NOT NULL,
  itemQuant INTEGER NOT NULL

  PRIMARY KEY (foodbankID)
);

