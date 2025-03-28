CREATE TABLE users (
    userID TEXT PRIMARY KEY NOT NULL,
    userName TEXT NOT NULL,
    firstName TEXT NOT NULL,
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

--4 users from gorup

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

