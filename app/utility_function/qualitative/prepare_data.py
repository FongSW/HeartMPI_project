import numpy as np
import tensorflow as tf
import cv2, os
from glob import glob
from numpy import load

def validate_img_array(files_path):

    # check 4 files
    for key, val in files_path.items():

        data_lst = ['lad', 'lcx', 'rca', key.split("_")[1]]

        if len(val) != 4:

            for i in val:
                file_name = os.path.splitext((os.path.basename(i)))[0].split("_")[1]
                if file_name in data_lst:
                    data_lst.remove(file_name)
                else:
                    raise Exception(f"ชื่อของเส้นเลือด {os.path.basename(i)} ไม่ถูกต้อง")
                
            raise Exception(f"ไม่สามารถทำนายข้อูลเชิงคุณภาพได้เนื่องจากไฟล์ในกลุ่ม {key} เหล่านี้หายไป {data_lst}")
            
        else:
            print(f"\t>>>>> Found {key}: {len(val)} files.")

def validate_img_array_v2(files_path):

    for key, val in files_path.items():
        
        if not(os.path.isfile(val)):
            raise Exception(f"ไม่สามารถทำนายข้อูลเชิงคุณภาพได้เนื่องจากไฟล์สำหรับเส้นเลือด {key} นี้หายไป ({val})")
        else:
            print(f"\t>>>>> Found: {val.split('/')[-1]} file for vessel {key}.")

def load_img_array(hn, df_quali):

    # path stress
    file_path_v2 = {
        "LAD"       : os.path.join(df_quali.stress_blackout_dpath.values[0], f"{hn}_lad.npy"),
        "LCX"       : os.path.join(df_quali.stress_blackout_dpath.values[0], f"{hn}_lcx.npy"),
        "RCA"       : os.path.join(df_quali.stress_blackout_dpath.values[0], f"{hn}_rca.npy"),
        "PATIENT"   : os.path.join(df_quali.stress_severity_dpath.values[0], f"{hn}_severity.npy")
    }

    # validate npy file
    print("-" * 25, "Validate file npy")
    # validate_img_array(files_path)
    validate_img_array_v2(file_path_v2)

    print("-" * 25, "Load image array")

    # load array
    # im_array = dict()
    # for im_path in files_path['stress_perfusion']:
    #     vessel_type = os.path.splitext((os.path.basename(im_path)))[0].split("_")[1]
    #     vessel = load(im_path) / 255.0
    #     vessel = np.expand_dims(vessel, axis=0)
    #     if vessel_type.lower() not in ('lad', 'lcx', 'rca'):
    #         vessel_type = f'patient'
    #     im_array[vessel_type.lower()] = vessel
    
    im_array_v2 = dict()
    for k, v in file_path_v2.items():

        img = load(v) / 255.0
        img = np.expand_dims(img, axis=0)
        im_array_v2[k] = img

    # check values
    for vessel, img in im_array_v2.items():
        print(f"\t>>>>> {vessel} shape: {img.shape}")
        print(f"\t>>>>> {vessel} min value: {np.min(img)}")
        print(f"\t>>>>> {vessel} max value: {np.max(img)}\n")

    return im_array_v2


def load_cropped_img(file_path, hn):
    
    # load polar map [convert + normalize]
    polar_path = f"{file_path}/{hn}_01.Tif"
    polar_map = cv2.imread(polar_path)
    polar_map = cv2.cvtColor(polar_map, cv2.COLOR_BGR2RGB) / 255.0
    polar_map = np.expand_dims(polar_map, axis=0)

    # load vessels [convert + normalize]
    vessel_path = f"{file_path}/{hn}_01"
    lad = cv2.imread(vessel_path + "_LAD.Tif")
    lad = cv2.cvtColor(lad, cv2.COLOR_BGR2RGB) / 255.0
    lad = np.expand_dims(lad, axis=0)

    lcx = cv2.imread(vessel_path + "_LCX.Tif")
    lcx = cv2.cvtColor(lcx, cv2.COLOR_BGR2RGB) / 255.0
    lcx = np.expand_dims(lcx, axis=0)
    
    rca = cv2.imread(vessel_path + "_RCA.Tif")
    rca = cv2.cvtColor(rca, cv2.COLOR_BGR2RGB) / 255.0
    rca = np.expand_dims(rca, axis=0)

    # print val
    print(f">>>>> Polar map: {np.min(polar_map)}, {np.max(polar_map)}")
    print(f">>>>> LAD: {np.min(lad)}, {np.max(lad)}")
    print(f">>>>> LCX: {np.min(lcx)}, {np.max(lcx)}")
    print(f">>>>> RCA: {np.min(rca)}, {np.max(rca)}")

    print(f">>>>> Polar map shape: {polar_map.shape}")
    print(f">>>>> LAD shape: {lad.shape}")
    print(f">>>>> LCX shape: {lcx.shape}")
    print(f">>>>> RCA shape: {rca.shape}")

    return {"cag": polar_map, "lad": lad, "lcx": lcx, "rca": rca}


# def load_qualitative_model(predict_type):

#     # qualitative model path
#     model_quali_path = f"./app/model/{predict_type}/qualitative"
#     if predict_type == 'airflow':
#         model_quali_path += "/best_model"

#     # object path
#     patient_path = [i for i in glob(f"{model_quali_path}/pateint/*")][-1] 
#     lad_path = [i for i in glob(f"{model_quali_path}/LAD/*")] 
#     lcx_path = [i for i in glob(f"{model_quali_path}/LCX/*")] 
#     rca_path = [i for i in glob(f"{model_quali_path}/RCA/*")] 

#     # load all model (This process is mock up for  FastAPI V1)
#     patient_model = Vgg19model()
#     patient_model.load_weights(patient_path)
#     # lad_model = Vgg19model()
#     # lad_model.load_weights(patient_path)
#     # lcx_model = Vgg19model()
#     # lcx_model.load_weights(patient_path)
#     # rca_model = Vgg19model()
#     # rca_model.load_weights(patient_path)

#     print(f">>>>> patient_path: {patient_path}")
#     print(f">>>>> lad_path: {lad_path}")
#     print(f">>>>> lcx_path: {lcx_path}")
#     print(f">>>>> rca_path: {rca_path}")

#     # return patient_model, lad_model, lcx_model, rca_model

#     return patient_model

# # load qualitative base model first when api start
# base_patient_path = [i for i in glob(f"./app/model/base/qualitative/pateint/*")][-1] 
# qualitative_base_airflow_patient_model = Vgg19model()
# qualitative_base_airflow_patient_model.load_weights(base_patient_path)

# # load qualitative airflow model first when api start
# airflow_patient_path = [i for i in glob(f"./app/model/airflow/qualitative/best_model/pateint/*")][-1] 
# qualitative_airflow_patient_model = Vgg19model()
# qualitative_airflow_patient_model.load_weights(airflow_patient_path)