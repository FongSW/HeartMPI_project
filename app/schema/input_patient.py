from pydantic import BaseModel
from fastapi import Form, Query
from typing import List

class Input_patient(BaseModel):
    mpi_test_id: int
    hn: str
    path_file: str
    

    @classmethod
    def as_form(
        cls,
        mpi_test_id: int = Form(...),
        hn: str = Form(...),
        path_file: str = Form(...)
        
    ):
        return cls(mpi_test_id=mpi_test_id, hn=hn, path_file=path_file)

class Predict_patient(BaseModel):
    mpi_test_id: int
    account_user_id: int

    @classmethod
    def as_form(
        cls,
        mpi_test_id: int = Form(...),
        account_user_id: int = Form(...)
    ):
        return cls(mpi_test_id=mpi_test_id, account_user_id=account_user_id)
    
class Predict_patient_v2(BaseModel):
    mpi_test_id: int
    ml_diag_id: List[int]

    @classmethod
    def as_form(
        cls,
        mpi_test_id: int = Query(...),
        ml_diag_id: List[int] = Query(...)
    ):
        return cls(mpi_test_id=mpi_test_id, ml_diag_id=ml_diag_id)

