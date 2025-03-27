-- Insert test users
INSERT INTO users (
    uuid, email, username, firstname, lastname, salt, password,
    tos_accepted, tos_accepted_date, last_login, bad_login_attempt, bad_login_count,
    account_locked, account_verified, account_verified_at,
    company_name, address, city, state, zip, phone, is_business, is_admin
)
VALUES 

('11111111-aaaa-bbbb-cccc-000000000001', 'admin@foodshare.com', 'adminuser', 'Alex', 'Admin', 'salt1', 'hashed_pw1',
 true, NOW(), NULL, NULL, 0,
 false, true, NOW(),
 NULL, '123 Admin Rd', 'New York', 'NY', '10001', '555-0001', false, true),


('11111111-aaaa-bbbb-cccc-000000000002', 'user1@foodshare.com', 'userone', 'Jamie', 'Doe', 'salt2', 'hashed_pw2',
 true, NOW(), NULL, NULL, 0,
 false, true, NOW(),
 NULL, '456 Maple St', 'Brooklyn', 'NY', '11201', '555-0002', false, false),


('11111111-aaaa-bbbb-cccc-000000000003', 'biz@foodshare.com', 'bizuser', 'Taylor', 'Smith', 'salt3', 'hashed_pw3',
 true, NOW(), NULL, NULL, 0,
 false, true, NOW(),
 'Taylor Bakery', '789 Market Ave', 'Chicago', 'IL', '60616', '555-0003', true, false),


('11111111-aaaa-bbbb-cccc-000000000004', 'locked@foodshare.com', 'lockeduser', 'Jordan', 'Lee', 'salt4', 'hashed_pw4',
 true, NOW(), NULL, NULL, 3,
 true, false, NULL,
 NULL, '321 Blocked Ln', 'Los Angeles', 'CA', '90001', '555-0004', false, false),


('11111111-aaaa-bbbb-cccc-000000000005', 'adminbiz@foodshare.com', 'adminbiz', 'Riley', 'Nguyen', 'salt5', 'hashed_pw5',
 true, NOW(), NULL, NULL, 0,
 false, true, NOW(),
 'Green Grocers Inc.', '500 Green Rd', 'Austin', 'TX', '73301', '555-0005', true, true);
