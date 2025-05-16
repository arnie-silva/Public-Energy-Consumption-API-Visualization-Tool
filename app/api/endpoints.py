from fastapi import APIRouter
from models.schemas import Item
from fetch_data import df
from fastapi.responses import JSONResponse
import torch
import torch.nn as nn
import torch.optim as optim

router = APIRouter()

class EnergyPredictor(nn.Module):
        def __init__(self):
                super(EnergyPredictor, self).__init__()
                self.linear = nn.Linear(1,1)
        
        def forward(self, x):
                return self.linear(x)
model = EnergyPredictor()

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

@router.get("/predict/{state_id}/{year}")
def predict(state_id: str, year: int):
    X = torch.tensor(df[(df['fueltypeid'] == 'ALL') & (df['location'] == state_id)]['year'].values, dtype=torch.float32)
    y = torch.tensor(df[(df['fueltypeid'] == 'ALL') & (df['location'] == state_id)]['total-consumption-btu'].values, dtype=torch.float32)
    criterion = nn.MSELoss()
    optimizer = optim.SGD(model.parameters(), lr=0.01)

    for epoch in range(100):
        model.train()
        output = model(X)
        loss = criterion(output, y)
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

    with torch.no_grad():
        input_tensor = torch.tensor([[year]], dtype=torch.float32)
        prediction = model(input_tensor).item()
    return {"predicted_value": prediction}

@router.post("/items/")
def create_item(item: Item):
    return {"received_item": item}
