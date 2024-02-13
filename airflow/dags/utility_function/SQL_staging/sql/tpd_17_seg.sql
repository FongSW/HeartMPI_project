DROP TABLE IF EXISTS public.tpd_17_seg;
--
-- Table structure for table `tpd_17_seg` 
--

CREATE TABLE tpd_17_seg (
    id SERIAL  PRIMARY KEY,
    mpi_test_id int NOT NULL,
    stress_sss decimal(6,2) NOT NULL,
    stress_sts decimal(6,2) NOT NULL,
    stress_sms decimal(6,2) NOT NULL,
    rest_srs decimal(6,2) NOT NULL,
    rest_sts decimal(6,2) NOT NULL,
    rest_sms decimal(6,2) NOT NULL,

    CONSTRAINT fk_mpi_test_id FOREIGN KEY(mpi_test_id) REFERENCES mpi_test(id) ON DELETE CASCADE;
)



ALTER TABLE IF EXISTS public.tpd_17_seg
    OWNER to airflow;
