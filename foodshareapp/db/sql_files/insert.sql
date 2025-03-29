--########################## BUSINESS INSERTIONS ####################################

--Insert 5 Foodbanks into business table

INSERT INTO business  VALUES ('dcf47826-e330-4754-8f86-3ebae7a4663b', 'Hope Bank', '3581 SW Archer Rd','Gainesville',
'Fl', '32608', 1, '29.6227377', '-82.3761601', '618e258b-2014-4bdf-a209-a223e268b814');

INSERT INTO business  VALUES ('db6b740c-74f4-44a0-95ea-5c16883fad88', 'Faith Bank', '25 Nw 16th Ave','Gainesville',
'Fl', '32601', 1, '29.6661887', '-82.3256044', 'ae90c77e-2b4d-4162-94b7-77467eeb2d98');

INSERT INTO business  VALUES ('96facdbd-f407-4a56-b889-51a3dab13ace', 'Help Bank', '1800 NE 12TH Ave','Gainesville',
'Fl', '32641', 1, '29.6640146', '-82.3009662', 'ea93b0c1-a985-444d-a10e-6444846c2337');

INSERT INTO business  VALUES ('dfe80b5e-89ff-4649-a174-8a3ff35e423b', 'Love Bank', '133 SW 34th St','Gainesville',
'Fl', '32607', 1, '29.6507802', '-82.37214', 'a3b18f5b-bfe8-4720-b678-c74b32d7258a');

INSERT INTO business  VALUES ('1701c23b-5492-4832-ae6b-86a8ea162f9c', 'Giving Bank', '4620 NW 39th Ave','Gainesville',
'Fl', '32606', 1, '29.6890763', '-82.3929102', 'c67f63ad-7741-4e29-a879-7aa1703f2109');

--Insert 5 businesses into business table

INSERT INTO business  VALUES ('b298ab1b-c281-46fe-a4ab-b738106df501', 'Outback Steakhouse', '3760 Archer Road','Gainesville',
'Fl', '32608', 0, '29.6211645', '-82.3800495', 'cb5a6b40-5998-454f-a623-6d20ecdb1705');

INSERT INTO business  VALUES ('7685b68c-9ddc-4d80-9a1c-bf701b581a09', 'Cheesecake Factory', '2851 SW 35th Drive, Suite 70','Gainesville',
'Fl', '32608', 0, '29.6263795', '-82.3751', '2667585a-13e0-4349-b100-3f3079fa469d');

INSERT INTO business  VALUES ('f7d97c9f-e3fa-4b76-a080-b2d3bdaa3a38', 'The Top', '30 North Main Street','Gainesville',
'Fl', '32601', 0, '29.652564', '-82.3252352', '22d9fc62-bcc7-41ea-9864-a5cd2784bfda');

INSERT INTO business  VALUES ('5b9003ac-f149-4c4e-8754-56ce0d762429', 'Carrabbas Italian Grill', '3021 SW 34th Street','Gainesville',
'Fl', '32608', 0, '29.6261194', '-82.3715944', '31675804-b4cd-412c-aca3-fbde51afa779');

INSERT INTO business  VALUES ('42b21442-3bb6-48a2-992f-9c7c331e86c6', 'Texas Roadhouse', '3984 SW 43rd Street','Gainesville',
'Fl', '32608', 0, '29.6170211', '-82.3895885', 'a591ead8-3cf7-4fee-bb19-607b0cc68ca7');

--########################## INVENTORY INSERTIONS ####################################

--Insert Inventory into Hope Bank
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

--Insert Inventory into Faith Bank

INSERT INTO  FoodBankInventory VALUES ('8f882212-08e8-47de-a1cf-f2043a58fdde', 'db6b740c-74f4-44a0-95ea-5c16883fad88',
'Chicken',4, 'Available');

INSERT INTO  FoodBankInventory VALUES ('4ac03e84-ded4-4325-991d-fee938abd934', 'db6b740c-74f4-44a0-95ea-5c16883fad88',
'Chicken',5, 'Available');

INSERT INTO  FoodBankInventory VALUES ('02522929-2648-4051-a3d8-503f4563e8dc', 'db6b740c-74f4-44a0-95ea-5c16883fad88',
'Grapes',2, 'Available');

INSERT INTO  FoodBankInventory VALUES ('e68343c0-8817-4f52-8b9e-bffb97e8b162', 'db6b740c-74f4-44a0-95ea-5c16883fad88',
'Ham',1, 'Available');

--Insert Inventory into Help Bank

INSERT INTO  FoodBankInventory VALUES ('7518fd36-ee4f-4243-9c2a-7616d48e28b3', '96facdbd-f407-4a56-b889-51a3dab13ace',
'Pear',1, 'Available');

INSERT INTO  FoodBankInventory VALUES ('0350fa67-8b2b-4da7-9e64-7e359a5bd615', '96facdbd-f407-4a56-b889-51a3dab13ace',
'Peach',1, 'Available');

--Insert Inventory into Love Bank

INSERT INTO  FoodBankInventory VALUES ('6e7c0ea6-7dda-41f7-babc-05f7e225f416', 'dfe80b5e-89ff-4649-a174-8a3ff35e423b',
'Fish',2, 'Available');

INSERT INTO  FoodBankInventory VALUES ('3fd6aa5e-c897-4782-b1a6-2f4e100aee21', 'dfe80b5e-89ff-4649-a174-8a3ff35e423b',
'Peas',1, 'Available');

INSERT INTO  FoodBankInventory VALUES ('d67f5748-54b5-43fd-8e11-608efbb0f698', 'dfe80b5e-89ff-4649-a174-8a3ff35e423b',
'Crackers',2, 'Available');

INSERT INTO  FoodBankInventory VALUES ('d5e63bdc-0068-4581-8720-9ee96f57d0bf', 'dfe80b5e-89ff-4649-a174-8a3ff35e423b',
'Crackers',1, 'Available');

INSERT INTO  donations  VALUES ('45a69c48-3b32-49a0-80ad-afb8193aa115', 'b298ab1b-c281-46fe-a4ab-b738106df501',
'dcf47826-e330-4754-8f86-3ebae7a4663b','2025-03-25 14:30:20',2.4, 23.02,
'{b82f4746-db31-4289-a34f-05a0d2d043e2, 1, steak, 42203df1-5e03-4112-aff3-431d563b877f, 2, fries}');

--########################## DONATION INSERTIONS ####################################

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

--####################################### user insertions ####################################


--4 users from group

INSERT INTO users VALUES ('0db55890-fe93-4063-b8e3-c61808b2a37f', 'kyle84', 'Kyle','Cortez',
'kcortez@ufl.edu', '352-232-9819', 'itlanghndk', 'kcor89t71', 1, '2025-03-01 09:08:12',
'2024-03-26 15:00:12', '2024-03-22 19:20:01', 2, 0, 1,
'2025-03-02 10:00:00');

INSERT INTO users VALUES ('a175b716-7496-4f69-8827-8c252b61d2e8', 'alex728', 'Alex','John',
'ajohn@ufl.edu', '352-123-2981', 'qvoxjfflgh', 'ajo81n99', 1, '2025-03-02 10:09:11',
'2024-03-25 14:25:08', '2024-03-18 12:55:22', 1, 0, 1,
'2025-03-03 10:00:00');

INSERT INTO users VALUES ('8e94946d-b499-44f7-b1d9-1fb71c80be5e', 'ine245', 'Ine','Park',
'ipark@ufl.edu', '352-525-1489', 'fxbfgcqjqb', 'par892lk', 1, '2025-03-03 11:22:00',
'2024-03-24 09:30:02', '2024-03-04 22:22:01', 3, 0, 1,
'2025-03-04 10:00:00');

INSERT INTO users VALUES ('72dc96f2-fde5-4f4c-8446-0f766529ddcc', 'dillon91', 'Dillon','Kilgallon',
'dkilgallon@ufl.edu', '352-981-0922', 'fzbuzrndib', 'dil90on00', 1, '2025-03-04 19:44:22',
'2024-03-25 11:22:22', '2024-03-18 19:00:02', 1, 0, 1,
'2025-03-05 10:00:00');


--5 foodbanks

INSERT INTO users VALUES ('618e258b-2014-4bdf-a209-a223e268b814', 'hopeBank22', 'Steve','Smith',
'steveSmith@hopeBankGNV.com', '352-198-2254', 'zhcfcswdbv', 'ho90espe0', 1, '2025-03-28 11:22:15',
'2024-03-27 16:20:15', '2024-03-29 19:25:11', 1, 0, 1,
'2025-03-29 10:00:00');

INSERT INTO users VALUES ('ae90c77e-2b4d-4162-94b7-77467eeb2d98', 'faithbank96', 'Jen','Lola',
'jenLola@faithBankGNV.com', '352-029-1235', 'dadgzrqpvw', 'f90ait0sh', 1, '2025-03-12 22:25:14',
'2024-03-24 07:44:25', '2024-03-25 10:11:55', 5, 0, 1,
'2025-03-13 10:00:00');

INSERT INTO users VALUES ('ea93b0c1-a985-444d-a10e-6444846c2337', 'helpbank22', 'Ben','Uoita',
'BenUoita@helpBankGNV.com', '352-452-0897', 'zyyfrwltrw', 'he873lps', 1, '2025-03-15 11:55:01',
'2024-03-27 19:22:10', '2024-03-26 08:24:10', 10, 0, 1,
'2025-03-16 10:00:00');

INSERT INTO users VALUES ('a3b18f5b-bfe8-4720-b678-c74b32d7258a', 'loveBank42', 'Nancy','Sharp',
'NancySharp@loveBankGNV.com', '352-789-2687', 'uettflroqc', 'lo9ve00e2', 1, '2025-02-27 09:30:00',
'2024-03-26 16:44:18', '2024-03-25 11:11:09', 6, 0, 1,
'2025-02-28 10:00:00');

INSERT INTO users VALUES ('c67f63ad-7741-4e29-a879-7aa1703f2109', 'givingBank67', 'Bart','Simpson',
'BartSimpson@givingBankGNV.com', '352-124-2382', 'ywxbniurwr', 'giv78ee90', 1, '2025-03-02 10:21:22',
'2024-03-22 14:22:11', '2024-03-21 10:10:09', 0, 0, 1,
'2025-03-03 10:00:00');

--5 businesses

INSERT INTO users VALUES ('cb5a6b40-5998-454f-a623-6d20ecdb1705', 'outBack54', 'Mike','Shapiro',
'mikeShapiro@outBackGNV.com', '352-983-2340', 'wgszoljttx', 'out78sdfback', 1, '2025-03-05 09:54:22',
'2024-03-15 16:25:10', '2024-03-14 16:00:00', 2, 0, 1,
'2025-03-06 10:00:00');

INSERT INTO users VALUES ('2667585a-13e0-4349-b100-3f3079fa469d', 'cheeseCake99', 'Jen','Bena',
'jenBena@cheeseCakeGNV.com', '352-564-6796', 'ztpyhiuhki', '89cheese90', 1, '2025-03-17 10:20:11',
'2024-03-20 18:10:10', '2024-03-20 18:05:06', 4, 0, 1,
'2025-03-18 10:00:00');

INSERT INTO users VALUES ('22d9fc62-bcc7-41ea-9864-a5cd2784bfda', 'top8912', 'Martin','Prince',
'martinPrince@topGNV.com', '352-258-8742', 'kstemjhheq', 'top902910', 1, '2025-03-12 09:08:22',
'2024-03-25 14:22:45', '2024-03-25 14:21:06', 9, 0, 1,
'2025-03-13 10:00:00');

INSERT INTO users VALUES ('31675804-b4cd-412c-aca3-fbde51afa779', 'carrabba99', 'Cindy','Cindyson',
'cindyCindyson@carrabbaGNV.com', '352-678-3402', 'checsoggmz', 'carba01932', 1, '2025-03-05 11:11:54',
'2024-03-26 19:30:45', '2024-03-20 15:15:06', 4, 0, 1,
'2025-03-06 10:00:00');

INSERT INTO users VALUES ('a591ead8-3cf7-4fee-bb19-607b0cc68ca7', 'texasRoad90', 'Tom','Benson',
'TomBenson@texasRoadGNV.com', '352-567-0569', 'ztpyhiuhki', 'texa8sse7', 1, '2025-03-09 12:12:53',
'2024-03-20 18:20:22', '2024-03-19 15:14:11', 1, 0, 1,
'2025-03-10 10:00:00');

--######################### reservation insertions ##########################################


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


