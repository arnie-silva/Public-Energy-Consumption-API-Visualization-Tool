from fastapi import APIRouter
from app.models.schemas import Item
from app.fetch_data import df
from fastapi.responses import JSONResponse

router = APIRouter()

@router.get("/")
def read_root():
    return {"message": "Please enter state code at the end of the backslash to receive state specific data"}

@router.get("/{state_id}")
def read_state(state_id: str):
    filtered_df = df[df["location"] == state_id]
    filtered_df = filtered_df[["stateDescription","fuelTypeDescription","consumption-for-eg-btu","total-consumption-btu"]]
    filtered_df = filtered_df.rename(columns={
    'stateDescription': 'State',
    'fuelTypeDescription': 'Fuel Type',
    'consumption-for-eg-btu': 'Consumption for Electric Generation (MMBtu)',
    'total-consumption-btu': 'Total Consumption (MMBtu)'
    })
    data_json = filtered_df.to_dict(orient='records')
    return JSONResponse(content=data_json)

@router.post("/items/")
def create_item(item: Item):
    return {"received_item": item}