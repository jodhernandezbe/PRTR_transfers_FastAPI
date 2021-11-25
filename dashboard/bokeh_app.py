#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Importing libraries
from base import creating_session_engine
from dashboard.tab_1 import creating_tab_1
from config import set_bokeh_port, FASTAPI_PORT, FASTAPI_ADDR, BOKEH_ADDR

import pandas as pd
from bokeh.models.widgets import Tabs
import asyncio
from bokeh.server.server import BaseServer
from bokeh.server.tornado import BokehTornado
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop
from threading import Thread
from bokeh.application import Application
from bokeh.application.handlers import FunctionHandler
from bokeh.server.util import bind_sockets


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
        ON tr.generic_sector_code = gis.generic_sector_code
        ORDER BY gs.generic_substance_name;
        '''

    # Reading the data
    df_transfers = pd.read_sql_query(sql_query_record, Engine)
    df_transfers.sort_values(by='reporting_year', inplace=True)
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

def  get_sockets():
    """bind to available socket in this system
    Returns:
        sockets, port -- sockets and port bind to
    """

    _sockets, _port = bind_sockets('0.0.0.0', 0)
    set_bokeh_port(_port)
    return _sockets, _port


def bk_worker(sockets, bokeh_port):

    asyncio.set_event_loop(asyncio.new_event_loop())

    websocket_origins = [f"{BOKEH_ADDR}:{bokeh_port}", f"{FASTAPI_ADDR}:{FASTAPI_PORT}"]
    _creating_dashboard = Application(FunctionHandler(creating_dashboard))

    bokeh_tornado = BokehTornado({'/bkapp': _creating_dashboard},
                            extra_websocket_origins=websocket_origins,
                            **{'use_xheaders': True})
    bokeh_http = HTTPServer(bokeh_tornado)
    bokeh_http.add_sockets(sockets)

    server = BaseServer(IOLoop.current(), bokeh_tornado, bokeh_http)
    server.start()
    server.io_loop.start()


if __name__ == '__main__':

    BK_SOCKETS, BK_PORT = get_sockets()

    t = Thread(target=bk_worker, args=[BK_SOCKETS, BK_PORT], daemon=True)
    t.start()
