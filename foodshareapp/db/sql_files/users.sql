CREATE TABLE users (
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

