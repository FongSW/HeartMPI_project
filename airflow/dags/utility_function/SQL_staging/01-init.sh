#!/bin/bash
set -e
export PGPASSWORD=$POSTGRES_PASSWORD;
psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" <<-EOSQL
  CREATE DATABASE $APP_DB_NAME;
  GRANT ALL PRIVILEGES ON DATABASE $APP_DB_NAME TO $POSTGRES_USER;
  BEGIN;
    DROP DATABASE IF EXISTS staging;
	CREATE DATABASE staging;

	DROP TABLE IF EXISTS public.mpi_test;
	CREATE TABLE mpi_test (
		id int PRIMARY KEY,
		hn_number varchar(9),
		mpi_exam_date date,
		dm varchar(10),
		ht varchar(10),
		dlp varchar(10),
		ckd varchar(10),
		weight decimal(5,2),
		height decimal(5,2),
		bmi decimal(5,2),
		age int,
		gender varchar(6),
		created_at timestamp
	);
	ALTER TABLE IF EXISTS public.mpi_test OWNER TO airflow;

	DROP TABLE IF EXISTS public.doctor_diag;
	CREATE TABLE doctor_diag (
		mpi_test_id int PRIMARY KEY,
		lad_predict varchar(10),
		lcx_predict varchar(10),
		rca_predict varchar(10),
		patient_predict varchar(10),
		CONSTRAINT fk_mpi_test_id FOREIGN KEY(mpi_test_id) REFERENCES mpi_test(id) ON DELETE CASCADE
	);
	ALTER TABLE IF EXISTS public.doctor_diag OWNER TO airflow;

	DROP TABLE IF EXISTS public.mpi_crop_img;
	CREATE TABLE mpi_crop_img (
		mpi_test_id int PRIMARY KEY, 
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
	ALTER TABLE IF EXISTS public.mpi_crop_img OWNER TO airflow;

	DROP TABLE IF EXISTS public.rest_quanti;
	CREATE TABLE rest_quanti (
		mpi_test_id int PRIMARY KEY,
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
	ALTER TABLE IF EXISTS public.rest_quanti OWNER TO airflow;

	DROP TABLE IF EXISTS public.stress_quanti;
	CREATE TABLE stress_quanti (
		mpi_test_id int PRIMARY KEY,
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

		CONSTRAINT fk_mpi_test_id FOREIGN KEY(mpi_test_id) REFERENCES mpi_test(id) ON DELETE CASCADE
	);
	ALTER TABLE IF EXISTS public.stress_quanti OWNER TO airflow;

	DROP TABLE IF EXISTS public.tpd_17_seg;
	CREATE TABLE tpd_17_seg (
		mpi_test_id int PRIMARY KEY,
		stress_sss decimal(6,2) NOT NULL,
		stress_sts decimal(6,2) NOT NULL,
		stress_sms decimal(6,2) NOT NULL,
		rest_srs decimal(6,2) NOT NULL,
		rest_sts decimal(6,2) NOT NULL,
		rest_sms decimal(6,2) NOT NULL,

		CONSTRAINT fk_mpi_test_id FOREIGN KEY(mpi_test_id) REFERENCES mpi_test(id) ON DELETE CASCADE
	);
	ALTER TABLE IF EXISTS public.tpd_17_seg OWNER TO airflow;

	DROP TABLE IF EXISTS public.used_by_incremental;
	CREATE TABLE used_by_incremental (
		mpi_test_id int PRIMARY KEY,
		patient_quanti boolean NOT NULL,
		patient_quali boolean NOT NULL,
		lad_quanti boolean NOT NULL,
		lad_quali boolean NOT NULL,
		lcx_quanti boolean NOT NULL,
		lcx_quali boolean NOT NULL,
		rca_quanti boolean NOT NULL,
		rca_quali boolean NOT NULL,

		CONSTRAINT fk_mpi_test_id FOREIGN KEY(mpi_test_id) REFERENCES mpi_test(id) ON DELETE CASCADE
	);
	ALTER TABLE IF EXISTS public.used_by_incremental OWNER TO airflow;
  COMMIT;
EOSQL