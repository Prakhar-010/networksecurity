import sys
import os
import pandas as pd
from networksecurity.utils.main_utils.utils import load_object
import certifi
from networksecurity.utils.ml_utils.model.estimator import NetworkModel

ca = certifi.where()

from dotenv import load_dotenv
load_dotenv()
mongo_db_url = os.getenv("MONGODB_URL_KEY")
print(mongo_db_url)

import pymongo
from fastapi import FastAPI, File, UploadFile, Request
from fastapi.responses import Response
from fastapi.middleware.cors import CORSMiddleware
from starlette.responses import RedirectResponse
import uvicorn

from networksecurity.exception.exception import CustomException
from networksecurity.logging.logger import logging
from networksecurity.pipeline.training_pipeline import TrainingPipeline
from networksecurity.constants.training_pipeline import DATA_INGESTION_COLLECTION_NAME, DATA_INGESTION_DATABASE_NAME

client = pymongo.MongoClient(mongo_db_url, tlsCAFile=ca)
database = client[DATA_INGESTION_DATABASE_NAME]
collection = database[DATA_INGESTION_COLLECTION_NAME]

app = FastAPI()
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
from fastapi.templating import Jinja2Templates
templates=Jinja2Templates(directory="./templates")

@app.get("/", tags=["authentication"])
async def index():
    return RedirectResponse(url="/docs")


@app.get("/train")
async def train_route():
    try:
        train_pipeline = TrainingPipeline()
        train_pipeline.run_pipeline()
        return Response("Training is successful")
    except Exception as e:
        raise CustomException(e, sys)
@app.post("/predict")
async def predict_route(request:Request,file:UploadFile=File(...)):
    
    try:
        df = pd.read_csv(file.file)
 
        processor = load_object("final_model/processor.pkl")
        final_model = load_object("final_model/model.pkl")
        network_model = NetworkModel(preprocessor=processor, model=final_model)
 
        y_pred = network_model.predict(df)
        df['predicted_column'] = y_pred
        df.to_csv("prediction_output/outpu.csv")
        table_html = df.to_html(classes='table table-striped')
        return templates.TemplateResponse(
    request=request,
    name="table.html",
    context={"table": table_html}
)
    except Exception as e:
        raise CustomException(e, sys)
 

if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000)