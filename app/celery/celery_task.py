from celery import shared_task, current_task
from app.utility_function.quantitative.ocr import ocr_mpi
from datetime import datetime
import os
import pydicom as dicom

# import quatitative utility function
from app.utility_function.quantitative.crud_db import insert_extract_mpi_test_data, check_mpi_test

# import qualitative utility function
from app.utility_function.qualitative.cropped_image.crop_v2 import prepare_img
from app.utility_function.qualitative.cropped_image.save_crop_vessel import insert_vessels_path

# import update status error function
from app.utility_function.return_error import update_status_return_msg

# Check image
def validate_image(path_file, hn_number):
    path_file = path_file.replace("\\", "/")

    dcm_files_path = [os.path.join(path_file, f) for f in os.listdir(path_file) if f.endswith(".dcm")]
    name_set    = {'rb', 'rd', 'ris', 'rs', 'sb', 'sd', 'sis', 'ss'}
    full_name   = {
        'rb':   'Rest Blackout Map', 
        'rd':   'Rest Def-Severity', 
        'ris':  'Rest', 
        'rs':   'Rest Severity', 
        'sb':   'Stress Blackout Map', 
        'sd':   'Stress Def-Severity', 
        'sis':  'Stress', 
        'ss':   'Stress Severity'
    } 

    # Check 8 DICOM files
    if len(dcm_files_path) != 8:
        raise Exception(f"พบ DICOM {len(dcm_files_path)} จาก 8 ไฟล์ โปรดตรวจสอบไฟล์ที่อัพโหลดอีกครั้ง")
    else:
        print(f">>>>> Found {len(dcm_files_path)} DICOM files.")

    # Check DICOM files for pattern and metadata
    for file_path in dcm_files_path:
        file_name = os.path.basename(file_path)
        series_name = os.path.splitext(file_name)[0]
        dcm_data = dicom.read_file(file_path)

        # Check DICOM files for pattern
        if series_name in name_set:
            name_set.remove(series_name)
        else:
            # f"'{file_name}' ไม่ใช่ไฟล์ในกลุ่มของ DICOM โปรดตรวจสอบไฟล์ที่อัพโหลดอีกครั้ง"
            raise Exception(f"ชื่อไฟล์ '{file_name}' ไม่ถูกต้องโปรดตรวจสอบไฟล์ที่อัพโหลดอีกครั้ง")

        # Check if file name is related to metadata (Series Description)
        if series_name != dcm_data[0x0008, 0x103e].value:
            raise Exception(f"ชื่อของไฟล์ '{file_name} ({full_name[file_name.split('.')[0]]})' และข้อมูลภายในไฟล์ไม่สอดคล้องกัน พบว่าข้อมูลภายในคือ '{full_name[dcm_data[0x0008, 0x103e].value]}' โปรดตรวจสอบไฟล์ที่อัพโหลดอีกครั้ง")
        
        # Check if hn number is correct or not
        if hn_number != dcm_data.PatientID:
            raise Exception(f"รหัสประจำตัวของผู้ป่วยไม่สอดคล้องกับข้อมูลรหัสประจำตัวของผู้ป่วยที่ถูกบันทึกภายในไฟล์ '{file_name} ({full_name[file_name.split('.')[0]]})'")

    # Check for duplicated files
    if name_set:
        raise Exception(f"พบไฟล์ DICOM ที่ซ้ำกัน ไฟล์เหล่านี้หายไป {name_set} โปรดตรวจสอบไฟล์ที่อัพโหลดอีกครั้ง")

class CustomTaskException(Exception):
    def __init__(self, message):
        self.message = message
        
# test
# 1, 039192-52, app/utility_function/data_for_test/039192-52 autoretry_for=(Exception,), retry_backoff=True , queue='extract_data'
@shared_task(bind=True,  track_started=True, name='extract_data:ocr_extract_task', acks_late=True)
def extract_task_data(self, hn: str, path_file: str, mpi_test_id: int):

    try:
        # Check image
        print("-" * 25, "Validate DICOM files", "-" * 25)
        validate_image(path_file, hn)

        # Extract ocr (quantitative)
        extract_df, confidence_df = ocr_mpi.main(path_file, hn)
        extract_df.replace({'-': '0'}, inplace=True)

        # Check mpi save in Database
        check_mpi_test(hn=hn, date_ext=extract_df.iloc[[0]].Date_MPI.values[0])
        
        # Crop image
        # dict keys: stress_perfusion, stress_severity, stress_blackout, stress_def-severity, rest_perfusion, rest_severity, rest_blackout, rest_def-severity
        cropped_img_path = prepare_img(hn, path_file)

        # Save extract data and crop image to Database
        insert_vessels_path(cropped_img_path, mpi_test_id)
        insert_extract_mpi_test_data(extract_df, confidence_df, mpi_test_id)

        return {"message": "The extracted data is complete"}
    
    except Exception as e:
        # Update the state to indicate failure
        current_task.update_state(state='FAILURE', meta={'exc_message': str(e)})
        update_status_return_msg(mpi_test_id=mpi_test_id, error=e, path_file=path_file)
        
        raise CustomTaskException(str(e))
        