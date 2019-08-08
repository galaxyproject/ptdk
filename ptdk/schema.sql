DROP TABLE IF EXISTS tutorials;

CREATE TABLE tutorials (
  uuid TEXT PRIMARY KEY,
  name TEXT NOT NULL,
  galaxy_url TEXT NOT NULL,
  workflow_id TEXT NOT NULL
);