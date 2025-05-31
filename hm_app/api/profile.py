from hm_app.db.models import UserProfile
from hm_app.db.schema import UserProfileSchema
from hm_app.db.database import SessionLocal
from fastapi import APIRouter, Depends, HTTPException
from typing import List
from sqlalchemy.orm import Session


user = APIRouter(prefix='/user', tags=['Users'])

async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@user.put('/{user_id}/', response_model=UserProfileSchema)
async def user_update(user_id: int, user: UserProfileSchema, db: Session = Depends(get_db)):
    user_db = db.query(UserProfile).filter(UserProfile.id == user_id).first()
    if not user_db:
        raise HTTPException(status_code=400, detail='User not found')

    for user_key, user_value in user.dict().items():
        setattr(user_db, user_key, user_value)

    db.add(user_db)
    db.commit()
    db.refresh(user_db)
    return user_db


@user.delete('/{user_id}/', response_model=dict)
async def user_delete(user_id: int, db: Session = Depends(get_db)):
    user_db = db.query(UserProfile).filter(UserProfile.id == user_id).first()
    if not user_db:
        raise HTTPException(status_code=404, detail='User not found')

    db.delete(user_db)
    db.commit()
    return {'message': 'Deleted'}

@user.get('/user/', response_model=List[UserProfileSchema])
async def users_list(db: Session = Depends(get_db)):
    return db.query(UserProfile).all()


@user.get('/{user_id}/', response_model=UserProfileSchema)
async def user_detail(user_id: int, db: Session = Depends(get_db)):
    user_db = db.query(UserProfile).filter(UserProfile.id == user_id).first()
    if not user_db:
        raise HTTPException(status_code=404, detail='User not found')
    return user_db


