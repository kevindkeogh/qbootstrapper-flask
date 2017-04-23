CREATE TABLE IF NOT EXISTS CONVENTIONS (name TEXT, currency TEXT, instrument TEXT, convention TEXT, CONSTRAINT name_currency UNIQUE (name, currency));
