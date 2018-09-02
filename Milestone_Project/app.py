from flask import Flask, render_template, request
import quandl
from bokeh.io import curdoc
from bokeh.layouts import column, widgetbox
from bokeh.models import ColumnDataSource, CheckboxGroup, TextInput
from bokeh.plotting import figure, show
from bokeh.embed import components
import requests
from datetime import datetime
app= Flask(__name__)

def create_figure(ticker_name, source, col_active0): #active1, active2, active3):
    p = figure(plot_width=800, plot_height=500, x_axis_type='datetime', x_axis_label = 'Date', y_axis_label = 'Price')

    color = {'close': "blue",
             'adj_close': "#7FC97F",
             'open': "#F0027F",
             'adj_open': "#E6550D"}
    legend = {'close': "Close Price",
             'adj_close': "Adjusted Close Price",
             'open': "Open Price",
             'adj_open': "Adjusted Open Price"}

    for i in col_active0:
        p.line('date', i, alpha=1, line_width=2, source=source, color=color[i], legend=legend[i])

    p.title.text = "%s Stock Price" %ticker_name
    p.legend.location = 'top_left'
    p.legend.click_policy="hide"

    p.title.align = 'center'
    p.title.text_font_size = '20pt'
    p.title.text_font = 'serif'

    # Axis titles
    p.xaxis.axis_label_text_font_size = '14pt'
    p.xaxis.axis_label_text_font_style = 'bold'
    p.yaxis.axis_label_text_font_size = '14pt'
    p.yaxis.axis_label_text_font_style = 'bold'

    # Tick labels
    p.xaxis.major_label_text_font_size = '12pt'
    p.yaxis.major_label_text_font_size = '12pt'
    return p

@app.route('/')
def index1():
    return render_template('index.html')

@app.route('/graph', methods=['get', 'post'])
def stock():
    ticker_name = request.form['ticker_name']
    quandl.ApiConfig.api_key = 'Y9QvH7-wD-UDNHcL2J_m'
    data = quandl.get_table('WIKI/PRICES', ticker=ticker_name, qopts={'columns': ['ticker', 'date', 'adj_close', 'close', 'open', 'adj_open']},
    paginate=True)
    source = ColumnDataSource(data.set_index(['ticker']))
    #r = requests.get('https://www.quandl.com/api/v3/datasets/WIKI/' + ticker_name + '.json?api_key=Y9QvH7-wD-UDNHcL2J_m')
    #json_object = r.json()
    #data = json_object['dataset']['data']
    #source = {"date": [], "open": [], "adj_open": [], "close": [], "adj_close": []}
    #for arr in data:
        #source['date'].append(arr[0])
        #source['open'].append(arr[1])
        #source['adj_open'].append(arr[8])
        #source['close'].append(arr[4])
        #source['adj_close'].append(arr[11])
    #source=ColumnDataSource(source)
    col_active0 = request.form.getlist('check')
    plot = create_figure(ticker_name, source, col_active0) #col_active1, col_active2, col_active3)

    script, div = components(plot)
    #print(col_active0)
    return render_template('about.html', script=script, div=div) #ticker_name=ticker_name, col_active0=col_active0) #col_active1=col_active1,
                           #col_active2=col_active2, col_active3=col_active3)

if __name__ == '__main__':
    app.run(port=5000)

# good job!