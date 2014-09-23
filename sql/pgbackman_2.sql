--
-- PgBackMan database - Upgrade from 1:1_0_0 to 2:1_1_0
--
-- Copyright (c) 2013-2014 Rafael Martinez Guerrero / PostgreSQL-es
-- rafael@postgresql.org.es / http://www.postgresql.org.es/
--
-- Copyright (c) 2014 USIT-University of Oslo
--
-- This file is part of PgBackMan
-- https://github.com/rafaelma/pgbackman
--

BEGIN;

INSERT INTO pgbackman_version (version,tag) VALUES ('2','v_1_1_0');

COMMIT;
