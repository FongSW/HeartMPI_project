DROP TABLE IF EXISTS public.mpi_test;
--
-- Table structure for table `mpi_test` 
--

CREATE TABLE mpi_test (
    id SERIAL  PRIMARY KEY,
    hn_number varchar(9),
    mpi_exam_date date,
    is_ocr_approved  boolean,
    bookmarked_ml_daig_id int,
    status varchar(10),

    dcm_dpath text,
    large_webp_dpath text,
    small_webp_dpath text,

    dm varchar(10),
    ht varchar(10),
    dlp varchar(10),
    ckd varchar(10),
    weight decimal(5,2),
    height decimal(5,2),
    bmi decimal(5,2),
    age int,
    created_at timestamp,
    updated_at timestamp,

    CONSTRAINT fk_hn_number FOREIGN KEY(hn_number) REFERENCES patient(hn_number) ON DELETE CASCADE
)


TABLESPACE pg_default;

ALTER TABLE IF EXISTS public.mpi_test
    OWNER to airflow;

INSERT INTO mpi_test
VALUES (1, '039192-52', '2023-02-02', true, 1, 'archived', '0', '0', '0', 'positive', 'positive', 'positive', 'positive', 150.00, 169.00, 100, 40, '2023-03-13 14:11:21', '2023-03-13 14:11:21');