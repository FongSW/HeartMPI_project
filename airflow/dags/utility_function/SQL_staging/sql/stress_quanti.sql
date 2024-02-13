-- --------------------------------------------------------
DROP TABLE IF EXISTS public.stress_quanti;
--
-- Table structure for table `stress_quanti` 
--

CREATE TABLE stress_quanti (
  id SERIAL  PRIMARY KEY,
  mpi_test_id int NOT NULL,

  max_perfusion decimal(6,2) NOT NULL,
  interval decimal(6,2) NOT NULL,
  es decimal(6,2) NOT NULL,
  ed decimal(6,2) NOT NULL,
  lvef decimal(6,2) NOT NULL,
  lad_perf_mean decimal(6,2) NOT NULL,
  lad_perf_sd decimal(6,2) NOT NULL,
  lad_wt_mean decimal(6,2) NOT NULL,
  lad_wt_sd decimal(6,2) NOT NULL,
  lad_wm_mean decimal(6,2) NOT NULL,
  lad_wm_sd decimal(6,2) NOT NULL,

  lcx_perf_mean decimal(6,2) NOT NULL, 
  lcx_perf_sd decimal(6,2) NOT NULL,
  lcx_wt_mean decimal(6,2) NOT NULL,
  lcx_wt_sd decimal(6,2) NOT NULL,
  lcx_wm_mean decimal(6,2) NOT NULL, 
  lcx_wm_sd decimal(6,2) NOT NULL,

  rca_perf_mean decimal(6,2) NOT NULL,
  rca_perf_sd decimal(6,2) NOT NULL,
  rca_wt_mean decimal(6,2) NOT NULL,
  rca_wt_sd decimal(6,2) NOT NULL, 
  rca_wm_mean decimal(6,2) NOT NULL,
  rca_wm_sd decimal(6,2) NOT NULL, 

  tot_perf_mean decimal(6,2) NOT NULL,
  tot_perf_sd decimal(6,2) NOT NULL,
  tot_wt_mean decimal(6,2) NOT NULL,
  tot_wt_sd decimal(6,2) NOT NULL,
  tot_wm_mean decimal(6,2) NOT NULL,
  tot_wm_sd decimal(6,2) NOT NULL,

  lad_perf_ext decimal(6,2) NOT NULL,
  lad_perf_sev decimal(6,2) NOT NULL,
  lad_wt_ext decimal(6,2) NOT NULL,
  lad_wt_sev decimal(6,2) NOT NULL,
  lad_wm_ext decimal(6,2) NOT NULL,
  lad_wm_sev decimal(6,2) NOT NULL,

  lcx_perf_ext decimal(6,2) NOT NULL, 
  lcx_perf_sev decimal(6,2) NOT NULL,
  lcx_wt_ext decimal(6,2) NOT NULL,
  lcx_wt_sev decimal(6,2) NOT NULL,
  lcx_wm_ext decimal(6,2) NOT NULL, 
  lcx_wm_sev decimal(6,2) NOT NULL,

  rca_perf_ext decimal(6,2) NOT NULL,
  rca_perf_sev decimal(6,2) NOT NULL,
  rca_wt_ext decimal(6,2) NOT NULL,
  rca_wt_sev decimal(6,2) NOT NULL, 
  rca_wm_ext decimal(6,2) NOT NULL,
  rca_wm_sev decimal(6,2) NOT NULL, 

  tot_perf_ext decimal(6,2) NOT NULL,
  tot_perf_sev decimal(6,2) NOT NULL,
  tot_wt_ext decimal(6,2) NOT NULL,
  tot_wt_sev decimal(6,2) NOT NULL,
  tot_wm_ext decimal(6,2) NOT NULL,
  tot_wm_sev decimal(6,2) NOT NULL,


  CONSTRAINT fk_mpi_test_id FOREIGN KEY(mpi_test_id) REFERENCES mpi_test(id) ON DELETE CASCADE;
)


ALTER TABLE IF EXISTS public.stress_quanti
    OWNER to airflow;
