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


ALTER TABLE IF EXISTS public.doctor_diag
    OWNER to airflow;



