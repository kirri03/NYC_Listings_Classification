from fastapi import FastAPI
import pandas as pd

from pydantic import BaseModel as PydanticBaseModel

from typing import Optional

from sqlalchemy import Column, Integer, String, Float, func, create_engine, Sequence
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "sqlite:///./nyc_data.db"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class BaseModel(PydanticBaseModel):
    class Config:
        arbitrary_types_allowed = True

class NYCListing(BaseModel):
    id:int
    name:Optional[str]
    neighbourhood_group:str
    neighbourhood:str
    latitude:float
    longitude:float
    room_type:str
    price:float


class NYCListingSQL(Base):
    __tablename__ = "nyc_listings"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    host_id = Column(Integer)
    host_name = Column(String)
    neighbourhood_group = Column(String)
    neighbourhood = Column(String)
    latitude = Column(Float)
    longitude = Column(Float)
    room_type = Column(String)
    price = Column(Float)


class AppReview(BaseModel):
    id_review:Optional[int] # puesto que ya se genera automaticamente y no se lo vamos a enviar
    email:str
    rating: int
    comment: Optional[str] = None

class ReviewSQL(Base):
    __tablename__ = "reviews"

    id_review = Column(Integer, Sequence('id_review_seq'), primary_key=True, index=True, autoincrement=True)
    email = Column(String)
    rating = Column(Integer)
    comment = Column(String)

Base.metadata.create_all(bind=engine)

# Insertamos datos si la tabla está vacía
def populate_nyc_data():
    session = SessionLocal()
    # Verificamos que esté vacía
    if session.query(NYCListingSQL).first() is None:
        # Inserta datos en la tabla nyc_listings
        data_nyc = pd.read_csv('nyc.csv')
        listings_data = data_nyc.to_dict(orient='records')
        session.bulk_insert_mappings(NYCListingSQL, listings_data)

        session.commit()
        session.close()

populate_nyc_data()


app = FastAPI(
    title="Servidor de datos",
    description="""Servimos datos de contratos, pero podríamos hacer muchas otras cosas, la la la.""",
    version="0.1.0",
)

data = pd.read_csv('./nyc.csv',sep=',')

@app.get("/retrieve_data/")
async def retrieve_data():
    session = SessionLocal()
    colselec = ['id', 'name', 'neighbourhood_group', 'neighbourhood', 'latitude', 'longitude', 'room_type', 'price']
    all_data = session.query(NYCListingSQL).with_entities(*[getattr(NYCListingSQL, col) for col in colselec]).limit(5000).all()
    session.close()

    return [NYCListing(**row._asdict()) for row in all_data]

@app.get("/retrieve_tarjetas/")
def retrieve_tarjetas():
    session = SessionLocal()

    # Obtenemos precios mínimo y máximo
    min_price = session.query(func.min(NYCListingSQL.price)).scalar()
    max_price = session.query(func.max(NYCListingSQL.price)).scalar()

    # Obtenemos precios promedio por cada vecindario
    neighborhoods = ["Brooklyn", "Manhattan", "Queens", "Bronx", "Staten Island"]
    average_prices = {}
    for neighborhood in neighborhoods:
        avg_price = session.query(func.avg(NYCListingSQL.price)).filter_by(neighbourhood_group=neighborhood).scalar()
        average_prices[neighborhood] = f"{round(avg_price, 2)} $"

    session.close()

    # Formateamos la respuesta
    minimo = f"{min_price} $"
    maximo = f"{max_price} $"
    mediabrooklyn = average_prices.get("Brooklyn")
    mediamanhattan = average_prices.get("Manhattan")
    mediaqueens = average_prices.get("Queens")
    mediabronx = average_prices.get("Bronx")
    mediastaten = average_prices.get("Staten Island")

    listado = [minimo, maximo, mediabrooklyn, mediamanhattan, mediaqueens, mediabronx, mediastaten]
    return listado

@app.post("/submit_review")
def submit_review(review: AppReview):
    new_review = ReviewSQL(email=review.email, rating=review.rating, comment=review.comment)
    session = SessionLocal()
    session.add(new_review)
    session.commit()
    session.close()
    
    return "Reseña de la aplicación enviada exitosamente"

@app.get("/retrieve_reviews/")
def retrieve_reviews():
    session = SessionLocal()
    reviews = session.query(ReviewSQL).all()
    session.close()
    
    return reviews