--
-- PostgreSQL database dump
--

-- Dumped from database version 9.6.3
-- Dumped by pg_dump version 9.6.3

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SET check_function_bodies = false;
SET client_min_messages = warning;
SET row_security = off;

SET search_path = public, pg_catalog;

SET default_tablespace = '';

SET default_with_oids = false;

--
-- Name: participation; Type: TABLE; Schema: public; Owner: rstapinski
--

CREATE TABLE participation (
    id integer NOT NULL,
    game_id integer,
    user_id integer
);


ALTER TABLE participation OWNER TO rstapinski;

--
-- Name: participation_id_seq; Type: SEQUENCE; Schema: public; Owner: rstapinski
--

CREATE SEQUENCE participation_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE participation_id_seq OWNER TO rstapinski;

--
-- Name: participation_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: rstapinski
--

ALTER SEQUENCE participation_id_seq OWNED BY participation.id;


--
-- Name: participation id; Type: DEFAULT; Schema: public; Owner: rstapinski
--

ALTER TABLE ONLY participation ALTER COLUMN id SET DEFAULT nextval('participation_id_seq'::regclass);


--
-- Name: participation participation_pkey; Type: CONSTRAINT; Schema: public; Owner: rstapinski
--

ALTER TABLE ONLY participation
    ADD CONSTRAINT participation_pkey PRIMARY KEY (id);


--
-- PostgreSQL database dump complete
--

