--Insert 5 Foodbanks into business table
CREATE TABLE business (
    businessID TEXT PRIMARY KEY NOT NULL,
    company_name TEXT NOT NULL,
    address TEXT NOT NULL,
    city TEXT NOT NULL,
    state TEXT NOT NULL,
    zip TEXT NOT NULL,
    isFoodbank BOOLEAN NOT NULL DEFAULT 0,
    lat TEXT NOT NULL,
    lng TEXT NOT NULL,
    assoc_user TEXT NOT NULL
);

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

