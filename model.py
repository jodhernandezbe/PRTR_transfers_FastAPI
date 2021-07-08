#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Importing libraries
from base import Base

from sqlalchemy import Column, Integer, String, ForeignKey, Float
from sqlalchemy.orm import relationship


class Record(Base):
    __tablename__ = 'record'

    record_id = Column(Integer(), primary_key=True)
    reporting_year = Column(Integer(), nullable=False)
    country = Column(String(3), nullable=False)
    generic_substance_id = Column(String(20),
                                ForeignKey(
                                    'generic_substance.generic_substance_id',
                                    ondelete='CASCADE',
                                    onupdate='cascade'
                                        ),
                                    nullable=False)
    generic_sector_code = Column(Integer(),
                                ForeignKey(
                                    'generic_sector.generic_sector_code',
                                    ondelete='CASCADE',
                                    onupdate='cascade'
                                        ),
                                    nullable=False)
    generic_transfer_class_id = Column(String(3),
                                ForeignKey(
                                    'generic_transfer_class.generic_transfer_class_id',
                                    ondelete='CASCADE',
                                    onupdate='cascade'
                                        ),
                                    nullable=False)
    number_of_facilities = Column(Integer(), nullable=False)
    total_transfer_amount_kg = Column(Float(precision=2), nullable=False)
    average_transfer_amount_kg = Column(Float(precision=2), nullable=False)
    median_transfer_amount_kg = Column(Float(precision=2), nullable=False)
    std_transfer_amount_kg = Column(Float(precision=2), nullable=False)
    max_transfer_amount_kg = Column(Float(precision=2), nullable=False)
    min_transfer_amount_kg = Column(Float(precision=2), nullable=False)

    generic_substance= relationship("GenericSubstance", back_populates="records")
    generic_sector = relationship("GenericSector", back_populates="records")
    generic_transfer_class = relationship("GenericTransferClass", back_populates="records")

    def __init__(self, **kwargs):
        self.record_id = kwargs['record_id']
        self.reporting_year = kwargs['reporting_year']
        self.country = kwargs['country']
        self.generic_substance_id = kwargs['generic_substance_id']
        self.generic_sector_code = kwargs['generic_sector_code']
        self.generic_transfer_class_id = kwargs['generic_transfer_class_id']
        self.number_of_facilities = kwargs['number_of_facilities']
        self.total_transfer_amount_kg = kwargs['total_transfer_amount_kg']
        self.average_transfer_amount_kg = kwargs['average_transfer_amount_kg']
        self.median_transfer_amount_kg = kwargs['median_transfer_amount_kg']
        self.std_transfer_amount_kg = kwargs['std_transfer_amount_kg']
        self.max_transfer_amount_kg = kwargs['max_transfer_amount_kg']
        self.min_transfer_amount_kg = kwargs['min_transfer_amount_kg']


class GenericSubstance(Base):
    __tablename__ = 'generic_substance'

    generic_substance_id = Column(String(20), primary_key=True)
    generic_substance_name = Column(String(300), nullable=False)
    cas_number = Column(String(20), nullable=True)

    records = relationship("Record", back_populates="generic_substance")

    def __init__(self, **kwargs):
        self.generic_substance_id = kwargs['generic_substance_id']
        self.generic_substance_name = kwargs['generic_substance_name']
        self.cas_number = kwargs['cas_number']


class GenericSector(Base):
    __tablename__ = 'generic_sector'

    generic_sector_code = Column(Integer(), primary_key=True)
    generic_sector_name = Column(String(250), nullable=False)

    records = relationship("Record", back_populates="generic_sector")

    def __init__(self, **kwargs):
        self.generic_sector_code = kwargs['generic_sector_code']
        self.generic_sector_name = kwargs['generic_sector_name']


class GenericTransferClass(Base):
    __tablename__ = 'generic_transfer_class'

    generic_transfer_class_id = Column(String(3), primary_key=True)
    generic_transfer_class_name = Column(String(250), nullable=False)
    transfer_class_wm_hierarchy_name = Column(String(20), nullable=False)

    records = relationship("Record", back_populates="generic_transfer_class")

    def __init__(self, **kwargs):
        self.generic_transfer_class_id = kwargs['generic_transfer_class_id']
        self.generic_transfer_class_name = kwargs['generic_transfer_class_name']
        self.transfer_class_wm_hierarchy_name = kwargs['transfer_class_wm_hierarchy_name']
