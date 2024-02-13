-- --------------------------------------------------------
DROP TABLE IF EXISTS public.rest_quanti;
--
-- Table structure for table `rest_quanti` 
--

CREATE TABLE rest_quanti (
  id SERIAL  PRIMARY KEY,
  mpi_test_id int,
  max_perfusion decimal(6,2),
  ocr_max_perfusion decimal(6,2),
  ocr_clv_max_perfusion decimal(6,2),  
  interval decimal(6,2),
  ocr_interval decimal(6,2),
  ocr_clv_interval decimal(6,2),

  es decimal(6,2),
  ocr_es decimal(6,2),
  ocr_clv_es decimal(6,2),

  ed decimal(6,2),
  ocr_ed decimal(6,2), 
  ocr_clv_ed decimal(6,2), 

  lvef decimal(6,2),
  ocr_lvef decimal(6,2),
  ocr_clv_lvef decimal(6,2),

  lad_perf_mean decimal(6,2),
  ocr_lad_perf_mean decimal(6,2),
  ocr_clv_lad_perf_mean decimal(6,2),

  lad_perf_sd decimal(6,2),
  ocr_lad_perf_sd decimal(6,2),
  ocr_clv_lad_perf_sd decimal(6,2),

  lad_wt_mean decimal(6,2),
  ocr_lad_wt_mean decimal(6,2),
  ocr_clv_lad_wt_mean decimal(6,2),

  lad_wt_sd decimal(6,2),
  ocr_lad_wt_sd decimal(6,2),
  ocr_clv_lad_wt_sd decimal(6,2), 

  lad_wm_mean decimal(6,2),
  ocr_lad_wm_mean decimal(6,2), 
  ocr_clv_lad_wm_mean decimal(6,2), 

  lad_wm_sd decimal(6,2),
  ocr_lad_wm_sd decimal(6,2), 
  ocr_clv_lad_wm_sd decimal(6,2),


  lcx_perf_mean decimal(6,2), 
  ocr_lcx_perf_mean decimal(6,2), 
  ocr_clv_lcx_perf_mean decimal(6,2), 

  lcx_perf_sd decimal(6,2),
  ocr_lcx_perf_sd decimal(6,2),
  ocr_clv_lcx_perf_sd decimal(6,2),

  lcx_wt_mean decimal(6,2),
  ocr_lcx_wt_mean decimal(6,2), 
  ocr_clv_lcx_wt_mean decimal(6,2), 

  lcx_wt_sd decimal(6,2),
  ocr_lcx_wt_sd decimal(6,2),
  ocr_clv_lcx_wt_sd decimal(6,2),

  lcx_wm_mean decimal(6,2), 
  ocr_lcx_wm_mean decimal(6,2),
  ocr_clv_lcx_wm_mean decimal(6,2), 

  lcx_wm_sd decimal(6,2),
  ocr_lcx_wm_sd decimal(6,2),
  ocr_clv_lcx_wm_sd decimal(6,2),


  rca_perf_mean decimal(6,2),
  ocr_rca_perf_mean decimal(6,2),
  ocr_clv_rca_perf_mean decimal(6,2),

  rca_perf_sd decimal(6,2),
  ocr_rca_perf_sd decimal(6,2), 
  ocr_clv_rca_perf_sd decimal(6,2), 

  rca_wt_mean decimal(6,2),
  ocr_rca_wt_mean decimal(6,2), 
  ocr_clv_rca_wt_mean decimal(6,2), 

  rca_wt_sd decimal(6,2), 
  ocr_rca_wt_sd decimal(6,2), 
  ocr_clv_rca_wt_sd decimal(6,2),

  rca_wm_mean decimal(6,2),
  ocr_rca_wm_mean decimal(6,2),
  ocr_clv_rca_wm_mean decimal(6,2),

  rca_wm_sd decimal(6,2), 
  ocr_rca_wm_sd decimal(6,2), 
  ocr_clv_rca_wm_sd decimal(6,2), 

  tot_perf_mean decimal(6,2),
  ocr_tot_perf_mean decimal(6,2),
  ocr_clv_tot_perf_mean decimal(6,2),

  tot_perf_sd decimal(6,2),
  ocr_tot_perf_sd decimal(6,2),
  ocr_clv_tot_perf_sd decimal(6,2),

  tot_wt_mean decimal(6,2),
  ocr_tot_wt_mean decimal(6,2),
  ocr_clv_tot_wt_mean decimal(6,2), 

  tot_wt_sd decimal(6,2),
  ocr_tot_wt_sd decimal(6,2),
  ocr_clv_tot_wt_sd decimal(6,2),
  
  tot_wm_mean decimal(6,2),
  ocr_tot_wm_mean decimal(6,2),
  ocr_clv_tot_wm_mean decimal(6,2),

  tot_wm_sd decimal(6,2),
  ocr_tot_wm_sd decimal(6,2), 
  ocr_clv_tot_wm_sd decimal(6,2),


  lad_perf_ext decimal(6,2),
  ocr_lad_perf_ext decimal(6,2),
  ocr_clv_lad_perf_ext decimal(6,2),

  lad_perf_sev decimal(6,2),
  ocr_lad_perf_sev decimal(6,2),
  ocr_clv_lad_perf_sev decimal(6,2),

  lad_wt_ext decimal(6,2),
  ocr_lad_wt_ext decimal(6,2),
  ocr_clv_lad_wt_ext decimal(6,2),

  lad_wt_sev decimal(6,2),
  ocr_lad_wt_sev decimal(6,2),
  ocr_clv_lad_wt_sev decimal(6,2), 

  lad_wm_ext decimal(6,2),
  ocr_lad_wm_ext decimal(6,2), 
  ocr_clv_lad_wm_ext decimal(6,2), 

  lad_wm_sev decimal(6,2),
  ocr_lad_wm_sev decimal(6,2), 
  ocr_clv_lad_wm_sev decimal(6,2),


  lcx_perf_ext decimal(6,2), 
  ocr_lcx_perf_ext decimal(6,2), 
  ocr_clv_lcx_perf_ext decimal(6,2), 

  lcx_perf_sev decimal(6,2),
  ocr_lcx_perf_sev decimal(6,2),
  ocr_clv_lcx_perf_sev decimal(6,2),

  lcx_wt_ext decimal(6,2),
  ocr_lcx_wt_ext decimal(6,2), 
  ocr_clv_lcx_wt_ext decimal(6,2), 

  lcx_wt_sev decimal(6,2),
  ocr_lcx_wt_sev decimal(6,2),
  ocr_clv_lcx_wt_sev decimal(6,2),

  lcx_wm_ext decimal(6,2), 
  ocr_lcx_wm_ext decimal(6,2),
  ocr_clv_lcx_wm_ext decimal(6,2), 

  lcx_wm_sev decimal(6,2),
  ocr_lcx_wm_sev decimal(6,2),
  ocr_clv_lcx_wm_sev decimal(6,2),


  rca_perf_ext decimal(6,2),
  ocr_rca_perf_ext decimal(6,2),
  ocr_clv_rca_perf_ext decimal(6,2),

  rca_perf_sev decimal(6,2),
  ocr_rca_perf_sev decimal(6,2), 
  ocr_clv_rca_perf_sev decimal(6,2), 

  rca_wt_ext decimal(6,2),
  ocr_rca_wt_ext decimal(6,2), 
  ocr_clv_rca_wt_ext decimal(6,2), 

  rca_wt_sev decimal(6,2), 
  ocr_rca_wt_sev decimal(6,2), 
  ocr_clv_rca_wt_sev decimal(6,2),

  rca_wm_ext decimal(6,2),
  ocr_rca_wm_ext decimal(6,2),
  ocr_clv_rca_wm_ext decimal(6,2),

  rca_wm_sev decimal(6,2), 
  ocr_rca_wm_sev decimal(6,2), 
  ocr_clv_rca_wm_sev decimal(6,2), 

  tot_perf_ext decimal(6,2),
  ocr_tot_perf_ext decimal(6,2),
  ocr_clv_tot_perf_ext decimal(6,2),

  tot_perf_sev decimal(6,2),
  ocr_tot_perf_sev decimal(6,2),
  ocr_clv_tot_perf_sev decimal(6,2),

  tot_wt_ext decimal(6,2),
  ocr_tot_wt_ext decimal(6,2),
  ocr_clv_tot_wt_ext decimal(6,2), 

  tot_wt_sev decimal(6,2),
  ocr_tot_wt_sev decimal(6,2),
  ocr_clv_tot_wt_sev decimal(6,2),
  
  tot_wm_ext decimal(6,2),
  ocr_tot_wm_ext decimal(6,2),
  ocr_clv_tot_wm_ext decimal(6,2),

  tot_wm_sev decimal(6,2),
  ocr_tot_wm_sev decimal(6,2), 
  ocr_clv_tot_wm_sev decimal(6,2),

  CONSTRAINT fk_mpi_test_id
  FOREIGN KEY(mpi_test_id)
  REFERENCES mpi_test(id)
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS public.rest_quanti
    OWNER to airflow;



