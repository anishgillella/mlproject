from flask import Flask, request, render_template
import numpy as np
import pandas as pd

# Import necessary modules for scaling and prediction
from sklearn.preprocessing import StandardScaler
from src.pipeline.predict_pipeline import CustomData, PredictPipeline

# Initialize a Flask application
application = Flask(__name__)

# Alias 'application' as 'app' for convenience
app = application

# Route for the home page (index page)
@app.route('/')
def index():
    # Render the 'index.html' template when the root URL is accessed
    return render_template('index.html')

# Route for handling predictions, accessible via '/predictdata'
@app.route('/predictdata', methods=['GET', 'POST'])
def predict_datapoint():
    # If the request method is GET, render the 'home.html' template
    if request.method == 'GET':
        return render_template('home.html')
    
    # If the request method is POST, process the form data
    else:
        # Create an instance of the CustomData class, mapping form inputs to backend variables
        data = CustomData(
            gender=request.form.get('gender'),
            race_ethnicity=request.form.get('ethnicity'),
            parental_level_of_education=request.form.get('parental_level_of_education'),
            lunch=request.form.get('lunch'),
            test_preparation_course=request.form.get('test_preparation_course'),
            reading_score=int(request.form.get('reading_score')),
            writing_score=int(request.form.get('writing_score'))
        )

        # Convert the custom data object into a DataFrame
        pred_df = data.get_data_as_data_frame()
        print(pred_df)  # Print the DataFrame for debugging purposes

        # Create an instance of the PredictPipeline class to handle predictions
        predict_pipeline = PredictPipeline()

        # Make a prediction using the predict_pipeline object
        results = predict_pipeline.predict(pred_df)

        # Render the 'home.html' template with the prediction results
        return render_template('home.html', results=results[0])

# Run the Flask application if this script is executed directly
if __name__ == "__main__":
    app.run(host="0.0.0.0")
