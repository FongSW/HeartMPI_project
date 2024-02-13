# import db connection
from app.config.connection_db import con_db

# import table schema
from app.schema.patient_info import mpi_crop_img

def insert_vessels_path(vessel_path, mpi_test_id):
    # vessel_path dict keys: stress_perfusion, stress_severity, stress_blackout, stress_def-severity, rest_perfusion, rest_severity, rest_blackout, rest_def-severity
    inserting = mpi_crop_img.insert().values(
        mpi_test_id = mpi_test_id,
        stress_perfusion_dpath = vessel_path['stress_perfusion'],
        rest_perfusion_dpath    = vessel_path['rest_perfusion'],

        stress_severity_dpath = vessel_path['stress_severity'],
        rest_severity_dpath = vessel_path['rest_severity'],

        stress_blackout_dpath = vessel_path['stress_blackout'],
        rest_blackout_dpath = vessel_path['rest_blackout'],

        stress_def_sev_dpath = vessel_path['stress_def-severity'],
        rest_def_sev_dpath = vessel_path['rest_def-severity']
    )

    # execute
    con_db.execute(inserting)
    print("The inserting data was successful.")