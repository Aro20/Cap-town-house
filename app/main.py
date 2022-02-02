
#Import main library
import numpy as np
import pandas as pd

#Import Flask modules
from flask import Flask, request, render_template

#Import pickle to save our model
import pickle 

#Initialize Flask and set the template folder to "template"
app = Flask(__name__, template_folder = 'template')

#Open our model 
model = pickle.load(open('app/model.pkl','rb'))

#create our "home" route using the "index.html" page
@app.route('/')
def home():
    return render_template('index.html')

#Set a post method to yield predictions on page
@app.route('/', methods = ['POST'])
def predict():
    
    #obtain all form values and place them in an array, 
    features = [x for x in request.form.values()]
    #Combine them all into a final numpy array and then to a dataframe
    final_features = [np.array(features)]
    final_features = pd.DataFrame(final_features, columns = ['Bathrooms', 'Bedrooms', 'Erf Size', 'Floor Size', 'Garages', 'Pet Friendly', 'Type of Property', 'Garden', 'Pool', 'Parking'])
    #predict the price given the values inputted by user
    prediction = model.predict(final_features)
    
    #Round the output to 2 decimal places
    output = round(prediction[0], 2)
    
    #If the output is negative, the values entered are unreasonable to the context of the application
    #If the output is greater than 0, return prediction
    if output < 0:
        return render_template('index.html', prediction_text = "Predicted Price is negative, values entered not reasonable")
    elif output >= 0:
        return render_template('index.html', prediction_text = 'Predicted Price of the house is: R{}'.format(output))   



