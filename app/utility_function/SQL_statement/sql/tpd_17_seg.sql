DROP TABLE IF EXISTS public.tpd_17_seg;
--
-- Table structure for table `tpd_17_seg` 
--

CREATE TABLE tpd_17_seg (
    id SERIAL  PRIMARY KEY,
    mpi_test_id int NOT NULL,

    stress_sss decimal(6,2),
    ocr_stress_sss decimal(6,2),
    ocr_clv_stress_sss decimal(6,2),

    stress_sts decimal(6,2),
    ocr_stress_sts decimal(6,2),
    ocr_clv_stress_sts decimal(6,2),

    stress_sms decimal(6,2),
    ocr_stress_sms decimal(6,2),
    ocr_clv_stress_sms decimal(6,2),

    rest_srs decimal(6,2),
    ocr_rest_srs decimal(6,2),
    ocr_clv_rest_srs decimal(6,2),

    rest_sts decimal(6,2),
    ocr_rest_sts decimal(6,2),
    ocr_clv_rest_sts decimal(6,2),

    rest_sms decimal(6,2),
    ocr_rest_sms decimal(6,2),
    ocr_clv_rest_sms decimal(6,2),

    CONSTRAINT fk_mpi_test_id
    FOREIGN KEY(mpi_test_id)
    REFERENCES mpi_test(id)
)


TABLESPACE pg_default;

ALTER TABLE IF EXISTS public.tpd_17_seg
    OWNER to airflow;
