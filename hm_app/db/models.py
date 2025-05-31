from sqlalchemy import String, Integer, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from hm_app.db.database import Base
from typing import Optional, List
from passlib.hash import bcrypt
from datetime import datetime


class UserProfile(Base):
    __tablename__ = 'user_profile'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    username: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    firstname: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    email: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    phone_number: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    age: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    password: Mapped[str] = mapped_column(String, nullable=False)

    user_houses: Mapped[List['House']] = relationship('House', back_populates='user',
                                                      cascade='all, delete-orphan')

    def set_passwords(self, password: str):
        self.password = bcrypt.hash(password)

    def check_password(self, password: str):
        return bcrypt.verify(password, self.password)


class House(Base):
    __tablename__ = 'house'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    total_live_area: Mapped[int] = mapped_column(Integer)
    built_year: Mapped[int] = mapped_column(Integer)
    garage_cars: Mapped[int] = mapped_column(Integer)
    basement_area: Mapped[int] = mapped_column(Integer)
    full_bath: Mapped[int] = mapped_column(Integer)
    quality_level: Mapped[int] = mapped_column(Integer)
    region: Mapped[Optional[str]] = mapped_column(String, unique=True, nullable=True)
    price: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('user_profile.id'))
    user: Mapped['UserProfile'] = relationship('UserProfile', back_populates='user_houses')


class RefreshToken(Base):
    __tablename__ = 'refresh_token'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    token: Mapped[str] = mapped_column(String, nullable=False)
    created_date: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    user_id: Mapped[int] = mapped_column(ForeignKey('user_profile.id'))
    user: Mapped['UserProfile'] = relationship('UserProfile')


