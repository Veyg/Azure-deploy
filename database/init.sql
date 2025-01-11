CREATE TABLE IF NOT EXISTS sample_table (
    id SERIAL PRIMARY KEY,
    data TEXT NOT NULL
);

INSERT INTO sample_table (data) VALUES ('Sample row 1'), ('Sample row 2');
