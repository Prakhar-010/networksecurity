import os
os.environ["OPENBLAS_NUM_THREADS"] = "1"
os.environ["OMP_NUM_THREADS"] = "1"
os.environ["MKL_NUM_THREADS"] = "1"

from networksecurity.components.data_ingestion import DataIngestion
import sys
from networksecurity.exception.exception import CustomException
from networksecurity.logging.logger import logging
from networksecurity.entity.config_entity import DataIngestionConfig, DataValidationConfig
from networksecurity.entity.config_entity import TrainingPipelineConfig
from networksecurity.components.data_validation import DataValidation
from networksecurity.entity.artifact_entity import DataIngestionArtifact

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

    except Exception as e:
        raise CustomException(e, sys)