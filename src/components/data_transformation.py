# Import necessary libraries and modules
import sys  # For system-specific parameters and functions
from dataclasses import dataclass  # For creating classes with automatically added special methods

# Import data manipulation and machine learning libraries
import numpy as np  # For numerical operations
import pandas as pd  # For data manipulation and analysis
from sklearn.compose import ColumnTransformer  # For applying different transformations to different columns
from sklearn.impute import SimpleImputer  # For handling missing values
from sklearn.pipeline import Pipeline  # For chaining multiple steps that can be cross-validated together
from sklearn.preprocessing import OneHotEncoder, StandardScaler  # For encoding categorical variables and scaling features

# Import custom exception and logging modules
from src.exception import CustomException  # Custom exception class for error handling
from src.logger import logging  # Custom logging module
import os  # For interacting with the operating system

# Import utility function for saving objects
from src.utils import save_object  # Custom function to save Python objects

# Configuration class for data transformation
@dataclass
class DataTransformationConfig:
    # Path to save the preprocessor object
    preprocessor_obj_file_path = os.path.join('artifacts', "preprocessor.pkl")  # Define the path to save the preprocessor object

# Main class for data transformation
class DataTransformation:
    def __init__(self):
        # Initialize with the configuration
        self.data_transformation_config = DataTransformationConfig()

    def get_data_transformer_object(self):
        '''
        This function creates and returns a data transformer object
        '''
        try:
            # Define numerical and categorical columns
            numerical_columns = ["writing_score", "reading_score"]  # List of numerical feature columns
            categorical_columns = [  # List of categorical feature columns
                "gender",
                "race_ethnicity",
                "parental_level_of_education",
                "lunch",
                "test_preparation_course"
            ] 
            
            # Create pipeline for numerical columns
            num_pipeline = Pipeline(
                steps = [
                    ('imputer', SimpleImputer(strategy="median")),  # Handle missing values with median
                    ('scaler', StandardScaler())  # Standardize the numerical features
                ]
            )

            # Create pipeline for categorical columns
            cat_pipeline = Pipeline(
                steps = [
                    ('imputer', SimpleImputer(strategy="most_frequent")),  # Handle missing values with mode
                    ('one_hot_encoder', OneHotEncoder(sparse_output=False)),  # Perform one-hot encoding
                    ('scaler', StandardScaler())  # Standardize the encoded features
                ]
            )
            
            logging.info("Categorical columns encoding completed")  # Log the completion of categorical encoding

            # Combine numerical and categorical pipelines
            preprocessor = ColumnTransformer(
                transformers=[
                    ('num_pipeline', num_pipeline, numerical_columns),  # Apply num_pipeline to numerical columns
                    ('cat_pipeline', cat_pipeline, categorical_columns)  # Apply cat_pipeline to categorical columns
                ]
            )
            
            return preprocessor  # Return the complete preprocessor object

        except Exception as e:
            # If an exception occurs, raise a custom exception with details
            raise CustomException(e, sys)
        
    def initiate_data_transformation(self, train_path, test_path):
        try:
            # Read train and test data from CSV files
            train_df = pd.read_csv(train_path)  # Read training data
            test_df = pd.read_csv(test_path)  # Read testing data

            logging.info("Read train and test data completed")  # Log the completion of data reading
            logging.info("Obtaining preprocessing object")  # Log the start of obtaining preprocessing object

            preprocessing_obj = self.get_data_transformer_object()  # Get the preprocessor object

            target_column_name = "math_score"  # Define the target column name
            numerical_columns = ["writing_score", "reading_score"]  # Define numerical columns

            # Separate features and target for training data
            input_feature_train_df = train_df.drop(columns=[target_column_name], axis=1)  # Features
            target_feature_train_df = train_df[target_column_name]  # Target

            # Separate features and target for testing data
            input_feature_test_df = test_df.drop(columns=[target_column_name], axis=1)  # Features
            target_feature_test_df = test_df[target_column_name]  # Target

            logging.info("Applying preprocessing object on training and testing dataframe")  # Log the start of preprocessing

            # Apply preprocessing
            input_feature_train_arr = preprocessing_obj.fit_transform(input_feature_train_df)  # Fit and transform training data
            input_feature_test_arr = preprocessing_obj.transform(input_feature_test_df)  # Transform testing data

            # Combine features and target
            train_arr = np.c_[input_feature_train_arr, np.array(target_feature_train_df)]  # For training data
            test_arr = np.c_[input_feature_test_arr, np.array(target_feature_test_df)]  # For testing data

            logging.info("Saved preprocessing object")  # Log the completion of preprocessing

            # Save the preprocessing object
            save_object(
                file_path=self.data_transformation_config.preprocessor_obj_file_path,  # Path to save
                obj=preprocessing_obj  # Object to save
            )

            return (
                train_arr,  # Transformed training data
                test_arr,  # Transformed testing data
                self.data_transformation_config.preprocessor_obj_file_path  # Path of saved preprocessor object
            )

        except Exception as e:
            # If an exception occurs, raise a custom exception with details
            raise CustomException(e, sys)