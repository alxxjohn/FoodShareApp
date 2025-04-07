--add 5 donations

CREATE TABLE donations (
    donationID TEXT PRIMARY KEY NOT NULL,
    businessID TEXT NOT NULL,
    foodbankID TEXT NOT NULL,
    donationDate DATETIME NOT NULL,
    donationWeight FLOAT NOT NULL,
    donationDolAmt FLOAT NOT NULL,
    donationsArray TEXT NOT NULL
);

--Outback donate to Hope Bank
INSERT INTO  donations  VALUES ('45a69c48-3b32-49a0-80ad-afb8193aa115', 'b298ab1b-c281-46fe-a4ab-b738106df501',
'dcf47826-e330-4754-8f86-3ebae7a4663b','2025-03-25 14:30:20',2.4, 23.02,
'{b82f4746-db31-4289-a34f-05a0d2d043e2, 1, steak, 42203df1-5e03-4112-aff3-431d563b877f, 2, fries}');

--Outback donate to Hope Bank  next day
INSERT INTO  donations  VALUES ('ca21a908-1edd-419e-b3c3-b05266b446f6', 'b298ab1b-c281-46fe-a4ab-b738106df501',
'dcf47826-e330-4754-8f86-3ebae7a4663b','2025-03-26 15:32:20',3.2, 33.25,
'{b01be156-a788-4b45-8077-6dcf9230e8e9, 2, steak, 25aba3bd-9efa-4d64-8fb3-c73c90127baf, 3, bread}');

--Carrabbas donates one item to Hope Bank same day as Outback
INSERT INTO  donations  VALUES ('14efbc57-fd3d-48c6-9be8-f59c5c1f800f', '5b9003ac-f149-4c4e-8754-56ce0d762429',
'dcf47826-e330-4754-8f86-3ebae7a4663b','2025-03-26 16:40:20',1, 12.26,
'{412b8bbc-238a-4b66-8de5-fc2e534d9481, 1, chicken}');

--Cheesecake Factory donates twice in same day to Love Bank
INSERT INTO  donations  VALUES ('122f3003-c45d-4323-858c-14636846dfe4', '7685b68c-9ddc-4d80-9a1c-bf701b581a09',
'dfe80b5e-89ff-4649-a174-8a3ff35e423b','2025-03-25 10:00:10',1, 13.25,
'{0a8f90db-abe4-4da4-b8b8-1deb8d01b1fb, 1, quesadilla}');

INSERT INTO  donations  VALUES ('e9396da2-0cd9-4493-985b-51ff399db9cf', '7685b68c-9ddc-4d80-9a1c-bf701b581a09',
'dfe80b5e-89ff-4649-a174-8a3ff35e423b','2025-03-25 18:30:20',3.5, 42.44,
'{1bad3fd1-3255-4dc7-b54f-67739dbb37e7, 2, pasta, 021c007e-57e5-4ea2-90d4-2e61c78e1ac2, 1, burger, aa8e69fc-6ffe-4b50-b452-023875f895f9, 4, Bread');

