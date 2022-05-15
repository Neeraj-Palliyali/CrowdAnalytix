import numpy as np
import pandas as pd

def check(df):
    if 'value_y' in df:
            if not np.isnan(df.value_y):
                return df.value_y
    if 'value_x' in df:
        if not np.isnan(df.value_x):
            return df.value_x
    if 'value' in df:
        if not np.isnan(df.value):
            return df.value
    return np.nan

def checknull(df):
    df = df.astype(float)
    if 'actual_val' in df:
        if not np.isnan(df.actual_val):
            return df.actual_val
        return check(df)
    else:
        
        return check(df)

# gallon to oz units
def gallonconvertToOunce(df):
    if not np.isnan(df.value):
        df.value = df.value*128
        return df.value
    return np.nan

# fl to oz
def convertflToOunce(df):
    if not np.isnan(df.value):
        df.value = df.value*1.04
        return df.value
    return np.nan

# ml to oz
def convertToOunce(df):
    if not np.isnan(df.value):
        df.value = df.value*0.033814
        return df.value
    return np.nan

# ounce proper extraction
def extractValsOz(col_name:str, df):
    # for oz vals
    dataframe = df[col_name].str.extract('(\d*\.\d+[oO][uU][nN][cC][eE]|\d+[oO][uU][nN][cC][eE]|\d*\.\d+ [oO][uU][nN][cC][eE]|\d+ [oO][uU][nN][cC][eE]|\d*\.\d+-[oO][uU][nN][cC][eE]|\d+-[oO][uU][nN][cC][eE]|\d*\.\d+[oO][zZ]|\d+[oO][zZ]|\d*\.\d+ [oO][zZ]|\d+ [oO][zZ]|\d*\.\d+-[oO][zZ]|\d+-[oO][zZ])')
    dataframe = dataframe[0].str.extract('(\d*\.\d+|\d+)')
    dataframe = dataframe[0].astype(float)
    dataframe.name = "value"
    dataframe = dataframe.to_frame()
    return dataframe

# gallon to ounce  extraction
def extractValsGa(col_name:str, df):
    # for oz vals
    dataframe = df[col_name].str.extract("(\d*\.\d+[gG][aA][lL]|\d+[gG][aA][lL]|\d*\.\d+ [gG][aA][lL]|\d+ [gG][aA][lL]|\d*\.\d+[.-][gG][aA][lL]|\d+[.-][gG][aA][lL]|\d*\.\d+[gG][aA][lL][lL][oO][nN]|\d+[gG][aA][lL][lL][oO][nN]|\d*\.\d+ [gG][aA][lL][lL][oO][nN]|\d+ [gG][aA][lL][lL][oO][nN]|\d*\.\d+[.-][gG][aA][lL][lL][oO][nN]|\d+[.-][gG][aA][lL][lL][oO][nN])")
    dataframe = dataframe[0].str.extract('(\d*\.\d+|\d+)')
    dataframe.rename(columns={0:"value",}, inplace=True)
    dataframe = dataframe.astype(float)
    dataframe = dataframe.apply(gallonconvertToOunce,axis=1).to_frame()
    dataframe.rename(columns={0:"value",}, inplace=True)
    return dataframe

# ml to ounce  extraction
def extractValsmL(col_name:str, df):
    # for oz vals
    dataframe = df[col_name].str.extract("(\d*\.\d+[mM][lL]|\d+[mM][lL]|\d*\.\d+ [mM][lL]|\d+ [mM][lL]|\d*\.\d+[.-][mM][lL]|\d+[.-][mM][lL])")
    dataframe = dataframe[0].str.extract('(\d*\.\d+|\d+)')
    dataframe.rename(columns={0:"value",}, inplace=True)
    dataframe = dataframe.astype(float)
    dataframe = dataframe.apply(convertToOunce,axis=1).to_frame()
    dataframe.rename(columns={0:"value",}, inplace=True)
    return dataframe

# fl to ounce  extraction
def extractValfloz(col_name:str, df):
    # for oz vals
    dataframe = df[col_name].str.extract("(\d*\.\d+[fF][lL][oO][zZ]|\d+[fF][lL][fF][lL][oO][zZ]|\d*\.\d+ [fF][lL] [oO][zZ]|\d+ [fF][lL] [oO][zZ]|\d*\.\d+[.-][fF][lL][.-][oO][zZ]|\d+[.-][fF][lL][.-][oO][zZ]|\d*\.\d+ [fF][lL][.-][oO][zZ]|\d+ [fF][lL][.-][oO][zZ]|\d*\.\d+[.-][fF][lL] [oO][zZ]|\d+[.-][fF][lL] [oO][zZ])")
    dataframe = dataframe[0].str.extract('(\d*\.\d+|\d+)')
    dataframe.rename(columns={0:"value",}, inplace=True)
    dataframe = dataframe.astype(float)
    dataframe = dataframe.apply(convertflToOunce,axis=1).to_frame()
    dataframe.rename(columns={0:"value",}, inplace=True)
    return dataframe


def regexExtraction(df):
    try:
        print("Handling exact oz - ounce")
        nedf = extractValsOz("title", df)
        nedf = pd.merge(nedf,extractValsOz("short_description",df), on=['item_id'])
        nedf = pd.merge(nedf,extractValsOz("long_description",df), on=['item_id'])
        nedf['actual_val']=nedf.apply(checknull, axis=1)
        nedf = nedf.drop(['value_x','value_y', 'value'], axis=1)
        print("Handling exact oz Successfull")
    except Exception as e:
        print("Handling exact oz failed!!!",e)
    
    try:
        print("Handling fl - ounce")
        nedf = pd.merge(nedf,extractValfloz("title", df), on=['item_id'])
        nedf = pd.merge(nedf,extractValfloz("short_description", df), on=['item_id'])
        nedf = pd.merge(nedf,extractValfloz("long_description",df), on=['item_id'])
        nedf['actual_val']=nedf.apply(checknull, axis=1)
        nedf = nedf.drop(['value_x','value_y', 'value'], axis=1) 
        print("Handling fl oz Successfull")
    except Exception as e:
        print("Handling fl oz failed!!!",e)
    
    try:
        print("Handling ml - ounce")
        nedf = pd.merge(nedf,extractValsmL("title", df), on=['item_id'])
        nedf = pd.merge(nedf,extractValsmL("short_description", df), on=['item_id'])
        nedf = pd.merge(nedf,extractValsmL("long_description",df), on=['item_id'])
        nedf['actual_val']=nedf.apply(checknull, axis=1)
        nedf = nedf.drop(['value_x','value_y', 'value'], axis=1)
        print("Handling ml oz Successfull")
    except Exception as e:
        print("Handling ml oz failed!!!",e)

    try:
        print("Handling gallon - ounce")
        nedf = pd.merge(nedf,extractValsGa("title", df), on=['item_id'])
        nedf = pd.merge(nedf,extractValsGa("short_description", df), on=['item_id'])
        nedf = pd.merge(nedf,extractValsGa("long_description",df), on=['item_id'])
        nedf['actual_val']=nedf.apply(checknull, axis=1)
        nedf = nedf.drop(['value_x','value_y', 'value'], axis=1)
        print("Handling gallon oz Successfull")
    except Exception as e:
        print("Handling gallon oz failed!!!",e)
    
    return nedf
    








