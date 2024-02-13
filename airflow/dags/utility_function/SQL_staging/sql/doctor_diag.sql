-- --------------------------------------------------------
DROP TABLE IF EXISTS public.doctor_diag;
--
-- Table structure for table `doctor_diag` 
--

CREATE TABLE doctor_diag (
  id SERIAL  PRIMARY KEY,
  mpi_test_id int,
  lad_predict varchar(10),
  lcx_predict varchar(10),
  rca_predict varchar(10),
  patient_predict varchar(10),
  
  CONSTRAINT fk_mpi_test_id FOREIGN KEY(mpi_test_id) REFERENCES mpi_test(id) ON DELETE CASCADE;
)

TABLESPACE pg_default;
ALTER TABLE IF EXISTS public.doctor_diag
    OWNER to airflow;

INSERT INTO public.doctor_diag(
	id, mpi_test_id, diagnosed_by, lad_predict, lcx_predict, rca_predict, patient_predict, created_at, updated_at)
	VALUES (1, 1, 1, 'positive', 'negative', 'negative', 'positive', '2023-03-014', '2023-03-014');

