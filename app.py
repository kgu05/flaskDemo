from flask import Flask, render_template, request, redirect
import requests
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from bokeh.plotting import figure, output_file, show
from bokeh.embed import components

app = Flask(__name__)

@app.route('/userinput', methods=['GET','POST'])
def userinput():
        return render_template('userinput.html')
        
@app.route('/plot', methods=['POST'])
def plot():    
    input=request.form['ticker']
    r = requests.get('https://www.quandl.com/api/v3/datatables/WIKI/PRICES.json?&ticker='+input+'&date.gte=20170201&date.lt=20170301&qopts.columns=ticker,date,close&api_key=y8syw1ZfeEzxDFTydbqx')
    json_object = r.json()
    temp = json_object['datatable']['data']
    data = pd.DataFrame(temp)
    data.columns = ['ticker','date','close']
    
    # Use Bokeh to generate plot
    date = np.array(data['date'], dtype=np.datetime64)
    close = np.array(data['close'])

    p = figure(title='Data from Quandl WIKI set', x_axis_type='datetime', x_axis_label='Date') 
    p.line(date, close, line_width=2, legend=input+': Close')
    
    script, div = components(p)
    return render_template('plot.html', ticker = input, script=script, div=div)


      
if __name__ == '__main__':
    app.run(debug=True)


