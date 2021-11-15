
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

def monthly(df):
    """ From a dataframe with daily increases returns a a montlhy average of the data 
        
        Parameters:
        dataframe with daily entries
    """    
    
    #df = df.groupby("Country/Region").sum()
    df = df.transpose()
    #Grouping monthly to get an average ,as data is daily and not monthly
    df_monthly = df.groupby(pd.Grouper(freq='M')).mean()
    df_monthly.index.name = 'Date'
    #Give a shorter name to the dates, to be easily interpretable
    df_monthly.index = df_monthly.index.strftime("%b%y")
    df_monthly.columns.name = 'Country'
    df_monthly
    return  df_monthly


def get_data_heat(continent,df,continents):
    """ returns data necessary for the callback function, selectiong only specific continents
        
        Parameters:
        continent, dataframe given by heat_df, and continent given by heat_df
    """  
    return monthly(df)[continents[continent]]

def heat_df(df,continents):
    """ returns a heatmap that will change every entry depneding on a selecting feature or group of countries,continents, also lets choose the dataframe if it is cases or deaths , cumulative or not
        
        Parameters:
        general dataframe, and list with groups of countries
    """  
    def modify_doc_heat(doc):
        
        OPTIONS = list(continents.keys())
        # defining a new dataframe with the strucutre supported by bokeh rect glyph 
        df1 = get_data_heat("All",df,continents).reset_index().melt(id_vars=['Date'],value_name="cases")
        # defining the source with data allow us make a callback by usng "data="
        source = ColumnDataSource(data=get_data_heat("All",df,continents).reset_index().melt(id_vars=['Date'],value_name="cases"))
        # Tools that are gonna be displayed
        TOOLS = "hover,save,pan,box_zoom,reset,wheel_zoom"

        #make list of the data for the heat map necesarry for callback
        date =list(get_data_heat("All",df,continents).index)
        countries = list(get_data_heat("All",df,continents).columns)
        # using colors from the library of bokeh
        colors = list(reversed(all_palettes['Viridis'][256]))[:256:12]
        # divides the color according to the number of cases
        mapper = LinearColorMapper(palette=colors, low=df1.cases.min(), high=df1.cases.max())

        # setting the main figure with title and general specifications 
        p = figure(title="Covid ({0} - {1})".format(date[0], date[-1]),
                    x_range=countries, y_range=list(reversed(date)),
                    x_axis_location="above", plot_width=1200, plot_height=400,
                   tools=TOOLS, toolbar_location='below',
                    tooltips=[('Date', '@Date'), ('Cases', '@cases'),('Country','@Country')])
        # features of the graph 
        p.grid.grid_line_color = None
        p.axis.axis_line_color = None
        p.axis.major_tick_line_color = None
        p.axis.major_label_text_font_size = "7px"
        p.axis.major_label_standoff = 0
        p.xaxis.major_label_orientation = pi / 3

        # Actual data in the heatmap 
        r = p.rect(x="Country", y="Date", width=1, height=1,
               source=source,
               fill_color= {'field': 'cases', 'transform': mapper},
               line_color=None)

        color_bar = ColorBar(color_mapper=mapper, major_label_text_font_size="7px",
                             ticker=BasicTicker(desired_num_ticks=len(colors)),
                             formatter=PrintfTickFormatter(format="%d"),
                             label_standoff=6, border_line_color=None)
        p.add_layout(color_bar, 'right')

        # introduce the dropdown menu into the function with the continents available for choosing
        select = Select(title="Continents", value="All", options=OPTIONS)

        # funtion for callback 
        def update_points(attrname, old, new):
            # First selecting the value picked by the user with .value
            N = str(select.value)

            #setting the new data that needs to be changed
            df1 = get_data_heat(N,df,continents).reset_index().melt(id_vars=['Date'],value_name="cases")
            date =list(get_data_heat(N,df,continents).index)
            countries = list(get_data_heat(N,df,continents).columns)
        
            source.data = get_data_heat(N,df,continents).reset_index().melt(id_vars=['Date'],value_name="cases")
            mapper.low = df1.cases.min()
            mapper.high = df1.cases.max()

            # if  you do not use x_range it will not work as in the others , tool me so long to find this lol
            p.x_range.factors = countries
            p.y_range.factors =list(reversed(date))
        
        # the callback 
        select.on_change('value', update_points)

        layout = column(row(select, width=400), row(p))

        doc.add_root(layout)
    #displaying
    show(modify_doc_heat)