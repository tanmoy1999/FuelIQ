from pydantic import BaseModel
from datetime import date

class FuelData(BaseModel):
    date: date
    fuel_price: float
    amount: float
    total_distance_covered: float
    fuel_filled: float
    full_tank_flag: bool


