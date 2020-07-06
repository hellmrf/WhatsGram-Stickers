CREATE TABLE users
(
    id serial,
    chat_id character varying(32),
    package_name character varying(64),
    stage smallint,
    package_title character varying(64),
    PRIMARY KEY (id),
    UNIQUE (chat_id)
);