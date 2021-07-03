#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Importing libraries
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

dir_path = os.path.dirname(os.path.realpath(__file__)) # current directory path

Engine = create_engine(f'sqlite:///{dir_path}/output/PRTR_transfers_summary.db')

Session = sessionmaker(bind=Engine)

Base = declarative_base()