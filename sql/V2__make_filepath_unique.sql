TRUNCATE TABLE documents;

ALTER TABLE documents
ADD CONSTRAINT unique_filepath UNIQUE (filepath);

