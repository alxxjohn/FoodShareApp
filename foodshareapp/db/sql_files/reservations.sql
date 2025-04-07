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

--Kyle Reserves something present at Hope Bank and shows up in hour
INSERT INTO reservations VALUES ('5441f9a7-0711-47ba-a2b8-28875d758194', 'dcf47826-e330-4754-8f86-3ebae7a4663b',
'2025-03-27 14:10:20','0db55890-fe93-4063-b8e3-c61808b2a37f','{1548ace8-4a45-4b16-9848-39be2a8173fc, 1, Orange}'
,'2025-03-27 15:00:00' ,1, '2025-03-27 15:10:20', 'Complete');

--Kyle Reserves something not present at Hope Bank
INSERT INTO reservations VALUES ('01f16fc4-ff39-47bd-a365-7c417f4c3097', 'dcf47826-e330-4754-8f86-3ebae7a4663b',
'2025-03-25 11:12:21','0db55890-fe93-4063-b8e3-c61808b2a37f','{54af4181-c528-4ed2-aa38-4e1b10dfc80d, 1, Sushi}'
,'2025-03-25 12:00:00', 1, '2025-03-25 13:21:30', 'Incomplete');

--Alex reserves everything at Help Bank
INSERT INTO reservations VALUES ('5746df75-2b94-4af5-8551-72f6932066fc', 'db6b740c-74f4-44a0-95ea-5c16883fad88',
'2025-03-24 10:11:21','a175b716-7496-4f69-8827-8c252b61d2e8',
'{7518fd36-ee4f-4243-9c2a-7616d48e28b3, 1, Pear, 0350fa67-8b2b-4da7-9e64-7e359a5bd615, 1, Peach}',
'2025-03-24 13:30:00', 1, '2025-03-24 15:20:00', 'Complete');

--Ine reserves more peas from love bank than available
INSERT INTO reservations VALUES ('cd196be6-f63e-4db0-aeea-12e86bdfd02a', 'dfe80b5e-89ff-4649-a174-8a3ff35e423b',
'2025-03-22 10:11:21','8e94946d-b499-44f7-b1d9-1fb71c80be5e',
'{3fd6aa5e-c897-4782-b1a6-2f4e100aee21, 2, Pear}',
'2025-03-22 12:30:30', 1, '2025-03-22 13:00:00', 'Complete');



