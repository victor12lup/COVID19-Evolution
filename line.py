#12061468
# Victor Salazar
from bokeh.io import output_notebook, show
from bokeh.transform import transform
from bokeh.palettes import all_palettes
from bokeh.layouts import column, row, gridplot
from bokeh.plotting import figure
from bokeh.models import CustomJS, Slider, ColumnDataSource, Select, TextInput, BasicTicker, ColorBar,LinearColorMapper, PrintfTickFormatter, HoverTool
import pandas as pd
import numpy as np 
from math import pi

def date_name(x):
    """ Returns a string which will be easier to red  
        
        Parameters:
        a datetime object
    """   
    return x.strftime('%y %b,%d')

def get_data_line(df,country):
    """ Return a dataframe in the format of line glyph of only one ocuntry  
        
        Parameters:
        dataframe and a country desired
    """   
    df_new = df.reset_index().melt(id_vars=['Country/Region'],value_name="Cases").rename(columns={'Country/Region':'Country','variable':'Date'})
    # add this variable to add it to the line graph , easier to read
    df_new['date_str'] = df_new.Date.map(date_name)
    df_new = df_new[df_new['Country']==country]
    
    return df_new


def line_graph(df):
    """ Return a line graph of an specific country which will be chosen by a dropdown menu 
        
        Parameters:
        dataframe 
    """   
    def modify_doc_line(doc):
        # general settings
        COUNTRIES = list(df.index)
        source = ColumnDataSource(data=get_data_line(df,"India"))
        tools = "save,pan,box_zoom,reset,wheel_zoom"
        hover = HoverTool(
            tooltips=[
                ("Date", "@date_str"),
                ("Country", "@Country"),
                ("Cases", "@Cases"),
            ]
        )
        # Important to add type datetime otherwise it will chnage the datetime to numbers and it will tot different
        p = figure(x_axis_type="datetime",plot_width=900, plot_height=300,tools=[tools,hover],title="Daily cases reported per country")     
        p.line(y='Cases', x='Date',line_color="red", line_width=1, source=source)
    
        p.xaxis.axis_label = "Date"
        p.yaxis.axis_label = "Cases"
        p.yaxis.major_label_orientation = "vertical"
        p.xaxis.major_label_orientation = pi / 3
        p.yaxis.major_label_orientation = pi / 3
        select = Select(title="Country", value="India", options=COUNTRIES )

        # This is the callback part 
        def update_points(attrname, old, new):
            N = str(select.value)
            # changing the dataframe to an specific country
            source.data = get_data_line(df,N)
        select.on_change('value', update_points)

        layout = column(row(select, width=400), row(p))

        doc.add_root(layout)

    show(modify_doc_line)

def line(df,continents, continent):
    """ Creates a line graph of many countries in just one 
        
        Parameters:
        dataframe , continent list and conitent desired
    """
    #general settings   
    colors = list(reversed(all_palettes['Viridis'][256]))[:256:20]
    tools = "save,pan,box_zoom,reset,wheel_zoom"
    hover = HoverTool(
        tooltips=[
            ("Date", "@date_str"),
            ("Country", "@Country"),
            ("Cases", "@Cases"),
        ]
    )
    # datetime format important
    p = figure(x_axis_type="datetime",plot_width=450, plot_height=600,tools=[tools,hover],title="Daily cases reported per country {0}".format(continent)) 
    x = 0
    #This will recursively take all the countries of a continent selected
    while x < len(continents[continent]):
        p.line(y='Cases', x='Date', line_color=colors[x], line_width=1, source= get_data_line(df,continents[continent][x]))
        x += 1
    p.xaxis.axis_label = "Date"
    p.yaxis.axis_label = "Cases"
    p.yaxis.major_label_orientation = "vertical"
    p.xaxis.major_label_orientation = pi / 3
    p.yaxis.major_label_orientation = pi / 3
    
    return p

            
def lines_countries(df,continents,continent1, continent2):
    """ Returns in a gridplot two line graphs calling the function line, better for the presentation 
        
        Parameters:
        dataframe with daily entries
    """   
    # calling the graphs
    na1 = line(df,continents,continent1)
    na2 = line(df,continents,continent2)
    p = gridplot([[na1,na2]])
    show(p)