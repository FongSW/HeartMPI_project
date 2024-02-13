from datetime import datetime
import json
import os
from app.utility_function.quantitative.crud_db import update_status_mpi_test

def update_status_return_msg(mpi_test_id, error, path_file):
    
    "This function updates the status failed in table mpi-test and returns a message error by json file."
    try:
        # Create datetime
        date_now = datetime.now().strftime('%Y-%m-%d %X')

        # Update status mpi_test
        update_status_mpi_test(mpi_test_id, date_now)

        # Create json file for returning error
        msg = {'message': str(error)}
        error_json = json.dumps(msg, ensure_ascii=False)
        with open(os.path.join(path_file, "error.json"), "w") as msg_error:
            msg_error.write(error_json)

    except Exception as e:
        print("Can not update error: ", e) 