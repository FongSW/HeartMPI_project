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

    CONSTRAINT fk_mpi_test_id
    FOREIGN KEY(mpi_test_id)
    REFERENCES mpi_test(id)
)


TABLESPACE pg_default;

ALTER TABLE IF EXISTS public.mpi_crop_img
    OWNER to airflow;