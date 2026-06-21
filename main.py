import os
os.environ["OPENBLAS_NUM_THREADS"] = "1"
os.environ["OMP_NUM_THREADS"] = "1"
os.environ["MKL_NUM_THREADS"] = "1"

from networksecurity.components.data_ingestion import DataIngestion
import sys
from networksecurity.exception.exception import CustomException
from networksecurity.logging.logger import logging
from networksecurity.entity.config_entity import DataIngestionConfig, DataValidationConfig,DataTransformationConfig,ModelTrainerConfig
from networksecurity.entity.config_entity import TrainingPipelineConfig
from networksecurity.components.data_validation import DataValidation
from networksecurity.components.data_transformation import DataTransformation
from networksecurity.entity.artifact_entity import DataIngestionArtifact
from networksecurity.components.model_trainer import ModelTrainer
if __name__ == "__main__":
    try:
        trainingpipelineconfig = TrainingPipelineConfig()  # ✅ this line was missing

        # Data Ingestion
        dataingestionconfig = DataIngestionConfig(trainingpipelineconfig)
        data_ingestion = DataIngestion(dataingestionconfig)
        dataingestionartifact = data_ingestion.initiate_data_ingestion()
        print(dataingestionartifact)

        # Data Validation
        datavalidationconfig = DataValidationConfig(trainingpipelineconfig)
        data_vaidation = DataValidation(dataingestionartifact, datavalidationconfig)
        data_vaidation_artifact = data_vaidation.initiate_data_validation()
        print(data_vaidation_artifact)
        
        #Data transformation
        datatransformationconfig=DataTransformationConfig(trainingpipelineconfig)
        data_transformation=DataTransformation(data_vaidation_artifact , datatransformationconfig)
        data_transformation_artifact=data_transformation.initiate_data_transformation()
        print(data_transformation_artifact)
        
        
        logging.info("Model Training sstared")
        model_trainer_config = ModelTrainerConfig(trainingpipelineconfig)
        model_trainer = ModelTrainer(model_trainer_config=model_trainer_config, data_transformation_artifact=data_transformation_artifact)
        model_trainer_artifact = model_trainer.initiate_model_trainer()

        logging.info("Model Training artifact created")
    except Exception as e:
        raise CustomException(e, sys)