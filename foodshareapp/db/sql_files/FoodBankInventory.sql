--create inventory for all foobanks with decent amount

CREATE TABLE FoodBankInventory
(
  itemID TEXT PRIMARY KEY NOT NULL,
  foodbankID TEXT NOT NULL,
  itemName TEXT NOT NULL,
  itemQuant INTEGER NOT NULL,
  itemStatus TEXT NOT NULL
);

--Hope Bank
INSERT INTO FoodBankInventory VALUES ('1548ace8-4a45-4b16-9848-39be2a8173fc', 'dcf47826-e330-4754-8f86-3ebae7a4663b',
'Orange',2, 'Available');

INSERT INTO  FoodBankInventory VALUES ('b7d29616-29e5-4cf9-92ee-904a7390b66e', 'dcf47826-e330-4754-8f86-3ebae7a4663b',
'Orange',2, 'Available');

INSERT INTO  FoodBankInventory VALUES ('e7d56a82-a8d2-46d1-957b-fb71d7b39d9b', 'dcf47826-e330-4754-8f86-3ebae7a4663b',
'Bread',1, 'Available');

INSERT INTO  FoodBankInventory VALUES ('b6d7367f-879e-443f-be8a-49908f52c943', 'dcf47826-e330-4754-8f86-3ebae7a4663b',
'Bread',2, 'Available');

INSERT INTO  FoodBankInventory VALUES ('4579c30e-d440-4bc4-8a4d-3ce4b81cf6e1', 'dcf47826-e330-4754-8f86-3ebae7a4663b',
'Pizza',2, 'Available');

--Faith Bank

INSERT INTO  FoodBankInventory VALUES ('8f882212-08e8-47de-a1cf-f2043a58fdde', 'db6b740c-74f4-44a0-95ea-5c16883fad88',
'Chicken',4, 'Available');

INSERT INTO  FoodBankInventory VALUES ('4ac03e84-ded4-4325-991d-fee938abd934', 'db6b740c-74f4-44a0-95ea-5c16883fad88',
'Chicken',5, 'Available');

INSERT INTO  FoodBankInventory VALUES ('02522929-2648-4051-a3d8-503f4563e8dc', 'db6b740c-74f4-44a0-95ea-5c16883fad88',
'Grapes',2, 'Available');

INSERT INTO  FoodBankInventory VALUES ('e68343c0-8817-4f52-8b9e-bffb97e8b162', 'db6b740c-74f4-44a0-95ea-5c16883fad88',
'Ham',1, 'Available');

--Help Bank
INSERT INTO  FoodBankInventory VALUES ('7518fd36-ee4f-4243-9c2a-7616d48e28b3', '96facdbd-f407-4a56-b889-51a3dab13ace',
'Pear',1, 'Available');

INSERT INTO  FoodBankInventory VALUES ('0350fa67-8b2b-4da7-9e64-7e359a5bd615', '96facdbd-f407-4a56-b889-51a3dab13ace',
'Peach',1, 'Available');

--Love Bank
INSERT INTO  FoodBankInventory VALUES ('6e7c0ea6-7dda-41f7-babc-05f7e225f416', 'dfe80b5e-89ff-4649-a174-8a3ff35e423b',
'Fish',2, 'Available');

INSERT INTO  FoodBankInventory VALUES ('3fd6aa5e-c897-4782-b1a6-2f4e100aee21', 'dfe80b5e-89ff-4649-a174-8a3ff35e423b',
'Peas',1, 'Available');

INSERT INTO  FoodBankInventory VALUES ('d67f5748-54b5-43fd-8e11-608efbb0f698', 'dfe80b5e-89ff-4649-a174-8a3ff35e423b',
'Crackers',2, 'Available');

INSERT INTO  FoodBankInventory VALUES ('d5e63bdc-0068-4581-8720-9ee96f57d0bf', 'dfe80b5e-89ff-4649-a174-8a3ff35e423b',
'Crackers',1, 'Available');