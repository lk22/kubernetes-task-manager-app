--
-- PostgreSQL database dump
--

\restrict 5G3Owj5XXpOhKa7ziehnWOlQooEzgeQn4POlVZTamIgrDa9edcIuZ5SX8Ko6lwZ

-- Dumped from database version 16.15 (Debian 16.15-1.pgdg13+2)
-- Dumped by pg_dump version 16.15 (Debian 16.15-1.pgdg13+2)

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: persistence_test; Type: TABLE; Schema: public; Owner: root
--

CREATE TABLE public.persistence_test (
    id integer NOT NULL,
    note text
);


ALTER TABLE public.persistence_test OWNER TO root;

--
-- Name: persistence_test_id_seq; Type: SEQUENCE; Schema: public; Owner: root
--

CREATE SEQUENCE public.persistence_test_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.persistence_test_id_seq OWNER TO root;

--
-- Name: persistence_test_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: root
--

ALTER SEQUENCE public.persistence_test_id_seq OWNED BY public.persistence_test.id;


--
-- Name: tasks; Type: TABLE; Schema: public; Owner: root
--

CREATE TABLE public.tasks (
    id character varying(36) NOT NULL,
    title character varying NOT NULL,
    description character varying,
    completed boolean
);


ALTER TABLE public.tasks OWNER TO root;

--
-- Name: persistence_test id; Type: DEFAULT; Schema: public; Owner: root
--

ALTER TABLE ONLY public.persistence_test ALTER COLUMN id SET DEFAULT nextval('public.persistence_test_id_seq'::regclass);


--
-- Data for Name: persistence_test; Type: TABLE DATA; Schema: public; Owner: root
--

COPY public.persistence_test (id, note) FROM stdin;
1	data survives pod restart
2	data survives pod restart
\.


--
-- Data for Name: tasks; Type: TABLE DATA; Schema: public; Owner: root
--

COPY public.tasks (id, title, description, completed) FROM stdin;
\.


--
-- Name: persistence_test_id_seq; Type: SEQUENCE SET; Schema: public; Owner: root
--

SELECT pg_catalog.setval('public.persistence_test_id_seq', 2, true);


--
-- Name: persistence_test persistence_test_pkey; Type: CONSTRAINT; Schema: public; Owner: root
--

ALTER TABLE ONLY public.persistence_test
    ADD CONSTRAINT persistence_test_pkey PRIMARY KEY (id);


--
-- Name: tasks tasks_pkey; Type: CONSTRAINT; Schema: public; Owner: root
--

ALTER TABLE ONLY public.tasks
    ADD CONSTRAINT tasks_pkey PRIMARY KEY (id);


--
-- Name: ix_tasks_id; Type: INDEX; Schema: public; Owner: root
--

CREATE INDEX ix_tasks_id ON public.tasks USING btree (id);


--
-- PostgreSQL database dump complete
--

\unrestrict 5G3Owj5XXpOhKa7ziehnWOlQooEzgeQn4POlVZTamIgrDa9edcIuZ5SX8Ko6lwZ

