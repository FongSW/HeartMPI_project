from ast import Bytes
import enum
from sqlalchemy import Integer, String, Float, DateTime, Table, Column, Boolean, Identity, Date, Text, TIMESTAMP, Enum, JSON
from app.config.connection_db import meta

feature_extraction_schema = Table(
    'feature_extraction_info', meta,
    Column('pid', Integer, Identity(start=1, cycle=True), primary_key=True),
    Column('HN', String),
    Column('date', Date),
    Column('path_file', String),
    Column('created_by', Integer),
    Column('created_at', DateTime),
    Column('updated_by', Integer),
    Column('updated_at', DateTime),
    Column('age', Integer),
    Column('gender', String),
    Column('BMI', Float(8, 3)),
    Column('DM', Integer),
    Column('HT', Integer),
    Column('DLP', Integer),
    Column('CKD', Integer),    
    Column('S_MaxPerfusion', Float(8, 3)),
    Column('S_Intervals', Integer),
    Column('S_ED', Integer),
    Column('S_ES', Integer),
    Column('S_EF', Integer),

    Column('SM_LADPerfusion', Float(8, 3)),
    Column('SSD_LADPerfusion', Float(8, 3)),
    Column('SM_LCXPerfusion', Float(8, 3)),
    Column('SSD_LCXPerfusion', Float(8, 3)),
    Column('SM_RCAPerfusion', Float(8, 3)),
    Column('SSD_RCAPerfusion', Float(8, 3)),
    Column('SM_TOTPerfusion', Float(8, 3)),
    Column('SSD_TOTPerfusion', Float(8, 3)),
    Column('SM_LADWallThickening', Float(8, 3)),
    Column('SSD_LADWallThickening', Float(8, 3)),
    Column('SM_LCXWallThickening', Float(8, 3)),
    Column('SSD_LCXWallThickening', Float(8, 3)),
    Column('SM_RCAWallThickening', Float(8, 3)),
    Column('SSD_RCAWallThickening', Float(8, 3)),
    Column('SM_TOTWallThickening', Float(8, 3)),
    Column('SSD_TOTWallThickening', Float(8, 3)),
    Column('SM_LADWallMotion', Float(8, 3)),
    Column('SSD_LADWallMotion', Float(8, 3)),
    Column('SM_LCXWallMotion', Float(8, 3)),
    Column('SSD_LCXWallMotion', Float(8, 3)),
    Column('SM_RCAWallMotion', Float(8, 3)),
    Column('SSD_RCAWallMotion', Float(8, 3)),
    Column('SM_TOTWallMotion', Float(8, 3)),
    Column('SSD_TOTWallMotion', Float(8, 3)),

    Column('SE_LADPerfusion', Integer),
    Column('SE_LCXPerfusion', Integer),       
    Column('SE_RCAPerfusion', Integer),
    Column('SE_TOTPerfusion', Integer),
    Column('SE_LADWallThickening', Integer),
    Column('SE_LCXWallThickening', Integer),
    Column('SE_RCAWallThickening', Integer),
    Column('SE_TOTWallThickening', Integer),
    Column('SE_LADWallMotion', Integer),
    Column('SE_LCXWallMotion', Integer),
    Column('SE_RCAWallMotion', Integer),
    Column('SE_TOTWallMotion', Integer),

    Column('SSEV_LADPerfusion', Float(8, 3)),
    Column('SSEV_LCXPerfusion', Float(8, 3)),       
    Column('SSEV_RCAPerfusion', Float(8, 3)),
    Column('SSEV_TOTPerfusion', Float(8, 3)),
    Column('SSEV_LADWallThickening', Float(8, 3)),
    Column('SSEV_LCXWallThickening', Float(8, 3)),
    Column('SSEV_RCAWallThickening', Float(8, 3)),
    Column('SSEV_TOTWallThickening', Float(8, 3)),
    Column('SSEV_LADWallMotion', Float(8, 3)),
    Column('SSEV_LCXWallMotion', Float(8, 3)),
    Column('SSEV_RCAWallMotion', Float(8, 3)),
    Column('SSEV_TOTWallMotion', Float(8, 3)),

    Column('R_MaxPerfusion', Float(8, 3)),
    Column('R_Intervals', Integer),
    Column('R_ED', Integer),
    Column('R_ES', Integer),
    Column('R_EF', Integer),

    Column('RM_LADPerfusion', Float(8, 3)),
    Column('RSD_LADPerfusion', Float(8, 3)),
    Column('RM_LCXPerfusion', Float(8, 3)),
    Column('RSD_LCXPerfusion', Float(8, 3)),   
    Column('RM_RCAPerfusion', Float(8, 3)),
    Column('RSD_RCAPerfusion', Float(8, 3)),
    Column('RM_TOTPerfusion', Float(8, 3)),
    Column('RSD_TOTPerfusion', Float(8, 3)),

    Column('RM_LADWallThickening', Float(8, 3)),
    Column('RSD_LADWallThickening', Float(8, 3)),

    Column('RM_LCXWallThickening', Float(8, 3)),
    Column('RSD_LCXWallThickening', Float(8, 3)),

    Column('RM_RCAWallThickening', Float(8, 3)),
    Column('RSD_RCAWallThickening', Float(8, 3)),

    Column('RM_TOTWallThickening', Float(8, 3)),
    Column('RSD_TOTWallThickening', Float(8, 3)),

    Column('RM_LADWallMotion', Float(8, 3)),
    Column('RSD_LADWallMotion', Float(8, 3)),

    Column('RM_LCXWallMotion', Float(8, 3)),
    Column('RSD_LCXWallMotion', Float(8, 3)),

    Column('RM_RCAWallMotion', Float(8, 3)),
    Column('RSD_RCAWallMotion', Float(8, 3)),

    Column('RM_TOTWallMotion', Float(8, 3)),
    Column('RSD_TOTWallMotion', Float(8, 3)),

    Column('RE_LADPerfusion', Integer),      
    Column('RE_LCXPerfusion', Integer),
    Column('RE_RCAPerfusion', Integer),
    Column('RE_TOTPerfusion', Integer),
    Column('RE_LADWallThickening', Integer),
    Column('RE_LCXWallThickening', Integer),
    Column('RE_RCAWallThickening', Integer),
    Column('RE_TOTWallThickening', Integer),
    Column('RE_LADWallMotion', Integer),
    Column('RE_LCXWallMotion', Integer),
    Column('RE_RCAWallMotion', Integer),
    Column('RE_TOTWallMotion', Integer),

    Column('RSEV_LADPerfusion', Float(8, 3)),      
    Column('RSEV_LCXPerfusion', Float(8, 3)),
    Column('RSEV_RCAPerfusion', Float(8, 3)),
    Column('RSEV_TOTPerfusion', Float(8, 3)),
    Column('RSEV_LADWallThickening', Float(8, 3)),
    Column('RSEV_LCXWallThickening', Float(8, 3)),
    Column('RSEV_RCAWallThickening', Float(8, 3)),
    Column('RSEV_TOTWallThickening', Float(8, 3)),
    Column('RSEV_LADWallMotion', Float(8, 3)),
    Column('RSEV_LCXWallMotion', Float(8, 3)),
    Column('RSEV_RCAWallMotion', Float(8, 3)),
    Column('RSEV_TOTWallMotion', Float(8, 3)),

    Column('SSS', Integer),
    Column('S_STS', Integer),       
    Column('S_SMS', Integer),
    Column('SRS', Integer),
    Column('R_STS', Integer),
    Column('R_SMS', Integer),
    Column('R_SMS', Integer),  
)

stress_quanti_schema = Table(
    'stress_quanti', meta,
    Column('id', Integer, Identity(start=1, cycle=True), primary_key=True),
    Column('mpi_test_id', Integer),

    Column('max_perfusion', Float(4, 2)),
    Column('ocr_max_perfusion', Float(4, 2)),
    Column('ocr_clv_max_perfusion', Float(4, 2)),  
    Column('interval', Float(4, 2)),
    Column('ocr_interval', Float(4, 2)),
    Column('ocr_clv_interval', Float(4, 2)),

    Column('es', Float(4, 2)),
    Column('ocr_es', Float(4, 2)),
    Column('ocr_clv_es', Float(4, 2)),

    Column('ed', Float(4, 2)),
    Column('ocr_ed', Float(4, 2)), 
    Column('ocr_clv_ed', Float(4, 2)), 

    Column('lvef', Float(4, 2)),
    Column('ocr_lvef', Float(4, 2)),
    Column('ocr_clv_lvef', Float(4, 2)),

    Column('lad_perf_mean', Float(4, 2)),
    Column('ocr_lad_perf_mean', Float(4, 2)),
    Column('ocr_clv_lad_perf_mean', Float(4, 2)),

    Column('lad_perf_sd', Float(4, 2)),
    Column('ocr_lad_perf_sd', Float(4, 2)),
    Column('ocr_clv_lad_perf_sd', Float(4, 2)),

    Column('lad_wt_mean', Float(4, 2)),
    Column('ocr_lad_wt_mean', Float(4, 2)),
    Column('ocr_clv_lad_wt_mean', Float(4, 2)),

    Column('lad_wt_sd', Float(4, 2)),
    Column('ocr_lad_wt_sd', Float(4, 2)),
    Column('ocr_clv_lad_wt_sd', Float(4, 2)), 

    Column('lad_wm_mean', Float(4, 2)),
    Column('ocr_lad_wm_mean', Float(4, 2)), 
    Column('ocr_clv_lad_wm_mean', Float(4, 2)), 

    Column('lad_wm_sd', Float(4, 2)),
    Column('ocr_lad_wm_sd', Float(4, 2)), 
    Column('ocr_clv_lad_wm_sd', Float(4, 2)),


    Column('lcx_perf_mean', Float(4, 2)), 
    Column('ocr_lcx_perf_mean', Float(4, 2)), 
    Column('ocr_clv_lcx_perf_mean', Float(4, 2)), 

    Column('lcx_perf_sd', Float(4, 2)),
    Column('ocr_lcx_perf_sd', Float(4, 2)),
    Column('ocr_clv_lcx_perf_sd', Float(4, 2)),

    Column('lcx_wt_mean', Float(4, 2)),
    Column('ocr_lcx_wt_mean', Float(4, 2)), 
    Column('ocr_clv_lcx_wt_mean', Float(4, 2)), 

    Column('lcx_wt_sd', Float(4, 2)),
    Column('ocr_lcx_wt_sd', Float(4, 2)),
    Column('ocr_clv_lcx_wt_sd', Float(4, 2)),

    Column('lcx_wm_mean', Float(4, 2)), 
    Column('ocr_lcx_wm_mean', Float(4, 2)),
    Column('ocr_clv_lcx_wm_mean', Float(4, 2)), 

    Column('lcx_wm_sd', Float(4, 2)),
    Column('ocr_lcx_wm_sd', Float(4, 2)),
    Column('ocr_clv_lcx_wm_sd', Float(4, 2)),


    Column('rca_perf_mean', Float(4, 2)),
    Column('ocr_rca_perf_mean', Float(4, 2)),
    Column('ocr_clv_rca_perf_mean', Float(4, 2)),

    Column('rca_perf_sd', Float(4, 2)),
    Column('ocr_rca_perf_sd', Float(4, 2)), 
    Column('ocr_clv_rca_perf_sd', Float(4, 2)), 

    Column('rca_wt_mean', Float(4, 2)),
    Column('ocr_rca_wt_mean', Float(4, 2)), 
    Column('ocr_clv_rca_wt_mean', Float(4, 2)), 

    Column('rca_wt_sd', Float(4, 2)), 
    Column('ocr_rca_wt_sd', Float(4, 2)), 
    Column('ocr_clv_rca_wt_sd', Float(4, 2)),

    Column('rca_wm_mean', Float(4, 2)),
    Column('ocr_rca_wm_mean', Float(4, 2)),
    Column('ocr_clv_rca_wm_mean', Float(4, 2)),

    Column('rca_wm_sd', Float(4, 2)), 
    Column('ocr_rca_wm_sd', Float(4, 2)), 
    Column('ocr_clv_rca_wm_sd', Float(4, 2)), 

    Column('tot_perf_mean', Float(4, 2)),
    Column('ocr_tot_perf_mean', Float(4, 2)),
    Column('ocr_clv_tot_perf_mean', Float(4, 2)),

    Column('tot_perf_sd', Float(4, 2)),
    Column('ocr_tot_perf_sd', Float(4, 2)),
    Column('ocr_clv_tot_perf_sd', Float(4, 2)),

    Column('tot_wt_mean', Float(4, 2)),
    Column('ocr_tot_wt_mean', Float(4, 2)),
    Column('ocr_clv_tot_wt_mean', Float(4, 2)), 

    Column('tot_wt_sd', Float(4, 2)),
    Column('ocr_tot_wt_sd', Float(4, 2)),
    Column('ocr_clv_tot_wt_sd', Float(4, 2)),
  
    Column('tot_wm_mean', Float(4, 2)),
    Column('ocr_tot_wm_mean', Float(4, 2)),
    Column('ocr_clv_tot_wm_mean', Float(4, 2)),

    Column('tot_wm_sd', Float(4, 2)),
    Column('ocr_tot_wm_sd', Float(4, 2)), 
    Column('ocr_clv_tot_wm_sd', Float(4, 2)),


    Column('lad_perf_ext', Float(4, 2)),
    Column('ocr_lad_perf_ext', Float(4, 2)),
    Column('ocr_clv_lad_perf_ext', Float(4, 2)),

    Column('lad_perf_sev', Float(4, 2)),
    Column('ocr_lad_perf_sev', Float(4, 2)),
    Column('ocr_clv_lad_perf_sev', Float(4, 2)),

    Column('lad_wt_ext', Float(4, 2)),
    Column('ocr_lad_wt_ext', Float(4, 2)),
    Column('ocr_clv_lad_wt_ext', Float(4, 2)),

    Column('lad_wt_sev', Float(4, 2)),
    Column('ocr_lad_wt_sev', Float(4, 2)),
    Column('ocr_clv_lad_wt_sev', Float(4, 2)), 

    Column('lad_wm_ext', Float(4, 2)),
    Column('ocr_lad_wm_ext', Float(4, 2)), 
    Column('ocr_clv_lad_wm_ext', Float(4, 2)), 

    Column('lad_wm_sev', Float(4, 2)),
    Column('ocr_lad_wm_sev', Float(4, 2)), 
    Column('ocr_clv_lad_wm_sev', Float(4, 2)),


    Column('lcx_perf_ext', Float(4, 2)), 
    Column('ocr_lcx_perf_ext', Float(4, 2)), 
    Column('ocr_clv_lcx_perf_ext', Float(4, 2)), 

    Column('lcx_perf_sev', Float(4, 2)),
    Column('ocr_lcx_perf_sev', Float(4, 2)),
    Column('ocr_clv_lcx_perf_sev', Float(4, 2)),

    Column('lcx_wt_ext', Float(4, 2)),
    Column('ocr_lcx_wt_ext', Float(4, 2)), 
    Column('ocr_clv_lcx_wt_ext', Float(4, 2)), 

    Column('lcx_wt_sev', Float(4, 2)),
    Column('ocr_lcx_wt_sev', Float(4, 2)),
    Column('ocr_clv_lcx_wt_sev', Float(4, 2)),

    Column('lcx_wm_ext', Float(4, 2)), 
    Column('ocr_lcx_wm_ext', Float(4, 2)),
    Column('ocr_clv_lcx_wm_ext', Float(4, 2)), 

    Column('lcx_wm_sev', Float(4, 2)),
    Column('ocr_lcx_wm_sev', Float(4, 2)),
    Column('ocr_clv_lcx_wm_sev', Float(4, 2)),


    Column('rca_perf_ext', Float(4, 2)),
    Column('ocr_rca_perf_ext', Float(4, 2)),
    Column('ocr_clv_rca_perf_ext', Float(4, 2)),

    Column('rca_perf_sev', Float(4, 2)),
    Column('ocr_rca_perf_sev', Float(4, 2)), 
    Column('ocr_clv_rca_perf_sev', Float(4, 2)), 

    Column('rca_wt_ext', Float(4, 2)),
    Column('ocr_rca_wt_ext', Float(4, 2)), 
    Column('ocr_clv_rca_wt_ext', Float(4, 2)), 

    Column('rca_wt_sev', Float(4, 2)), 
    Column('ocr_rca_wt_sev', Float(4, 2)), 
    Column('ocr_clv_rca_wt_sev', Float(4, 2)),

    Column('rca_wm_ext', Float(4, 2)),
    Column('ocr_rca_wm_ext', Float(4, 2)),
    Column('ocr_clv_rca_wm_ext', Float(4, 2)),

    Column('rca_wm_sev', Float(4, 2)), 
    Column('ocr_rca_wm_sev', Float(4, 2)), 
    Column('ocr_clv_rca_wm_sev', Float(4, 2)), 

    Column('tot_perf_ext', Float(4, 2)),
    Column('ocr_tot_perf_ext', Float(4, 2)),
    Column('ocr_clv_tot_perf_ext', Float(4, 2)),

    Column('tot_perf_sev', Float(4, 2)),
    Column('ocr_tot_perf_sev', Float(4, 2)),
    Column('ocr_clv_tot_perf_sev', Float(4, 2)),

    Column('tot_wt_ext', Float(4, 2)),
    Column('ocr_tot_wt_ext', Float(4, 2)),
    Column('ocr_clv_tot_wt_ext', Float(4, 2)), 

    Column('tot_wt_sev', Float(4, 2)),
    Column('ocr_tot_wt_sev', Float(4, 2)),
    Column('ocr_clv_tot_wt_sev', Float(4, 2)),
  
    Column('tot_wm_ext', Float(4, 2)),
    Column('ocr_tot_wm_ext', Float(4, 2)),
    Column('ocr_clv_tot_wm_ext', Float(4, 2)),

    Column('tot_wm_sev', Float(4, 2)),
    Column('ocr_tot_wm_sev', Float(4, 2)), 
    Column('ocr_clv_tot_wm_sev', Float(4, 2)), 
)

rest_quanti_schema = Table(
    'rest_quanti', meta,
    Column('id', Integer, Identity(start=1, cycle=True), primary_key=True),
    Column('mpi_test_id', Integer),

    Column('max_perfusion', Float(4, 2)),
    Column('ocr_max_perfusion', Float(4, 2)),
    Column('ocr_clv_max_perfusion', Float(4, 2)),  
    Column('interval', Float(4, 2)),
    Column('ocr_interval', Float(4, 2)),
    Column('ocr_clv_interval', Float(4, 2)),

    Column('es', Float(4, 2)),
    Column('ocr_es', Float(4, 2)),
    Column('ocr_clv_es', Float(4, 2)),

    Column('ed', Float(4, 2)),
    Column('ocr_ed', Float(4, 2)), 
    Column('ocr_clv_ed', Float(4, 2)), 

    Column('lvef', Float(4, 2)),
    Column('ocr_lvef', Float(4, 2)),
    Column('ocr_clv_lvef', Float(4, 2)),

    Column('lad_perf_mean', Float(4, 2)),
    Column('ocr_lad_perf_mean', Float(4, 2)),
    Column('ocr_clv_lad_perf_mean', Float(4, 2)),

    Column('lad_perf_sd', Float(4, 2)),
    Column('ocr_lad_perf_sd', Float(4, 2)),
    Column('ocr_clv_lad_perf_sd', Float(4, 2)),

    Column('lad_wt_mean', Float(4, 2)),
    Column('ocr_lad_wt_mean', Float(4, 2)),
    Column('ocr_clv_lad_wt_mean', Float(4, 2)),

    Column('lad_wt_sd', Float(4, 2)),
    Column('ocr_lad_wt_sd', Float(4, 2)),
    Column('ocr_clv_lad_wt_sd', Float(4, 2)), 

    Column('lad_wm_mean', Float(4, 2)),
    Column('ocr_lad_wm_mean', Float(4, 2)), 
    Column('ocr_clv_lad_wm_mean', Float(4, 2)), 

    Column('lad_wm_sd', Float(4, 2)),
    Column('ocr_lad_wm_sd', Float(4, 2)), 
    Column('ocr_clv_lad_wm_sd', Float(4, 2)),


    Column('lcx_perf_mean', Float(4, 2)), 
    Column('ocr_lcx_perf_mean', Float(4, 2)), 
    Column('ocr_clv_lcx_perf_mean', Float(4, 2)), 

    Column('lcx_perf_sd', Float(4, 2)),
    Column('ocr_lcx_perf_sd', Float(4, 2)),
    Column('ocr_clv_lcx_perf_sd', Float(4, 2)),

    Column('lcx_wt_mean', Float(4, 2)),
    Column('ocr_lcx_wt_mean', Float(4, 2)), 
    Column('ocr_clv_lcx_wt_mean', Float(4, 2)), 

    Column('lcx_wt_sd', Float(4, 2)),
    Column('ocr_lcx_wt_sd', Float(4, 2)),
    Column('ocr_clv_lcx_wt_sd', Float(4, 2)),

    Column('lcx_wm_mean', Float(4, 2)), 
    Column('ocr_lcx_wm_mean', Float(4, 2)),
    Column('ocr_clv_lcx_wm_mean', Float(4, 2)), 

    Column('lcx_wm_sd', Float(4, 2)),
    Column('ocr_lcx_wm_sd', Float(4, 2)),
    Column('ocr_clv_lcx_wm_sd', Float(4, 2)),


    Column('rca_perf_mean', Float(4, 2)),
    Column('ocr_rca_perf_mean', Float(4, 2)),
    Column('ocr_clv_rca_perf_mean', Float(4, 2)),

    Column('rca_perf_sd', Float(4, 2)),
    Column('ocr_rca_perf_sd', Float(4, 2)), 
    Column('ocr_clv_rca_perf_sd', Float(4, 2)), 

    Column('rca_wt_mean', Float(4, 2)),
    Column('ocr_rca_wt_mean', Float(4, 2)), 
    Column('ocr_clv_rca_wt_mean', Float(4, 2)), 

    Column('rca_wt_sd', Float(4, 2)), 
    Column('ocr_rca_wt_sd', Float(4, 2)), 
    Column('ocr_clv_rca_wt_sd', Float(4, 2)),

    Column('rca_wm_mean', Float(4, 2)),
    Column('ocr_rca_wm_mean', Float(4, 2)),
    Column('ocr_clv_rca_wm_mean', Float(4, 2)),

    Column('rca_wm_sd', Float(4, 2)), 
    Column('ocr_rca_wm_sd', Float(4, 2)), 
    Column('ocr_clv_rca_wm_sd', Float(4, 2)), 

    Column('tot_perf_mean', Float(4, 2)),
    Column('ocr_tot_perf_mean', Float(4, 2)),
    Column('ocr_clv_tot_perf_mean', Float(4, 2)),

    Column('tot_perf_sd', Float(4, 2)),
    Column('ocr_tot_perf_sd', Float(4, 2)),
    Column('ocr_clv_tot_perf_sd', Float(4, 2)),

    Column('tot_wt_mean', Float(4, 2)),
    Column('ocr_tot_wt_mean', Float(4, 2)),
    Column('ocr_clv_tot_wt_mean', Float(4, 2)), 

    Column('tot_wt_sd', Float(4, 2)),
    Column('ocr_tot_wt_sd', Float(4, 2)),
    Column('ocr_clv_tot_wt_sd', Float(4, 2)),
  
    Column('tot_wm_mean', Float(4, 2)),
    Column('ocr_tot_wm_mean', Float(4, 2)),
    Column('ocr_clv_tot_wm_mean', Float(4, 2)),

    Column('tot_wm_sd', Float(4, 2)),
    Column('ocr_tot_wm_sd', Float(4, 2)), 
    Column('ocr_clv_tot_wm_sd', Float(4, 2)),


    Column('lad_perf_ext', Float(4, 2)),
    Column('ocr_lad_perf_ext', Float(4, 2)),
    Column('ocr_clv_lad_perf_ext', Float(4, 2)),

    Column('lad_perf_sev', Float(4, 2)),
    Column('ocr_lad_perf_sev', Float(4, 2)),
    Column('ocr_clv_lad_perf_sev', Float(4, 2)),

    Column('lad_wt_ext', Float(4, 2)),
    Column('ocr_lad_wt_ext', Float(4, 2)),
    Column('ocr_clv_lad_wt_ext', Float(4, 2)),

    Column('lad_wt_sev', Float(4, 2)),
    Column('ocr_lad_wt_sev', Float(4, 2)),
    Column('ocr_clv_lad_wt_sev', Float(4, 2)), 

    Column('lad_wm_ext', Float(4, 2)),
    Column('ocr_lad_wm_ext', Float(4, 2)), 
    Column('ocr_clv_lad_wm_ext', Float(4, 2)), 

    Column('lad_wm_sev', Float(4, 2)),
    Column('ocr_lad_wm_sev', Float(4, 2)), 
    Column('ocr_clv_lad_wm_sev', Float(4, 2)),


    Column('lcx_perf_ext', Float(4, 2)), 
    Column('ocr_lcx_perf_ext', Float(4, 2)), 
    Column('ocr_clv_lcx_perf_ext', Float(4, 2)), 

    Column('lcx_perf_sev', Float(4, 2)),
    Column('ocr_lcx_perf_sev', Float(4, 2)),
    Column('ocr_clv_lcx_perf_sev', Float(4, 2)),

    Column('lcx_wt_ext', Float(4, 2)),
    Column('ocr_lcx_wt_ext', Float(4, 2)), 
    Column('ocr_clv_lcx_wt_ext', Float(4, 2)), 

    Column('lcx_wt_sev', Float(4, 2)),
    Column('ocr_lcx_wt_sev', Float(4, 2)),
    Column('ocr_clv_lcx_wt_sev', Float(4, 2)),

    Column('lcx_wm_ext', Float(4, 2)), 
    Column('ocr_lcx_wm_ext', Float(4, 2)),
    Column('ocr_clv_lcx_wm_ext', Float(4, 2)), 

    Column('lcx_wm_sev', Float(4, 2)),
    Column('ocr_lcx_wm_sev', Float(4, 2)),
    Column('ocr_clv_lcx_wm_sev', Float(4, 2)),


    Column('rca_perf_ext', Float(4, 2)),
    Column('ocr_rca_perf_ext', Float(4, 2)),
    Column('ocr_clv_rca_perf_ext', Float(4, 2)),

    Column('rca_perf_sev', Float(4, 2)),
    Column('ocr_rca_perf_sev', Float(4, 2)), 
    Column('ocr_clv_rca_perf_sev', Float(4, 2)), 

    Column('rca_wt_ext', Float(4, 2)),
    Column('ocr_rca_wt_ext', Float(4, 2)), 
    Column('ocr_clv_rca_wt_ext', Float(4, 2)), 

    Column('rca_wt_sev', Float(4, 2)), 
    Column('ocr_rca_wt_sev', Float(4, 2)), 
    Column('ocr_clv_rca_wt_sev', Float(4, 2)),

    Column('rca_wm_ext', Float(4, 2)),
    Column('ocr_rca_wm_ext', Float(4, 2)),
    Column('ocr_clv_rca_wm_ext', Float(4, 2)),

    Column('rca_wm_sev', Float(4, 2)), 
    Column('ocr_rca_wm_sev', Float(4, 2)), 
    Column('ocr_clv_rca_wm_sev', Float(4, 2)), 

    Column('tot_perf_ext', Float(4, 2)),
    Column('ocr_tot_perf_ext', Float(4, 2)),
    Column('ocr_clv_tot_perf_ext', Float(4, 2)),

    Column('tot_perf_sev', Float(4, 2)),
    Column('ocr_tot_perf_sev', Float(4, 2)),
    Column('ocr_clv_tot_perf_sev', Float(4, 2)),

    Column('tot_wt_ext', Float(4, 2)),
    Column('ocr_tot_wt_ext', Float(4, 2)),
    Column('ocr_clv_tot_wt_ext', Float(4, 2)), 

    Column('tot_wt_sev', Float(4, 2)),
    Column('ocr_tot_wt_sev', Float(4, 2)),
    Column('ocr_clv_tot_wt_sev', Float(4, 2)),
  
    Column('tot_wm_ext', Float(4, 2)),
    Column('ocr_tot_wm_ext', Float(4, 2)),
    Column('ocr_clv_tot_wm_ext', Float(4, 2)),

    Column('tot_wm_sev', Float(4, 2)),
    Column('ocr_tot_wm_sev', Float(4, 2)), 
    Column('ocr_clv_tot_wm_sev', Float(4, 2)), 
)

tpd_17_seg_schema = Table(
    'tpd_17_seg', meta,
    Column('id', Integer, Identity(start=1, cycle=True), primary_key=True),
    Column('mpi_test_id', Integer),

    Column('stress_sss', Float(4, 2)),
    Column('ocr_stress_sss', Float(4, 2)),
    Column('ocr_clv_stress_sss', Float(4, 2)),

    Column('stress_sts', Float(4, 2)),
    Column('ocr_stress_sts', Float(4, 2)),
    Column('ocr_clv_stress_sts', Float(4, 2)),

    Column('stress_sms', Float(4, 2)),
    Column('ocr_stress_sms', Float(4, 2)),
    Column('ocr_clv_stress_sms', Float(4, 2)),

    Column('rest_srs', Float(4, 2)),
    Column('ocr_rest_srs', Float(4, 2)),
    Column('ocr_clv_rest_srs', Float(4, 2)),

    Column('rest_sts', Float(4, 2)),
    Column('ocr_rest_sts', Float(4, 2)),
    Column('ocr_clv_rest_sts', Float(4, 2)),

    Column('rest_sms', Float(4, 2)),
    Column('ocr_rest_sms', Float(4, 2)),
    Column('ocr_clv_rest_sms', Float(4, 2)),
)

mpi_test_schema = Table(
    'mpi_test', meta,
    Column('id', Integer, primary_key=True),
    Column('hn_number', String(9)),
    Column('mpi_exam_date', Date),
    Column('is_ocr_approved', Boolean),
    Column('bookmarked_ml_daig_id', Integer),
    Column('status', String(10)),
    Column('dcm_dpath', Text),
    Column('large_webp_dpath', Text), 
    Column('small_webp_dpath', Text), 
    Column('dm', String(10)),
    Column('ht', String(10)),
    Column('dlp', String(10)),
    Column('ckd', String(10)),
    Column('weight', Float(3, 2)),
    Column('height', Float(3, 2)),
    Column('bmi', Float(3, 2)),
    Column('age', Integer),
    Column('created_at', TIMESTAMP),
    Column('updated_at', TIMESTAMP)
)

mpi_crop_img = Table(
    'mpi_crop_img', meta,
    Column('id', Integer, primary_key=True),
    Column('mpi_test_id', Integer),

    Column('stress_perfusion_dpath', String(100)),
    Column('rest_perfusion_dpath', String(100)),

    Column('stress_severity_dpath', String(100)),
    Column('rest_severity_dpath', String(100)),

    Column('stress_blackout_dpath', String(100)),
    Column('rest_blackout_dpath', String(100)),

    Column('stress_def_sev_dpath', String(100)),
    Column('rest_def_sev_dpath', String(100))
)

class target_enum(enum.Enum):
    lad = 'LAD'
    lcx = 'LCX'
    rca = 'RCA'
    patient = 'PATIENT'

ml_model = Table(
    'ml_model', meta,
    Column('id', Integer, primary_key=True),
    Column('name', String(10)),
    Column('type', String(18)),
    Column('target', Enum(target_enum)),
    Column('version', String(12)),

    Column('val_acc', Float(3, 2)),
    Column('val_specificity', Float(3, 2)),
    Column('val_precision', Float(3, 2)),
    Column('val_recall', Float(3, 2)),
    Column('val_f1', Float(3, 2)),
    Column('val_fnr', Float(3, 2)),
    Column('val_tpr', Float(3, 2)),
    Column('val_tnr', Float(3, 2)),
    Column('val_fpt', Float(3, 2)),
    Column('adapt_graph', JSON),
    Column('brand_quanti_model', String(18)),
    Column('is_best', Boolean),

    Column('created_at', TIMESTAMP),
    Column('updated_at', TIMESTAMP),

)

ml_diag = Table(
    'ml_diag', meta,
    Column('id', Integer, primary_key=True),
    Column('mpi_test_id', Integer),
    Column('lad_ml_model_id', Integer),
    Column('lcx_ml_model_id', Integer),
    Column('rca_ml_model_id', Integer),
    Column('patient_ml_model_id', Integer),

    Column('lad_predict', Integer),
    Column('lcx_predict', Integer),
    Column('rca_predict', Integer),
    Column('patient_predict', Integer),

    Column('lad_predict_proba', Float(1, 2)),
    Column('lcx_predict_proba', Float(1, 2)),
    Column('rca_predict_proba', Float(1, 2)),
    Column('patient_predict_proba', Float(1, 2)),

    Column('created_at', TIMESTAMP),
    Column('updated_at', TIMESTAMP),
    Column('updated_by', Integer)
)