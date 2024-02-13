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
);


INSERT INTO public.patient(
	hn_number, first_name, last_name, dob, age_at_reg, gender, weight, height, created_at, updated_at)
	VALUES ('039192-52', 'Siripakorn', 'Worrawunsunthara', '2000-02-04', 5, 'male', 50, 50, '2023-01-02', '2023-01-02');

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

    CONSTRAINT patient_mpi_test_fk FOREIGN KEY (hn_number) REFERENCES patient(hn_number) ON DELETE CASCADE
    -- CONSTRAINT ml_diag_mpi_test_fk FOREIGN KEY (bookmarked_ml_daig_id) REFERENCES ml_diag(id) ON DELETE CASCADE
);


INSERT INTO mpi_test
VALUES 
    (1, '039192-52', '2023-02-02', true, 1, 'archived', '0', '0', '0', 'positive', 'positive', 'positive', 'positive', 150.00, 169.00, 100, 40, '2023-03-01 21:26:51.219669', '2023-03-01 21:26:51.219669'),
    (2, '039192-52', '2023-02-03', true, 1, 'archived', '0', '0', '0', 'positive', 'positive', 'positive', 'positive', 150.00, 169.00, 100, 40, '2023-03-02 21:26:51.219669', '2023-03-02 21:26:51.219669'),
    (3, '039192-52', '2023-02-04', true, 1, 'archived', '0', '0', '0', 'positive', 'positive', 'positive', 'positive', 150.00, 169.00, 100, 40, '2023-03-01 21:26:51.219669', '2023-03-01 21:26:51.219669'),
    (4, '039192-52', '2023-02-05', true, 1, 'archived', '0', '0', '0', 'positive', 'positive', 'positive', 'positive', 150.00, 169.00, 100, 40, '2023-03-02 21:26:51.219669', '2023-03-02 21:26:51.219669'),
    (5, '039192-52', '2023-02-06', true, 1, 'archived', '0', '0', '0', 'positive', 'positive', 'positive', 'positive', 150.00, 169.00, 100, 40, '2023-03-01 21:26:51.219669', '2023-03-01 21:26:51.219669'),
    (6, '039192-52', '2023-02-07', true, 1, 'archived', '0', '0', '0', 'positive', 'positive', 'positive', 'positive', 150.00, 169.00, 100, 40, '2023-03-02 21:26:51.219669', '2023-03-02 21:26:51.219669'),
    (7, '039192-52', '2023-02-08', true, 1, 'archived', '0', '0', '0', 'positive', 'positive', 'positive', 'positive', 150.00, 169.00, 100, 40, '2023-03-01 21:26:51.219669', '2023-03-01 21:26:51.219669'),
    (8, '039192-52', '2023-02-09', true, 1, 'archived', '0', '0', '0', 'positive', 'positive', 'positive', 'positive', 150.00, 169.00, 100, 40, '2023-03-02 21:26:51.219669', '2023-03-02 21:26:51.219669'),
    (9, '039192-52', '2023-02-10', true, 1, 'archived', '0', '0', '0', 'positive', 'positive', 'positive', 'positive', 150.00, 169.00, 100, 40, '2023-03-01 21:26:51.219669', '2023-03-01 21:26:51.219669'),
    (10, '039192-52', '2023-02-11', true, 1, 'archived', '0', '0', '0', 'positive', 'positive', 'positive', 'positive', 150.00, 169.00, 100, 40, '2023-03-02 21:26:51.219669', '2023-03-02 21:26:51.219669');

DROP TABLE IF EXISTS public.mpi_crop_img;
--
-- Table structure for table `mpi_crop_img` 
--

CREATE TABLE mpi_crop_img (
    id SERIAL PRIMARY KEY,
    mpi_test_id int,
    stress_perfusion_dpath varchar(100),
    rest_perfusion_dpath varchar(100),

    stress_severity_dpath varchar(100),
    rest_severity_dpath varchar(100),

    stress_blackout_dpath varchar(100),
    rest_blackout_dpath varchar(100),

    stress_def_sev_dpath varchar(100),
    rest_def_sev_dpath varchar(100),

    CONSTRAINT fk_mpi_test_id FOREIGN KEY(mpi_test_id) REFERENCES mpi_test(id) ON DELETE CASCADE
);


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

  CONSTRAINT fk_mpi_test_id FOREIGN KEY(mpi_test_id) REFERENCES mpi_test(id) ON DELETE CASCADE
);


-- --------------------------------------------------------
DROP TABLE IF EXISTS public.stress_quanti;
--
-- Table structure for table `stress_quanti` 
--

CREATE TABLE stress_quanti (
  id SERIAL  PRIMARY KEY,
  mpi_test_id int NOT NULL,

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

  CONSTRAINT fk_mpi_test_id FOREIGN KEY(mpi_test_id) REFERENCES mpi_test(id) ON DELETE CASCADE
);


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

    CONSTRAINT fk_mpi_test_id FOREIGN KEY(mpi_test_id) REFERENCES mpi_test(id) ON DELETE CASCADE
);

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
  
  CONSTRAINT fk_mpi_test_id FOREIGN KEY(mpi_test_id) REFERENCES mpi_test(id) ON DELETE CASCADE
);

INSERT INTO doctor_diag
VALUES 
    (1, 1, 1, 1, 0, 1),
    (2, 2, 1, 0, 1, 1),
    (3, 3, 0, 1, 1, 1),
    (4, 4, 1, 0, 1, 1),
    (5, 5, 1, 1, 0, 1),
    (6, 6, 1, 1, 0, 1),
    (7, 7, 1, 0, 1, 1),
    (8, 8, 0, 1, 1, 1),
    (9, 9, 1, 0, 1, 1),
    (10, 10, 1, 1, 0, 1);
    


ALTER TABLE IF EXISTS public.ml_diag
    OWNER to airflow;

DROP TABLE IF EXISTS public.ml_model;
--
-- Table structure for table `ml_model` 
--
CREATE TYPE ML_TARGET AS enum('LAD', 'LCX', 'RCA', 'PATIENT');
CREATE TABLE ml_model (
  id SERIAL  PRIMARY KEY,
  name varchar(10),
  indicator varchar(15),
  type varchar(18),
  target ML_TARGET,
  version varchar(12),
  val_acc decimal(3,2),
  val_specificity decimal(3,2),
  val_precision decimal(3,2),
  val_recall decimal(3,2),
  val_f1 decimal(3,2),
  val_fnr decimal(3,2),
  val_tpr decimal(3,2),
  val_tnr decimal(3,2),
  val_fpt decimal(3,2),
  adapt_graph JSON,
  brand_quanti_model varchar(18),
  model_dpath varchar(100),
  is_best boolean,
  created_at timestamp,
  updated_at timestamp
);

INSERT INTO ml_model (name, indicator, type, target, version, val_acc, val_specificity, val_precision, val_recall, val_f1, val_fnr, val_tpr, val_tnr, val_fpt, adapt_graph, brand_quanti_model, model_dpath, is_best, created_at, updated_at)
VALUES
    ('Base', 'Qualitative', 'Base', 'LAD', '01.01.2023', 0.88, 0.97, 0.97, 0.97, 0.97, 0.10, 0.90, 0.90, 0.10, '{"model_id":1,"name":"Base","indicator":"Qualitative","type":"-","version":"01.01.2023"}', '-', './app/model/base/qualitative/LAD/', TRUE, '2077-03-02 21:26:51.219669', '2077-03-02 21:26:51.219669'),
    ('Base', 'Qualitative', 'Base', 'LCX', '01.01.2023', 0.96, 0.99, 0.98, 0.97, 0.97, 0.05, 0.95, 0.90, 0.10, '{"model_id":2,"name":"Base","indicator":"Qualitative","type":"-","version":"01.01.2023"}', '-', './app/model/base/qualitative/LCX/', TRUE, '2077-03-02 21:26:51.219669', '2077-03-02 21:26:51.219669'),
    ('Base', 'Qualitative', 'Base', 'RCA', '01.01.2023', 0.88, 0.97, 0.97, 0.97, 0.97, 0.10, 0.90, 0.90, 0.10, '{"model_id":3,"name":"Base","indicator":"Qualitative","type":"-","version":"01.01.2023"}', '-', './app/model/base/qualitative/RCA/', TRUE, '2077-03-02 21:26:51.219669', '2077-03-02 21:26:51.219669'),
    ('Base', 'Qualitative', 'Base', 'PATIENT', '01.01.2023', 0.88, 0.97, 0.97, 0.97, 0.97, 0.10, 0.90, 0.90, 0.10, '{"model_id":4,"name":"Base","indicator":"Qualitative","type":"-","version":"01.01.2023"}', '-', './app/model/base/qualitative/PATIENT/', TRUE, '2077-03-02 21:26:51.219669', '2077-03-02 21:26:51.219669'),

    ('Base', 'Quantitative', 'Base', 'LAD', '01.01.2023', 0.88, 0.97, 0.97, 0.97, 0.97, 0.10, 0.90, 0.90, 0.10, '{"model_id":5,"name":"Base","indicator":"Quantitative","type":"-","version":"01.01.2023"}', 'lgbm', './app/model/base/quantitative/LAD', TRUE, '2077-03-02 21:26:51.219669', '2077-03-02 21:26:51.219669'),
    ('Base', 'Quantitative', 'Base', 'LCX', '01.01.2023', 0.96, 0.99, 0.98, 0.97, 0.97, 0.05, 0.95, 0.90, 0.10, '{"model_id":6,"name":"Base","indicator":"Quantitative","type":"-","version":"01.01.2023"}', 'lgbm', './app/model/base/quantitative/LCX', TRUE, '2077-03-02 21:26:51.219669', '2077-03-02 21:26:51.219669'),
    ('Base', 'Quantitative', 'Base', 'RCA', '01.01.2023', 0.88, 0.97, 0.97, 0.97, 0.97, 0.10, 0.90, 0.90, 0.10, '{"model_id":7,"name":"Base","indicator":"Quantitative","type":"-","version":"01.01.2023"}', 'lgbm', './app/model/base/quantitative/RCA', TRUE, '2077-03-02 21:26:51.219669', '2077-03-02 21:26:51.219669'),
    ('Base', 'Quantitative', 'Base', 'PATIENT', '01.01.2023', 0.88, 0.97, 0.97, 0.97, 0.97, 0.10, 0.90, 0.90, 0.10, '{"model_id":8,"name":"Base","indicator":"Quantitative","type":"-","version":"01.01.2023"}', 'lgbm', './app/model/base/quantitative/PATIENT', TRUE, '2077-03-02 21:26:51.219669', '2077-03-02 21:26:51.219669'),

    ('Base', 'Hybrid', 'Base', 'LAD', '01.01.2023', 0.88, 0.97, 0.97, 0.97, 0.97, 0.10, 0.90, 0.90, 0.10, '{"model_id":9,"name":"Base","indicator":"Hybrid","type":"-","version":"01.01.2023"}', '-', './app/model/base/Hybrid/LAD', TRUE, '2077-03-02 21:26:51.219669', '2077-03-02 21:26:51.219669'),
    ('Base', 'Hybrid', 'Base', 'LCX', '01.01.2023', 0.96, 0.99, 0.98, 0.97, 0.97, 0.05, 0.95, 0.90, 0.10, '{"model_id":10,"name":"Base","indicator":"Hybrid","type":"-","version":"01.01.2023"}', '-', './app/model/base/Hybrid/LCX', TRUE, '2077-03-02 21:26:51.219669', '2077-03-02 21:26:51.219669'),
    ('Base', 'Hybrid', 'Base', 'RCA', '01.01.2023', 0.88, 0.97, 0.97, 0.97, 0.97, 0.10, 0.90, 0.90, 0.10, '{"model_id":11,"name":"Base","indicator":"Hybrid","type":"-","version":"01.01.2023"}', '-', './app/model/base/Hybrid/RCA', TRUE, '2077-03-02 21:26:51.219669', '2077-03-02 21:26:51.219669'),
    ('Base', 'Hybrid', 'Base', 'PATIENT', '01.01.2023', 0.88, 0.97, 0.97, 0.97, 0.97, 0.10, 0.90, 0.90, 0.10, '{"model_id":12,"name":"Base","indicator":"Hybrid","type":"-","version":"01.01.2023"}', '-', './app/model/base/Hybrid/PATIENT', TRUE, '2077-03-02 21:26:51.219669', '2077-03-02 21:26:51.219669'),
    
    ('Adaptive', 'Qualitative', 'Fully Re-train', 'LAD', '01.05.2023', 0.88, 0.97, 0.97, 0.97, 0.97, 0.1, 0.9, 0.9, 0.1, '{"name": "Adaptive", "type": "-", "version": "01.05.2023", "model_id": 25, "indicator": "Qualitative"}', '-', './app/model/airflow/qualitative/best_model/LAD', TRUE, '2077-03-02 21:26:51.219669+07', '2077-03-02 21:26:51.219669+07'),
    ('Adaptive', 'Qualitative', 'Fully Re-train', 'LCX', '01.05.2023', 0.96, 0.99, 0.98, 0.97, 0.97, 0.05, 0.95, 0.9, 0.1, '{"name": "Adaptive", "type": "-", "version": "01.05.2023", "model_id": 26, "indicator": "Qualitative"}', '-', './app/model/airflow/qualitative/best_model/LCX', TRUE, '2077-03-02 21:26:51.219669+07', '2077-03-02 21:26:51.219669+07'),
    ('Adaptive', 'Qualitative', 'Fully Re-train', 'RCA', '01.05.2023', 0.88, 0.97, 0.97, 0.97, 0.97, 0.1, 0.9, 0.9, 0.1, '{"name": "Adaptive", "type": "-", "version": "01.05.2023", "model_id": 27, "indicator": "Qualitative"}', '-', './app/model/airflow/qualitative/best_model/RCA', TRUE, '2077-03-02 21:26:51.219669+07', '2077-03-02 21:26:51.219669+07'),
    ('Adaptive', 'Qualitative', 'Incremental', 'PATIENT', '01.05.2023', 0.88, 0.97, 0.97, 0.97, 0.97, 0.1, 0.9, 0.9, 0.1, '{"name": "Adaptive", "type": "-", "version": "01.01.2023", "model_id": 16, "indicator": "Qualitative", "child": {"name": "Adaptive", "type": "-", "version": "01.05.2023", "model_id": 28, "indicator": "Qualitative"}}', '-', './app/model/airflow/qualitative/best_model/PATIENT', TRUE, '2077-03-02 21:26:51.219669+07', '2077-03-02 21:26:51.219669+07'),
    
    ('Adaptive', 'Quantitative', 'Fully Re-train', 'LAD', '01.05.2023', 0.88, 0.97, 0.97, 0.97, 0.97, 0.1, 0.9, 0.9, 0.1, '{"name": "Adaptive", "type": "-", "version": "01.05.2023", "model_id": 29, "indicator": "Quantitative"}', 'lgbm', './app/model/airflow/quantitative/best_model/LAD', TRUE, '2077-03-02 21:26:51.219669+07', '2077-03-02 21:26:51.219669+07'),
    ('Adaptive', 'Quantitative', 'Fully Re-train', 'LCX', '01.05.2023', 0.96, 0.99, 0.98, 0.97, 0.97, 0.05, 0.95, 0.9, 0.1, '{"name": "Adaptive", "type": "-", "version": "01.05.2023", "model_id": 30, "indicator": "Quantitative"}', 'lgbm', './app/model/airflow/quantitative/best_model/LCX', TRUE, '2077-03-02 21:26:51.219669+07', '2077-03-02 21:26:51.219669+07'),
    ('Adaptive', 'Quantitative', 'Fully Re-train', 'RCA', '01.05.2023', 0.88, 0.97, 0.97, 0.97, 0.97, 0.1, 0.9, 0.9, 0.1, '{"name": "Adaptive", "type": "-", "version": "01.05.2023", "model_id": 31, "indicator": "Quantitative"}', 'lgbm', './app/model/airflow/quantitative/best_model/RCA', TRUE, '2077-03-02 21:26:51.219669+07', '2077-03-02 21:26:51.219669+07'),
    ('Adaptive', 'Quantitative', 'Incremental', 'PATIENT', '01.05.2023', 0.88, 0.97, 0.97, 0.97, 0.97, 0.1, 0.9, 0.9, 0.1, '{"name": "Adaptive", "type": "-", "version": "01.01.2023", "model_id": 20, "indicator": "Quantitative", "child": {"name": "Adaptive", "type": "-", "version": "01.05.2023", "model_id": 32, "indicator": "Quantitative"}}', 'lgbm', './app/model/airflow/quantitative/best_model/PATIENT', TRUE, '2077-03-02 21:26:51.219669+07', '2077-03-02 21:26:51.219669+07'),
    
    ('Adaptive', 'Hybrid', 'Fully Re-train', 'LAD', '01.05.2023', 0.88, 0.97, 0.97, 0.97, 0.97, 0.1, 0.9, 0.9, 0.1, '{"name": "Adaptive", "type": "-", "version": "01.05.2023", "model_id": 33, "indicator": "Hybrid"}', '-', './app/model/airflow/best_model/Hybrid/LAD', TRUE, '2077-03-02 21:26:51.219669+07', '2077-03-02 21:26:51.219669+07'),
    ('Adaptive', 'Hybrid', 'Fully Re-train', 'LCX', '01.05.2023', 0.96, 0.99, 0.98, 0.97, 0.97, 0.05, 0.95, 0.9, 0.1, '{"name": "Adaptive", "type": "-", "version": "01.05.2023", "model_id": 34, "indicator": "Hybrid"}', '-', './app/model/airflow/best_model/Hybrid/LCX', TRUE, '2077-03-02 21:26:51.219669+07', '2077-03-02 21:26:51.219669+07'),
    ('Adaptive', 'Hybrid', 'Fully Re-train', 'RCA', '01.05.2023', 0.88, 0.97, 0.97, 0.97, 0.97, 0.1, 0.9, 0.9, 0.1, '{"name": "Adaptive", "type": "-", "version": "01.05.2023", "model_id": 35, "indicator": "Hybrid"}', '-', './app/model/airflow/best_model/Hybrid/RCA', TRUE, '2077-03-02 21:26:51.219669+07', '2077-03-02 21:26:51.219669+07'),
    ('Adaptive', 'Hybrid', 'Incremental', 'PATIENT', '01.05.2023', 0.88, 0.97, 0.97, 0.97, 0.97, 0.1, 0.9, 0.9, 0.1, '{"name": "Adaptive", "type": "-", "version": "01.01.2023", "model_id": 24, "indicator": "Hybrid", "child": {"name": "Adaptive", "type": "-", "version": "01.05.2023", "model_id": 36, "indicator": "Hybrid"}}', '-', './app/model/airflow/best_model/Hybrid/PATIENT', TRUE, '2077-03-02 21:26:51.219669+07', '2077-03-02 21:26:51.219669+07');

ALTER TABLE IF EXISTS public.ml_model
    OWNER to airflow;

DROP TABLE IF EXISTS public.ml_diag;
--
-- Table structure for table `ml_diag` 
--

CREATE TABLE ml_diag (
  id SERIAL  PRIMARY KEY,
  mpi_test_id int,
  lad_ml_model_id int,
  lcx_ml_model_id int,
  rca_ml_model_id int,
  patient_ml_model_id int,
  lad_predict varchar(10),
  lcx_predict varchar(10),
  rca_predict varchar(10),
  patient_predict varchar(10),

  lad_predict_proba decimal(3,2),
  lcx_predict_proba decimal(3,2),
  rca_predict_proba decimal(3,2),
  patient_predict_proba decimal(3,2),
  created_at timestamp,
  updated_at timestamp,
  updated_by int,
  
  CONSTRAINT fk_mpi_test_id FOREIGN KEY(mpi_test_id) REFERENCES mpi_test(id) ON DELETE CASCADE,
  CONSTRAINT fk_lad_ml_model_id FOREIGN KEY(lad_ml_model_id) REFERENCES ml_model(id) ON DELETE CASCADE,
  CONSTRAINT fk_lcx_ml_model_id FOREIGN KEY(lcx_ml_model_id) REFERENCES ml_model(id) ON DELETE CASCADE,
  CONSTRAINT fk_rca_ml_model_id FOREIGN KEY(rca_ml_model_id) REFERENCES ml_model(id) ON DELETE CASCADE,
  CONSTRAINT fk_patient_ml_model_id FOREIGN KEY(patient_ml_model_id) REFERENCES ml_model(id) ON DELETE CASCADE
);


ALTER TABLE IF EXISTS public.ml_diag
    OWNER to airflow;

