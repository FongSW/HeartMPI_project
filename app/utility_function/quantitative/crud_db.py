import pandas as pd
import numpy as np
from app.schema.patient_info import stress_quanti_schema, rest_quanti_schema, tpd_17_seg_schema, mpi_test_schema, ml_diag
from app.config.connection_db import con_db
from datetime import datetime


def check_mpi_test(hn, date_ext):
    """
    This function is used to check if an MPI test is saved in the database or not.
    """

    try:
        # 1. Query data from the mpi_test table
        query = f"SELECT hn_number, mpi_exam_date FROM mpi_test \
                 WHERE mpi_test.hn_number = '{hn}' AND mpi_test.mpi_exam_date = '{date_ext}' AND mpi_test.status != 'archived'"
        df_mpi_test = pd.read_sql(query, con_db)

        # 2. Check if the DataFrame is empty or not:
        if not df_mpi_test.empty:
            print(f'>>>>> Duplicate information hn: {hn}, date_ext: {date_ext}')
            raise Exception(f"รหัสประจำตัวผู้ป่วยและวันที่ตรวจ ซ้ำในฐานข้อมูล")

    except Exception as e:
        print(">>>>> Error Reason:", e)
        raise Exception(e)
    
def insert_extract_mpi_test_data(extract_df, confidence_df, mpi_test_id):

    """ This function is used to insert OCR extract data into the main database """

    # Create datetime
    date_now = datetime.now().strftime('%Y-%m-%d %X')

    # insert data each of table 
    save_stress_quanti(extract_df, confidence_df, mpi_test_id)
    save_rest_quanti(extract_df, confidence_df, mpi_test_id)
    save_tpd_17_seg(extract_df, confidence_df, mpi_test_id)
    update_date_mpi_test(extract_df.iloc[[0]].Date_MPI.values[0], mpi_test_id, date_now)

def query_quanti_data_to_df(mpi_test_id):
    """This function is used to query MPI test by mpi_test_id"""
    try:
        # Query data from tables stress_quanti, rest_quanti, mpi_test, tpd_17_seg (male, female)
        query_mpi_test = f"""
            SELECT mpi_test.*, tpd_17_seg.*, patient.gender
            FROM mpi_test
            INNER JOIN tpd_17_seg ON mpi_test.id = tpd_17_seg.mpi_test_id
            INNER JOIN patient ON mpi_test.hn_number = patient.hn_number
            WHERE mpi_test.id = '{str(mpi_test_id)}'
        """
        df_mpi_test = pd.read_sql(query_mpi_test, con_db).reset_index(drop=True)

        query_stress_quanti = f"""
            SELECT *
            FROM stress_quanti
            WHERE mpi_test_id = '{str(mpi_test_id)}'
        """
        df_stress_quanti = pd.read_sql(query_stress_quanti, con_db).reset_index(drop=True)

        query_rest_quanti = f"""
            SELECT *
            FROM rest_quanti
            WHERE mpi_test_id = '{str(mpi_test_id)}'
        """
        df_rest_quanti = pd.read_sql(query_rest_quanti, con_db).reset_index(drop=True)

        # Add prefix to table stress_quanti and rest_quanti
        df_stress_quanti.columns = ['s_' + str(col) for col in df_stress_quanti.columns]
        df_rest_quanti.columns = ['r_' + str(col) for col in df_rest_quanti.columns]

        # Concatenate df_quanti
        df_quanti = pd.concat([df_mpi_test, df_stress_quanti, df_rest_quanti], axis=1)

        # Define column names
        column_names = [
            "s_max_perfusion", "s_interval", "s_ed", "s_es", "s_lvef", "s_lad_perf_mean", "s_lad_perf_sd",
            "s_lcx_perf_mean", "s_lcx_perf_sd", "s_rca_perf_mean", "s_rca_perf_sd", "s_tot_perf_mean",
            "s_tot_perf_sd", "s_lad_wt_mean", "s_lad_wt_sd", "s_lcx_wt_mean", "s_lcx_wt_sd", "s_rca_wt_mean",
            "s_rca_wt_sd", "s_tot_wt_mean", "s_tot_wt_sd", "s_lad_wm_mean", "s_lad_wm_sd", "s_lcx_wm_mean",
            "s_lcx_wm_sd", "s_rca_wm_mean", "s_rca_wm_sd", "s_tot_wm_mean", "s_tot_wm_sd", "s_lad_perf_ext",
            "s_lcx_perf_ext", "s_rca_perf_ext", "s_tot_perf_ext", "s_lad_wt_ext", "s_lcx_wt_ext", "s_rca_wt_ext",
            "s_tot_wt_ext", "s_lad_wm_ext", "s_lcx_wm_ext", "s_rca_wm_ext", "s_tot_wm_ext", "s_lad_perf_sev",
            "s_lcx_perf_sev", "s_rca_perf_sev", "s_tot_perf_sev", "s_lad_wt_sev", "s_lcx_wt_sev", "s_rca_wt_sev",
            "s_tot_wt_sev", "s_lad_wm_sev", "s_lcx_wm_sev", "s_rca_wm_sev", "s_tot_wm_sev", "r_max_perfusion",
            "r_interval", "r_ed", "r_es", "r_lvef", "r_lad_perf_mean", "r_lad_perf_sd", "r_lcx_perf_mean",
            "r_lcx_perf_sd", "r_rca_perf_mean", "r_rca_perf_sd", "r_tot_perf_mean", "r_tot_perf_sd", "r_lad_wt_mean",
            "r_lad_wt_sd", "r_lcx_wt_mean", "r_lcx_wt_sd", "r_rca_wt_mean", "r_rca_wt_sd", "r_tot_wt_mean",
            "r_tot_wt_sd", "r_lad_wm_mean", "r_lad_wm_sd", "r_lcx_wm_mean", "r_lcx_wm_sd", "r_rca_wm_mean",
            "r_rca_wm_sd", "r_tot_wm_mean", "r_tot_wm_sd", "r_lad_perf_ext", "r_lcx_perf_ext", "r_rca_perf_ext",
            "r_tot_perf_ext", "r_lad_wt_ext", "r_lcx_wt_ext", "r_rca_wt_ext", "r_tot_wt_ext", "r_lad_wm_ext",
            "r_lcx_wm_ext", "r_rca_wm_ext", "r_tot_wm_ext", "r_lad_perf_sev", "r_lcx_perf_sev", "r_rca_perf_sev",
            "r_tot_perf_sev", "r_lad_wt_sev", "r_lcx_wt_sev", "r_rca_wt_sev", "r_tot_wt_sev", "r_lad_wm_sev",
            "r_lcx_wm_sev", "r_rca_wm_sev", "r_tot_wm_sev", "stress_sss", "stress_sts", 'stress_sms', 'rest_srs',
            'rest_sts', 'rest_sms', "age", "gender", "bmi", "dm", "ht", "dlp", "ckd"
        ]

        # Filter columns
        df_quanti = df_quanti[column_names]

        # Check for null values
        if df_quanti.isnull().values.any():
            null_cols = df_quanti.columns[df_quanti.isnull().sum() > 0].tolist()
            null_cols_str = ', '.join(null_cols)
            print(f'Found null value in column(s): {null_cols_str}')
            raise Exception("ไม่สามารถทำนาย เนื่องจากไม่มีข้อมูลครบ")
        else:
            print(df_quanti)
            return df_quanti

    except Exception as e:
        print("Can not query data. Reason:", e)
        raise Exception('ไม่สามารถทำนาย')

def save_stress_quanti(result_extract, result_confidence, mpi_test_id):
    result_extract.fillna(0, inplace=True)
    insert_data = stress_quanti_schema.insert().values(
        mpi_test_id = mpi_test_id, # stress_quanti_schema.iloc[[0]].date.values[0],

        max_perfusion = result_extract.iloc[[0]].S_MaxPerfusion.values[0],
        ocr_max_perfusion = result_extract.iloc[[0]].S_MaxPerfusion.values[0],
        ocr_clv_max_perfusion = result_confidence.iloc[[0]].S_MaxPerfusion.values[0],

        interval = result_extract.iloc[[0]].S_Intervals.values[0],
        ocr_interval = result_extract.iloc[[0]].S_Intervals.values[0],
        ocr_clv_interval = result_confidence.iloc[[0]].S_Intervals.values[0],

        es = result_extract.iloc[[0]].S_ES.values[0],
        ocr_es = result_extract.iloc[[0]].S_ES.values[0],
        ocr_clv_es = result_confidence.iloc[[0]].S_ES.values[0],

        ed = result_extract.iloc[[0]].S_ED.values[0],
        ocr_ed = result_extract.iloc[[0]].S_ED.values[0], 
        ocr_clv_ed = result_confidence.iloc[[0]].S_ED.values[0], 

        lvef = result_extract.iloc[[0]].S_EF.values[0],
        ocr_lvef = result_extract.iloc[[0]].S_EF.values[0],
        ocr_clv_lvef = result_confidence.iloc[[0]].S_EF.values[0],

        lad_perf_mean = result_extract.iloc[[0]].SM_LADPerfusion.values[0],
        ocr_lad_perf_mean = result_extract.iloc[[0]].SM_LADPerfusion.values[0],
        ocr_clv_lad_perf_mean = result_confidence.iloc[[0]].SM_LADPerfusion.values[0],

        lad_perf_sd = result_extract.iloc[[0]].SSD_LADPerfusion.values[0],
        ocr_lad_perf_sd = result_extract.iloc[[0]].SSD_LADPerfusion.values[0],
        ocr_clv_lad_perf_sd = result_confidence.iloc[[0]].SSD_LADPerfusion.values[0],

        lad_wt_mean = result_extract.iloc[[0]].SM_LADWallThickening.values[0],
        ocr_lad_wt_mean = result_extract.iloc[[0]].SM_LADWallThickening.values[0],
        ocr_clv_lad_wt_mean = result_confidence.iloc[[0]].SM_LADWallThickening.values[0],

        lad_wt_sd = result_extract.iloc[[0]].SSD_LADWallThickening.values[0],
        ocr_lad_wt_sd = result_extract.iloc[[0]].SSD_LADWallThickening.values[0],
        ocr_clv_lad_wt_sd = result_confidence.iloc[[0]].SSD_LADWallThickening.values[0], 

        lad_wm_mean = result_extract.iloc[[0]].SM_LADWallMotion.values[0],
        ocr_lad_wm_mean = result_extract.iloc[[0]].SM_LADWallMotion.values[0], 
        ocr_clv_lad_wm_mean = result_confidence.iloc[[0]].SM_LADWallMotion.values[0], 

        lad_wm_sd = result_extract.iloc[[0]].SSD_LADWallMotion.values[0],
        ocr_lad_wm_sd = result_extract.iloc[[0]].SSD_LADWallMotion.values[0], 
        ocr_clv_lad_wm_sd = result_confidence.iloc[[0]].SSD_LADWallMotion.values[0],

        lcx_perf_mean = result_extract.iloc[[0]].SM_LCXPerfusion.values[0], 
        ocr_lcx_perf_mean = result_extract.iloc[[0]].SM_LCXPerfusion.values[0], 
        ocr_clv_lcx_perf_mean = result_confidence.iloc[[0]].SM_LCXPerfusion.values[0], 

        lcx_perf_sd = result_extract.iloc[[0]].SSD_LCXPerfusion.values[0],
        ocr_lcx_perf_sd = result_extract.iloc[[0]].SSD_LCXPerfusion.values[0],
        ocr_clv_lcx_perf_sd = result_confidence.iloc[[0]].SSD_LCXPerfusion.values[0],

        lcx_wt_mean = result_extract.iloc[[0]].SM_LCXWallThickening.values[0],
        ocr_lcx_wt_mean = result_extract.iloc[[0]].SM_LCXWallThickening.values[0], 
        ocr_clv_lcx_wt_mean = result_confidence.iloc[[0]].SM_LCXWallThickening.values[0], 

        lcx_wt_sd = result_extract.iloc[[0]].SSD_LCXWallThickening.values[0],
        ocr_lcx_wt_sd = result_extract.iloc[[0]].SSD_LCXWallThickening.values[0],
        ocr_clv_lcx_wt_sd = result_confidence.iloc[[0]].SSD_LCXWallThickening.values[0],

        lcx_wm_mean = result_extract.iloc[[0]].SM_LCXWallMotion.values[0], 
        ocr_lcx_wm_mean = result_extract.iloc[[0]].SM_LCXWallMotion.values[0],
        ocr_clv_lcx_wm_mean = result_confidence.iloc[[0]].SM_LCXWallMotion.values[0], 

        lcx_wm_sd = result_extract.iloc[[0]].SSD_LCXWallMotion.values[0],
        ocr_lcx_wm_sd = result_extract.iloc[[0]].SSD_LCXWallMotion.values[0],
        ocr_clv_lcx_wm_sd = result_confidence.iloc[[0]].SSD_LCXWallMotion.values[0],


        rca_perf_mean = result_extract.iloc[[0]].SM_RCAPerfusion.values[0],
        ocr_rca_perf_mean = result_extract.iloc[[0]].SM_RCAPerfusion.values[0],
        ocr_clv_rca_perf_mean = result_confidence.iloc[[0]].SM_RCAPerfusion.values[0],

        rca_perf_sd = result_extract.iloc[[0]].SSD_RCAPerfusion.values[0],
        ocr_rca_perf_sd = result_extract.iloc[[0]].SSD_RCAPerfusion.values[0], 
        ocr_clv_rca_perf_sd = result_confidence.iloc[[0]].SSD_RCAPerfusion.values[0], 

        rca_wt_mean = result_extract.iloc[[0]].SM_RCAWallThickening.values[0],
        ocr_rca_wt_mean = result_extract.iloc[[0]].SM_RCAWallThickening.values[0], 
        ocr_clv_rca_wt_mean = result_confidence.iloc[[0]].SM_RCAWallThickening.values[0], 

        rca_wt_sd = result_extract.iloc[[0]].SSD_RCAWallThickening.values[0], 
        ocr_rca_wt_sd = result_extract.iloc[[0]].SSD_RCAWallThickening.values[0], 
        ocr_clv_rca_wt_sd = result_confidence.iloc[[0]].SSD_RCAWallThickening.values[0],

        rca_wm_mean = result_extract.iloc[[0]].SM_RCAWallMotion.values[0],
        ocr_rca_wm_mean = result_extract.iloc[[0]].SM_RCAWallMotion.values[0],
        ocr_clv_rca_wm_mean = result_confidence.iloc[[0]].SM_RCAWallMotion.values[0],

        rca_wm_sd = result_extract.iloc[[0]].SSD_RCAWallMotion.values[0], 
        ocr_rca_wm_sd = result_extract.iloc[[0]].SSD_RCAWallMotion.values[0], 
        ocr_clv_rca_wm_sd = result_confidence.iloc[[0]].SSD_RCAWallMotion.values[0], 

        tot_perf_mean = result_extract.iloc[[0]].SM_TOTPerfusion.values[0],
        ocr_tot_perf_mean = result_extract.iloc[[0]].SM_TOTPerfusion.values[0],
        ocr_clv_tot_perf_mean = result_confidence.iloc[[0]].SM_TOTPerfusion.values[0],

        tot_perf_sd = result_extract.iloc[[0]].SSD_TOTPerfusion.values[0],
        ocr_tot_perf_sd = result_extract.iloc[[0]].SSD_TOTPerfusion.values[0],
        ocr_clv_tot_perf_sd = result_confidence.iloc[[0]].SSD_TOTPerfusion.values[0],

        tot_wt_mean = result_extract.iloc[[0]].SM_TOTWallThickening.values[0],
        ocr_tot_wt_mean = result_extract.iloc[[0]].SM_TOTWallThickening.values[0],
        ocr_clv_tot_wt_mean = result_confidence.iloc[[0]].SM_TOTWallThickening.values[0], 

        tot_wt_sd = result_extract.iloc[[0]].SSD_TOTWallThickening.values[0],
        ocr_tot_wt_sd = result_extract.iloc[[0]].SSD_TOTWallThickening.values[0],
        ocr_clv_tot_wt_sd = result_confidence.iloc[[0]].SSD_TOTWallThickening.values[0],
  
        tot_wm_mean = result_extract.iloc[[0]].SM_TOTWallMotion.values[0],
        ocr_tot_wm_mean = result_extract.iloc[[0]].SM_TOTWallMotion.values[0],
        ocr_clv_tot_wm_mean = result_confidence.iloc[[0]].SM_TOTWallMotion.values[0],

        tot_wm_sd = result_extract.iloc[[0]].SSD_TOTWallMotion.values[0],
        ocr_tot_wm_sd = result_extract.iloc[[0]].SSD_TOTWallMotion.values[0], 
        ocr_clv_tot_wm_sd = result_confidence.iloc[[0]].SSD_TOTWallMotion.values[0],

        lad_perf_ext = result_extract.iloc[[0]].SE_LADPerfusion.values[0],
        ocr_lad_perf_ext = result_extract.iloc[[0]].SE_LADPerfusion.values[0],
        ocr_clv_lad_perf_ext = result_confidence.iloc[[0]].SE_LADPerfusion.values[0],

        lad_perf_sev = result_extract.iloc[[0]].SSEV_LADPerfusion.values[0],
        ocr_lad_perf_sev = result_extract.iloc[[0]].SSEV_LADPerfusion.values[0],
        ocr_clv_lad_perf_sev = result_confidence.iloc[[0]].SSEV_LADPerfusion.values[0],

        lad_wt_ext = result_extract.iloc[[0]].SE_LADWallThickening.values[0],
        ocr_lad_wt_ext = result_extract.iloc[[0]].SE_LADWallThickening.values[0],
        ocr_clv_lad_wt_ext = result_confidence.iloc[[0]].SE_LADWallThickening.values[0],

        lad_wt_sev = result_extract.iloc[[0]].SSEV_LADWallThickening.values[0],
        ocr_lad_wt_sev = result_extract.iloc[[0]].SSEV_LADWallThickening.values[0],
        ocr_clv_lad_wt_sev = result_confidence.iloc[[0]].SSEV_LADWallThickening.values[0], 

        lad_wm_ext = result_extract.iloc[[0]].SE_LADWallMotion.values[0],
        ocr_lad_wm_ext = result_extract.iloc[[0]].SE_LADWallMotion.values[0], 
        ocr_clv_lad_wm_ext = result_confidence.iloc[[0]].SE_LADWallMotion.values[0], 

        lad_wm_sev = result_extract.iloc[[0]].SSEV_LADWallMotion.values[0],
        ocr_lad_wm_sev = result_extract.iloc[[0]].SSEV_LADWallMotion.values[0], 
        ocr_clv_lad_wm_sev = result_confidence.iloc[[0]].SSEV_LADWallMotion.values[0],

        lcx_perf_ext = result_extract.iloc[[0]].SE_LCXPerfusion.values[0], 
        ocr_lcx_perf_ext = result_extract.iloc[[0]].SE_LCXPerfusion.values[0], 
        ocr_clv_lcx_perf_ext = result_confidence.iloc[[0]].SE_LCXPerfusion.values[0], 

        lcx_perf_sev = result_extract.iloc[[0]].SSEV_LCXPerfusion.values[0],
        ocr_lcx_perf_sev = result_extract.iloc[[0]].SSEV_LCXPerfusion.values[0],
        ocr_clv_lcx_perf_sev = result_confidence.iloc[[0]].SSEV_LCXPerfusion.values[0],

        lcx_wt_ext = result_extract.iloc[[0]].SE_LCXWallThickening.values[0],
        ocr_lcx_wt_ext = result_extract.iloc[[0]].SE_LCXWallThickening.values[0], 
        ocr_clv_lcx_wt_ext = result_confidence.iloc[[0]].SE_LCXWallThickening.values[0], 

        lcx_wt_sev = result_extract.iloc[[0]].SSEV_LCXWallThickening.values[0],
        ocr_lcx_wt_sev = result_extract.iloc[[0]].SSEV_LCXWallThickening.values[0],
        ocr_clv_lcx_wt_sev = result_confidence.iloc[[0]].SSEV_LCXWallThickening.values[0],

        lcx_wm_ext = result_extract.iloc[[0]].SE_LCXWallMotion.values[0], 
        ocr_lcx_wm_ext = result_extract.iloc[[0]].SE_LCXWallMotion.values[0],
        ocr_clv_lcx_wm_ext = result_confidence.iloc[[0]].SE_LCXWallMotion.values[0], 

        lcx_wm_sev = result_extract.iloc[[0]].SSEV_LCXWallMotion.values[0],
        ocr_lcx_wm_sev = result_extract.iloc[[0]].SSEV_LCXWallMotion.values[0],
        ocr_clv_lcx_wm_sev = result_confidence.iloc[[0]].SSEV_LCXWallMotion.values[0],
#
        rca_perf_ext = result_extract.iloc[[0]].SE_RCAPerfusion.values[0],
        ocr_rca_perf_ext = result_extract.iloc[[0]].SE_RCAPerfusion.values[0],
        ocr_clv_rca_perf_ext = result_confidence.iloc[[0]].SE_RCAPerfusion.values[0],

        rca_perf_sev = result_extract.iloc[[0]].SSEV_RCAPerfusion.values[0],
        ocr_rca_perf_sev = result_extract.iloc[[0]].SSEV_RCAPerfusion.values[0], 
        ocr_clv_rca_perf_sev = result_confidence.iloc[[0]].SSEV_RCAPerfusion.values[0], 

        rca_wt_ext = result_extract.iloc[[0]].SE_RCAWallThickening.values[0],
        ocr_rca_wt_ext = result_extract.iloc[[0]].SE_RCAWallThickening.values[0], 
        ocr_clv_rca_wt_ext = result_confidence.iloc[[0]].SE_RCAWallThickening.values[0], 

        rca_wt_sev = result_extract.iloc[[0]].SSEV_RCAWallThickening.values[0], 
        ocr_rca_wt_sev = result_extract.iloc[[0]].SSEV_RCAWallThickening.values[0], 
        ocr_clv_rca_wt_sev = result_confidence.iloc[[0]].SSEV_RCAWallThickening.values[0],

        rca_wm_ext = result_extract.iloc[[0]].SE_RCAWallMotion.values[0],
        ocr_rca_wm_ext = result_extract.iloc[[0]].SE_RCAWallMotion.values[0],
        ocr_clv_rca_wm_ext = result_confidence.iloc[[0]].SE_RCAWallMotion.values[0],

        rca_wm_sev = result_extract.iloc[[0]].SSEV_RCAWallMotion.values[0], 
        ocr_rca_wm_sev = result_extract.iloc[[0]].SSEV_RCAWallMotion.values[0], 
        ocr_clv_rca_wm_sev = result_confidence.iloc[[0]].SSEV_RCAWallMotion.values[0], 
        
        tot_perf_ext = result_extract.iloc[[0]].SE_TOTPerfusion.values[0],
        ocr_tot_perf_ext = result_extract.iloc[[0]].SE_TOTPerfusion.values[0],
        ocr_clv_tot_perf_ext = result_confidence.iloc[[0]].SE_TOTPerfusion.values[0],

        tot_perf_sev = result_extract.iloc[[0]].SSEV_TOTPerfusion.values[0],
        ocr_tot_perf_sev = result_extract.iloc[[0]].SSEV_TOTPerfusion.values[0],
        ocr_clv_tot_perf_sev = result_confidence.iloc[[0]].SSEV_TOTPerfusion.values[0],

        tot_wt_ext = result_extract.iloc[[0]].SE_TOTWallThickening.values[0],
        ocr_tot_wt_ext = result_extract.iloc[[0]].SE_TOTWallThickening.values[0],
        ocr_clv_tot_wt_ext = result_confidence.iloc[[0]].SE_TOTWallThickening.values[0], 

        tot_wt_sev = result_extract.iloc[[0]].SSEV_TOTWallThickening.values[0],
        ocr_tot_wt_sev = result_extract.iloc[[0]].SSEV_TOTWallThickening.values[0],
        ocr_clv_tot_wt_sev = result_confidence.iloc[[0]].SSEV_TOTWallThickening.values[0],
  
        tot_wm_ext = result_extract.iloc[[0]].SE_TOTWallMotion.values[0],
        ocr_tot_wm_ext = result_extract.iloc[[0]].SE_TOTWallMotion.values[0],
        ocr_clv_tot_wm_ext = result_confidence.iloc[[0]].SE_TOTWallMotion.values[0],

        tot_wm_sev = result_extract.iloc[[0]].SSEV_TOTWallMotion.values[0],
        ocr_tot_wm_sev = result_extract.iloc[[0]].SSEV_TOTWallMotion.values[0], 
        ocr_clv_tot_wm_sev = result_confidence.iloc[[0]].SSEV_TOTWallMotion.values[0],
    )  
    # execute
    con_db.execute(insert_data)
    print("The inserted data stress_quanti table was successful.")

def save_rest_quanti(result_extract, result_confidence, mpi_test_id):
    result_extract.fillna(0, inplace=True)
    insert_data = rest_quanti_schema.insert().values(
        mpi_test_id = mpi_test_id, # stress_quanti_schema.iloc[[0]].date.values[0],

        max_perfusion = result_extract.iloc[[0]].R_MaxPerfusion.values[0],
        ocr_max_perfusion = result_extract.iloc[[0]].R_MaxPerfusion.values[0],
        ocr_clv_max_perfusion = result_confidence.iloc[[0]].R_MaxPerfusion.values[0],

        interval = result_extract.iloc[[0]].R_Intervals.values[0],
        ocr_interval = result_extract.iloc[[0]].R_Intervals.values[0],
        ocr_clv_interval = result_confidence.iloc[[0]].R_Intervals.values[0],

        es = result_extract.iloc[[0]].R_ES.values[0],
        ocr_es = result_extract.iloc[[0]].R_ES.values[0],
        ocr_clv_es = result_confidence.iloc[[0]].R_ES.values[0],

        ed = result_extract.iloc[[0]].R_ED.values[0],
        ocr_ed = result_extract.iloc[[0]].R_ED.values[0], 
        ocr_clv_ed = result_confidence.iloc[[0]].R_ED.values[0], 

        lvef = result_extract.iloc[[0]].R_EF.values[0],
        ocr_lvef = result_extract.iloc[[0]].R_EF.values[0],
        ocr_clv_lvef = result_confidence.iloc[[0]].R_EF.values[0],

        lad_perf_mean = result_extract.iloc[[0]].RM_LADPerfusion.values[0],
        ocr_lad_perf_mean = result_extract.iloc[[0]].RM_LADPerfusion.values[0],
        ocr_clv_lad_perf_mean = result_confidence.iloc[[0]].RM_LADPerfusion.values[0],

        lad_perf_sd = result_extract.iloc[[0]].RSD_LADPerfusion.values[0],
        ocr_lad_perf_sd = result_extract.iloc[[0]].RSD_LADPerfusion.values[0],
        ocr_clv_lad_perf_sd = result_confidence.iloc[[0]].RSD_LADPerfusion.values[0],

        lad_wt_mean = result_extract.iloc[[0]].RM_LADWallThickening.values[0],
        ocr_lad_wt_mean = result_extract.iloc[[0]].RM_LADWallThickening.values[0],
        ocr_clv_lad_wt_mean = result_confidence.iloc[[0]].RM_LADWallThickening.values[0],

        lad_wt_sd = result_extract.iloc[[0]].RSD_LADWallThickening.values[0],
        ocr_lad_wt_sd = result_extract.iloc[[0]].RSD_LADWallThickening.values[0],
        ocr_clv_lad_wt_sd = result_confidence.iloc[[0]].RSD_LADWallThickening.values[0], 

        lad_wm_mean = result_extract.iloc[[0]].RM_LADWallMotion.values[0],
        ocr_lad_wm_mean = result_extract.iloc[[0]].RM_LADWallMotion.values[0], 
        ocr_clv_lad_wm_mean = result_confidence.iloc[[0]].RM_LADWallMotion.values[0], 

        lad_wm_sd = result_extract.iloc[[0]].RSD_LADWallMotion.values[0],
        ocr_lad_wm_sd = result_extract.iloc[[0]].RSD_LADWallMotion.values[0], 
        ocr_clv_lad_wm_sd = result_confidence.iloc[[0]].RSD_LADWallMotion.values[0],

        lcx_perf_mean = result_extract.iloc[[0]].RM_LCXPerfusion.values[0], 
        ocr_lcx_perf_mean = result_extract.iloc[[0]].RM_LCXPerfusion.values[0], 
        ocr_clv_lcx_perf_mean = result_confidence.iloc[[0]].RM_LCXPerfusion.values[0], 

        lcx_perf_sd = result_extract.iloc[[0]].RSD_LCXPerfusion.values[0],
        ocr_lcx_perf_sd = result_extract.iloc[[0]].RSD_LCXPerfusion.values[0],
        ocr_clv_lcx_perf_sd = result_confidence.iloc[[0]].RSD_LCXPerfusion.values[0],

        lcx_wt_mean = result_extract.iloc[[0]].RM_LCXWallThickening.values[0],
        ocr_lcx_wt_mean = result_extract.iloc[[0]].RM_LCXWallThickening.values[0], 
        ocr_clv_lcx_wt_mean = result_confidence.iloc[[0]].RM_LCXWallThickening.values[0], 

        lcx_wt_sd = result_extract.iloc[[0]].RSD_LCXWallThickening.values[0],
        ocr_lcx_wt_sd = result_extract.iloc[[0]].RSD_LCXWallThickening.values[0],
        ocr_clv_lcx_wt_sd = result_confidence.iloc[[0]].RSD_LCXWallThickening.values[0],

        lcx_wm_mean = result_extract.iloc[[0]].RM_LCXWallMotion.values[0], 
        ocr_lcx_wm_mean = result_extract.iloc[[0]].RM_LCXWallMotion.values[0],
        ocr_clv_lcx_wm_mean = result_confidence.iloc[[0]].RM_LCXWallMotion.values[0], 

        lcx_wm_sd = result_extract.iloc[[0]].RSD_LCXWallMotion.values[0],
        ocr_lcx_wm_sd = result_extract.iloc[[0]].RSD_LCXWallMotion.values[0],
        ocr_clv_lcx_wm_sd = result_confidence.iloc[[0]].RSD_LCXWallMotion.values[0],


        rca_perf_mean = result_extract.iloc[[0]].RM_RCAPerfusion.values[0],
        ocr_rca_perf_mean = result_extract.iloc[[0]].RM_RCAPerfusion.values[0],
        ocr_clv_rca_perf_mean = result_confidence.iloc[[0]].RM_RCAPerfusion.values[0],

        rca_perf_sd = result_extract.iloc[[0]].RSD_RCAPerfusion.values[0],
        ocr_rca_perf_sd = result_extract.iloc[[0]].RSD_RCAPerfusion.values[0], 
        ocr_clv_rca_perf_sd = result_confidence.iloc[[0]].RSD_RCAPerfusion.values[0], 

        rca_wt_mean = result_extract.iloc[[0]].RM_RCAWallThickening.values[0],
        ocr_rca_wt_mean = result_extract.iloc[[0]].RM_RCAWallThickening.values[0], 
        ocr_clv_rca_wt_mean = result_confidence.iloc[[0]].RM_RCAWallThickening.values[0], 

        rca_wt_sd = result_extract.iloc[[0]].RSD_RCAWallThickening.values[0], 
        ocr_rca_wt_sd = result_extract.iloc[[0]].RSD_RCAWallThickening.values[0], 
        ocr_clv_rca_wt_sd = result_confidence.iloc[[0]].RSD_RCAWallThickening.values[0],

        rca_wm_mean = result_extract.iloc[[0]].RM_RCAWallMotion.values[0],
        ocr_rca_wm_mean = result_extract.iloc[[0]].RM_RCAWallMotion.values[0],
        ocr_clv_rca_wm_mean = result_confidence.iloc[[0]].RM_RCAWallMotion.values[0],

        rca_wm_sd = result_extract.iloc[[0]].RSD_RCAWallMotion.values[0], 
        ocr_rca_wm_sd = result_extract.iloc[[0]].RSD_RCAWallMotion.values[0], 
        ocr_clv_rca_wm_sd = result_confidence.iloc[[0]].RSD_RCAWallMotion.values[0], 

        tot_perf_mean = result_extract.iloc[[0]].RM_TOTPerfusion.values[0],
        ocr_tot_perf_mean = result_extract.iloc[[0]].RM_TOTPerfusion.values[0],
        ocr_clv_tot_perf_mean = result_confidence.iloc[[0]].RM_TOTPerfusion.values[0],

        tot_perf_sd = result_extract.iloc[[0]].RSD_TOTPerfusion.values[0],
        ocr_tot_perf_sd = result_extract.iloc[[0]].RSD_TOTPerfusion.values[0],
        ocr_clv_tot_perf_sd = result_confidence.iloc[[0]].RSD_TOTPerfusion.values[0],

        tot_wt_mean = result_extract.iloc[[0]].RM_TOTWallThickening.values[0],
        ocr_tot_wt_mean = result_extract.iloc[[0]].RM_TOTWallThickening.values[0],
        ocr_clv_tot_wt_mean = result_confidence.iloc[[0]].RM_TOTWallThickening.values[0], 

        tot_wt_sd = result_extract.iloc[[0]].RSD_TOTWallThickening.values[0],
        ocr_tot_wt_sd = result_extract.iloc[[0]].RSD_TOTWallThickening.values[0],
        ocr_clv_tot_wt_sd = result_confidence.iloc[[0]].RSD_TOTWallThickening.values[0],
  
        tot_wm_mean = result_extract.iloc[[0]].RM_TOTWallMotion.values[0],
        ocr_tot_wm_mean = result_extract.iloc[[0]].RM_TOTWallMotion.values[0],
        ocr_clv_tot_wm_mean = result_confidence.iloc[[0]].RM_TOTWallMotion.values[0],

        tot_wm_sd = result_extract.iloc[[0]].RSD_TOTWallMotion.values[0],
        ocr_tot_wm_sd = result_extract.iloc[[0]].RSD_TOTWallMotion.values[0], 
        ocr_clv_tot_wm_sd = result_confidence.iloc[[0]].RSD_TOTWallMotion.values[0],

        lad_perf_ext = result_extract.iloc[[0]].RE_LADPerfusion.values[0],
        ocr_lad_perf_ext = result_extract.iloc[[0]].RE_LADPerfusion.values[0],
        ocr_clv_lad_perf_ext = result_confidence.iloc[[0]].RE_LADPerfusion.values[0],

        lad_perf_sev = result_extract.iloc[[0]].RSEV_LADPerfusion.values[0],
        ocr_lad_perf_sev = result_extract.iloc[[0]].RSEV_LADPerfusion.values[0],
        ocr_clv_lad_perf_sev = result_confidence.iloc[[0]].RSEV_LADPerfusion.values[0],

        lad_wt_ext = result_extract.iloc[[0]].RE_LADWallThickening.values[0],
        ocr_lad_wt_ext = result_extract.iloc[[0]].RE_LADWallThickening.values[0],
        ocr_clv_lad_wt_ext = result_confidence.iloc[[0]].RE_LADWallThickening.values[0],

        lad_wt_sev = result_extract.iloc[[0]].RSEV_LADWallThickening.values[0],
        ocr_lad_wt_sev = result_extract.iloc[[0]].RSEV_LADWallThickening.values[0],
        ocr_clv_lad_wt_sev = result_confidence.iloc[[0]].RSEV_LADWallThickening.values[0], 

        lad_wm_ext = result_extract.iloc[[0]].RE_LADWallMotion.values[0],
        ocr_lad_wm_ext = result_extract.iloc[[0]].RE_LADWallMotion.values[0], 
        ocr_clv_lad_wm_ext = result_confidence.iloc[[0]].RE_LADWallMotion.values[0], 

        lad_wm_sev = result_extract.iloc[[0]].RSEV_LADWallMotion.values[0],
        ocr_lad_wm_sev = result_extract.iloc[[0]].RSEV_LADWallMotion.values[0], 
        ocr_clv_lad_wm_sev = result_confidence.iloc[[0]].RSEV_LADWallMotion.values[0],

        lcx_perf_ext = result_extract.iloc[[0]].RE_LCXPerfusion.values[0], 
        ocr_lcx_perf_ext = result_extract.iloc[[0]].RE_LCXPerfusion.values[0], 
        ocr_clv_lcx_perf_ext = result_confidence.iloc[[0]].RE_LCXPerfusion.values[0], 

        lcx_perf_sev = result_extract.iloc[[0]].RSEV_LCXPerfusion.values[0],
        ocr_lcx_perf_sev = result_extract.iloc[[0]].RSEV_LCXPerfusion.values[0],
        ocr_clv_lcx_perf_sev = result_confidence.iloc[[0]].RSEV_LCXPerfusion.values[0],

        lcx_wt_ext = result_extract.iloc[[0]].RE_LCXWallThickening.values[0],
        ocr_lcx_wt_ext = result_extract.iloc[[0]].RE_LCXWallThickening.values[0], 
        ocr_clv_lcx_wt_ext = result_confidence.iloc[[0]].RE_LCXWallThickening.values[0], 

        lcx_wt_sev = result_extract.iloc[[0]].RSEV_LCXWallThickening.values[0],
        ocr_lcx_wt_sev = result_extract.iloc[[0]].RSEV_LCXWallThickening.values[0],
        ocr_clv_lcx_wt_sev = result_confidence.iloc[[0]].RSEV_LCXWallThickening.values[0],

        lcx_wm_ext = result_extract.iloc[[0]].RE_LCXWallMotion.values[0], 
        ocr_lcx_wm_ext = result_extract.iloc[[0]].RE_LCXWallMotion.values[0],
        ocr_clv_lcx_wm_ext = result_confidence.iloc[[0]].RE_LCXWallMotion.values[0], 

        lcx_wm_sev = result_extract.iloc[[0]].RSEV_LCXWallMotion.values[0],
        ocr_lcx_wm_sev = result_extract.iloc[[0]].RSEV_LCXWallMotion.values[0],
        ocr_clv_lcx_wm_sev = result_confidence.iloc[[0]].RSEV_LCXWallMotion.values[0],
#
        rca_perf_ext = result_extract.iloc[[0]].RE_RCAPerfusion.values[0],
        ocr_rca_perf_ext = result_extract.iloc[[0]].RE_RCAPerfusion.values[0],
        ocr_clv_rca_perf_ext = result_confidence.iloc[[0]].RE_RCAPerfusion.values[0],

        rca_perf_sev = result_extract.iloc[[0]].RSEV_RCAPerfusion.values[0],
        ocr_rca_perf_sev = result_extract.iloc[[0]].RSEV_RCAPerfusion.values[0], 
        ocr_clv_rca_perf_sev = result_confidence.iloc[[0]].RSEV_RCAPerfusion.values[0], 

        rca_wt_ext = result_extract.iloc[[0]].RE_RCAWallThickening.values[0],
        ocr_rca_wt_ext = result_extract.iloc[[0]].RE_RCAWallThickening.values[0], 
        ocr_clv_rca_wt_ext = result_confidence.iloc[[0]].RE_RCAWallThickening.values[0], 

        rca_wt_sev = result_extract.iloc[[0]].RSEV_RCAWallThickening.values[0], 
        ocr_rca_wt_sev = result_extract.iloc[[0]].RSEV_RCAWallThickening.values[0], 
        ocr_clv_rca_wt_sev = result_confidence.iloc[[0]].RSEV_RCAWallThickening.values[0],

        rca_wm_ext = result_extract.iloc[[0]].RE_RCAWallMotion.values[0],
        ocr_rca_wm_ext = result_extract.iloc[[0]].RE_RCAWallMotion.values[0],
        ocr_clv_rca_wm_ext = result_confidence.iloc[[0]].RE_RCAWallMotion.values[0],

        rca_wm_sev = result_extract.iloc[[0]].RSEV_RCAWallMotion.values[0], 
        ocr_rca_wm_sev = result_extract.iloc[[0]].RSEV_RCAWallMotion.values[0], 
        ocr_clv_rca_wm_sev = result_confidence.iloc[[0]].RSEV_RCAWallMotion.values[0], 
        
        tot_perf_ext = result_extract.iloc[[0]].RE_TOTPerfusion.values[0],
        ocr_tot_perf_ext = result_extract.iloc[[0]].RE_TOTPerfusion.values[0],
        ocr_clv_tot_perf_ext = result_confidence.iloc[[0]].RE_TOTPerfusion.values[0],

        tot_perf_sev = result_extract.iloc[[0]].RSEV_TOTPerfusion.values[0],
        ocr_tot_perf_sev = result_extract.iloc[[0]].RSEV_TOTPerfusion.values[0],
        ocr_clv_tot_perf_sev = result_confidence.iloc[[0]].RSEV_TOTPerfusion.values[0],

        tot_wt_ext = result_extract.iloc[[0]].RE_TOTWallThickening.values[0],
        ocr_tot_wt_ext = result_extract.iloc[[0]].RE_TOTWallThickening.values[0],
        ocr_clv_tot_wt_ext = result_confidence.iloc[[0]].RE_TOTWallThickening.values[0], 

        tot_wt_sev = result_extract.iloc[[0]].RSEV_TOTWallThickening.values[0],
        ocr_tot_wt_sev = result_extract.iloc[[0]].RSEV_TOTWallThickening.values[0],
        ocr_clv_tot_wt_sev = result_confidence.iloc[[0]].RSEV_TOTWallThickening.values[0],
  
        tot_wm_ext = result_extract.iloc[[0]].RE_TOTWallMotion.values[0],
        ocr_tot_wm_ext = result_extract.iloc[[0]].RE_TOTWallMotion.values[0],
        ocr_clv_tot_wm_ext = result_confidence.iloc[[0]].RE_TOTWallMotion.values[0],

        tot_wm_sev = result_extract.iloc[[0]].RSEV_TOTWallMotion.values[0],
        ocr_tot_wm_sev = result_extract.iloc[[0]].RSEV_TOTWallMotion.values[0], 
        ocr_clv_tot_wm_sev = result_confidence.iloc[[0]].RSEV_TOTWallMotion.values[0],
    )  
    # execute
    con_db.execute(insert_data)
    print("The inserted data in rest_quanti table was successful.")

def save_tpd_17_seg(result_extract, result_confidence, mpi_test_id):
    result_extract.fillna(0, inplace=True)
    insert_data = tpd_17_seg_schema.insert().values(
        mpi_test_id = mpi_test_id, # stress_quanti_schema.iloc[[0]].date.values[0],

        stress_sss = result_extract.iloc[[0]].SSS.values[0],
        ocr_stress_sss = result_extract.iloc[[0]].SSS.values[0],
        ocr_clv_stress_sss = result_confidence.iloc[[0]].SSS.values[0],

        stress_sts = result_extract.iloc[[0]].S_STS.values[0],
        ocr_stress_sts = result_extract.iloc[[0]].S_STS.values[0],
        ocr_clv_stress_sts = result_confidence.iloc[[0]].S_STS.values[0],

        stress_sms = result_extract.iloc[[0]].S_SMS.values[0],
        ocr_stress_sms = result_extract.iloc[[0]].S_SMS.values[0],
        ocr_clv_stress_sms = result_confidence.iloc[[0]].S_SMS.values[0],

        rest_srs = result_extract.iloc[[0]].SRS.values[0],
        ocr_rest_srs = result_extract.iloc[[0]].SRS.values[0],
        ocr_clv_rest_srs = result_confidence.iloc[[0]].SRS.values[0],

        rest_sts = result_extract.iloc[[0]].R_STS.values[0],
        ocr_rest_sts = result_extract.iloc[[0]].R_STS.values[0],
        ocr_clv_rest_sts = result_confidence.iloc[[0]].R_STS.values[0],

        rest_sms = result_extract.iloc[[0]].R_SMS.values[0],
        ocr_rest_sms = result_extract.iloc[[0]].R_SMS.values[0],
        ocr_clv_rest_sms = result_confidence.iloc[[0]].R_SMS.values[0],
    )
    # execute
    con_db.execute(insert_data)
    print("The inserted data in tpd_17_seg table was successful.")

def update_date_mpi_test(date, mpi_test_id, date_now):
    condition = mpi_test_schema.c.id == int(mpi_test_id)
    update_data = mpi_test_schema.update().where(condition).values(mpi_exam_date = str(date), updated_at = date_now)

    # execute
    con_db.execute(update_data)
    print("The updated mpi_exam_date was successful.")

def update_status_mpi_test(mpi_test_id, date_now):
    condition = mpi_test_schema.c.id == int(mpi_test_id)
    update_data = mpi_test_schema.update().where(condition).values(status = "failed", updated_at = date_now)

    # execute
    con_db.execute(update_data)
    print("The updated mpi_exam_date was successful.")

def insert_result_prediction(series_result_predict):
    insert_data = ml_diag.insert().values(
        mpi_test_id = series_result_predict.mpi_test_id,
        ml_model_id = series_result_predict.ml_model_id,
        lad_predict = series_result_predict.predict_lad,
        lcx_predict = series_result_predict.predict_lcx,
        rca_predict = series_result_predict.predict_rca,
        patient_predict = series_result_predict.predict_patient,
        lad_predict_proba = series_result_predict.predict_prob_lad,
        lcx_predict_proba = series_result_predict.predict_prob_lcx,
        rca_predict_proba = series_result_predict.predict_prob_rca,
        patient_predict_proba = series_result_predict.predict_prob_patient,
        created_at = series_result_predict.created_at,
        updated_at = series_result_predict.created_at,
        updated_by = series_result_predict.updated_by,
    )
    # execute
    con_db.execute(insert_data)
    print("The inserted result prediction was successful.")


