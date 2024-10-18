CREATE TABLE contacts (
    id SERIAL PRIMARY KEY,
    fullname VARCHAR(255) NOT NULL,
    phone_number VARCHAR(20) NOT NULL,
    email VARCHAR(100),
);

-- Create an index on the phone_number column for faster lookups
CREATE INDEX idx_contacts_phone_number ON contacts(phone_number);

-- Add a constraint to ensure phone numbers are unique
ALTER TABLE contacts ADD CONSTRAINT unique_phone_number UNIQUE (phone_number);
