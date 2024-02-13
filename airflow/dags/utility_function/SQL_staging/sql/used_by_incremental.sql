DROP TABLE IF EXISTS public.used_by_incremental;
--
-- Table structure for table `used_by_incremental` 
--

CREATE TABLE used_by_incremental (
    id SERIAL  PRIMARY KEY,
    mpi_test_id int NOT NULL,
    patient_quanti boolean NOT NULL,
    patient_quali boolean NOT NULL,
    lad_quanti boolean NOT NULL,
    lad_quali boolean NOT NULL,
    lcx_quanti boolean NOT NULL,
    lcx_quali boolean NOT NULL,
    rca_quanti boolean NOT NULL,
    rca_quali boolean NOT NULL,

    CONSTRAINT fk_mpi_test_id FOREIGN KEY(mpi_test_id) REFERENCES mpi_test(id) ON DELETE CASCADE;
)


ALTER TABLE IF EXISTS public.used_by_incremental
    OWNER to airflow;
