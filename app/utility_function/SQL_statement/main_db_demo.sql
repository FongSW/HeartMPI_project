-- PATIENT
DROP TABLE IF EXISTS public.patient;
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

INSERT INTO public.patient(hn_number, first_name, last_name, dob, age_at_reg, gender, weight, height, created_at, updated_at)
    VALUES 
        ('039192-52', 'Siripakorn', 'Worrawunsunthara', '2000-02-04', 5, 'male', 50, 50, '2023-01-02', '2023-01-02');

-- ------------------------------------------------------------------------------------------------------------------------------------------------------------------------


-- MPI_TEST
DROP TABLE IF EXISTS public.mpi_test;
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
);


INSERT INTO public.mpi_test
VALUES 
    (1,     '039192-52', '2023-02-02', true, 1, 'archived', '0', '0', '0', 'positive', 'positive', 'positive', 'positive', 150.00, 169.00, 100, 40, '2023-03-01 21:26:51.219669', '2023-03-01 21:26:51.219669'),
    (2,     '039192-52', '2023-02-03', true, 1, 'archived', '0', '0', '0', 'positive', 'positive', 'positive', 'positive', 150.00, 169.00, 100, 40, '2023-03-02 21:26:51.219669', '2023-03-02 21:26:51.219669'),
    (3,     '039192-52', '2023-02-04', true, 1, 'archived', '0', '0', '0', 'positive', 'positive', 'positive', 'positive', 150.00, 169.00, 100, 40, '2023-03-01 21:26:51.219669', '2023-03-01 21:26:51.219669'),
    (4,     '039192-52', '2023-02-05', true, 1, 'archived', '0', '0', '0', 'positive', 'positive', 'positive', 'positive', 150.00, 169.00, 100, 40, '2023-03-02 21:26:51.219669', '2023-03-02 21:26:51.219669'),
    (5,     '039192-52', '2023-02-06', true, 1, 'archived', '0', '0', '0', 'positive', 'positive', 'positive', 'positive', 150.00, 169.00, 100, 40, '2023-03-01 21:26:51.219669', '2023-03-01 21:26:51.219669'),
    (6,     '039192-52', '2023-02-07', true, 1, 'archived', '0', '0', '0', 'positive', 'positive', 'positive', 'positive', 150.00, 169.00, 100, 40, '2023-03-02 21:26:51.219669', '2023-03-02 21:26:51.219669'),
    (7,     '039192-52', '2023-02-08', true, 1, 'archived', '0', '0', '0', 'positive', 'positive', 'positive', 'positive', 150.00, 169.00, 100, 40, '2023-03-01 21:26:51.219669', '2023-03-01 21:26:51.219669'),
    (8,     '039192-52', '2023-02-09', true, 1, 'archived', '0', '0', '0', 'positive', 'positive', 'positive', 'positive', 150.00, 169.00, 100, 40, '2023-03-02 21:26:51.219669', '2023-03-02 21:26:51.219669'),
    (9,     '039192-52', '2023-02-10', true, 1, 'archived', '0', '0', '0', 'positive', 'positive', 'positive', 'positive', 150.00, 169.00, 100, 40, '2023-03-01 21:26:51.219669', '2023-03-01 21:26:51.219669'),
    (10,    '039192-52', '2023-02-11', true, 1, 'archived', '0', '0', '0', 'positive', 'positive', 'positive', 'positive', 150.00, 169.00, 100, 40, '2023-03-02 21:26:51.219669', '2023-03-02 21:26:51.219669');

-- ------------------------------------------------------------------------------------------------------------------------------------------------------------------------

-- MPI_CROP_IMG
DROP TABLE IF EXISTS public.mpi_crop_img;
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

INSERT INTO public.mpi_crop_img(mpi_test_id, stress_perfusion_dpath, rest_perfusion_dpath, stress_severity_dpath, rest_severity_dpath, stress_blackout_dpath, rest_blackout_dpath, stress_def_sev_dpath, rest_def_sev_dpath)
VALUES 
    (1,     '/opt/heartmpi-front-web/data/4dm-mpi/completed/039192-52/98/data/cropped_images/stress/perfusion', '/opt/heartmpi-front-web/data/4dm-mpi/completed/039192-52/98/data/cropped_images/rest/perfusion', '/opt/heartmpi-front-web/data/4dm-mpi/completed/039192-52/98/data/cropped_images/stress/severity', '/opt/heartmpi-front-web/data/4dm-mpi/completed/039192-52/98/data/cropped_images/rest/severity', '/opt/heartmpi-front-web/data/4dm-mpi/completed/039192-52/98/data/cropped_images/stress/blackout', '/opt/heartmpi-front-web/data/4dm-mpi/completed/039192-52/98/data/cropped_images/rest/blackout', '/opt/heartmpi-front-web/data/4dm-mpi/completed/039192-52/98/data/cropped_images/stress/def-severity', '/opt/heartmpi-front-web/data/4dm-mpi/completed/039192-52/98/data/cropped_images/rest/def-severity'),
    (2,     '/opt/heartmpi-front-web/data/4dm-mpi/completed/039192-52/98/data/cropped_images/stress/perfusion', '/opt/heartmpi-front-web/data/4dm-mpi/completed/039192-52/98/data/cropped_images/rest/perfusion', '/opt/heartmpi-front-web/data/4dm-mpi/completed/039192-52/98/data/cropped_images/stress/severity', '/opt/heartmpi-front-web/data/4dm-mpi/completed/039192-52/98/data/cropped_images/rest/severity', '/opt/heartmpi-front-web/data/4dm-mpi/completed/039192-52/98/data/cropped_images/stress/blackout', '/opt/heartmpi-front-web/data/4dm-mpi/completed/039192-52/98/data/cropped_images/rest/blackout', '/opt/heartmpi-front-web/data/4dm-mpi/completed/039192-52/98/data/cropped_images/stress/def-severity', '/opt/heartmpi-front-web/data/4dm-mpi/completed/039192-52/98/data/cropped_images/rest/def-severity'),
    (3,     '/opt/heartmpi-front-web/data/4dm-mpi/completed/039192-52/98/data/cropped_images/stress/perfusion', '/opt/heartmpi-front-web/data/4dm-mpi/completed/039192-52/98/data/cropped_images/rest/perfusion', '/opt/heartmpi-front-web/data/4dm-mpi/completed/039192-52/98/data/cropped_images/stress/severity', '/opt/heartmpi-front-web/data/4dm-mpi/completed/039192-52/98/data/cropped_images/rest/severity', '/opt/heartmpi-front-web/data/4dm-mpi/completed/039192-52/98/data/cropped_images/stress/blackout', '/opt/heartmpi-front-web/data/4dm-mpi/completed/039192-52/98/data/cropped_images/rest/blackout', '/opt/heartmpi-front-web/data/4dm-mpi/completed/039192-52/98/data/cropped_images/stress/def-severity', '/opt/heartmpi-front-web/data/4dm-mpi/completed/039192-52/98/data/cropped_images/rest/def-severity'),
    (4,     '/opt/heartmpi-front-web/data/4dm-mpi/completed/039192-52/98/data/cropped_images/stress/perfusion', '/opt/heartmpi-front-web/data/4dm-mpi/completed/039192-52/98/data/cropped_images/rest/perfusion', '/opt/heartmpi-front-web/data/4dm-mpi/completed/039192-52/98/data/cropped_images/stress/severity', '/opt/heartmpi-front-web/data/4dm-mpi/completed/039192-52/98/data/cropped_images/rest/severity', '/opt/heartmpi-front-web/data/4dm-mpi/completed/039192-52/98/data/cropped_images/stress/blackout', '/opt/heartmpi-front-web/data/4dm-mpi/completed/039192-52/98/data/cropped_images/rest/blackout', '/opt/heartmpi-front-web/data/4dm-mpi/completed/039192-52/98/data/cropped_images/stress/def-severity', '/opt/heartmpi-front-web/data/4dm-mpi/completed/039192-52/98/data/cropped_images/rest/def-severity'),
    (5,     '/opt/heartmpi-front-web/data/4dm-mpi/completed/039192-52/98/data/cropped_images/stress/perfusion', '/opt/heartmpi-front-web/data/4dm-mpi/completed/039192-52/98/data/cropped_images/rest/perfusion', '/opt/heartmpi-front-web/data/4dm-mpi/completed/039192-52/98/data/cropped_images/stress/severity', '/opt/heartmpi-front-web/data/4dm-mpi/completed/039192-52/98/data/cropped_images/rest/severity', '/opt/heartmpi-front-web/data/4dm-mpi/completed/039192-52/98/data/cropped_images/stress/blackout', '/opt/heartmpi-front-web/data/4dm-mpi/completed/039192-52/98/data/cropped_images/rest/blackout', '/opt/heartmpi-front-web/data/4dm-mpi/completed/039192-52/98/data/cropped_images/stress/def-severity', '/opt/heartmpi-front-web/data/4dm-mpi/completed/039192-52/98/data/cropped_images/rest/def-severity'),
    (6,     '/opt/heartmpi-front-web/data/4dm-mpi/completed/039192-52/98/data/cropped_images/stress/perfusion', '/opt/heartmpi-front-web/data/4dm-mpi/completed/039192-52/98/data/cropped_images/rest/perfusion', '/opt/heartmpi-front-web/data/4dm-mpi/completed/039192-52/98/data/cropped_images/stress/severity', '/opt/heartmpi-front-web/data/4dm-mpi/completed/039192-52/98/data/cropped_images/rest/severity', '/opt/heartmpi-front-web/data/4dm-mpi/completed/039192-52/98/data/cropped_images/stress/blackout', '/opt/heartmpi-front-web/data/4dm-mpi/completed/039192-52/98/data/cropped_images/rest/blackout', '/opt/heartmpi-front-web/data/4dm-mpi/completed/039192-52/98/data/cropped_images/stress/def-severity', '/opt/heartmpi-front-web/data/4dm-mpi/completed/039192-52/98/data/cropped_images/rest/def-severity'),
    (7,     '/opt/heartmpi-front-web/data/4dm-mpi/completed/039192-52/98/data/cropped_images/stress/perfusion', '/opt/heartmpi-front-web/data/4dm-mpi/completed/039192-52/98/data/cropped_images/rest/perfusion', '/opt/heartmpi-front-web/data/4dm-mpi/completed/039192-52/98/data/cropped_images/stress/severity', '/opt/heartmpi-front-web/data/4dm-mpi/completed/039192-52/98/data/cropped_images/rest/severity', '/opt/heartmpi-front-web/data/4dm-mpi/completed/039192-52/98/data/cropped_images/stress/blackout', '/opt/heartmpi-front-web/data/4dm-mpi/completed/039192-52/98/data/cropped_images/rest/blackout', '/opt/heartmpi-front-web/data/4dm-mpi/completed/039192-52/98/data/cropped_images/stress/def-severity', '/opt/heartmpi-front-web/data/4dm-mpi/completed/039192-52/98/data/cropped_images/rest/def-severity'),
    (8,     '/opt/heartmpi-front-web/data/4dm-mpi/completed/039192-52/98/data/cropped_images/stress/perfusion', '/opt/heartmpi-front-web/data/4dm-mpi/completed/039192-52/98/data/cropped_images/rest/perfusion', '/opt/heartmpi-front-web/data/4dm-mpi/completed/039192-52/98/data/cropped_images/stress/severity', '/opt/heartmpi-front-web/data/4dm-mpi/completed/039192-52/98/data/cropped_images/rest/severity', '/opt/heartmpi-front-web/data/4dm-mpi/completed/039192-52/98/data/cropped_images/stress/blackout', '/opt/heartmpi-front-web/data/4dm-mpi/completed/039192-52/98/data/cropped_images/rest/blackout', '/opt/heartmpi-front-web/data/4dm-mpi/completed/039192-52/98/data/cropped_images/stress/def-severity', '/opt/heartmpi-front-web/data/4dm-mpi/completed/039192-52/98/data/cropped_images/rest/def-severity'),
    (9,     '/opt/heartmpi-front-web/data/4dm-mpi/completed/039192-52/98/data/cropped_images/stress/perfusion', '/opt/heartmpi-front-web/data/4dm-mpi/completed/039192-52/98/data/cropped_images/rest/perfusion', '/opt/heartmpi-front-web/data/4dm-mpi/completed/039192-52/98/data/cropped_images/stress/severity', '/opt/heartmpi-front-web/data/4dm-mpi/completed/039192-52/98/data/cropped_images/rest/severity', '/opt/heartmpi-front-web/data/4dm-mpi/completed/039192-52/98/data/cropped_images/stress/blackout', '/opt/heartmpi-front-web/data/4dm-mpi/completed/039192-52/98/data/cropped_images/rest/blackout', '/opt/heartmpi-front-web/data/4dm-mpi/completed/039192-52/98/data/cropped_images/stress/def-severity', '/opt/heartmpi-front-web/data/4dm-mpi/completed/039192-52/98/data/cropped_images/rest/def-severity'),
    (10,    '/opt/heartmpi-front-web/data/4dm-mpi/completed/039192-52/98/data/cropped_images/stress/perfusion', '/opt/heartmpi-front-web/data/4dm-mpi/completed/039192-52/98/data/cropped_images/rest/perfusion', '/opt/heartmpi-front-web/data/4dm-mpi/completed/039192-52/98/data/cropped_images/stress/severity', '/opt/heartmpi-front-web/data/4dm-mpi/completed/039192-52/98/data/cropped_images/rest/severity', '/opt/heartmpi-front-web/data/4dm-mpi/completed/039192-52/98/data/cropped_images/stress/blackout', '/opt/heartmpi-front-web/data/4dm-mpi/completed/039192-52/98/data/cropped_images/rest/blackout', '/opt/heartmpi-front-web/data/4dm-mpi/completed/039192-52/98/data/cropped_images/stress/def-severity', '/opt/heartmpi-front-web/data/4dm-mpi/completed/039192-52/98/data/cropped_images/rest/def-severity');

-- ------------------------------------------------------------------------------------------------------------------------------------------------------------------------

-- STRESS_QUANTI
DROP TABLE IF EXISTS public.stress_quanti;
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

INSERT INTO public.stress_quanti (mpi_test_id, max_perfusion, ocr_max_perfusion, ocr_clv_max_perfusion, "interval", ocr_interval, ocr_clv_interval, es, ocr_es, ocr_clv_es, ed, ocr_ed, ocr_clv_ed, lvef, ocr_lvef, ocr_clv_lvef, lad_perf_mean, ocr_lad_perf_mean, ocr_clv_lad_perf_mean, lad_perf_sd, ocr_lad_perf_sd, ocr_clv_lad_perf_sd, lad_wt_mean, ocr_lad_wt_mean, ocr_clv_lad_wt_mean, lad_wt_sd, ocr_lad_wt_sd, ocr_clv_lad_wt_sd, lad_wm_mean, ocr_lad_wm_mean, ocr_clv_lad_wm_mean, lad_wm_sd, ocr_lad_wm_sd, ocr_clv_lad_wm_sd, lcx_perf_mean, ocr_lcx_perf_mean, ocr_clv_lcx_perf_mean, lcx_perf_sd, ocr_lcx_perf_sd, ocr_clv_lcx_perf_sd, lcx_wt_mean, ocr_lcx_wt_mean, ocr_clv_lcx_wt_mean, lcx_wt_sd, ocr_lcx_wt_sd, ocr_clv_lcx_wt_sd, lcx_wm_mean, ocr_lcx_wm_mean, ocr_clv_lcx_wm_mean, lcx_wm_sd, ocr_lcx_wm_sd, ocr_clv_lcx_wm_sd, rca_perf_mean, ocr_rca_perf_mean, ocr_clv_rca_perf_mean, rca_perf_sd, ocr_rca_perf_sd, ocr_clv_rca_perf_sd, rca_wt_mean, ocr_rca_wt_mean, ocr_clv_rca_wt_mean, rca_wt_sd, ocr_rca_wt_sd, ocr_clv_rca_wt_sd, rca_wm_mean, ocr_rca_wm_mean, ocr_clv_rca_wm_mean, rca_wm_sd, ocr_rca_wm_sd, ocr_clv_rca_wm_sd, tot_perf_mean, ocr_tot_perf_mean, ocr_clv_tot_perf_mean, tot_perf_sd, ocr_tot_perf_sd, ocr_clv_tot_perf_sd, tot_wt_mean, ocr_tot_wt_mean, ocr_clv_tot_wt_mean, tot_wt_sd, ocr_tot_wt_sd, ocr_clv_tot_wt_sd, tot_wm_mean, ocr_tot_wm_mean, ocr_clv_tot_wm_mean, tot_wm_sd, ocr_tot_wm_sd, ocr_clv_tot_wm_sd, lad_perf_ext, ocr_lad_perf_ext, ocr_clv_lad_perf_ext, lad_perf_sev, ocr_lad_perf_sev, ocr_clv_lad_perf_sev, lad_wt_ext, ocr_lad_wt_ext, ocr_clv_lad_wt_ext, lad_wt_sev, ocr_lad_wt_sev, ocr_clv_lad_wt_sev, lad_wm_ext, ocr_lad_wm_ext, ocr_clv_lad_wm_ext, lad_wm_sev, ocr_lad_wm_sev, ocr_clv_lad_wm_sev, lcx_perf_ext, ocr_lcx_perf_ext, ocr_clv_lcx_perf_ext, lcx_perf_sev, ocr_lcx_perf_sev, ocr_clv_lcx_perf_sev, lcx_wt_ext, ocr_lcx_wt_ext, ocr_clv_lcx_wt_ext, lcx_wt_sev, ocr_lcx_wt_sev, ocr_clv_lcx_wt_sev, lcx_wm_ext, ocr_lcx_wm_ext, ocr_clv_lcx_wm_ext, lcx_wm_sev, ocr_lcx_wm_sev, ocr_clv_lcx_wm_sev, rca_perf_ext, ocr_rca_perf_ext, ocr_clv_rca_perf_ext, rca_perf_sev, ocr_rca_perf_sev, ocr_clv_rca_perf_sev, rca_wt_ext, ocr_rca_wt_ext, ocr_clv_rca_wt_ext, rca_wt_sev, ocr_rca_wt_sev, ocr_clv_rca_wt_sev, rca_wm_ext, ocr_rca_wm_ext, ocr_clv_rca_wm_ext, rca_wm_sev, ocr_rca_wm_sev, ocr_clv_rca_wm_sev, tot_perf_ext, ocr_tot_perf_ext, ocr_clv_tot_perf_ext, tot_perf_sev, ocr_tot_perf_sev, ocr_clv_tot_perf_sev, tot_wt_ext, ocr_tot_wt_ext, ocr_clv_tot_wt_ext, tot_wt_sev, ocr_tot_wt_sev, ocr_clv_tot_wt_sev, tot_wm_ext, ocr_tot_wm_ext, ocr_clv_tot_wm_ext, tot_wm_sev, ocr_tot_wm_sev, ocr_clv_tot_wm_sev) 
VALUES 
    (1, 1172.00, 1172.00, 94.00, 8.00, 8.00, 54.00, 28.00, 28.00, 95.00, 95.00, 95.00, 96.00, 70.00, 70.00, 80.00, 0.00, 0.00, 95.00, 0.80, 0.80, 94.00, -1.00, -1.00, 90.00, 0.60, 0.60, 94.00, -1.10, -1.10, 47.00, 1.00, 1.00, 96.00, 1.30, 1.30, 95.00, 2.30, 2.30, 94.00, -0.90, -0.90, 0.00, 0.80, 0.80, 94.00, -0.70, -0.70, 0.00, 0.40, 0.40, 95.00, -0.70, -0.70, 0.00, 1.70, 1.70, 74.00, -0.50, -0.50, 0.00, 1.00, 1.00, 96.00, -0.80, -0.80, 0.00, 0.70, 0.70, 90.00, 0.20, 0.20, 93.00, 1.60, 1.60, 96.00, -0.80, -0.80, 0.00, 0.80, 0.80, 96.00, -0.80, -0.80, 0.00, 0.90, 0.90, 95.00, 0.00, 0.00, 59.00, 0.00, 0.00, 91.00, 0.00, 0.00, 59.00, 0.00, 0.00, 91.00, 0.00, 0.00, 59.00, 0.00, 0.00, 91.00, 26.00, 26.00, 96.00, 4.50, 4.50, 85.00, 0.00, 0.00, 59.00, 0.00, 0.00, 91.00, 0.00, 0.00, 90.00, 0.00, 0.00, 94.00, 0.00, 0.00, 59.00, 0.00, 0.00, 91.00, 0.00, 0.00, 90.00, 0.00, 0.00, 94.00, 0.00, 0.00, 94.00, 0.00, 0.00, 96.00, 5.00, 5.00, 56.00, 4.40, 4.40, 59.00, 0.00, 0.00, 94.00, 0.00, 0.00, 96.00, 0.00, 0.00, 88.00, 0.00, 0.00, 94.00),
    (2, 1172.00, 1172.00, 94.00, 8.00, 8.00, 54.00, 28.00, 28.00, 95.00, 95.00, 95.00, 96.00, 70.00, 70.00, 80.00, 0.00, 0.00, 95.00, 0.80, 0.80, 94.00, -1.00, -1.00, 90.00, 0.60, 0.60, 94.00, -1.10, -1.10, 47.00, 1.00, 1.00, 96.00, 1.30, 1.30, 95.00, 2.30, 2.30, 94.00, -0.90, -0.90, 0.00, 0.80, 0.80, 94.00, -0.70, -0.70, 0.00, 0.40, 0.40, 95.00, -0.70, -0.70, 0.00, 1.70, 1.70, 74.00, -0.50, -0.50, 0.00, 1.00, 1.00, 96.00, -0.80, -0.80, 0.00, 0.70, 0.70, 90.00, 0.20, 0.20, 93.00, 1.60, 1.60, 96.00, -0.80, -0.80, 0.00, 0.80, 0.80, 96.00, -0.80, -0.80, 0.00, 0.90, 0.90, 95.00, 0.00, 0.00, 59.00, 0.00, 0.00, 91.00, 0.00, 0.00, 59.00, 0.00, 0.00, 91.00, 0.00, 0.00, 59.00, 0.00, 0.00, 91.00, 26.00, 26.00, 96.00, 4.50, 4.50, 85.00, 0.00, 0.00, 59.00, 0.00, 0.00, 91.00, 0.00, 0.00, 90.00, 0.00, 0.00, 94.00, 0.00, 0.00, 59.00, 0.00, 0.00, 91.00, 0.00, 0.00, 90.00, 0.00, 0.00, 94.00, 0.00, 0.00, 94.00, 0.00, 0.00, 96.00, 5.00, 5.00, 56.00, 4.40, 4.40, 59.00, 0.00, 0.00, 94.00, 0.00, 0.00, 96.00, 0.00, 0.00, 88.00, 0.00, 0.00, 94.00),
    (3, 1172.00, 1172.00, 94.00, 8.00, 8.00, 54.00, 28.00, 28.00, 95.00, 95.00, 95.00, 96.00, 70.00, 70.00, 80.00, 0.00, 0.00, 95.00, 0.80, 0.80, 94.00, -1.00, -1.00, 90.00, 0.60, 0.60, 94.00, -1.10, -1.10, 47.00, 1.00, 1.00, 96.00, 1.30, 1.30, 95.00, 2.30, 2.30, 94.00, -0.90, -0.90, 0.00, 0.80, 0.80, 94.00, -0.70, -0.70, 0.00, 0.40, 0.40, 95.00, -0.70, -0.70, 0.00, 1.70, 1.70, 74.00, -0.50, -0.50, 0.00, 1.00, 1.00, 96.00, -0.80, -0.80, 0.00, 0.70, 0.70, 90.00, 0.20, 0.20, 93.00, 1.60, 1.60, 96.00, -0.80, -0.80, 0.00, 0.80, 0.80, 96.00, -0.80, -0.80, 0.00, 0.90, 0.90, 95.00, 0.00, 0.00, 59.00, 0.00, 0.00, 91.00, 0.00, 0.00, 59.00, 0.00, 0.00, 91.00, 0.00, 0.00, 59.00, 0.00, 0.00, 91.00, 26.00, 26.00, 96.00, 4.50, 4.50, 85.00, 0.00, 0.00, 59.00, 0.00, 0.00, 91.00, 0.00, 0.00, 90.00, 0.00, 0.00, 94.00, 0.00, 0.00, 59.00, 0.00, 0.00, 91.00, 0.00, 0.00, 90.00, 0.00, 0.00, 94.00, 0.00, 0.00, 94.00, 0.00, 0.00, 96.00, 5.00, 5.00, 56.00, 4.40, 4.40, 59.00, 0.00, 0.00, 94.00, 0.00, 0.00, 96.00, 0.00, 0.00, 88.00, 0.00, 0.00, 94.00),
    (4, 1172.00, 1172.00, 94.00, 8.00, 8.00, 54.00, 28.00, 28.00, 95.00, 95.00, 95.00, 96.00, 70.00, 70.00, 80.00, 0.00, 0.00, 95.00, 0.80, 0.80, 94.00, -1.00, -1.00, 90.00, 0.60, 0.60, 94.00, -1.10, -1.10, 47.00, 1.00, 1.00, 96.00, 1.30, 1.30, 95.00, 2.30, 2.30, 94.00, -0.90, -0.90, 0.00, 0.80, 0.80, 94.00, -0.70, -0.70, 0.00, 0.40, 0.40, 95.00, -0.70, -0.70, 0.00, 1.70, 1.70, 74.00, -0.50, -0.50, 0.00, 1.00, 1.00, 96.00, -0.80, -0.80, 0.00, 0.70, 0.70, 90.00, 0.20, 0.20, 93.00, 1.60, 1.60, 96.00, -0.80, -0.80, 0.00, 0.80, 0.80, 96.00, -0.80, -0.80, 0.00, 0.90, 0.90, 95.00, 0.00, 0.00, 59.00, 0.00, 0.00, 91.00, 0.00, 0.00, 59.00, 0.00, 0.00, 91.00, 0.00, 0.00, 59.00, 0.00, 0.00, 91.00, 26.00, 26.00, 96.00, 4.50, 4.50, 85.00, 0.00, 0.00, 59.00, 0.00, 0.00, 91.00, 0.00, 0.00, 90.00, 0.00, 0.00, 94.00, 0.00, 0.00, 59.00, 0.00, 0.00, 91.00, 0.00, 0.00, 90.00, 0.00, 0.00, 94.00, 0.00, 0.00, 94.00, 0.00, 0.00, 96.00, 5.00, 5.00, 56.00, 4.40, 4.40, 59.00, 0.00, 0.00, 94.00, 0.00, 0.00, 96.00, 0.00, 0.00, 88.00, 0.00, 0.00, 94.00),
    (5, 1172.00, 1172.00, 94.00, 8.00, 8.00, 54.00, 28.00, 28.00, 95.00, 95.00, 95.00, 96.00, 70.00, 70.00, 80.00, 0.00, 0.00, 95.00, 0.80, 0.80, 94.00, -1.00, -1.00, 90.00, 0.60, 0.60, 94.00, -1.10, -1.10, 47.00, 1.00, 1.00, 96.00, 1.30, 1.30, 95.00, 2.30, 2.30, 94.00, -0.90, -0.90, 0.00, 0.80, 0.80, 94.00, -0.70, -0.70, 0.00, 0.40, 0.40, 95.00, -0.70, -0.70, 0.00, 1.70, 1.70, 74.00, -0.50, -0.50, 0.00, 1.00, 1.00, 96.00, -0.80, -0.80, 0.00, 0.70, 0.70, 90.00, 0.20, 0.20, 93.00, 1.60, 1.60, 96.00, -0.80, -0.80, 0.00, 0.80, 0.80, 96.00, -0.80, -0.80, 0.00, 0.90, 0.90, 95.00, 0.00, 0.00, 59.00, 0.00, 0.00, 91.00, 0.00, 0.00, 59.00, 0.00, 0.00, 91.00, 0.00, 0.00, 59.00, 0.00, 0.00, 91.00, 26.00, 26.00, 96.00, 4.50, 4.50, 85.00, 0.00, 0.00, 59.00, 0.00, 0.00, 91.00, 0.00, 0.00, 90.00, 0.00, 0.00, 94.00, 0.00, 0.00, 59.00, 0.00, 0.00, 91.00, 0.00, 0.00, 90.00, 0.00, 0.00, 94.00, 0.00, 0.00, 94.00, 0.00, 0.00, 96.00, 5.00, 5.00, 56.00, 4.40, 4.40, 59.00, 0.00, 0.00, 94.00, 0.00, 0.00, 96.00, 0.00, 0.00, 88.00, 0.00, 0.00, 94.00),
    (6, 1172.00, 1172.00, 94.00, 8.00, 8.00, 54.00, 28.00, 28.00, 95.00, 95.00, 95.00, 96.00, 70.00, 70.00, 80.00, 0.00, 0.00, 95.00, 0.80, 0.80, 94.00, -1.00, -1.00, 90.00, 0.60, 0.60, 94.00, -1.10, -1.10, 47.00, 1.00, 1.00, 96.00, 1.30, 1.30, 95.00, 2.30, 2.30, 94.00, -0.90, -0.90, 0.00, 0.80, 0.80, 94.00, -0.70, -0.70, 0.00, 0.40, 0.40, 95.00, -0.70, -0.70, 0.00, 1.70, 1.70, 74.00, -0.50, -0.50, 0.00, 1.00, 1.00, 96.00, -0.80, -0.80, 0.00, 0.70, 0.70, 90.00, 0.20, 0.20, 93.00, 1.60, 1.60, 96.00, -0.80, -0.80, 0.00, 0.80, 0.80, 96.00, -0.80, -0.80, 0.00, 0.90, 0.90, 95.00, 0.00, 0.00, 59.00, 0.00, 0.00, 91.00, 0.00, 0.00, 59.00, 0.00, 0.00, 91.00, 0.00, 0.00, 59.00, 0.00, 0.00, 91.00, 26.00, 26.00, 96.00, 4.50, 4.50, 85.00, 0.00, 0.00, 59.00, 0.00, 0.00, 91.00, 0.00, 0.00, 90.00, 0.00, 0.00, 94.00, 0.00, 0.00, 59.00, 0.00, 0.00, 91.00, 0.00, 0.00, 90.00, 0.00, 0.00, 94.00, 0.00, 0.00, 94.00, 0.00, 0.00, 96.00, 5.00, 5.00, 56.00, 4.40, 4.40, 59.00, 0.00, 0.00, 94.00, 0.00, 0.00, 96.00, 0.00, 0.00, 88.00, 0.00, 0.00, 94.00),
    (7, 1172.00, 1172.00, 94.00, 8.00, 8.00, 54.00, 28.00, 28.00, 95.00, 95.00, 95.00, 96.00, 70.00, 70.00, 80.00, 0.00, 0.00, 95.00, 0.80, 0.80, 94.00, -1.00, -1.00, 90.00, 0.60, 0.60, 94.00, -1.10, -1.10, 47.00, 1.00, 1.00, 96.00, 1.30, 1.30, 95.00, 2.30, 2.30, 94.00, -0.90, -0.90, 0.00, 0.80, 0.80, 94.00, -0.70, -0.70, 0.00, 0.40, 0.40, 95.00, -0.70, -0.70, 0.00, 1.70, 1.70, 74.00, -0.50, -0.50, 0.00, 1.00, 1.00, 96.00, -0.80, -0.80, 0.00, 0.70, 0.70, 90.00, 0.20, 0.20, 93.00, 1.60, 1.60, 96.00, -0.80, -0.80, 0.00, 0.80, 0.80, 96.00, -0.80, -0.80, 0.00, 0.90, 0.90, 95.00, 0.00, 0.00, 59.00, 0.00, 0.00, 91.00, 0.00, 0.00, 59.00, 0.00, 0.00, 91.00, 0.00, 0.00, 59.00, 0.00, 0.00, 91.00, 26.00, 26.00, 96.00, 4.50, 4.50, 85.00, 0.00, 0.00, 59.00, 0.00, 0.00, 91.00, 0.00, 0.00, 90.00, 0.00, 0.00, 94.00, 0.00, 0.00, 59.00, 0.00, 0.00, 91.00, 0.00, 0.00, 90.00, 0.00, 0.00, 94.00, 0.00, 0.00, 94.00, 0.00, 0.00, 96.00, 5.00, 5.00, 56.00, 4.40, 4.40, 59.00, 0.00, 0.00, 94.00, 0.00, 0.00, 96.00, 0.00, 0.00, 88.00, 0.00, 0.00, 94.00),
    (8, 1172.00, 1172.00, 94.00, 8.00, 8.00, 54.00, 28.00, 28.00, 95.00, 95.00, 95.00, 96.00, 70.00, 70.00, 80.00, 0.00, 0.00, 95.00, 0.80, 0.80, 94.00, -1.00, -1.00, 90.00, 0.60, 0.60, 94.00, -1.10, -1.10, 47.00, 1.00, 1.00, 96.00, 1.30, 1.30, 95.00, 2.30, 2.30, 94.00, -0.90, -0.90, 0.00, 0.80, 0.80, 94.00, -0.70, -0.70, 0.00, 0.40, 0.40, 95.00, -0.70, -0.70, 0.00, 1.70, 1.70, 74.00, -0.50, -0.50, 0.00, 1.00, 1.00, 96.00, -0.80, -0.80, 0.00, 0.70, 0.70, 90.00, 0.20, 0.20, 93.00, 1.60, 1.60, 96.00, -0.80, -0.80, 0.00, 0.80, 0.80, 96.00, -0.80, -0.80, 0.00, 0.90, 0.90, 95.00, 0.00, 0.00, 59.00, 0.00, 0.00, 91.00, 0.00, 0.00, 59.00, 0.00, 0.00, 91.00, 0.00, 0.00, 59.00, 0.00, 0.00, 91.00, 26.00, 26.00, 96.00, 4.50, 4.50, 85.00, 0.00, 0.00, 59.00, 0.00, 0.00, 91.00, 0.00, 0.00, 90.00, 0.00, 0.00, 94.00, 0.00, 0.00, 59.00, 0.00, 0.00, 91.00, 0.00, 0.00, 90.00, 0.00, 0.00, 94.00, 0.00, 0.00, 94.00, 0.00, 0.00, 96.00, 5.00, 5.00, 56.00, 4.40, 4.40, 59.00, 0.00, 0.00, 94.00, 0.00, 0.00, 96.00, 0.00, 0.00, 88.00, 0.00, 0.00, 94.00),
    (9, 1172.00, 1172.00, 94.00, 8.00, 8.00, 54.00, 28.00, 28.00, 95.00, 95.00, 95.00, 96.00, 70.00, 70.00, 80.00, 0.00, 0.00, 95.00, 0.80, 0.80, 94.00, -1.00, -1.00, 90.00, 0.60, 0.60, 94.00, -1.10, -1.10, 47.00, 1.00, 1.00, 96.00, 1.30, 1.30, 95.00, 2.30, 2.30, 94.00, -0.90, -0.90, 0.00, 0.80, 0.80, 94.00, -0.70, -0.70, 0.00, 0.40, 0.40, 95.00, -0.70, -0.70, 0.00, 1.70, 1.70, 74.00, -0.50, -0.50, 0.00, 1.00, 1.00, 96.00, -0.80, -0.80, 0.00, 0.70, 0.70, 90.00, 0.20, 0.20, 93.00, 1.60, 1.60, 96.00, -0.80, -0.80, 0.00, 0.80, 0.80, 96.00, -0.80, -0.80, 0.00, 0.90, 0.90, 95.00, 0.00, 0.00, 59.00, 0.00, 0.00, 91.00, 0.00, 0.00, 59.00, 0.00, 0.00, 91.00, 0.00, 0.00, 59.00, 0.00, 0.00, 91.00, 26.00, 26.00, 96.00, 4.50, 4.50, 85.00, 0.00, 0.00, 59.00, 0.00, 0.00, 91.00, 0.00, 0.00, 90.00, 0.00, 0.00, 94.00, 0.00, 0.00, 59.00, 0.00, 0.00, 91.00, 0.00, 0.00, 90.00, 0.00, 0.00, 94.00, 0.00, 0.00, 94.00, 0.00, 0.00, 96.00, 5.00, 5.00, 56.00, 4.40, 4.40, 59.00, 0.00, 0.00, 94.00, 0.00, 0.00, 96.00, 0.00, 0.00, 88.00, 0.00, 0.00, 94.00),
    (10, 1172.00, 1172.00, 94.00, 8.00, 8.00, 54.00, 28.00, 28.00, 95.00, 95.00, 95.00, 96.00, 70.00, 70.00, 80.00, 0.00, 0.00, 95.00, 0.80, 0.80, 94.00, -1.00, -1.00, 90.00, 0.60, 0.60, 94.00, -1.10, -1.10, 47.00, 1.00, 1.00, 96.00, 1.30, 1.30, 95.00, 2.30, 2.30, 94.00, -0.90, -0.90, 0.00, 0.80, 0.80, 94.00, -0.70, -0.70, 0.00, 0.40, 0.40, 95.00, -0.70, -0.70, 0.00, 1.70, 1.70, 74.00, -0.50, -0.50, 0.00, 1.00, 1.00, 96.00, -0.80, -0.80, 0.00, 0.70, 0.70, 90.00, 0.20, 0.20, 93.00, 1.60, 1.60, 96.00, -0.80, -0.80, 0.00, 0.80, 0.80, 96.00, -0.80, -0.80, 0.00, 0.90, 0.90, 95.00, 0.00, 0.00, 59.00, 0.00, 0.00, 91.00, 0.00, 0.00, 59.00, 0.00, 0.00, 91.00, 0.00, 0.00, 59.00, 0.00, 0.00, 91.00, 26.00, 26.00, 96.00, 4.50, 4.50, 85.00, 0.00, 0.00, 59.00, 0.00, 0.00, 91.00, 0.00, 0.00, 90.00, 0.00, 0.00, 94.00, 0.00, 0.00, 59.00, 0.00, 0.00, 91.00, 0.00, 0.00, 90.00, 0.00, 0.00, 94.00, 0.00, 0.00, 94.00, 0.00, 0.00, 96.00, 5.00, 5.00, 56.00, 4.40, 4.40, 59.00, 0.00, 0.00, 94.00, 0.00, 0.00, 96.00, 0.00, 0.00, 88.00, 0.00, 0.00, 94.00);

-- ------------------------------------------------------------------------------------------------------------------------------------------------------------------------

-- REST_QUANTI
DROP TABLE IF EXISTS public.rest_quanti;
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

INSERT INTO public.rest_quanti (mpi_test_id, max_perfusion, ocr_max_perfusion, ocr_clv_max_perfusion, "interval", ocr_interval, ocr_clv_interval, es, ocr_es, ocr_clv_es, ed, ocr_ed, ocr_clv_ed, lvef, ocr_lvef, ocr_clv_lvef, lad_perf_mean, ocr_lad_perf_mean, ocr_clv_lad_perf_mean, lad_perf_sd, ocr_lad_perf_sd, ocr_clv_lad_perf_sd, lad_wt_mean, ocr_lad_wt_mean, ocr_clv_lad_wt_mean, lad_wt_sd, ocr_lad_wt_sd, ocr_clv_lad_wt_sd, lad_wm_mean, ocr_lad_wm_mean, ocr_clv_lad_wm_mean, lad_wm_sd, ocr_lad_wm_sd, ocr_clv_lad_wm_sd, lcx_perf_mean, ocr_lcx_perf_mean, ocr_clv_lcx_perf_mean, lcx_perf_sd, ocr_lcx_perf_sd, ocr_clv_lcx_perf_sd, lcx_wt_mean, ocr_lcx_wt_mean, ocr_clv_lcx_wt_mean, lcx_wt_sd, ocr_lcx_wt_sd, ocr_clv_lcx_wt_sd, lcx_wm_mean, ocr_lcx_wm_mean, ocr_clv_lcx_wm_mean, lcx_wm_sd, ocr_lcx_wm_sd, ocr_clv_lcx_wm_sd, rca_perf_mean, ocr_rca_perf_mean, ocr_clv_rca_perf_mean, rca_perf_sd, ocr_rca_perf_sd, ocr_clv_rca_perf_sd, rca_wt_mean, ocr_rca_wt_mean, ocr_clv_rca_wt_mean, rca_wt_sd, ocr_rca_wt_sd, ocr_clv_rca_wt_sd, rca_wm_mean, ocr_rca_wm_mean, ocr_clv_rca_wm_mean, rca_wm_sd, ocr_rca_wm_sd, ocr_clv_rca_wm_sd, tot_perf_mean, ocr_tot_perf_mean, ocr_clv_tot_perf_mean, tot_perf_sd, ocr_tot_perf_sd, ocr_clv_tot_perf_sd, tot_wt_mean, ocr_tot_wt_mean, ocr_clv_tot_wt_mean, tot_wt_sd, ocr_tot_wt_sd, ocr_clv_tot_wt_sd, tot_wm_mean, ocr_tot_wm_mean, ocr_clv_tot_wm_mean, tot_wm_sd, ocr_tot_wm_sd, ocr_clv_tot_wm_sd, lad_perf_ext, ocr_lad_perf_ext, ocr_clv_lad_perf_ext, lad_perf_sev, ocr_lad_perf_sev, ocr_clv_lad_perf_sev, lad_wt_ext, ocr_lad_wt_ext, ocr_clv_lad_wt_ext, lad_wt_sev, ocr_lad_wt_sev, ocr_clv_lad_wt_sev, lad_wm_ext, ocr_lad_wm_ext, ocr_clv_lad_wm_ext, lad_wm_sev, ocr_lad_wm_sev, ocr_clv_lad_wm_sev, lcx_perf_ext, ocr_lcx_perf_ext, ocr_clv_lcx_perf_ext, lcx_perf_sev, ocr_lcx_perf_sev, ocr_clv_lcx_perf_sev, lcx_wt_ext, ocr_lcx_wt_ext, ocr_clv_lcx_wt_ext, lcx_wt_sev, ocr_lcx_wt_sev, ocr_clv_lcx_wt_sev, lcx_wm_ext, ocr_lcx_wm_ext, ocr_clv_lcx_wm_ext, lcx_wm_sev, ocr_lcx_wm_sev, ocr_clv_lcx_wm_sev, rca_perf_ext, ocr_rca_perf_ext, ocr_clv_rca_perf_ext, rca_perf_sev, ocr_rca_perf_sev, ocr_clv_rca_perf_sev, rca_wt_ext, ocr_rca_wt_ext, ocr_clv_rca_wt_ext, rca_wt_sev, ocr_rca_wt_sev, ocr_clv_rca_wt_sev, rca_wm_ext, ocr_rca_wm_ext, ocr_clv_rca_wm_ext, rca_wm_sev, ocr_rca_wm_sev, ocr_clv_rca_wm_sev, tot_perf_ext, ocr_tot_perf_ext, ocr_clv_tot_perf_ext, tot_perf_sev, ocr_tot_perf_sev, ocr_clv_tot_perf_sev, tot_wt_ext, ocr_tot_wt_ext, ocr_clv_tot_wt_ext, tot_wt_sev, ocr_tot_wt_sev, ocr_clv_tot_wt_sev, tot_wm_ext, ocr_tot_wm_ext, ocr_clv_tot_wm_ext, tot_wm_sev, ocr_tot_wm_sev, ocr_clv_tot_wm_sev)
VALUES 
    (1, 415.00, 415.00, 93.00, 8.00, 8.00, 54.00, 31.00, 31.00, 94.00, 92.00, 92.00, 96.00, 66.00, 66.00, 84.00, 0.50, 0.50, 95.00, 0.80, 0.80, 94.00, 0.60, 0.60, 95.00, 0.80, 0.80, 94.00, -0.70, -0.70, 0.00, 0.60, 0.60, 94.00, 1.90, 1.90, 94.00, 2.10, 2.10, 91.00, -0.10, -0.10, 0.00, 1.40, 1.40, 96.00, -0.80, -0.80, 0.00, 0.30, 0.30, 94.00, 0.20, 0.20, 96.00, 1.50, 1.50, 96.00, -0.10, -0.10, 0.00, 0.80, 0.80, 95.00, -1.60, -1.60, 82.00, 0.80, 0.80, 96.00, 0.80, 0.80, 94.00, 1.50, 1.50, 95.00, 0.10, 0.10, 96.00, 1.20, 1.20, 93.00, -1.00, -1.00, 89.00, 0.70, 0.70, 85.00, 0.00, 0.00, 59.00, 0.00, 0.00, 91.00, 0.00, 0.00, 59.00, 0.00, 0.00, 91.00, 0.00, 0.00, 59.00, 0.00, 0.00, 91.00, 38.00, 38.00, 95.00, 4.10, 4.10, 78.00, 0.00, 0.00, 59.00, 0.00, 0.00, 91.00, 0.00, 0.00, 90.00, 0.00, 0.00, 94.00, 1.00, 1.00, 41.00, 2.60, 2.60, 94.00, 0.00, 0.00, 90.00, 0.00, 0.00, 94.00, 0.00, 0.00, 94.00, 0.00, 0.00, 96.00, 10.00, 10.00, 96.00, 3.70, 3.70, 91.00, 0.00, 0.00, 94.00, 0.00, 0.00, 96.00, 0.00, 0.00, 88.00, 0.00, 0.00, 94.00),
    (2, 415.00, 415.00, 93.00, 8.00, 8.00, 54.00, 31.00, 31.00, 94.00, 92.00, 92.00, 96.00, 66.00, 66.00, 84.00, 0.50, 0.50, 95.00, 0.80, 0.80, 94.00, 0.60, 0.60, 95.00, 0.80, 0.80, 94.00, -0.70, -0.70, 0.00, 0.60, 0.60, 94.00, 1.90, 1.90, 94.00, 2.10, 2.10, 91.00, -0.10, -0.10, 0.00, 1.40, 1.40, 96.00, -0.80, -0.80, 0.00, 0.30, 0.30, 94.00, 0.20, 0.20, 96.00, 1.50, 1.50, 96.00, -0.10, -0.10, 0.00, 0.80, 0.80, 95.00, -1.60, -1.60, 82.00, 0.80, 0.80, 96.00, 0.80, 0.80, 94.00, 1.50, 1.50, 95.00, 0.10, 0.10, 96.00, 1.20, 1.20, 93.00, -1.00, -1.00, 89.00, 0.70, 0.70, 85.00, 0.00, 0.00, 59.00, 0.00, 0.00, 91.00, 0.00, 0.00, 59.00, 0.00, 0.00, 91.00, 0.00, 0.00, 59.00, 0.00, 0.00, 91.00, 38.00, 38.00, 95.00, 4.10, 4.10, 78.00, 0.00, 0.00, 59.00, 0.00, 0.00, 91.00, 0.00, 0.00, 90.00, 0.00, 0.00, 94.00, 1.00, 1.00, 41.00, 2.60, 2.60, 94.00, 0.00, 0.00, 90.00, 0.00, 0.00, 94.00, 0.00, 0.00, 94.00, 0.00, 0.00, 96.00, 10.00, 10.00, 96.00, 3.70, 3.70, 91.00, 0.00, 0.00, 94.00, 0.00, 0.00, 96.00, 0.00, 0.00, 88.00, 0.00, 0.00, 94.00),
    (3, 415.00, 415.00, 93.00, 8.00, 8.00, 54.00, 31.00, 31.00, 94.00, 92.00, 92.00, 96.00, 66.00, 66.00, 84.00, 0.50, 0.50, 95.00, 0.80, 0.80, 94.00, 0.60, 0.60, 95.00, 0.80, 0.80, 94.00, -0.70, -0.70, 0.00, 0.60, 0.60, 94.00, 1.90, 1.90, 94.00, 2.10, 2.10, 91.00, -0.10, -0.10, 0.00, 1.40, 1.40, 96.00, -0.80, -0.80, 0.00, 0.30, 0.30, 94.00, 0.20, 0.20, 96.00, 1.50, 1.50, 96.00, -0.10, -0.10, 0.00, 0.80, 0.80, 95.00, -1.60, -1.60, 82.00, 0.80, 0.80, 96.00, 0.80, 0.80, 94.00, 1.50, 1.50, 95.00, 0.10, 0.10, 96.00, 1.20, 1.20, 93.00, -1.00, -1.00, 89.00, 0.70, 0.70, 85.00, 0.00, 0.00, 59.00, 0.00, 0.00, 91.00, 0.00, 0.00, 59.00, 0.00, 0.00, 91.00, 0.00, 0.00, 59.00, 0.00, 0.00, 91.00, 38.00, 38.00, 95.00, 4.10, 4.10, 78.00, 0.00, 0.00, 59.00, 0.00, 0.00, 91.00, 0.00, 0.00, 90.00, 0.00, 0.00, 94.00, 1.00, 1.00, 41.00, 2.60, 2.60, 94.00, 0.00, 0.00, 90.00, 0.00, 0.00, 94.00, 0.00, 0.00, 94.00, 0.00, 0.00, 96.00, 10.00, 10.00, 96.00, 3.70, 3.70, 91.00, 0.00, 0.00, 94.00, 0.00, 0.00, 96.00, 0.00, 0.00, 88.00, 0.00, 0.00, 94.00),
    (4, 415.00, 415.00, 93.00, 8.00, 8.00, 54.00, 31.00, 31.00, 94.00, 92.00, 92.00, 96.00, 66.00, 66.00, 84.00, 0.50, 0.50, 95.00, 0.80, 0.80, 94.00, 0.60, 0.60, 95.00, 0.80, 0.80, 94.00, -0.70, -0.70, 0.00, 0.60, 0.60, 94.00, 1.90, 1.90, 94.00, 2.10, 2.10, 91.00, -0.10, -0.10, 0.00, 1.40, 1.40, 96.00, -0.80, -0.80, 0.00, 0.30, 0.30, 94.00, 0.20, 0.20, 96.00, 1.50, 1.50, 96.00, -0.10, -0.10, 0.00, 0.80, 0.80, 95.00, -1.60, -1.60, 82.00, 0.80, 0.80, 96.00, 0.80, 0.80, 94.00, 1.50, 1.50, 95.00, 0.10, 0.10, 96.00, 1.20, 1.20, 93.00, -1.00, -1.00, 89.00, 0.70, 0.70, 85.00, 0.00, 0.00, 59.00, 0.00, 0.00, 91.00, 0.00, 0.00, 59.00, 0.00, 0.00, 91.00, 0.00, 0.00, 59.00, 0.00, 0.00, 91.00, 38.00, 38.00, 95.00, 4.10, 4.10, 78.00, 0.00, 0.00, 59.00, 0.00, 0.00, 91.00, 0.00, 0.00, 90.00, 0.00, 0.00, 94.00, 1.00, 1.00, 41.00, 2.60, 2.60, 94.00, 0.00, 0.00, 90.00, 0.00, 0.00, 94.00, 0.00, 0.00, 94.00, 0.00, 0.00, 96.00, 10.00, 10.00, 96.00, 3.70, 3.70, 91.00, 0.00, 0.00, 94.00, 0.00, 0.00, 96.00, 0.00, 0.00, 88.00, 0.00, 0.00, 94.00),
    (5, 415.00, 415.00, 93.00, 8.00, 8.00, 54.00, 31.00, 31.00, 94.00, 92.00, 92.00, 96.00, 66.00, 66.00, 84.00, 0.50, 0.50, 95.00, 0.80, 0.80, 94.00, 0.60, 0.60, 95.00, 0.80, 0.80, 94.00, -0.70, -0.70, 0.00, 0.60, 0.60, 94.00, 1.90, 1.90, 94.00, 2.10, 2.10, 91.00, -0.10, -0.10, 0.00, 1.40, 1.40, 96.00, -0.80, -0.80, 0.00, 0.30, 0.30, 94.00, 0.20, 0.20, 96.00, 1.50, 1.50, 96.00, -0.10, -0.10, 0.00, 0.80, 0.80, 95.00, -1.60, -1.60, 82.00, 0.80, 0.80, 96.00, 0.80, 0.80, 94.00, 1.50, 1.50, 95.00, 0.10, 0.10, 96.00, 1.20, 1.20, 93.00, -1.00, -1.00, 89.00, 0.70, 0.70, 85.00, 0.00, 0.00, 59.00, 0.00, 0.00, 91.00, 0.00, 0.00, 59.00, 0.00, 0.00, 91.00, 0.00, 0.00, 59.00, 0.00, 0.00, 91.00, 38.00, 38.00, 95.00, 4.10, 4.10, 78.00, 0.00, 0.00, 59.00, 0.00, 0.00, 91.00, 0.00, 0.00, 90.00, 0.00, 0.00, 94.00, 1.00, 1.00, 41.00, 2.60, 2.60, 94.00, 0.00, 0.00, 90.00, 0.00, 0.00, 94.00, 0.00, 0.00, 94.00, 0.00, 0.00, 96.00, 10.00, 10.00, 96.00, 3.70, 3.70, 91.00, 0.00, 0.00, 94.00, 0.00, 0.00, 96.00, 0.00, 0.00, 88.00, 0.00, 0.00, 94.00),
    (6, 415.00, 415.00, 93.00, 8.00, 8.00, 54.00, 31.00, 31.00, 94.00, 92.00, 92.00, 96.00, 66.00, 66.00, 84.00, 0.50, 0.50, 95.00, 0.80, 0.80, 94.00, 0.60, 0.60, 95.00, 0.80, 0.80, 94.00, -0.70, -0.70, 0.00, 0.60, 0.60, 94.00, 1.90, 1.90, 94.00, 2.10, 2.10, 91.00, -0.10, -0.10, 0.00, 1.40, 1.40, 96.00, -0.80, -0.80, 0.00, 0.30, 0.30, 94.00, 0.20, 0.20, 96.00, 1.50, 1.50, 96.00, -0.10, -0.10, 0.00, 0.80, 0.80, 95.00, -1.60, -1.60, 82.00, 0.80, 0.80, 96.00, 0.80, 0.80, 94.00, 1.50, 1.50, 95.00, 0.10, 0.10, 96.00, 1.20, 1.20, 93.00, -1.00, -1.00, 89.00, 0.70, 0.70, 85.00, 0.00, 0.00, 59.00, 0.00, 0.00, 91.00, 0.00, 0.00, 59.00, 0.00, 0.00, 91.00, 0.00, 0.00, 59.00, 0.00, 0.00, 91.00, 38.00, 38.00, 95.00, 4.10, 4.10, 78.00, 0.00, 0.00, 59.00, 0.00, 0.00, 91.00, 0.00, 0.00, 90.00, 0.00, 0.00, 94.00, 1.00, 1.00, 41.00, 2.60, 2.60, 94.00, 0.00, 0.00, 90.00, 0.00, 0.00, 94.00, 0.00, 0.00, 94.00, 0.00, 0.00, 96.00, 10.00, 10.00, 96.00, 3.70, 3.70, 91.00, 0.00, 0.00, 94.00, 0.00, 0.00, 96.00, 0.00, 0.00, 88.00, 0.00, 0.00, 94.00),
    (7, 415.00, 415.00, 93.00, 8.00, 8.00, 54.00, 31.00, 31.00, 94.00, 92.00, 92.00, 96.00, 66.00, 66.00, 84.00, 0.50, 0.50, 95.00, 0.80, 0.80, 94.00, 0.60, 0.60, 95.00, 0.80, 0.80, 94.00, -0.70, -0.70, 0.00, 0.60, 0.60, 94.00, 1.90, 1.90, 94.00, 2.10, 2.10, 91.00, -0.10, -0.10, 0.00, 1.40, 1.40, 96.00, -0.80, -0.80, 0.00, 0.30, 0.30, 94.00, 0.20, 0.20, 96.00, 1.50, 1.50, 96.00, -0.10, -0.10, 0.00, 0.80, 0.80, 95.00, -1.60, -1.60, 82.00, 0.80, 0.80, 96.00, 0.80, 0.80, 94.00, 1.50, 1.50, 95.00, 0.10, 0.10, 96.00, 1.20, 1.20, 93.00, -1.00, -1.00, 89.00, 0.70, 0.70, 85.00, 0.00, 0.00, 59.00, 0.00, 0.00, 91.00, 0.00, 0.00, 59.00, 0.00, 0.00, 91.00, 0.00, 0.00, 59.00, 0.00, 0.00, 91.00, 38.00, 38.00, 95.00, 4.10, 4.10, 78.00, 0.00, 0.00, 59.00, 0.00, 0.00, 91.00, 0.00, 0.00, 90.00, 0.00, 0.00, 94.00, 1.00, 1.00, 41.00, 2.60, 2.60, 94.00, 0.00, 0.00, 90.00, 0.00, 0.00, 94.00, 0.00, 0.00, 94.00, 0.00, 0.00, 96.00, 10.00, 10.00, 96.00, 3.70, 3.70, 91.00, 0.00, 0.00, 94.00, 0.00, 0.00, 96.00, 0.00, 0.00, 88.00, 0.00, 0.00, 94.00),
    (8, 415.00, 415.00, 93.00, 8.00, 8.00, 54.00, 31.00, 31.00, 94.00, 92.00, 92.00, 96.00, 66.00, 66.00, 84.00, 0.50, 0.50, 95.00, 0.80, 0.80, 94.00, 0.60, 0.60, 95.00, 0.80, 0.80, 94.00, -0.70, -0.70, 0.00, 0.60, 0.60, 94.00, 1.90, 1.90, 94.00, 2.10, 2.10, 91.00, -0.10, -0.10, 0.00, 1.40, 1.40, 96.00, -0.80, -0.80, 0.00, 0.30, 0.30, 94.00, 0.20, 0.20, 96.00, 1.50, 1.50, 96.00, -0.10, -0.10, 0.00, 0.80, 0.80, 95.00, -1.60, -1.60, 82.00, 0.80, 0.80, 96.00, 0.80, 0.80, 94.00, 1.50, 1.50, 95.00, 0.10, 0.10, 96.00, 1.20, 1.20, 93.00, -1.00, -1.00, 89.00, 0.70, 0.70, 85.00, 0.00, 0.00, 59.00, 0.00, 0.00, 91.00, 0.00, 0.00, 59.00, 0.00, 0.00, 91.00, 0.00, 0.00, 59.00, 0.00, 0.00, 91.00, 38.00, 38.00, 95.00, 4.10, 4.10, 78.00, 0.00, 0.00, 59.00, 0.00, 0.00, 91.00, 0.00, 0.00, 90.00, 0.00, 0.00, 94.00, 1.00, 1.00, 41.00, 2.60, 2.60, 94.00, 0.00, 0.00, 90.00, 0.00, 0.00, 94.00, 0.00, 0.00, 94.00, 0.00, 0.00, 96.00, 10.00, 10.00, 96.00, 3.70, 3.70, 91.00, 0.00, 0.00, 94.00, 0.00, 0.00, 96.00, 0.00, 0.00, 88.00, 0.00, 0.00, 94.00),
    (9, 415.00, 415.00, 93.00, 8.00, 8.00, 54.00, 31.00, 31.00, 94.00, 92.00, 92.00, 96.00, 66.00, 66.00, 84.00, 0.50, 0.50, 95.00, 0.80, 0.80, 94.00, 0.60, 0.60, 95.00, 0.80, 0.80, 94.00, -0.70, -0.70, 0.00, 0.60, 0.60, 94.00, 1.90, 1.90, 94.00, 2.10, 2.10, 91.00, -0.10, -0.10, 0.00, 1.40, 1.40, 96.00, -0.80, -0.80, 0.00, 0.30, 0.30, 94.00, 0.20, 0.20, 96.00, 1.50, 1.50, 96.00, -0.10, -0.10, 0.00, 0.80, 0.80, 95.00, -1.60, -1.60, 82.00, 0.80, 0.80, 96.00, 0.80, 0.80, 94.00, 1.50, 1.50, 95.00, 0.10, 0.10, 96.00, 1.20, 1.20, 93.00, -1.00, -1.00, 89.00, 0.70, 0.70, 85.00, 0.00, 0.00, 59.00, 0.00, 0.00, 91.00, 0.00, 0.00, 59.00, 0.00, 0.00, 91.00, 0.00, 0.00, 59.00, 0.00, 0.00, 91.00, 38.00, 38.00, 95.00, 4.10, 4.10, 78.00, 0.00, 0.00, 59.00, 0.00, 0.00, 91.00, 0.00, 0.00, 90.00, 0.00, 0.00, 94.00, 1.00, 1.00, 41.00, 2.60, 2.60, 94.00, 0.00, 0.00, 90.00, 0.00, 0.00, 94.00, 0.00, 0.00, 94.00, 0.00, 0.00, 96.00, 10.00, 10.00, 96.00, 3.70, 3.70, 91.00, 0.00, 0.00, 94.00, 0.00, 0.00, 96.00, 0.00, 0.00, 88.00, 0.00, 0.00, 94.00),
    (10, 415.00, 415.00, 93.00, 8.00, 8.00, 54.00, 31.00, 31.00, 94.00, 92.00, 92.00, 96.00, 66.00, 66.00, 84.00, 0.50, 0.50, 95.00, 0.80, 0.80, 94.00, 0.60, 0.60, 95.00, 0.80, 0.80, 94.00, -0.70, -0.70, 0.00, 0.60, 0.60, 94.00, 1.90, 1.90, 94.00, 2.10, 2.10, 91.00, -0.10, -0.10, 0.00, 1.40, 1.40, 96.00, -0.80, -0.80, 0.00, 0.30, 0.30, 94.00, 0.20, 0.20, 96.00, 1.50, 1.50, 96.00, -0.10, -0.10, 0.00, 0.80, 0.80, 95.00, -1.60, -1.60, 82.00, 0.80, 0.80, 96.00, 0.80, 0.80, 94.00, 1.50, 1.50, 95.00, 0.10, 0.10, 96.00, 1.20, 1.20, 93.00, -1.00, -1.00, 89.00, 0.70, 0.70, 85.00, 0.00, 0.00, 59.00, 0.00, 0.00, 91.00, 0.00, 0.00, 59.00, 0.00, 0.00, 91.00, 0.00, 0.00, 59.00, 0.00, 0.00, 91.00, 38.00, 38.00, 95.00, 4.10, 4.10, 78.00, 0.00, 0.00, 59.00, 0.00, 0.00, 91.00, 0.00, 0.00, 90.00, 0.00, 0.00, 94.00, 1.00, 1.00, 41.00, 2.60, 2.60, 94.00, 0.00, 0.00, 90.00, 0.00, 0.00, 94.00, 0.00, 0.00, 94.00, 0.00, 0.00, 96.00, 10.00, 10.00, 96.00, 3.70, 3.70, 91.00, 0.00, 0.00, 94.00, 0.00, 0.00, 96.00, 0.00, 0.00, 88.00, 0.00, 0.00, 94.00);

-- ------------------------------------------------------------------------------------------------------------------------------------------------------------------------

-- TPD_17_SEG
DROP TABLE IF EXISTS public.tpd_17_seg;
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

INSERT INTO public.tpd_17_seg (mpi_test_id, stress_sss, ocr_stress_sss, ocr_clv_stress_sss, stress_sts, ocr_stress_sts, ocr_clv_stress_sts, stress_sms, ocr_stress_sms, ocr_clv_stress_sms, rest_srs, ocr_rest_srs, ocr_clv_rest_srs, rest_sts, ocr_rest_sts, ocr_clv_rest_sts, rest_sms, ocr_rest_sms, ocr_clv_rest_sms) 
VALUES 
    (1, 3.00, 3.00, 32.00, 1.00, 1.00, 82.00, 0.00, 0.00, 74.00, 6.00, 6.00, 77.00, 814.00, 814.00, 80.00, 0.00, 0.00, 74.00),
    (2, 3.00, 3.00, 32.00, 1.00, 1.00, 82.00, 0.00, 0.00, 74.00, 6.00, 6.00, 77.00, 814.00, 814.00, 80.00, 0.00, 0.00, 74.00),
    (3, 3.00, 3.00, 32.00, 1.00, 1.00, 82.00, 0.00, 0.00, 74.00, 6.00, 6.00, 77.00, 814.00, 814.00, 80.00, 0.00, 0.00, 74.00),
    (4, 3.00, 3.00, 32.00, 1.00, 1.00, 82.00, 0.00, 0.00, 74.00, 6.00, 6.00, 77.00, 814.00, 814.00, 80.00, 0.00, 0.00, 74.00),
    (5, 3.00, 3.00, 32.00, 1.00, 1.00, 82.00, 0.00, 0.00, 74.00, 6.00, 6.00, 77.00, 814.00, 814.00, 80.00, 0.00, 0.00, 74.00),
    (6, 3.00, 3.00, 32.00, 1.00, 1.00, 82.00, 0.00, 0.00, 74.00, 6.00, 6.00, 77.00, 814.00, 814.00, 80.00, 0.00, 0.00, 74.00),
    (7, 3.00, 3.00, 32.00, 1.00, 1.00, 82.00, 0.00, 0.00, 74.00, 6.00, 6.00, 77.00, 814.00, 814.00, 80.00, 0.00, 0.00, 74.00),
    (8, 3.00, 3.00, 32.00, 1.00, 1.00, 82.00, 0.00, 0.00, 74.00, 6.00, 6.00, 77.00, 814.00, 814.00, 80.00, 0.00, 0.00, 74.00),
    (9, 3.00, 3.00, 32.00, 1.00, 1.00, 82.00, 0.00, 0.00, 74.00, 6.00, 6.00, 77.00, 814.00, 814.00, 80.00, 0.00, 0.00, 74.00),
    (10, 3.00, 3.00, 32.00, 1.00, 1.00, 82.00, 0.00, 0.00, 74.00, 6.00, 6.00, 77.00, 814.00, 814.00, 80.00, 0.00, 0.00, 74.00);

-- ------------------------------------------------------------------------------------------------------------------------------------------------------------------------

-- DOCTOR_DIAG
DROP TABLE IF EXISTS public.doctor_diag;
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

-- ------------------------------------------------------------------------------------------------------------------------------------------------------------------------

-- ML_MODEL
DROP TABLE IF EXISTS public.ml_model;
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
    ('Base', 'Qualitative', 'Base', 'LAD', '01.01.2023', 0.88, 0.97, 0.97, 0.97, 0.97, 0.10, 0.90, 0.90, 0.10, '{"model_id":1,"name":"Base","indicator":"Qualitative","type":"-","version":"01.01.2023"}', '-', '/opt/app/model/base/qualitative/LAD/', TRUE, '2077-03-02 21:26:51.219669', '2077-03-02 21:26:51.219669'),
    ('Base', 'Qualitative', 'Base', 'LCX', '01.01.2023', 0.96, 0.99, 0.98, 0.97, 0.97, 0.05, 0.95, 0.90, 0.10, '{"model_id":2,"name":"Base","indicator":"Qualitative","type":"-","version":"01.01.2023"}', '-', '/opt/app/model/base/qualitative/LCX/', TRUE, '2077-03-02 21:26:51.219669', '2077-03-02 21:26:51.219669'),
    ('Base', 'Qualitative', 'Base', 'RCA', '01.01.2023', 0.88, 0.97, 0.97, 0.97, 0.97, 0.10, 0.90, 0.90, 0.10, '{"model_id":3,"name":"Base","indicator":"Qualitative","type":"-","version":"01.01.2023"}', '-', '/opt/app/model/base/qualitative/RCA/', TRUE, '2077-03-02 21:26:51.219669', '2077-03-02 21:26:51.219669'),
    ('Base', 'Qualitative', 'Base', 'PATIENT', '01.01.2023', 0.88, 0.97, 0.97, 0.97, 0.97, 0.10, 0.90, 0.90, 0.10, '{"model_id":4,"name":"Base","indicator":"Qualitative","type":"-","version":"01.01.2023"}', '-', '/opt/app/model/base/qualitative/PATIENT/', TRUE, '2077-03-02 21:26:51.219669', '2077-03-02 21:26:51.219669'),

    ('Base', 'Quantitative', 'Base', 'LAD', '01.01.2023', 0.88, 0.97, 0.97, 0.97, 0.97, 0.10, 0.90, 0.90, 0.10, '{"model_id":5,"name":"Base","indicator":"Quantitative","type":"-","version":"01.01.2023"}', 'lgbm', '/opt/app/model/base/quantitative/LAD', TRUE, '2077-03-02 21:26:51.219669', '2077-03-02 21:26:51.219669'),
    ('Base', 'Quantitative', 'Base', 'LCX', '01.01.2023', 0.96, 0.99, 0.98, 0.97, 0.97, 0.05, 0.95, 0.90, 0.10, '{"model_id":6,"name":"Base","indicator":"Quantitative","type":"-","version":"01.01.2023"}', 'lgbm', '/opt/app/model/base/quantitative/LCX', TRUE, '2077-03-02 21:26:51.219669', '2077-03-02 21:26:51.219669'),
    ('Base', 'Quantitative', 'Base', 'RCA', '01.01.2023', 0.88, 0.97, 0.97, 0.97, 0.97, 0.10, 0.90, 0.90, 0.10, '{"model_id":7,"name":"Base","indicator":"Quantitative","type":"-","version":"01.01.2023"}', 'lgbm', '/opt/app/model/base/quantitative/RCA', TRUE, '2077-03-02 21:26:51.219669', '2077-03-02 21:26:51.219669'),
    ('Base', 'Quantitative', 'Base', 'PATIENT', '01.01.2023', 0.88, 0.97, 0.97, 0.97, 0.97, 0.10, 0.90, 0.90, 0.10, '{"model_id":8,"name":"Base","indicator":"Quantitative","type":"-","version":"01.01.2023"}', 'lgbm', '/opt/app/model/base/quantitative/PATIENT', TRUE, '2077-03-02 21:26:51.219669', '2077-03-02 21:26:51.219669'),

    ('Base', 'Hybrid', 'Base', 'LAD', '01.01.2023', 0.88, 0.97, 0.97, 0.97, 0.97, 0.10, 0.90, 0.90, 0.10, '{"model_id":9,"name":"Base","indicator":"Hybrid","type":"-","version":"01.01.2023"}', '-', '/opt/app/model/base/Hybrid/LAD', TRUE, '2077-03-02 21:26:51.219669', '2077-03-02 21:26:51.219669'),
    ('Base', 'Hybrid', 'Base', 'LCX', '01.01.2023', 0.96, 0.99, 0.98, 0.97, 0.97, 0.05, 0.95, 0.90, 0.10, '{"model_id":10,"name":"Base","indicator":"Hybrid","type":"-","version":"01.01.2023"}', '-', '/opt/app/model/base/Hybrid/LCX', TRUE, '2077-03-02 21:26:51.219669', '2077-03-02 21:26:51.219669'),
    ('Base', 'Hybrid', 'Base', 'RCA', '01.01.2023', 0.88, 0.97, 0.97, 0.97, 0.97, 0.10, 0.90, 0.90, 0.10, '{"model_id":11,"name":"Base","indicator":"Hybrid","type":"-","version":"01.01.2023"}', '-', '/opt/app/model/base/Hybrid/RCA', TRUE, '2077-03-02 21:26:51.219669', '2077-03-02 21:26:51.219669'),
    ('Base', 'Hybrid', 'Base', 'PATIENT', '01.01.2023', 0.88, 0.97, 0.97, 0.97, 0.97, 0.10, 0.90, 0.90, 0.10, '{"model_id":12,"name":"Base","indicator":"Hybrid","type":"-","version":"01.01.2023"}', '-', '/opt/app/model/base/Hybrid/PATIENT', TRUE, '2077-03-02 21:26:51.219669', '2077-03-02 21:26:51.219669');

-- ------------------------------------------------------------------------------------------------------------------------------------------------------------------------
