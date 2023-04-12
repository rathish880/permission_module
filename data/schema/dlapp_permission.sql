-- Schema for DLAPP Permissions.

CREATE TABLE permission(
    permission_id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    user_name TEXT NOT NULL,
    user_group TEXT NOT NULL,
    permission_date TIMESTAMPZ NOT NULL,
    permission_time TEXT NOT NULL,
    requested_on TIMESTAMPZ NOT NULL DEFAULT NOW(),
    acted_on TIMESTAMPZ,
    reason TEXT NOT NULL
);

CREATE TABLE userinfo(
    username TEXT PRIMARY KEY,
    token TEXT
);
