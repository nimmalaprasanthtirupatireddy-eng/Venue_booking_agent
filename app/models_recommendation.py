from typing import Optional
from pydantic import BaseModel


class RestaurantPreference(BaseModel):
    location: Optional[str] = None
    cuisine: Optional[str] = None
    budget: Optional[str] = None
    min_rating: Optional[float] = None
    dietary: Optional[str] = None
    ambience: Optional[str] = None


class SelectedRestaurant(BaseModel):
    id: Optional[str] = None
    name: Optional[str] = None
    phone: Optional[str] = None