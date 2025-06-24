ALTER TABLE documents
    ADD COLUMN checksum BINARY(32),
    DROP INDEX unique_filepath,
    ADD CONSTRAINT documents_unique_checksum UNIQUE (checksum);
