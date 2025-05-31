from fastapi import APIRouter, Depends, HTTPException
from hm_app.db.models import House, UserProfile
from hm_app.db.schema import HouseSchema, HouseListSchema
from hm_app.db.database import SessionLocal
from sklearn.preprocessing import StandardScaler
from sqlalchemy.orm import Session
from typing import List
from pathlib import Path
import joblib 
import numpy as np #np import
import pandas as pd #pd import 


house_router = APIRouter(prefix='/house', tags=['Houses'])

BASE_DIR = Path(__file__).resolve().parent.parent.parent

model_path = BASE_DIR / 'house_price_model_job.pkl'  
scaler_path = BASE_DIR / 'scaler.pkl'  

model = joblib.load(model_path)
scaler = joblib.load(scaler_path)

async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@house_router.post('/', response_model=HouseSchema)
async def house_create(house: HouseSchema, db: Session = Depends(get_db)):
    user_db = db.query(UserProfile).filter(UserProfile.id == house.user_id).first()
    if not user_db:
        raise HTTPException(status_code=404, detail='User not found')

    house_db = House(**house.dict())
    db.add(house_db)
    db.commit()
    db.refresh(house_db)
    return house
 
@house_router.get('/', response_model=List[HouseListSchema])                    
async def house_list(db: Session = Depends(get_db)):
    return db.query(House).all()

@house_router.get('/{house_id}/', response_model=HouseSchema)
async def house_detail(house_id: int, db: Session = Depends(get_db)):
    house_db = db.query(House).filter(House.id == house_id).first()
    if not house_db:
        raise HTTPException(status_code=404, detail='House not found')
    return house_db

@house_router.put('/{house_id}/', response_model=HouseSchema)
async def house_update(house_id: int, house: HouseSchema, db: Session = Depends(get_db)):
    house_db = db.query(House).filter(House.id == house_id).first()
    if not house_db:
        raise HTTPException(status_code=404, detail='House not found')

    for house_key, house_value in house.dict().items():
        setattr(house_db, house_key, house_value)

    db.add(house_db)
    db.commit()
    db.refresh(house_db)
    return house_db

model_columns = [
    'GrLivArea',
    'FullBath',
    'OverallQual'
    'YearBuilt',
    'GarageCars',
    'TotalBsmtSF'
]


@house_router.post('/predict/')
async def predict_price(house: HouseSchema, db: Session = Depends(get_db)):
    input_data = {
        'GrLivArea': house.total_live_area,
        'TotalBsmtSF': house.basement_area,
        'YearBuilt': house.built_year,
        'GarageCars': house.garage_cars,
        'FullBath': house.full_bath,
        'OverallQual': house.quality_level
    }
    input_df = pd.DataFrame([input_data])
    scaled_df = scaler.transform(input_df)
    predicted_price = model.predict(scaled_df)[0]

#print func
    print(model.predict(scaled_df))
    return {'predicted_price': round(predicted_price)}


@house_router.delete('/{house_id}/', response_model=dict)
async def house_delete(house_id: int, db: Session = Depends(get_db)):
    house_db = db.query(House).filter(House.id == house_id).first()
    if not house_db:
        raise HTTPException(status_code=404, detail='House not found')

    db.delete(house_db)
    db.commit()
    return {'message': 'Deleted'}
