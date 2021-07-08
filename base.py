#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Importing libraries
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

Base = declarative_base()
dir_path = os.path.dirname(os.path.realpath(__file__)) # current directory path

def creating_session_engine(check_same_thread=True):
    '''
    Function to create SQLite session and engine
    '''

    Engine = create_engine(f'sqlite:///{dir_path}/output/PRTR_transfers_summary.db',
                        connect_args={"check_same_thread": check_same_thread})

    Session = sessionmaker(bind=Engine, autocommit=False, autoflush=False)

    return Engine, Session