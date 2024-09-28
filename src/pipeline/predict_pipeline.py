import sys
import pandas as pd
from src.exception import CustomException  # Import custom exception handling class
from src.utils import load_object  # Import utility function to load objects (e.g., model, preprocessor)

class PredictPipeline:
    def __init__(self):
        pass  # The constructor is currently empty, but it's set up for potential future extensions

    def predict(self, features):
        """
        This method loads the trained model and preprocessor, scales the input features,
        and makes predictions based on the input data.
        """
        try:
            # Define paths to the saved model and preprocessor objects
            model_path = 'artifacts\model.pkl'
            preprocessor_path = 'artifacts\preprocessor.pkl'
            
            # Load the model and preprocessor from their respective files
            model = load_object(file_path=model_path)
            preprocessor = load_object(file_path=preprocessor_path)
            
            # Scale the input features using the preprocessor
            data_scaled = preprocessor.transform(features)
            
            # Use the model to make predictions on the scaled data
            preds = model.predict(data_scaled)
            return preds  # Return the predictions

        except Exception as e:
            # If an error occurs, raise a custom exception with the error message and system info
            raise CustomException(e, sys)

class CustomData:
    """
    This class is responsible for mapping all the inputs from an HTML form to 
    corresponding backend values, storing them as attributes, and converting them to a DataFrame.
    """
    
    def __init__(self,
                 gender: str,
                 race_ethnicity: str,
                 parental_level_of_education,
                 lunch: str,
                 test_preparation_course: str,
                 reading_score: int,
                 writing_score: int):
        # Initialize the class with the input values
        self.gender = gender
        self.race_ethnicity = race_ethnicity
        self.parental_level_of_education = parental_level_of_education
        self.lunch = lunch
        self.test_preparation_course = test_preparation_course
        self.reading_score = reading_score
        self.writing_score = writing_score

    def get_data_as_data_frame(self):
        """
        This method converts the instance attributes into a pandas DataFrame,
        which can be used as input for the prediction pipeline.
        """
        try:
            # Create a dictionary with the input data, each key corresponds to a column name in the DataFrame
            custom_data_input_dict = {
                "gender": [self.gender],
                "race_ethnicity": [self.race_ethnicity],
                "parental_level_of_education": [self.parental_level_of_education],
                "lunch": [self.lunch],
                "test_preparation_course": [self.test_preparation_course],
                "reading_score": [self.reading_score],
                "writing_score": [self.writing_score]
            }
            
            # Convert the dictionary to a pandas DataFrame and return it
            return pd.DataFrame(custom_data_input_dict)
        
        except Exception as e:
            # If an error occurs, raise a custom exception with the error message and system info
            raise CustomException(e, sys)
   