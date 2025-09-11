# -*- coding: utf-8 -*-
"""
---------------------------------------------------------------------------------------------------
    Written by      : Rob Lewis

    Date            : 07SEP2025

    Purpose         : Store all main imports in one place

    Dependencies    :

    Program name    : imports

    Modifications
    -------------
    07SEP2025   RLEWIS  Initial Version
---------------------------------------------------------------------------------------------------
"""


# ---------------
# --- Imports ---
# ---------------

import pandas as pd                 # For data manipulation
import numpy  as np                 # For scientific calculations
import requests                     # For making HTTP requests
import xml.etree.ElementTree as ET  # For parsing XML files
import logging                      # For creating logs

from google.cloud import storage    # For interacting with Google Cloud Storage (GCS)
from datetime     import datetime, date, timedelta   # For generating dates
from dateutil.relativedelta import relativedelta     # For working with timedeltas