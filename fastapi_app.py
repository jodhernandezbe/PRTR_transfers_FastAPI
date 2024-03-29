#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Importing libraries
from base import creating_session_engine
import model
from query import get_records, get_records_by_conditions, getting_list_of_lists
from schema import RecordRequestModel, RecordResponseModel, RecordRequestInequalityModel
from config import FASTAPI_PORT, FASTAPI_ADDR, BOKEH_URL, FASTAPI_URL

from fastapi import FastAPI, Depends, HTTPException, Body, Request
from sqlalchemy.orm import Session
import uvicorn
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from bokeh.embed import server_document
import os

dir_path = os.path.dirname(os.path.realpath(__file__)) # current directory path

templates_path = f'{dir_path}/templates'
templates = Jinja2Templates(directory=templates_path)

Engine, SessionLocal = creating_session_engine(check_same_thread=False)
model.Base.metadata.create_all(bind=Engine)


app = FastAPI(title='PRTR Transfers Summary REST Services',
            description=
            
            f'''This is an API that contains summary information for the data that were obtained by performing data engineering to three Pollutant Release and Transfer Register (​PRTR) systems. The three PRTR systems are the <a href="http://www.npi.gov.au/" rel="noopener noreferrer" target="_blank">National Pollutant Inventory (NPI)</a>, the <a href="https://www.canada.ca/en/services/environment/pollution-waste-management/national-pollutant-release-inventory.html" rel="noopener noreferrer" target="_blank">National Pollutant Release Inventory (NPRI)</a>, and the <a href="https://www.epa.gov/toxics-release-inventory-tri-program" rel="noopener noreferrer" target="_blank">Toxics Release Inventory (TRI)</a>. A GitHub repository contains the Python Scripts that run the generic data engineering procedure for the three PRTR systems (see <a href="https://github.com/jodhernandezbe/PRTR_transfers">PRTR_transfers</a>).<br><p><a href="{FASTAPI_URL}">PRTR transfers summary - Website</a></p>
            ''',
            version='1',
            contact={
                    "name": "Jose D. Hernandez-Betancur",
                    "url": "www.sustineritechem.com",
                    "email": "jodhernandezbemj@gmail.com"
                    },
            license_info={
                    "name": "GNU General Public License v3.0",
                    "url": "https://github.com/jodhernandezbe/PRTR_transfers_FastAPI/blob/local/LICENSE",
                        },
            docs_url="/v1/api_documentation",
            redoc_url=None)

static_path = f'{dir_path}/static'
app.mount("/static",
        StaticFiles(directory=static_path),
        name="static")


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get('/',
        summary='Home',
        response_class = HTMLResponse,
        include_in_schema=False,
        responses = {200: {'description': 'HTML home',
                            'content': {'text/html': {}}}}
        )
def get_sector_records(request: Request):    
    return templates.TemplateResponse("home.html", {"request": request})

@app.get('/about/',
        summary='About',
        response_class = HTMLResponse,
        include_in_schema=False,
        responses = {200: {'description': 'HTML about',
                            'content': {'text/html': {}}}}
        )
def get_sector_records(request: Request):    
    return templates.TemplateResponse("about.html", {"request": request})


@app.get('/dashboard/',
        summary='Dashboard',
        response_class = HTMLResponse,
        include_in_schema=False,
        responses = {200: {'description': 'HTML about',
                            'content': {'text/html': {}}}}
        )
def get_sector_records(request: Request):
    script = server_document(f'{BOKEH_URL}/bkapp', resources=None)
    return templates.TemplateResponse("dashboard.html", {"request": request, 'script': script})
        

@app.get('/sectors/',
        summary='Generic industry sectors in the PRTR_transfers_summary database',
        response_class = HTMLResponse,
        include_in_schema=False,
        responses = {200: {'description': 'HTML table with generic industry sectors',
                            'content': {'text/html': {}}}}
        )
def get_sector_records(request: Request, db: Session = Depends(get_db)):
    columns, outer_list = getting_list_of_lists(db, model.GenericSector)    
    context = {'table_title': 'Generic industry sectors',
                'columns': columns,
                'record_rows': outer_list,
                'request': request}
    return templates.TemplateResponse("table.html", context=context)    


@app.get('/substances/',
        summary='Generic substances in the PRTR_transfers_summary database',
        response_class = HTMLResponse,
        include_in_schema=False,
        responses = {200: {'description': 'HTML table with generic substances',
                            'content': {'text/html': {}}}})
def get_substance_records(request: Request, db: Session = Depends(get_db)):
    columns, outer_list = getting_list_of_lists(db, model.GenericSubstance)    
    context = {'table_title': 'Generic substances',
                'columns': columns,
                'record_rows': outer_list,
                'request': request}
    return templates.TemplateResponse("table.html", context=context) 


@app.get('/transfer_classes/',
        summary='Generic transfer classes in the PRTR_transfers_summary database',
        response_class = HTMLResponse,
        include_in_schema=False,
        responses = {200: {'description': 'HTML table with generic transfer classes',
                            'content': {'text/html': {}}}})
def get_transfer_class_records(request: Request, db: Session = Depends(get_db)):
    columns, outer_list = getting_list_of_lists(db, model.GenericTransferClass)    
    context = {'table_title': 'Generic transfer classes',
                'columns': columns,
                'record_rows': outer_list,
                'request': request}
    return templates.TemplateResponse("table.html", context=context)


@app.post('/v1/records/',
        summary='PRTR transfers summary data',
        response_model=RecordResponseModel,
        responses = {
                    200: {'description': 'JSON output obtained based on user input parameter(s)',
                        'content': {
                                    'application/json': {
                                        'example': {
                                            "reporting_year": 2013,
                                            "country": "AUS",
                                            "generic_substance_id": "64175",
                                            "generic_sector_code": 10,
                                            "generic_transfer_class_id": "M7",
                                            "number_of_facilities": 91,
                                            "total_transfer_amount_kg": 9577900.5,
                                            "average_transfer_amount_kg": 105251.65,
                                            "median_transfer_amount_kg": 12576.8,
                                            "std_transfer_amount_kg": 435590.29,
                                            "max_transfer_amount_kg": 3845510.0,
                                            "min_transfer_amount_kg": 81.0
                                                    }
                                                        }
                                    }
                        }
                    }
        )
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


@app.post('/v1/conditional_records/',
        summary='PRTR transfers summary data based on conditions',
        response_model=RecordResponseModel,
        responses = {
                    200: {'description': 'JSON output obtained based on user input parameter(s)',
                        'content': {
                                    'application/json': {
                                        'example': {
                                            "reporting_year": 2019,
                                            "country": "CAN",
                                            "generic_substance_id": "98828",
                                            "generic_sector_code": 46,
                                            "generic_transfer_class_id": "M7",
                                            "number_of_facilities": 3,
                                            "total_transfer_amount_kg": 12594.84,
                                            "average_transfer_amount_kg": 4198.28,
                                            "median_transfer_amount_kg": 1.6,
                                            "std_transfer_amount_kg": 7270.13,
                                            "max_transfer_amount_kg": 12593.1,
                                            "min_transfer_amount_kg": 0.14
                                                    }
                                                        }
                                    }
                        }
                    }
        )
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


def start_uvicorn():
    uvicorn.run("fastapi_app:app", host=FASTAPI_ADDR,
                port=FASTAPI_PORT, log_level="info",
                reload=True)

if __name__ == "__main__":
    start_uvicorn()

