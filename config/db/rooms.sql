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
-- Name: rooms; Type: TABLE; Schema: public; Owner: rstapinski
--

CREATE TABLE rooms (
    id integer NOT NULL,
    name text,
    status text,
    buyin integer,
    type text,
    seats integer
);


ALTER TABLE rooms OWNER TO rstapinski;

--
-- Name: rooms_id_seq; Type: SEQUENCE; Schema: public; Owner: rstapinski
--

CREATE SEQUENCE rooms_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE rooms_id_seq OWNER TO rstapinski;

--
-- Name: rooms_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: rstapinski
--

ALTER SEQUENCE rooms_id_seq OWNED BY rooms.id;


--
-- Name: rooms id; Type: DEFAULT; Schema: public; Owner: rstapinski
--

ALTER TABLE ONLY rooms ALTER COLUMN id SET DEFAULT nextval('rooms_id_seq'::regclass);


--
-- Name: rooms rooms_pkey; Type: CONSTRAINT; Schema: public; Owner: rstapinski
--

ALTER TABLE ONLY rooms
    ADD CONSTRAINT rooms_pkey PRIMARY KEY (id);


--
-- PostgreSQL database dump complete
--

