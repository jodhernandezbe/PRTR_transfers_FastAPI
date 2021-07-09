#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Importing libraries
from pydantic import BaseModel
from typing import Optional


class RecordRequestModel(BaseModel):
    reporting_year: Optional[int] = None
    country: Optional[str] = None
    generic_substance_id: Optional[str] = None
    generic_sector_code: Optional[int] = None
    generic_transfer_class_id: Optional[str] = None

    class Config:
        orm_mode = True


class RecordResponseModel(RecordRequestModel):
    record_id: int
    number_of_facilities: int
    total_transfer_amount_kg: float
    average_transfer_amount_kg: float
    median_transfer_amount_kg: float
    std_transfer_amount_kg: float
    max_transfer_amount_kg: float
    min_transfer_amount_kg: float

    class Config:
        orm_mode = True


class RecordRequestInequalityModel(BaseModel):
    generic_sector_code: Optional[int] = None
    generic_substance_id: Optional[str] = None
    generic_transfer_class_id: Optional[str] = None
    total_transfer_amount_kg: Optional[str] = None
    average_transfer_amount_kg: Optional[str] = None
    median_transfer_amount_kg: Optional[str] = None
    max_transfer_amount_kg: Optional[str] = None
    min_transfer_amount_kg: Optional[str] = None

    class Config:
        orm_mode = True


class SectorResponseModel(BaseModel) :
    generic_sector_code : int
    generic_sector_name: str

    class Config:
        orm_mode = True


class TransferClassResponseModel(BaseModel) :
    generic_transfer_class_id : str
    generic_transfer_class_name: str
    transfer_class_wm_hierarchy_name : str

    class Config:
        orm_mode = True


class SubstanceResponseModel(BaseModel) :
    generic_substance_id : str
    generic_substance_name: str
    cas_number: str

    class Config:
        orm_mode = True