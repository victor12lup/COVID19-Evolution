#12061468
# Victor Salazar 

from bokeh.io import output_notebook, show
from bokeh.transform import transform
from bokeh.palettes import all_palettes
from bokeh.layouts import column, row
from bokeh.plotting import figure
from bokeh.models import CustomJS, Slider, ColumnDataSource, Select, TextInput, BasicTicker, ColorBar,LinearColorMapper, PrintfTickFormatter
import pandas as pd
import numpy as np 
from math import pi

def get_data_evo(df_cumu,df1_cumu,continents,continent,day):
    """ By giving two dataframes , deaths and cases we merge them and add a new variable in the dataframe average showing an approximation of both, returns a datframe with the desired info in the format for bokeh 
        
        Parameters:
        dataframe with daily entries
    """    
    df = df_cumu.loc[continents[continent]] 
    # substract so that we can start from 1 in the slider , index is 0 
    x = df_cumu.columns[day-1]
    df = pd.merge(df_cumu.loc[continents[continent]][x], df1_cumu.loc[continents[continent]][x],left_index=True, right_index=True).rename(columns={str(x) +'_x':"Cases", str(x) +'_y':"Deaths"})
    # cahnging the columns name to an easier one
    df = df.reset_index().rename(columns={'Country/Region':'Country'})
    df['average'] = df['Cases']+df['Deaths']/2
    # this is a mathematical formula to approximate 2 numbers into a list of higher to lower , found on the internet 
    df['r'] = (((100-1)*(df['average']-df['average'].min()))/(df['average'].max()-df['average'].min())) + 1
    return df 
def scatter(df,df1,continents): 
    """ Returns a scatter plot which increase in size while there are more cases or deaths in a specific country 
        
        Parameters:
        dataframes of deaths and cases, and list whith continents
    """     
    def modify_doc_evo(doc):
        # Setting general data from the figure 
        OPTIONS = list(continents.keys())

        TOOLS = "hover,save,pan,box_zoom,reset,wheel_zoom"

        source = ColumnDataSource(data=get_data_evo(df,df1,continents,'All',1))
        colors = list(reversed(all_palettes['Viridis'][256]))[:256:12]
    
        mapper = LinearColorMapper(palette=colors, low=get_data_evo(df,df1,continents,'All',1).r.min(), high=get_data_evo(df,df1,continents,'All',1).r.max())
        # Gives the number of days that have passed since corona appeared
        days_slider = Slider(start=1, end=462, value=1, step=1, title="Days")
        # dropdown menu so that we can restrict the group of countries 
        select = Select(title="Continents", value="All", options=OPTIONS )
    
        p = figure(title = 'Covid Cases vs Causalities countries' ,plot_width=400, plot_height=400,tools=TOOLS, tooltips=[('Country', '@Country'), ('Cases', '@Cases'),('Deaths','@Deaths')])
        p.circle(x='Cases', y='Deaths', size = 'r',source=source, fill_alpha=0.6,
                 fill_color={'field': 'r', 'transform': mapper})
    
        p.xaxis.axis_label = 'Cases'
        p.yaxis.axis_label = 'Deaths'
        p.yaxis.major_label_orientation = "vertical"
        p.xaxis.major_label_orientation = pi / 3
        p.yaxis.major_label_orientation = pi / 3
    
        def update_points(attrname, old, new):
            # This is the callback function getting the new numbers of day everytime 
            # number of day
            N = int(days_slider.value)
            # group of countries
            M = str(select.value)
            
            source.data = get_data_evo(df,df1,continents,M,N)
            

        
        days_slider.on_change('value', update_points)
        select.on_change('value',update_points)
    
        layout = column(row(select, days_slider, width=400), row(p))

        doc.add_root(layout)

    show(modify_doc_evo)  