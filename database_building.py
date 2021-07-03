#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Importing libraries
from model import Record, GenericSubstance, GenericSector, GenericTransferClass
from base import Session, Engine

import yaml
import os
from zipfile import ZipFile
import logging
import pandas as pd
logging.basicConfig(level=logging.INFO)

dir_path = os.path.dirname(os.path.realpath(__file__)) # current directory path


def config(filepath):
    '''
    Function to load yaml files with information needed for transforming the data
    '''

    with open(filepath,
                mode='r') as f:
        file = yaml.load(f, Loader=yaml.FullLoader)

    return file


def calling_transformed_files(csv_from_path=['npi', 'npri', 'tri']):
    '''
    Function to call and concatenate all PRTRs or calling other files
    '''

    input_path = f'{dir_path}/input/input.zip'
    with ZipFile(input_path) as input_zip:

        df = pd.DataFrame()
        for file in csv_from_path:
            data = input_zip.open(f'{file}.csv')
            df_u = pd.read_csv(data, dtype={'national_substance_id': object})
            df = pd.concat([df, df_u],
                            axis=0, ignore_index=True)
            del df_u

    return df


def organizing_database_tables():
    '''
    Function to organize the tables for the PRTR_transfers_summary database
    '''

    dfs = {}

    # Calling columns for using and their names
    db_normalization_path = f'{dir_path}/input/database_tables.yaml'
    db_normalization = config(db_normalization_path)['table']

    # Calling PRTR systems
    prtr = calling_transformed_files()
    country_to_prtr = {'USA': 'TRI', 'AUS': 'NPI', 'CAN': 'NPRI'}
    prtr['prtr_system'] = prtr.country.apply(lambda x: country_to_prtr[x])
    country_to_ics = {'USA': 'USA_NAICS', 'AUS': 'ANZSIC', 'CAN': 'CAN_NAICS'}
    prtr['industry_classification_system'] = prtr.country.apply(lambda x: country_to_ics[x])
    prtr.drop(columns=['cas_number', 'national_substance_name'], inplace=True)
    prtr_columns = list(prtr.columns)

    # Calling sectors
    sector = calling_transformed_files(csv_from_path=['national_to_generic_sector'])

    # Calling substances
    substance = calling_transformed_files(csv_from_path=['national_to_generic_substance'])

    # Calling transfer classes
    t_class = calling_transformed_files(csv_from_path=['national_to_generic_transfer'])
    t_class = t_class[pd.notnull(t_class.generic_transfer_class_id)]
    # Merging dataframes
    mergings = [
                [sector, ['national_sector_code', 'industry_classification_system']],
                [t_class, ['national_transfer_class_name', 'prtr_system']],
                [substance, ['national_substance_id', 'prtr_system']]
                ]
    del sector, substance, t_class
    for merging in mergings:
        prtr = pd.merge(prtr, merging[0], how='left', on=merging[1])
    del mergings
    prtr.drop_duplicates(keep='first', subset=prtr_columns, inplace=True)
    prtr = prtr.where(pd.notnull(prtr), None)
    prtr['cas_number'] = prtr['cas_number'].fillna('-')

    # Creating 'national_facility_country' (provisional)
    grouping = ['country', 'national_facility_id']
    prtr['national_facility_country_id'] = pd.Series(prtr.groupby(grouping).ngroup() + 1)

    # Selecting columns of interest
    unique_fields = set([value for values in db_normalization.values() for value in values['cols']])
    intersection = list(unique_fields & set(prtr.columns))
    intersection += ['national_facility_country_id', 'transfer_amount_kg']    
    prtr = prtr[intersection]

    # Summing facility records
    grouping = [col for col in prtr.columns if col not in ['transfer_amount_kg']]
    prtr = prtr.groupby(grouping, as_index=False).sum()
    prtr.reset_index(inplace=True, drop=True)

    # Obtaining the other values
    grouping = [col for col in prtr.columns if col not in
        ['transfer_amount_kg', 'national_facility_country_id']]
    prtr.drop(columns=['national_facility_country_id'], inplace=True)
    prtr['number_of_facilities'] = 1
    prtr = prtr.groupby(grouping, as_index=False)\
        .agg(number_of_facilities=('number_of_facilities', 'sum'),
            total_transfer_amount_kg=('transfer_amount_kg', 'sum'),
            average_transfer_amount_kg=('transfer_amount_kg', 'mean'),
            median_transfer_amount_kg=('transfer_amount_kg', 'median'),
            std_transfer_amount_kg=('transfer_amount_kg', 'std'),
            max_transfer_amount_kg=('transfer_amount_kg', 'max'),
            min_transfer_amount_kg=('transfer_amount_kg', 'min'))
    prtr['std_transfer_amount_kg'] = prtr['std_transfer_amount_kg'].fillna(0)
    float_columns = prtr.select_dtypes(include=['float64']).columns
    prtr[float_columns] = prtr[float_columns].round(2)
    prtr.reset_index(drop=True, inplace=True)
    prtr['record_id'] = pd.Series(list(range(1, prtr.shape[0] + 1)))

    # Creating individual tables
    for table, params in db_normalization.items():
        df_table = prtr[params['cols']]
        df_table = df_table.drop_duplicates(keep='first', subset=params['key']).reset_index(drop=True)
        dfs.update({table: df_table})

    return dfs


def loading_data(dfs, logger):
    '''
    Function to load the data into the database
    '''

    # Dictionary to associate each table file with each table in the SQL database
    Dic_tables = {'generic_sector': GenericSector,
                'generic_substance': GenericSubstance,
                'generic_transfer_class': GenericTransferClass,
                'record': Record}

    for filename in reversed(list(Dic_tables.keys())):
        Object = Dic_tables[filename]
        Object.__table__.drop(Engine, checkfirst=True)

    # Saving each table
    for filename, Object in Dic_tables.items():
        Object.__table__.create(Engine, checkfirst=True)
        session = Session()
        logger.info(f' Loading table {filename} into the PRTR_transfers_summary database')
        # Saving each record by table
        for _, row in dfs[filename].iterrows():
            context = row.to_dict()
            instance = Object(**context)
            session.add(instance)
        session.commit()
        session.close()


def main():
    '''
    Function to run the procedure that builds the PRTR_transfers_summary database 
    '''

    logger = logging.getLogger('Building the PRTR_transfers_summary database')
    
    # Organizing the normalized schema for the database
    logger.info(f'Normalizing the schema for the database from input data')
    dfs = organizing_database_tables()

    # Persisting the data into the database
    logger.info(f'Creating the database schema and loading the data')
    loading_data(dfs, logger)


if __name__ == '__main__':
    main()