#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Importing libraries
from base import creating_session_engine
from tab_1 import creating_tab_1
from tab_2 import creating_tab_2
from tab_3 import creating_tab_3

import pandas as pd
from bokeh.models.widgets import Tabs
from bokeh.io import curdoc


def open_dataframe():
    '''
    Function to open the database
    '''

    # Creating engine
    Engine, _ = creating_session_engine()

    # SQL Query (SQLite)
    sql_query_record = '''
        SELECT  tr.reporting_year,
                tr.country,
                (tr.generic_sector_code || " : " || gis.generic_sector_name ) AS generic_sector,
                (tr.generic_substance_id || " : " || gs.generic_substance_name ) AS generic_substance,
                (tr.generic_transfer_class_id || " : " || gtc.generic_transfer_class_name ) AS generic_transfer_class,
                gtc.transfer_class_wm_hierarchy_name,
                tr.total_transfer_amount_kg,
                tr.number_of_facilities
        FROM record AS tr
        INNER JOIN generic_substance AS gs
        ON tr.generic_substance_id = gs.generic_substance_id
        INNER JOIN generic_transfer_class AS gtc
        ON tr.generic_transfer_class_id = gtc.generic_transfer_class_id
        INNER JOIN generic_sector AS gis
        ON tr.generic_sector_code = gis.generic_sector_code
        ORDER BY gs.generic_substance_id AND tr.reporting_year;
        '''

    df = pd.concat([chunk for chunk in pd.read_sql_query(sql_query_record, Engine, chunksize=10000)])
    
    grouping_cols = ['reporting_year',
                    'country', 'generic_sector',
                    'generic_transfer_class',
                    'transfer_class_wm_hierarchy_name']

    df_rows = df.groupby(grouping_cols,
                    as_index=False)[['total_transfer_amount_kg', 'number_of_facilities']].sum()
    df_rows['generic_substance'] = 'All'
    df = pd.concat([df_rows, df])
    del df_rows

    return df


def creating_dashboard():
    '''
    Function to create the dashboard
    '''

    df_transfers = open_dataframe()
    df_transfers['reporting_year'] = df_transfers['reporting_year'].apply(lambda x: str(x))
    substances = df_transfers['generic_substance'].unique().tolist()
    countries = df_transfers['country'].unique().tolist()
    waste_managements = df_transfers['transfer_class_wm_hierarchy_name'].unique().tolist()
    transfer_classes = df_transfers['generic_transfer_class'].unique().tolist()
    transfer_classes.sort()
    years = df_transfers['reporting_year'].unique().tolist()

    # Creating each of the tabs
    tab1 = creating_tab_1(df_transfers, substances, countries,
                        waste_managements, years)
    tab2 = creating_tab_2(df_transfers, substances, countries,
                        transfer_classes, years)
    tab3 = creating_tab_3(df_transfers, substances, countries,
                        years)

    # Put all the tabs into one application
    tabs = Tabs(tabs=[tab1, tab2, tab3])


    curdoc().add_root(tabs)


# Running the dashboard
creating_dashboard()