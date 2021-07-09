#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Importing libraries
from model import Record, GenericSubstance, GenericSector, GenericTransferClass

from sqlalchemy.orm import Session
from sqlalchemy.inspection import inspect
import re
from collections import defaultdict
import pandas as pd


def get_records(db: Session, fields):
    '''
    Function to make a query for obtaining information
    considering the PRTR country
    '''

    results = db.query(Record).filter_by(**{k: v for k, v in fields.items() if v is not None})
    results = results.all()

    return results


def get_records_by_conditions(db: Session, fields):
    '''
    Function to get records based on threshold
    '''

    regex = re.compile(r'^([!=><]{1,2})\s?(\d+.?\d*)$')

    cols_for_queries = {'total_transfer_amount_kg': Record.total_transfer_amount_kg,
                        'average_transfer_amount_kg': Record.average_transfer_amount_kg,
                        'median_transfer_amount_kg': Record.median_transfer_amount_kg,
                        'max_transfer_amount_kg': Record.max_transfer_amount_kg,
                        'min_transfer_amount_kg': Record.min_transfer_amount_kg,
                        'generic_substance_id': Record.generic_substance_id,
                        'generic_transfer_class_id': Record.generic_transfer_class_id,
                        'generic_sector_code': Record.generic_sector_code}

    non_empty_queries = {k: v for k, v in fields.items() if v is not None}
    results = db.query(Record)
    for key, value in non_empty_queries.items():
        if key in ['generic_substance_id', 'generic_transfer_class_id', 'generic_sector_code']:
            results = results.filter(cols_for_queries[key] == value)
        else:
            inequality = re.match(regex, value).group(1)
            number = float(re.match(regex, value).group(2))
            if inequality == '==':
                results = results.filter(cols_for_queries[key] == number)
            elif inequality == '>':
                results = results.filter(cols_for_queries[key] > number)
            elif inequality == '>=':
                results = results.filter(cols_for_queries[key] >= number)
            elif inequality == '<':
                results = results.filter(cols_for_queries[key] < number)
            elif inequality == '<=':
                results = results.filter(cols_for_queries[key] <= number)
            elif inequality == '!=':
                results = results.filter(cols_for_queries[key] != number)
    results = results.all()
    
    return results


def get_substances(db: Session):
    '''
    Function to get all the substances
    '''

    results = db.query(GenericSubstance).all()
    results = pd.DataFrame(query_to_dict(results))
    results.drop(columns=['records'], inplace=True)

    return results


def get_sectors(db: Session):
    '''
    Function to get all the industry sectors
    '''

    results = db.query(GenericSector).all()
    results = pd.DataFrame(query_to_dict(results))
    results.drop(columns=['records'], inplace=True)

    return results


def get_transfer_classes(db: Session):
    '''
    Function to get all the transfer classes
    '''

    results = db.query(GenericTransferClass).all()
    results = pd.DataFrame(query_to_dict(results))
    results.drop(columns=['records'], inplace=True)

    return results


def query_to_dict(rset):
    '''
    Function to convert the query to dicts
    '''

    result = defaultdict(list)
    for obj in rset:
        instance = inspect(obj)
        for key, x in instance.attrs.items():
            result[key].append(x.value)
    return result



