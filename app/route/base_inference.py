from fastapi import APIRouter, Depends
import pandas as pd
from datetime import datetime, timedelta, timezone
from time import time

# import the connection to postgres
from app.config.connection_db import con_db

# import db schema
from app.schema.input_patient import Predict_patient, Predict_patient_v2

# import JWT
# from app.auth.jwt_bearer import JWTBearer
# from app.auth.jwt_handler import signJWT

# import quantitative utility function
from app.utility_function.quantitative.model_utility import predict_quantitative_model
from app.utility_function.quantitative.pre_process import pre_processing
from app.config.connection_db import con_db

# import query quantitative data 
from app.utility_function.quantitative.crud_db import query_quanti_data_to_df

# import qualitative utility function
from app.utility_function.qualitative.prepare_data import load_img_array
from app.utility_function.qualitative.predict_qualitative import predict_qualitative_v2
from app.utility_function.ensemble_calculate import ensemble
from app.utility_function.query_ml_model import model_acc_global_cache

# import insert result prediction function
from app.utility_function.save_predict_result import prepare_to_insert, prepare_to_update

# router
base_inference_route = APIRouter(
    prefix='/base-inference', 
    tags=['base-inference'], 
    responses={404: {"description": "Not found"}} 
)

@base_inference_route.post("/quantitative/")
async def base_quantitative_model(data: Predict_patient = Depends(Predict_patient.as_form)):
    try:
        # 1. query db
        df_quanti = query_quanti_data_to_df(data.mpi_test_id)

        # 2. check data
        if df_quanti.shape[0] != 1: raise Exception(f'พบผลการตรวจของรหัสผลตรวจ (mpi_tets_id) : {data.mpi_test_id} ไม่เท่ากับ 1 ผลตรวจ โปรดตรวจสอบและลองอีกครั้ง')

        # 3. get and prepare data 
        quanti_features = pre_processing(df_quanti) 

        # 4. predict class
        quanti_predict_data = predict_quantitative_model(quanti_features, name_indicator='Base_Quantitative')
        print(quanti_predict_data)

        # 5. Save info prediction at db
        quanti_predict_data = prepare_to_insert(data.account_user_id,  mpi_test_id=data.mpi_test_id, predict_result=quanti_predict_data, inference_name='Base_Quantitative')

        # 6. Add status
        quanti_predict_data['status'] = "SUCCESS"

        return quanti_predict_data
    except Exception as e:
        print(e)
        # Update the state to indicate failure
        return {
            "status": "FAILURE",
            "detail": str(e)
        }

@base_inference_route.post("/qualitative/")
async def base_qualitative_model(data: Predict_patient = Depends(Predict_patient.as_form)):
    try:
        # 1. qurey crop image path (now use only perfusion_stress)
        df_quali = pd.read_sql(f'''SELECT * FROM mpi_crop_img WHERE mpi_test_id = '{data.mpi_test_id}' ''', con_db)
        hn = (pd.read_sql(f'''SELECT hn_number FROM mpi_test WHERE id = '{data.mpi_test_id}' ''', con_db)).values[0][0]
        if df_quali.shape[0] != 1: raise Exception(f'พบผลการตรวจของรหัสผลตรวจ (mpi_tets_id) : {data.mpi_test_id} ไม่เท่ากับ 1 ผลตรวจ โปรดตรวจสอบและลองอีกครั้ง')

        # 2. prepare img_data(np.array)
        quali_img_data = load_img_array(hn, df_quali)

        # 3. predict quali (mock up predict vessels)
        quali_predict_data = predict_qualitative_v2(quali_img_data, name='Base')

        # 4. save prediction result to table ml_diag
        quali_predict_data = prepare_to_insert(data.account_user_id, mpi_test_id=data.mpi_test_id, predict_result=quali_predict_data, inference_name='Base_Qualitative')

        # 6. Add status
        quali_predict_data['status'] = "SUCCESS"

        # 5. Return
        return quali_predict_data

    except Exception as e:
        print(e)
        # Update the state to indicate failure
        return {
            "status": "FAILURE",
            "detail": str(e)
        }

@base_inference_route.post("/hybrid/")
async def base_hybrid_model(data: Predict_patient = Depends(Predict_patient.as_form)):
    try:
        # 1.1 qurey quantitative data 
        df_quanti = query_quanti_data_to_df(data.mpi_test_id)

        # 1.2 qurey crop image path (now use only perfusion_stress)
        df_quali = pd.read_sql(f'''SELECT * FROM mpi_crop_img WHERE mpi_test_id = '{data.mpi_test_id}' ''', con_db)
        hn = (pd.read_sql(f'''SELECT hn_number FROM mpi_test WHERE id = '{data.mpi_test_id}' ''', con_db)).values[0][0]

        # 2. Check data 
        if df_quanti.shape[0] != 1 or df_quali.shape[0] != 1: raise Exception(f'พบผลการตรวจของรหัสผลตรวจ (mpi_tets_id) : {data.mpi_test_id} ไม่เท่ากับ 1 ผลตรวจ โปรดตรวจสอบและลองอีกครั้ง')
    
        # 3.1 prepare data, load model, load info :quanti
        quanti_features = pre_processing(df_quanti)

        # 3.2 prepare data, load model, load info :quali
        quali_img_data = load_img_array(hn, df_quali)

        # 4.1 predict quanti
        indicator = "Base_Hybrid"
        quanti_predict_data = predict_quantitative_model(quanti_features, indicator)

        # 4.2 predict quali
        quali_predict_data = predict_qualitative_v2(quali_img_data, name='Base')
    
        # 5. ensemble model max( quantitative score*base model acc, qualitative score*base model acc )
        predict_patient, predict_prob_patient = ensemble('patient', quanti_predict_data['predict_patient'], quanti_predict_data['predict_prob_patient'], quali_predict_data['predict_patient'], quali_predict_data['predict_prob_patient'], model_acc_global_cache['quanti_patient'], model_acc_global_cache['qualit_patient'])
        predict_rca, predict_prob_rca = ensemble('rca', quanti_predict_data['predict_rca'], quanti_predict_data['predict_prob_rca'], quali_predict_data['predict_rca'], quali_predict_data['predict_prob_rca'], model_acc_global_cache['quanti_rca'], model_acc_global_cache['qualit_rca'])
        predict_lad, predict_prob_lad = ensemble('lad', quanti_predict_data['predict_lad'], quanti_predict_data['predict_prob_lad'], quali_predict_data['predict_lad'], quali_predict_data['predict_prob_lad'], model_acc_global_cache['quanti_lad'], model_acc_global_cache['qualit_lad'])
        predict_lcx, predict_prob_lcx = ensemble('lcx', quanti_predict_data['predict_lcx'], quanti_predict_data['predict_prob_lcx'], quali_predict_data['predict_lcx'], quali_predict_data['predict_prob_lcx'], model_acc_global_cache['quanti_lcx'], model_acc_global_cache['qualit_lcx'])

        # 6. Save info prediction at db
        hybrid_predict_data = {
            'predict_prob_rca': predict_prob_rca,
            'predict_prob_lad': predict_prob_lad,
            'predict_prob_lcx': predict_prob_lcx,
            'predict_prob_patient': predict_prob_patient,
            'predict_rca': predict_rca,
            'predict_lad': predict_lad,
            'predict_lcx': predict_lcx,
            'predict_patient': predict_patient
        }

        # 7. Save info prediction at db
        hybrid_predict_data = prepare_to_insert(data.account_user_id, mpi_test_id=data.mpi_test_id, predict_result=hybrid_predict_data, inference_name='Base_Hybrid')

        # 8. Add status
        hybrid_predict_data['status'] = "SUCCESS"

        # 9. Return
        return hybrid_predict_data

    except Exception as e:
        print(e)
        # Update the state to indicate failure
        return {
            "status": "FAILURE",
            "detail": str(e)
        }


@base_inference_route.post("/all/")
async def base_all_model(data: Predict_patient = Depends(Predict_patient.as_form)):
    try:
        # 1.1 qurey quantitative data 
        df_quanti = query_quanti_data_to_df(data.mpi_test_id)

        # 1.2 qurey crop image path (now use only perfusion_stress)
        df_quali = pd.read_sql(f'''SELECT * FROM mpi_crop_img WHERE mpi_test_id = '{data.mpi_test_id}' ''', con_db)
        hn = (pd.read_sql(f'''SELECT hn_number FROM mpi_test WHERE id = '{data.mpi_test_id}' ''', con_db)).values[0][0]

        # 2. Check data 
        if df_quanti.shape[0] != 1 or df_quali.shape[0] != 1:  raise Exception(f'พบผลการตรวจของรหัสผลตรวจ (mpi_tets_id) : {data.mpi_test_id} ไม่เท่ากับ 1 ผลตรวจ โปรดตรวจสอบและลองอีกครั้ง')
    
        # 3.1 prepare data, load model, load info :quanti
        quanti_features = pre_processing(df_quanti)

        # 3.2 prepare data, load model, load info :quali
        quali_img_data = load_img_array(hn, df_quali)

        # 4.1 predict quanti
        indicator = "Base_Hybrid"
        quanti_predict_data = predict_quantitative_model(quanti_features, indicator)

        # 4.2 predict quali
        quali_predict_data = predict_qualitative_v2(quali_img_data, name='Base')
    
        # 5. ensemble model max( quantitative score*base model acc, qualitative score*base model acc )
        predict_patient, predict_prob_patient = ensemble('patient', quanti_predict_data['predict_patient'], quanti_predict_data['predict_prob_patient'], quali_predict_data['predict_patient'], quali_predict_data['predict_prob_patient'], model_acc_global_cache['quanti_patient'], model_acc_global_cache['qualit_patient'])
        predict_rca, predict_prob_rca = ensemble('rca', quanti_predict_data['predict_rca'], quanti_predict_data['predict_prob_rca'], quali_predict_data['predict_rca'], quali_predict_data['predict_prob_rca'], model_acc_global_cache['quanti_rca'], model_acc_global_cache['qualit_rca'])
        predict_lad, predict_prob_lad = ensemble('lad', quanti_predict_data['predict_lad'], quanti_predict_data['predict_prob_lad'], quali_predict_data['predict_lad'], quali_predict_data['predict_prob_lad'], model_acc_global_cache['quanti_lad'], model_acc_global_cache['qualit_lad'])
        predict_lcx, predict_prob_lcx = ensemble('lcx', quanti_predict_data['predict_lcx'], quanti_predict_data['predict_prob_lcx'], quali_predict_data['predict_lcx'], quali_predict_data['predict_prob_lcx'], model_acc_global_cache['quanti_lcx'], model_acc_global_cache['qualit_lcx'])

        all_predict_data = {
            "base_quantitative" : {
                "predict_rca" :         quanti_predict_data['predict_rca'],
                "predict_prob_rca":     quanti_predict_data['predict_prob_rca'],
                "predict_lad" :         quanti_predict_data['predict_lad'],
                "predict_prob_lad":     quanti_predict_data['predict_prob_lad'],
                "predict_lcx" :         quanti_predict_data['predict_lcx'],
                "predict_prob_lcx":     quanti_predict_data['predict_prob_lcx'],
                "predict_patient" :     quanti_predict_data['predict_patient'],
                "predict_prob_patient": quanti_predict_data['predict_prob_patient']
            },

            "base_qualitative": {
                "predict_rca" :         quali_predict_data['predict_rca'],
                "predict_prob_rca":     quali_predict_data['predict_prob_rca'],
                "predict_lad" :         quali_predict_data['predict_lad'],
                "predict_prob_lad":     quali_predict_data['predict_prob_lad'],
                "predict_lcx" :         quali_predict_data['predict_lcx'],
                "predict_prob_lcx":     quali_predict_data['predict_prob_lcx'],
                "predict_patient" :     quali_predict_data['predict_patient'],
                "predict_prob_patient": quali_predict_data['predict_prob_patient']
            },

            "base_hybrid" : {
                "predict_rca" :         predict_rca,
                "predict_prob_rca":     predict_prob_rca,
                "predict_lad" :         predict_lad,
                "predict_prob_lad":     predict_prob_lad,
                "predict_lcx" :         predict_lcx,
                "predict_prob_lcx":     predict_prob_lcx,
                "predict_patient" :     predict_patient,
                "predict_prob_patient": predict_prob_patient
            }
        }

        # 5. save prediction result to table ml_diag
        all_predict_data = prepare_to_insert(data.account_user_id, data.mpi_test_id, all_predict_data, inference_name='Base_All')

        # 6. Add status
        all_predict_data['status'] = "SUCCESS"

        # 7. Return
        return all_predict_data

    except Exception as e:
        print(e)
        # Update the state to indicate failure
        return {
            "status": "FAILURE",
            "detail": str(e)
        }

# ---------------------------- v2 -------------------------------
@base_inference_route.post("/quantitative-v2/")
async def base_quantitative_modele_v2(data: Predict_patient_v2 = Depends(Predict_patient_v2.as_form)):
    try:
        # 1. query db
        df_quanti = query_quanti_data_to_df(data.mpi_test_id)

        # 2. check data
        if df_quanti.shape[0] != 1: raise Exception(f'พบผลการตรวจของรหัสผลตรวจ (mpi_tets_id) : {data.mpi_test_id} ไม่เท่ากับ 1 ผลตรวจ โปรดตรวจสอบและลองอีกครั้ง')

        # 3. get and prepare data 
        quanti_features = pre_processing(df_quanti) 

        # 4. predict class
        quanti_predict_data = predict_quantitative_model(quanti_features, name_indicator='Base_Quantitative')
        print(quanti_predict_data)

        # 5. Save info prediction at db
        quanti_predict_data = prepare_to_update(data.ml_diag_id, predict_result=quanti_predict_data, inference_name='Base_Quantitative')

        # 6. Add status
        quanti_predict_data['status'] = "SUCCESS"

        return quanti_predict_data
    except Exception as e:
        print(e)
        # Update the state to indicate failure
        return {
            "status": "FAILURE",
            "detail": str(e)
        }

@base_inference_route.post("/qualitative-v2/")
async def base_qualitative_model_v2(data: Predict_patient_v2 = Depends(Predict_patient_v2.as_form)):
    try:
        # Timer start
        start_time = time()

        # 1. qurey crop image path (now use only perfusion_stress) & hn
        df_quali = pd.read_sql(f'''SELECT * FROM mpi_crop_img WHERE mpi_test_id = '{data.mpi_test_id}' ''', con_db)
        hn = (pd.read_sql(f'''SELECT hn_number FROM mpi_test WHERE id = '{data.mpi_test_id}' ''', con_db)).values[0][0]
        if df_quali.shape[0] != 1: raise Exception(f'พบผลการตรวจของรหัสผลตรวจ (mpi_tets_id) : {data.mpi_test_id} ไม่เท่ากับ 1 ผลตรวจ โปรดตรวจสอบและลองอีกครั้ง')

        # 2. prepare img_data(np.array)
        quali_img_data = load_img_array(hn, df_quali)

        # 3. predict quali (mock up predict vessels)
        quali_predict_data = predict_qualitative_v2(quali_img_data, name='Base')

        # 4. save prediction result to table ml_diag
        quali_predict_data = prepare_to_update(data.ml_diag_id, predict_result=quali_predict_data, inference_name='Base_Qualitative')

        # 6. Add status
        quali_predict_data['status'] = "SUCCESS"

        # Measure the current time again
        end_time = time()
        print("-" * 25, "Elapsed time")
        print(f"\t>>>>> {end_time - start_time:.2f} seconds")

        # 5. Return
        return quali_predict_data

    except Exception as e:
        print(e)
        # Update the state to indicate failure
        return {
            "status": "FAILURE",
            "detail": str(e)
        }

@base_inference_route.post("/hybrid-v2/")
async def base_hybrid_model_v2(data: Predict_patient_v2 = Depends(Predict_patient_v2.as_form)):
    try:
        # Timer start
        start_time = time()

        # 1.1 qurey quantitative data 
        df_quanti = query_quanti_data_to_df(data.mpi_test_id)

        # 1.2 qurey crop image path (now use only perfusion_stress)
        df_quali = pd.read_sql(f'''SELECT * FROM mpi_crop_img WHERE mpi_test_id = '{data.mpi_test_id}' ''', con_db)
        hn = (pd.read_sql(f'''SELECT hn_number FROM mpi_test WHERE id = '{data.mpi_test_id}' ''', con_db)).values[0][0]

        # 2. Check data 
        if df_quanti.shape[0] != 1 or df_quali.shape[0] != 1: raise Exception(f'พบผลการตรวจของรหัสผลตรวจ (mpi_tets_id) : {data.mpi_test_id} ไม่เท่ากับ 1 ผลตรวจ โปรดตรวจสอบและลองอีกครั้ง')
    
        # 3.1 prepare data, load model, load info :quanti
        quanti_features = pre_processing(df_quanti)

        # 3.2 prepare data, load model, load info :quali
        quali_img_data = load_img_array(hn, df_quali)

        # 4.1 predict quanti
        indicator = "Base_Hybrid"
        quanti_predict_data = predict_quantitative_model(quanti_features, indicator)

        # 4.2 predict quali
        quali_predict_data = predict_qualitative_v2(quali_img_data, name='Base')
    
        # 5. ensemble model max( quantitative score*base model acc, qualitative score*base model acc )
        predict_patient, predict_prob_patient = ensemble('patient', quanti_predict_data['predict_patient'], quanti_predict_data['predict_prob_patient'], quali_predict_data['predict_patient'], quali_predict_data['predict_prob_patient'], model_acc_global_cache['quanti_patient'], model_acc_global_cache['qualit_patient'])
        predict_rca, predict_prob_rca = ensemble('rca', quanti_predict_data['predict_rca'], quanti_predict_data['predict_prob_rca'], quali_predict_data['predict_rca'], quali_predict_data['predict_prob_rca'], model_acc_global_cache['quanti_rca'], model_acc_global_cache['qualit_rca'])
        predict_lad, predict_prob_lad = ensemble('lad', quanti_predict_data['predict_lad'], quanti_predict_data['predict_prob_lad'], quali_predict_data['predict_lad'], quali_predict_data['predict_prob_lad'], model_acc_global_cache['quanti_lad'], model_acc_global_cache['qualit_lad'])
        predict_lcx, predict_prob_lcx = ensemble('lcx', quanti_predict_data['predict_lcx'], quanti_predict_data['predict_prob_lcx'], quali_predict_data['predict_lcx'], quali_predict_data['predict_prob_lcx'], model_acc_global_cache['quanti_lcx'], model_acc_global_cache['qualit_lcx'])

        # 6. Save info prediction at db
        hybrid_predict_data = {
            'predict_prob_rca': predict_prob_rca,
            'predict_prob_lad': predict_prob_lad,
            'predict_prob_lcx': predict_prob_lcx,
            'predict_prob_patient': predict_prob_patient,
            'predict_rca': predict_rca,
            'predict_lad': predict_lad,
            'predict_lcx': predict_lcx,
            'predict_patient': predict_patient
        }

        # 7. Save info prediction at db
        hybrid_predict_data = prepare_to_update(data.ml_diag_id, predict_result=hybrid_predict_data, inference_name='Base_Hybrid')

        # 8. Add status
        hybrid_predict_data['status'] = "SUCCESS"

        # Measure the current time again
        end_time = time()
        print("-" * 25, "Elapsed time")
        print(f"\t>>>>> {end_time - start_time:.2f} seconds")

        # 9. Return
        return hybrid_predict_data

    except Exception as e:
        print(e)
        # Update the state to indicate failure
        return {
            "status": "FAILURE",
            "detail": str(e)
        }


@base_inference_route.post("/all-v2/")
async def base_all_model_v2(data: Predict_patient_v2 = Depends(Predict_patient_v2.as_form)):
    try:
        # Timer start
        start_time = time()

        # 1.1 qurey quantitative data 
        df_quanti = query_quanti_data_to_df(data.mpi_test_id)

        # 1.2 qurey crop image path (now use only perfusion_stress)
        df_quali = pd.read_sql(f'''SELECT * FROM mpi_crop_img WHERE mpi_test_id = '{data.mpi_test_id}' ''', con_db)
        hn = (pd.read_sql(f'''SELECT hn_number FROM mpi_test WHERE id = '{data.mpi_test_id}' ''', con_db)).values[0][0]

        # 2. Check data 
        if df_quanti.shape[0] != 1 or df_quali.shape[0] != 1:  raise Exception(f'พบผลการตรวจของรหัสผลตรวจ (mpi_tets_id) : {data.mpi_test_id} ไม่เท่ากับ 1 ผลตรวจ โปรดตรวจสอบและลองอีกครั้ง')
    
        # 3.1 prepare data, load model, load info :quanti
        quanti_features = pre_processing(df_quanti)

        # 3.2 prepare data, load model, load info :quali
        quali_img_data = load_img_array(hn, df_quali)
        # quali_patient_model = load_qualitative_model(predict_type='base')

        # 4.1 predict quanti
        indicator = "Base_Hybrid"
        quanti_predict_data = predict_quantitative_model(quanti_features, indicator)

        # 4.2 predict quali
        quali_predict_data = predict_qualitative_v2(quali_img_data, name='Base')
    
        # 5. ensemble model max( quantitative score*base model acc, qualitative score*base model acc )
        predict_patient, predict_prob_patient = ensemble('patient', quanti_predict_data['predict_patient'], quanti_predict_data['predict_prob_patient'], quali_predict_data['predict_patient'], quali_predict_data['predict_prob_patient'], model_acc_global_cache['quanti_patient'], model_acc_global_cache['qualit_patient'])
        predict_rca, predict_prob_rca = ensemble('rca', quanti_predict_data['predict_rca'], quanti_predict_data['predict_prob_rca'], quali_predict_data['predict_rca'], quali_predict_data['predict_prob_rca'], model_acc_global_cache['quanti_rca'], model_acc_global_cache['qualit_rca'])
        predict_lad, predict_prob_lad = ensemble('lad', quanti_predict_data['predict_lad'], quanti_predict_data['predict_prob_lad'], quali_predict_data['predict_lad'], quali_predict_data['predict_prob_lad'], model_acc_global_cache['quanti_lad'], model_acc_global_cache['qualit_lad'])
        predict_lcx, predict_prob_lcx = ensemble('lcx', quanti_predict_data['predict_lcx'], quanti_predict_data['predict_prob_lcx'], quali_predict_data['predict_lcx'], quali_predict_data['predict_prob_lcx'], model_acc_global_cache['quanti_lcx'], model_acc_global_cache['qualit_lcx'])


        all_predict_data = {
            "base_quantitative" : {
                "predict_rca" :         quanti_predict_data['predict_rca'],
                "predict_prob_rca":     quanti_predict_data['predict_prob_rca'],
                "predict_lad" :         quanti_predict_data['predict_lad'],
                "predict_prob_lad":     quanti_predict_data['predict_prob_lad'],
                "predict_lcx" :         quanti_predict_data['predict_lcx'],
                "predict_prob_lcx":     quanti_predict_data['predict_prob_lcx'],
                "predict_patient" :     quanti_predict_data['predict_patient'],
                "predict_prob_patient": quanti_predict_data['predict_prob_patient']
            },

            "base_qualitative": {
                "predict_rca" :         quali_predict_data['predict_rca'],
                "predict_prob_rca":     quali_predict_data['predict_prob_rca'],
                "predict_lad" :         quali_predict_data['predict_lad'],
                "predict_prob_lad":     quali_predict_data['predict_prob_lad'],
                "predict_lcx" :         quali_predict_data['predict_lcx'],
                "predict_prob_lcx":     quali_predict_data['predict_prob_lcx'],
                "predict_patient" :     quali_predict_data['predict_patient'],
                "predict_prob_patient": quali_predict_data['predict_prob_patient']
            },

            "base_hybrid" : {
                "predict_rca" :         predict_rca,
                "predict_prob_rca":     predict_prob_rca,
                "predict_lad" :         predict_lad,
                "predict_prob_lad":     predict_prob_lad,
                "predict_lcx" :         predict_lcx,
                "predict_prob_lcx":     predict_prob_lcx,
                "predict_patient" :     predict_patient,
                "predict_prob_patient": predict_prob_patient
            }
        }

        # 5. save prediction result to table ml_diag
        print(f">>>>> The updated result ml_diag_id {data.ml_diag_id}. Base_All")
        all_predict_data = prepare_to_update(data.ml_diag_id, all_predict_data, inference_name='Base_All')

        # Measure the current time again
        end_time = time()
        print("-" * 25, "Elapsed time")
        print(f"\t>>>>> {end_time - start_time:.2f} seconds")

        # 6. Add status
        all_predict_data['status'] = "SUCCESS"

        # 7. Return
        return all_predict_data

    except Exception as e:
        print(e)
        # Update the state to indicate failure
        return {
            "status": "FAILURE",
            "detail": str(e)
        }
   
@base_inference_route.post("/test-super-learner/")
async def base_quantitative_model_test(data: Predict_patient = Depends(Predict_patient.as_form)):
    from module_superlearner.superlearner_model import SuperLearnerClassifier
    
    print(SuperLearnerClassifier)
    import pickle
    import numpy as np
    # Now you can import from the root
    try:
        # 1. query db
        df_quanti = query_quanti_data_to_df(data.mpi_test_id)

        # 2. check data
        if df_quanti.shape[0] != 1: raise Exception(f'พบผลการตรวจของรหัสผลตรวจ (mpi_tets_id) : {data.mpi_test_id} ไม่เท่ากับ 1 ผลตรวจ โปรดตรวจสอบและลองอีกครั้ง')

        # 3. get and prepare data 
        quanti_features = pre_processing(df_quanti) 
        print('ssss',quanti_features)

        # 4. predict class
        p_file_model = '/opt/app/model/base/quantitative/test_superlearner_model/test_superlearner_model_v3.pickle'
        model = pickle.load(open(p_file_model, 'rb'))
        #model = joblib.load(p_file_model)
        pred = model.predict(quanti_features)
        pred_prob = model.predict_proba(quanti_features)
        pred_prob = round(float(np.max(pred_prob)), 2 )
        print('>>>>>',pred_prob)
        quanti_predict_data = {
            'predict': int(pred[0]),
            'predict_proba': pred_prob
        }
        print(quanti_predict_data)


        # 6. Add status
        quanti_predict_data['status'] = "SUCCESS"

        return quanti_predict_data
    except Exception as e:
        print(e)
        # Update the state to indicate failure
        return {
            "status": "FAILURE",
            "detail": str(e)
        }
