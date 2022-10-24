#!/usr/bin/python3
"""
BaseModel Class of Models Module
"""

import os
import json
import models
from uuid import uuid4, UUID
from datetime import datetime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Float, DateTime

storage_type = os.environ.get('HBNB_TYPE_STORAGE')

"""
    Creates instance of Base if storage type is a database
    If not database storage, uses class Base
"""
if storage_type == 'db':
    Base = declarative_base()
else:
    class Base:
        pass


class BaseModel:
    """
        attributes and functions for BaseModel class
    """

    if storage_type == 'db':
        id = Column(String(60), nullable=False, primary_key=True)
        created_at = Column(DateTime, nullable=False,
                            default=datetime.utcnow())
        updated_at = Column(DateTime, nullable=False,
                            default=datetime.utcnow())

    def __init__(self, *args, **kwargs):
        """instantiation of new BaseModel Class"""
        if kwargs:
            self.__set_attributes(kwargs)
        else:
            self.id = str(uuid4())
            self.created_at = datetime.now()

    def __set_attributes(self, attr_dict):
        """
            private: converts kwargs values to python class attributes
        """
        if 'id' not in attr_dict:
            attr_dict['id'] = str(uuid4())
        if 'created_at' not in attr_dict:
            attr_dict['created_at'] = datetime.now()
        elif not isinstance(attr_dict['created_at'], datetime):
            attr_dict['created_at'] = datetime.strptime(
                attr_dict['created_at'], '%Y-%m-%d %H:%M:%S.%f')
        if 'updated_at' in attr_dict:
            if not isinstance(attr_dict['updated_at'], datetime):
                attr_dict['updated_at'] = datetime.strptime(
                    attr_dict['updated_at'], '%Y-%m-%d %H:%M:%S.%f')
        if storage_type != 'db':
            if attr_dict['__class__']:
                attr_dict.pop('__class__')
        for attr, val in attr_dict.items():
            setattr(self, attr, val)

    def __is_serializable(self, obj_v):
        """
            private: checks if object is serializable
        """
        try:
            obj_to_str = json.dumps(obj_v)
            return obj_to_str is not None and isinstance(obj_to_str, str)
        except:
            return False

    def bm_update(self, name, value):
        """
            updates the basemodel and sets the correct attributes
