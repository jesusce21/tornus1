
CREATE TABLE tobjects
(
  id serial NOT NULL,
  parent_id integer,
  parent_order integer,
  key character varying(64) NOT NULL,
  klass character varying(64) NOT NULL,
  data json NOT NULL,
  CONSTRAINT tobjects_pkey PRIMARY KEY (id)
);

ALTER TABLE tobjects ADD CONSTRAINT fk_tobjects_parent FOREIGN KEY (parent_id)
  REFERENCES tobjects(id);
CREATE UNIQUE INDEX idx_tobjects_parent_key ON tobjects(parent_id, key);
CREATE INDEX idx_tobjects_key ON tobjects(key);
CREATE INDEX idx_tobjects_klass ON tobjects(klass);
