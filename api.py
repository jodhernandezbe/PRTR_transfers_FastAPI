#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Importing libraries
from base import creating_session_engine
import model
from query import get_records, get_records_by_conditions
from schema import RecordRequestModel, RecordResponseModel, RecordRequestInequalityModel

from fastapi import FastAPI, Depends, HTTPException, Body
from sqlalchemy.orm import Session
import uvicorn
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse


Engine, SessionLocal = creating_session_engine(check_same_thread=False)
model.Base.metadata.create_all(bind=Engine)
app = FastAPI(title='PRTR transfers summary data',
            description='This is an API that summarizes the information obtained by performing data engineering to 3 Pollutant Release and Transfer Register (​PRTR) systems. The 3 PRTR systems are the Australian National Provider Identifier (NPI), the Canadian National Pollutant Release Inventory (NPRI), and the United States of America Toxics Release Inventory (TRI). A GitHub repository contains the Python Scripts that run the generic data engineering procedure for the 3 PRTR systems (see <a href="https://github.com/jodhernandezbe/PRTR_transfers">PRTR_transfers</a>). Also, A GitHub repository has information about how to obtain the SQL database, API, and schemas for the PRTR transfers summary data (see <a href="https://github.com/jodhernandezbe/PRTR_transfers_FastAPI">PRTR_transfers_FastAPI</a>).',
            version='0.0.1')

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post('/records/',
        summary='PRTR transfers summary data',
        response_model=RecordResponseModel,
        response_model_exclude={'record_id'})
def read_record(record_request: RecordRequestModel = Body(...,
                examples={'example_1': {'summary': 'All parameters',
                                    'description': 'A query with all parameters specified by the user',
                                    'value': {
                                        'reporting_year': 1987,
                                        'country': 'USA',
                                        'generic_substance_id': 'NA-01',
                                        'generic_sector_code': 24,
                                        'generic_transfer_class_id': 'M4'
                                            }
                                        },
                        'example_2': {'summary': 'Excluding a parameter',
                                    'description': 'A query with one parameter excluded by the user',
                                    'value': {
                                        'reporting_year': 2019,
                                        'generic_substance_id': 'NA-06',
                                        'generic_sector_code': 71,
                                        'generic_transfer_class_id': 'M9'
                                            }
                                        },
                        'example_3': {'summary': 'Excluding many parameters',
                                    'description': 'A query with many parameters excluded by the user',
                                    'value': {
                                        'country': 'CAN'
                                            }
                                    }
                        }
                                                        ),
                db: Session = Depends(get_db)
                ):
    '''
    Fucntion to HTTP request and response for records
    '''

    record_request_dict = record_request.dict()
    records = get_records(db, record_request_dict)

    if not records:
        raise HTTPException(status_code=404, detail="Record not found")

    json_compatible_item_data = jsonable_encoder(records)
    
    return JSONResponse(content=json_compatible_item_data)


@app.post('/conditional_records/',
        summary='PRTR transfers summary data based on conditions',
        response_model=RecordResponseModel,
        response_model_exclude={'record_id'})
def read_record_with_condition(record_request: RecordRequestInequalityModel = Body(...,
                                examples={'example_1': {'summary': 'Chemical and total quantity',
                                                        'description': 'A query with a chemical and a condition on the total transfer quantity specified by the user',
                                                        'value': {
                                                            'generic_substance_id': '7440020',
                                                            'total_transfer_amount_kg': '>= 100.00'
                                                                }
                                                        },
                                        'example_2': {'summary': 'Sector and max quantity',
                                                    'description': 'A query with an industry sector and a condition on the maximum transfer quantity specified by the user',
                                                    'value': {
                                                        'generic_sector_code': 24,
                                                        'max_transfer_amount_kg': '>= 10000'
                                                            }
                                                        },
                                        'example_3': {'summary': 'Only a summary quantity',
                                                    'description': 'A query with only a condition on any summary quantity specified by the user',
                                                    'value': {
                                                        'average_transfer_amount_kg': '< 0.5'
                                                            }
                                                    }
                        }
                                
                                                                                    ),
                            db: Session = Depends(get_db)
                            ):
    '''
    Function to HTTP request and response for records based on conditions
    '''

    record_request_dict = record_request.dict()
    records = get_records_by_conditions(db, record_request_dict)

    if not records:
        raise HTTPException(status_code=404, detail="Record not found")

    json_compatible_item_data = jsonable_encoder(records)
    
    return JSONResponse(content=json_compatible_item_data)


if __name__ == "__main__":
    uvicorn.run("api:app", host="127.0.0.1",
                port=8000, log_level="info",
                reload=True)

