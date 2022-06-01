
from typing import Optional, List

import pandas as pd
from fastapi import FastAPI
from pydantic import BaseModel

api = FastAPI(
    title='Query Expansion API',
    description='API for expanding search query using relationships captured in an entity graph',
    version='1.0.0'
)
