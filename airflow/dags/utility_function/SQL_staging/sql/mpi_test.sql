DROP TABLE IF EXISTS public.mpi_test;
--
-- Table structure for table `mpi_test` 
--

CREATE TABLE mpi_test (
    id int PRIMARY KEY,
    hn_number varchar(9),
    mpi_exam_date date,
    dm varchar(10),
    ht varchar(10),
    dlp varchar(10),
    ckd varchar(10),
    weight decimal(5,2),
    height decimal(5,2),
    bmi decimal(5,2),
    age int,
    created_at timestamp,
)



ALTER TABLE IF EXISTS public.mpi_test
    OWNER to airflow;