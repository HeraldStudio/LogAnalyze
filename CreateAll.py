#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
 Create On: November 01, 2016
    Author: corvo
"""

from databases.tables import Base, DayLogAnalyze
from databases.db import engine

Base.metadata.create_all(engine) #create all of Class which belonged to Base Class
