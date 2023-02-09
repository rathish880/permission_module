-- Schema for Reporter.

CREATE TABLE reports (
       report_id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
       reported_on TIMESTAMPTZ NOT NULL DEFAULT NOW(),
       reported_group TEXT NOT NULL,
       period INTEGER NOT NULL,
       details TEXT NOT NULL
);
