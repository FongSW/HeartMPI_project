DROP TABLE IF EXISTS public.patient;
--
-- Table structure for table `patient` 
--

CREATE TABLE patient (
    hn_number varchar(9) PRIMARY KEY,
    first_name varchar(150),
    last_name  varchar(150),
    dob date,
    age_at_reg int,
    gender varchar(6),
    weight decimal(5,2),
    height decimal(5,2),
    created_at timestamp,
    updated_at timestamp
)


TABLESPACE pg_default;

ALTER TABLE IF EXISTS public.patient
    OWNER to airflow;

INSERT INTO public.patient(
	hn_number, first_name, last_name, dob, age_at_reg, gender, weight, height, created_at, updated_at)
	VALUES ('039192-52', 'Siripakorn', 'Worrawunsunthara', '2000-02-04', 5, 'male', 50, 50, '2023-01-02', '2023-01-02');