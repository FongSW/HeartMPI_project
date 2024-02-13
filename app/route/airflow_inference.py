from fastapi import APIRouter, Depends
import pandas as pd
from app.schema.input_patient import Predict_patient, Predict_patient_v2
#import JWT
# from app.auth.jwt_bearer import JWTBearer
# from app.auth.jwt_handler import signJWT

# import quantitative utility function
from app.utility_function.quantitative.model_utility import predict_quantitative_model
from app.utility_function.quantitative.pre_process import pre_processing
from app.config.connection_db import con_db

# import qualitative utility function
from app.utility_function.qualitative.prepare_data import load_img_array
from app.utility_function.qualitative.predict_qualitative import predict_qualitative

# import utility function
from app.utility_function.ensemble_calculate import ensemble

# import query quantitative data 
from app.utility_function.quantitative.crud_db import query_quanti_data_to_df

# import save predict result
from app.utility_function.save_predict_result import prepare_to_insert, prepare_to_update

# router
airflow_inference_route = APIRouter(
    prefix='/airflow-inference', 
    tags=['airflow-inference'], 
    responses={404: {"description": "Not found"}}
)

@airflow_inference_route.post("/quantitative/")
async def airflow_quantitative_model(data: Predict_patient = Depends(Predict_patient.as_form)):

    try:

        # 1. query db
        df_quanti = query_quanti_data_to_df(data.mpi_test_id)

        # 2. check data 
        if df_quanti.shape[0] != 1:
            raise Exception(f'พบผลการตรวจของรหัสผลตรวจ (mpi_tets_id) : {data.mpi_test_id} ไม่เท่ากับ 1 ผลตรวจ โปรดตรวจสอบและลองอีกครั้ง')

        # 3. Prepare data 
        quanti_features = pre_processing(df_quanti)

        # 4. predict class
        indicator = "Adaptive_Quantitative"
        quanti_predict_data = predict_quantitative_model(quanti_features, indicator)

        # 5. Save info prediction at db
        quanti_predict_data = prepare_to_insert(data.account_user_id, data.mpi_test_id, quanti_predict_data, inference_name='Adaptive_Quantitative')

        # 6. add status
        quanti_predict_data['status'] = 'SUCCESS'

        return quanti_predict_data
    
    except Exception as e:
        
        return {"status": "FAILURE", "detail": str(e)}


@airflow_inference_route.post("/qualitative/")
async def airflow_qualitative_model(data: Predict_patient = Depends(Predict_patient.as_form)):

    try:

        # 1. qurey crop image path (now use only perfusion_stress)
        df_quali = pd.read_sql(f'''SELECT * FROM mpi_crop_img WHERE mpi_test_id = '{data.mpi_test_id}' ''', con_db)
        if df_quali.shape[0] != 1: raise Exception(f'พบผลการตรวจของรหัสผลตรวจ (mpi_tets_id) : {data.mpi_test_id} ไม่เท่ากับ 1 ผลตรวจ โปรดตรวจสอบและลองอีกครั้ง')

        # 2. prepare img_data(np.array)
        quali_img_data = load_img_array(df_quali)

        # 3. predict quali (mock up predict vessels)
        quali_predict_data = predict_qualitative(quali_img_data, name='Adaptive')

        # 4. save prediction result to table ml_diag
        quali_predict_data = prepare_to_insert(data.account_user_id, data.mpi_test_id, quali_predict_data, inference_name='Adaptive_Qualitative')

        # 5. add status
        quali_predict_data['status'] = 'SUCCESS'

        # 6. return
        return quali_predict_data

    except Exception as e:
        
        return {"status": "FAILURE", "detail": str(e)}

@airflow_inference_route.post("/hybrid/")
async def airflow_hybrid_model(data: Predict_patient = Depends(Predict_patient.as_form)):
    
    try:
        # ตัวอย่างชื่อตัวแปร quali_predict_prob_lcx, quanti_predict_prob_lcx
        # 1.1 query quanti
        df_quanti = query_quanti_data_to_df(data.mpi_test_id)
        if df_quanti.shape[0] != 1: raise Exception(f'พบผลการตรวจของรหัสผลตรวจ (mpi_tets_id) : {data.mpi_test_id} ไม่เท่ากับ 1 ผลตรวจ โปรดตรวจสอบและลองอีกครั้ง')

        # 1.2 query quali
        df_quali = pd.read_sql(f'''SELECT * FROM mpi_crop_img WHERE mpi_test_id = '{data.mpi_test_id}' ''', con_db)
        if df_quali.shape[0] != 1: raise Exception(f'พบผลการตรวจของรหัสผลตรวจ (mpi_tets_id) : {data.mpi_test_id} ไม่เท่ากับ 1 ผลตรวจ โปรดตรวจสอบและลองอีกครั้ง')
    
        # 2.1 prepare quanti
        quanti_features = pre_processing(df_quanti)

        # 2.2 prepare quali
        quali_img_data = load_img_array(df_quali)

        # 3.1 predict quanti
        indicator = "Adaptive_Quantitative"
        quanti_predict_data = predict_quantitative_model(quanti_features, indicator)

        # 3.2 predict quali
        quali_predict_data = predict_qualitative(quali_img_data, name='Adaptive')

        # 4. ensemble model max( quantitative score*base model acc, qualitative score*base model acc )
        predict_patient, predict_prob_patient = ensemble(quanti_predict_data['predict_prob_patient'], quanti_predict_data['predict_patient'], quali_predict_data['predict_prob_patient'], quali_predict_data['predict_patient'])
        predict_rca, predict_prob_rca = ensemble(quanti_predict_data['predict_prob_rca'], quanti_predict_data['predict_rca'], quali_predict_data['predict_prob_rca'], quali_predict_data['predict_rca'])
        predict_lad, predict_prob_lad = ensemble(quanti_predict_data['predict_prob_lad'], quanti_predict_data['predict_lad'], quali_predict_data['predict_prob_lad'], quali_predict_data['predict_lad'])
        predict_lcx, predict_prob_lcx = ensemble(quanti_predict_data['predict_prob_lcx'], quanti_predict_data['predict_lcx'], quali_predict_data['predict_prob_lcx'], quali_predict_data['predict_lcx'])

        # 5. save prediction result to table ml_diag
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
        hybrid_predict_data = prepare_to_insert(data.account_user_id, data.mpi_test_id, hybrid_predict_data, inference_name='Adaptive_Hybrid')

        # 6. add status
        hybrid_predict_data['status'] = 'SUCCESS'

        # 7. return
        return hybrid_predict_data

    except Exception as e:

        return {"status": "FAILURE", "detail": str(e)}

@airflow_inference_route.post("/all/")
async def airflow_all_model(data: Predict_patient = Depends(Predict_patient.as_form)):

    try:
        # ตัวอย่างชื่อตัวแปร quali_predict_prob_lcx, quanti_predict_prob_lcx
        # 1.1 query quanti
        df_quanti = query_quanti_data_to_df(data.mpi_test_id)
        if df_quanti.shape[0] != 1: raise Exception(f'พบผลการตรวจของรหัสผลตรวจ (mpi_tets_id) : {data.mpi_test_id} ไม่เท่ากับ 1 ผลตรวจ โปรดตรวจสอบและลองอีกครั้ง')

        # 1.2 query quali
        df_quali = pd.read_sql(f'''SELECT * FROM mpi_crop_img WHERE mpi_test_id = '{data.mpi_test_id}' ''', con_db)
        if df_quali.shape[0] != 1: raise Exception(f'พบผลการตรวจของรหัสผลตรวจ (mpi_tets_id) : {data.mpi_test_id} ไม่เท่ากับ 1 ผลตรวจ โปรดตรวจสอบและลองอีกครั้ง')
    
        # 2.1 prepare quanti
        quanti_features = pre_processing(df_quanti)

        # 2.2 prepare quali
        quali_img_data = load_img_array(df_quali)

        # 3.1 predict quanti
        indicator = "Adaptive_Quantitative"
        quanti_predict_data = predict_quantitative_model(quanti_features, indicator)

        # 3.2 predict quali
        quali_predict_data = predict_qualitative(quali_img_data, name='Adaptive')

        # 4. ensemble model max( quantitative score*base model acc, qualitative score*base model acc )
        predict_patient, predict_prob_patient = ensemble(quanti_predict_data['predict_prob_patient'], quanti_predict_data['predict_patient'], quali_predict_data['predict_prob_patient'], quali_predict_data['predict_patient'])
        predict_rca, predict_prob_rca = ensemble(quanti_predict_data['predict_prob_rca'], quanti_predict_data['predict_rca'], quali_predict_data['predict_prob_rca'], quali_predict_data['predict_rca'])
        predict_lad, predict_prob_lad = ensemble(quanti_predict_data['predict_prob_lad'], quanti_predict_data['predict_lad'], quali_predict_data['predict_prob_lad'], quali_predict_data['predict_lad'])
        predict_lcx, predict_prob_lcx = ensemble(quanti_predict_data['predict_prob_lcx'], quanti_predict_data['predict_lcx'], quali_predict_data['predict_prob_lcx'], quali_predict_data['predict_lcx'])
        all_predict_data = {
            "airflow_quantitative" : {
                "predict_rca" :         quanti_predict_data['predict_rca'],
                "predict_prob_rca":     quanti_predict_data['predict_prob_rca'],
                "predict_lad" :         quanti_predict_data['predict_lad'],
                "predict_prob_lad":     quanti_predict_data['predict_prob_lad'],
                "predict_lcx" :         quanti_predict_data['predict_lcx'],
                "predict_prob_lcx":     quanti_predict_data['predict_prob_lcx'],
                "predict_patient" :     quanti_predict_data['predict_patient'],
                "predict_prob_patient": quanti_predict_data['predict_prob_patient']
            },

            "airflow_qualitative": {
                "predict_rca" :         quali_predict_data['predict_rca'],
                "predict_prob_rca":     quali_predict_data['predict_prob_rca'],
                "predict_lad" :         quali_predict_data['predict_lad'],
                "predict_prob_lad":     quali_predict_data['predict_prob_lad'],
                "predict_lcx" :         quali_predict_data['predict_lcx'],
                "predict_prob_lcx":     quali_predict_data['predict_prob_lcx'],
                "predict_patient" :     quali_predict_data['predict_patient'],
                "predict_prob_patient": quali_predict_data['predict_prob_patient']
            },

            "airflow_hybrid" : {
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
        all_predict_data = prepare_to_insert(data.account_user_id, data.mpi_test_id, all_predict_data, inference_name='Adaptive_All')

        # 6. add status
        all_predict_data['status'] = 'SUCCESS'

        # 7. return
        return all_predict_data
    
    except Exception as e:

        return {"status": "FAILURE", "detail": str(e)}
    
@airflow_inference_route.post("/quantitative-v2/")
async def airflow_quantitative_model_v2(data: Predict_patient_v2 = Depends(Predict_patient_v2.as_form)):

    try:

        # 1. query db
        df_quanti = query_quanti_data_to_df(data.mpi_test_id)

        # 2. check data 
        if df_quanti.shape[0] != 1:
            raise Exception(f'พบผลการตรวจของรหัสผลตรวจ (mpi_tets_id) : {data.mpi_test_id} ไม่เท่ากับ 1 ผลตรวจ โปรดตรวจสอบและลองอีกครั้ง')

        # 3. Prepare data 
        quanti_features = pre_processing(df_quanti)

        # 4. predict class
        indicator = "Adaptive_Quantitative"
        quanti_predict_data = predict_quantitative_model(quanti_features, indicator)

        # 5. Save info prediction at db
        quanti_predict_data = prepare_to_update(data.ml_diag_id, predict_result=quanti_predict_data, inference_name='Adaptive_Quantitative')
                              

        # 6. add status
        quanti_predict_data['status'] = 'SUCCESS'

        return quanti_predict_data
    
    except Exception as e:
        
        return {"status": "FAILURE", "detail": str(e)}
    
@airflow_inference_route.post("/qualitative-v2/")
async def airflow_qualitative_model_v2(data: Predict_patient_v2 = Depends(Predict_patient_v2.as_form)):

    try:

        # 1. qurey crop image path (now use only perfusion_stress)
        df_quali = pd.read_sql(f'''SELECT * FROM mpi_crop_img WHERE mpi_test_id = '{data.mpi_test_id}' ''', con_db)
        if df_quali.shape[0] != 1: raise Exception(f'พบผลการตรวจของรหัสผลตรวจ (mpi_tets_id) : {data.mpi_test_id} ไม่เท่ากับ 1 ผลตรวจ โปรดตรวจสอบและลองอีกครั้ง')

        # 2. prepare img_data(np.array)
        quali_img_data = load_img_array(df_quali)

        # 3. predict quali (mock up predict vessels)
        quali_predict_data = predict_qualitative(quali_img_data, name='Adaptive')

        # 4. save prediction result to table ml_diag
        quali_predict_data = prepare_to_update(data.ml_diag_id, predict_result=quali_predict_data, inference_name='Adaptive_Qualitative')
                            
        # 5. add status
        quali_predict_data['status'] = 'SUCCESS'

        # 6. return
        return quali_predict_data

    except Exception as e:
        
        return {"status": "FAILURE", "detail": str(e)}
    
@airflow_inference_route.post("/hybrid-v2/")
async def airflow_hybrid_model_v2(data: Predict_patient_v2 = Depends(Predict_patient_v2.as_form)):
    
    try:
        # ตัวอย่างชื่อตัวแปร quali_predict_prob_lcx, quanti_predict_prob_lcx
        # 1.1 query quanti
        df_quanti = query_quanti_data_to_df(data.mpi_test_id)
        if df_quanti.shape[0] != 1: raise Exception(f'พบผลการตรวจของรหัสผลตรวจ (mpi_tets_id) : {data.mpi_test_id} ไม่เท่ากับ 1 ผลตรวจ โปรดตรวจสอบและลองอีกครั้ง')

        # 1.2 query quali
        df_quali = pd.read_sql(f'''SELECT * FROM mpi_crop_img WHERE mpi_test_id = '{data.mpi_test_id}' ''', con_db)
        if df_quali.shape[0] != 1: raise Exception(f'พบผลการตรวจของรหัสผลตรวจ (mpi_tets_id) : {data.mpi_test_id} ไม่เท่ากับ 1 ผลตรวจ โปรดตรวจสอบและลองอีกครั้ง')
    
        # 2.1 prepare quanti
        quanti_features = pre_processing(df_quanti)

        # 2.2 prepare quali
        quali_img_data = load_img_array(df_quali)

        # 3.1 predict quanti
        indicator = "Adaptive_Quantitative"
        quanti_predict_data = predict_quantitative_model(quanti_features, indicator)

        # 3.2 predict quali
        quali_predict_data = predict_qualitative(quali_img_data, name='Adaptive')

        # 4. ensemble model max( quantitative score*base model acc, qualitative score*base model acc )
        predict_patient, predict_prob_patient = ensemble(quanti_predict_data['predict_prob_patient'], quanti_predict_data['predict_patient'], quali_predict_data['predict_prob_patient'], quali_predict_data['predict_patient'])
        predict_rca, predict_prob_rca = ensemble(quanti_predict_data['predict_prob_rca'], quanti_predict_data['predict_rca'], quali_predict_data['predict_prob_rca'], quali_predict_data['predict_rca'])
        predict_lad, predict_prob_lad = ensemble(quanti_predict_data['predict_prob_lad'], quanti_predict_data['predict_lad'], quali_predict_data['predict_prob_lad'], quali_predict_data['predict_lad'])
        predict_lcx, predict_prob_lcx = ensemble(quanti_predict_data['predict_prob_lcx'], quanti_predict_data['predict_lcx'], quali_predict_data['predict_prob_lcx'], quali_predict_data['predict_lcx'])

        # 5. save prediction result to table ml_diag
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
        hybrid_predict_data = prepare_to_update(data.ml_diag_id, predict_result=hybrid_predict_data, inference_name='Adaptive_Hybrid')
                              

        # 6. add status
        hybrid_predict_data['status'] = 'SUCCESS'

        # 7. return
        return hybrid_predict_data

    except Exception as e:

        return {"status": "FAILURE", "detail": str(e)}
    
@airflow_inference_route.post("/all-v2/")
async def airflow_all_model_v2(data: Predict_patient_v2 = Depends(Predict_patient_v2.as_form)):

    try:
        # ตัวอย่างชื่อตัวแปร quali_predict_prob_lcx, quanti_predict_prob_lcx
        # 1.1 query quanti
        df_quanti = query_quanti_data_to_df(data.mpi_test_id)
        if df_quanti.shape[0] != 1: raise Exception(f'พบผลการตรวจของรหัสผลตรวจ (mpi_tets_id) : {data.mpi_test_id} ไม่เท่ากับ 1 ผลตรวจ โปรดตรวจสอบและลองอีกครั้ง')

        # 1.2 query quali
        df_quali = pd.read_sql(f'''SELECT * FROM mpi_crop_img WHERE mpi_test_id = '{data.mpi_test_id}' ''', con_db)
        if df_quali.shape[0] != 1: raise Exception(f'พบผลการตรวจของรหัสผลตรวจ (mpi_tets_id) : {data.mpi_test_id} ไม่เท่ากับ 1 ผลตรวจ โปรดตรวจสอบและลองอีกครั้ง')
    
        # 2.1 prepare quanti
        quanti_features = pre_processing(df_quanti)

        # 2.2 prepare quali
        quali_img_data = load_img_array(df_quali)

        # 3.1 predict quanti
        indicator = "Adaptive_Quantitative"
        quanti_predict_data = predict_quantitative_model(quanti_features, indicator)

        # 3.2 predict quali
        quali_predict_data = predict_qualitative(quali_img_data, name='Adaptive')

        # 4. ensemble model max( quantitative score*base model acc, qualitative score*base model acc )
        predict_patient, predict_prob_patient = ensemble(quanti_predict_data['predict_prob_patient'], quanti_predict_data['predict_patient'], quali_predict_data['predict_prob_patient'], quali_predict_data['predict_patient'])
        predict_rca, predict_prob_rca = ensemble(quanti_predict_data['predict_prob_rca'], quanti_predict_data['predict_rca'], quali_predict_data['predict_prob_rca'], quali_predict_data['predict_rca'])
        predict_lad, predict_prob_lad = ensemble(quanti_predict_data['predict_prob_lad'], quanti_predict_data['predict_lad'], quali_predict_data['predict_prob_lad'], quali_predict_data['predict_lad'])
        predict_lcx, predict_prob_lcx = ensemble(quanti_predict_data['predict_prob_lcx'], quanti_predict_data['predict_lcx'], quali_predict_data['predict_prob_lcx'], quali_predict_data['predict_lcx'])
        all_predict_data = {
            "airflow_quantitative" : {
                "predict_rca" :         quanti_predict_data['predict_rca'],
                "predict_prob_rca":     quanti_predict_data['predict_prob_rca'],
                "predict_lad" :         quanti_predict_data['predict_lad'],
                "predict_prob_lad":     quanti_predict_data['predict_prob_lad'],
                "predict_lcx" :         quanti_predict_data['predict_lcx'],
                "predict_prob_lcx":     quanti_predict_data['predict_prob_lcx'],
                "predict_patient" :     quanti_predict_data['predict_patient'],
                "predict_prob_patient": quanti_predict_data['predict_prob_patient']
            },

            "airflow_qualitative": {
                "predict_rca" :         quali_predict_data['predict_rca'],
                "predict_prob_rca":     quali_predict_data['predict_prob_rca'],
                "predict_lad" :         quali_predict_data['predict_lad'],
                "predict_prob_lad":     quali_predict_data['predict_prob_lad'],
                "predict_lcx" :         quali_predict_data['predict_lcx'],
                "predict_prob_lcx":     quali_predict_data['predict_prob_lcx'],
                "predict_patient" :     quali_predict_data['predict_patient'],
                "predict_prob_patient": quali_predict_data['predict_prob_patient']
            },

            "airflow_hybrid" : {
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
        all_predict_data = prepare_to_update(data.ml_diag_id, predict_result=all_predict_data, inference_name='Adaptive_All')
                          
        # 6. add status
        all_predict_data['status'] = 'SUCCESS'

        # 7. return
        return all_predict_data
    
    except Exception as e:

        return {"status": "FAILURE", "detail": str(e)}