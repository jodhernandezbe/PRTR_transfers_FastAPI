#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Importing libraries
from fastapi_app import start_uvicorn
from dashboard.bokeh_app import get_sockets, bk_worker
from config import BOKEH_URL, FASTAPI_URL

from threading import Thread


def run():
    '''
    Run PRTR_transfers_summary
    '''

    # get sockets, so bkapp and app can talk
    bk_sockets, bk_port = get_sockets()

    # start bokeh sever
    thread_bokeh = Thread(target=bk_worker, args=[bk_sockets, bk_port], daemon=True)
    thread_bokeh.start()

    # start fastapi
    start_uvicorn()

if __name__ == '__main__':
    run()