CREATE TABLE IF NOT EXISTS foodshare_users (
    uuid uuid NOT NULL,
    email text NOT NULL,
    username text NOT NULL,
    firstname text NOT NULL,
    lastname text NOT NULL,
    salt text NOT NULL,
    password text NOT NULL,
    tos_accepted boolean NOT NULL DEFAULT true,
    tos_accepted_date timestamp with time zone NOT NULL DEFAULT now(),
    last_login timestamp with time zone,
    bad_login_attempt timestamp with time zone,
    bad_login_count integer,
    account_locked boolean NOT NULL DEFAULT false,
    account_verified boolean DEFAULT true,
    account_verified_at timestamp,
  
    PRIMARY KEY (uuid),
    CONSTRAINT unique_email UNIQUE (email)

);