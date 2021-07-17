#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Importing libraries
import pandas as pd
from base import creating_session_engine
from dashboard.tab_1 import creating_tab_1

from bokeh.models.widgets import Tabs

def creating_dashboard(doc):
    '''
    Function to create the dashboard
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
                tr.total_transfer_amount_kg
        FROM record AS tr
        INNER JOIN generic_substance AS gs
        ON tr.generic_substance_id = gs.generic_substance_id
        INNER JOIN generic_transfer_class AS gtc
        ON tr.generic_transfer_class_id = gtc.generic_transfer_class_id
        INNER JOIN generic_sector AS gis
        ON tr.generic_sector_code = gis.generic_sector_code;
        '''

    # Reading the data
    df_transfers = pd.read_sql_query(sql_query_record, Engine)
    df_transfers['reporting_year'] = df_transfers['reporting_year'].apply(lambda x: str(x))

    substances = df_transfers['generic_substance'].unique().tolist()
    countries = df_transfers['country'].unique().tolist()
    waste_managements = df_transfers['transfer_class_wm_hierarchy_name'].unique().tolist()
    years = df_transfers['reporting_year'].unique().tolist()

    # Creating each of the tabs
    tab1 = creating_tab_1(df_transfers, substances, countries,
                        waste_managements, years)

    # Put all the tabs into one application
    tabs = Tabs(tabs=[tab1])


    doc.add_root(tabs)
