import pandas as pd
import numpy as np
from regex_handling import regexExtraction

# total number of rows in the csv ignoring where prediction is none
# print(df[df['quantity_prediction'].notna() & df['scent_prediction'].notna()].index)
def getTotalRowsPrediction(df)->int:
    ifno = df['scent_prediction'].apply(checkIfNone)
    # reducing total length from number of nan values 
    return len(df) - ifno.isnull().sum()

# total number of rows in the csv ignoring where prediction is none
# function to ignore none
def checkIfNone(df):
    if df == "None":
        return np.nan
    return df

# distinct values without split
def getDistinctValuesScent(df)-> list:
    return df['scent_prediction'].unique()



# replace comma with space so as to make all space seperated
def splitValues(df):
    df = df.replace(",", " ")
    return df.split()

def saveScent(newdf):
    # to reset index
    newdf = newdf.reset_index()
    # renaming columns for better understanding  
    newdf = newdf.rename(columns={'index':'scent_value','scent_prediction':'count'})
    # distinct scents and their counts
    newdf = newdf['scent_value'].apply(splitValues).explode().value_counts()

    # printing scents with their count
    print("Scents with their count:\n",newdf)
    return newdf




if __name__ == "__main__":
    # python data_handling.py
    # added the data set at a data dataset folder
    # getting the data into a dataframe
    df = pd.read_csv("data_set\interview_scent.csv", header=[0], index_col=0)
    
    # part a
    # ignoring prediction = none
    
    print("=====================================================================")
    print("\t\t\tPART A ANSWER")
    print("Total number of rows in the csv ignoring where prediction is none:",getTotalRowsPrediction(df))

    # part B
    # distinct values without split
    print("=====================================================================")
    print("\t\t\tPART B ANSWER")
    # print("Distinct values in without split:",getDistinctValuesScent(df))

    # distinct values with split
    newdf = df['scent_prediction'].value_counts()
    newdf = saveScent(newdf)
    print("=====================================================================")
    print("The total number of distinct scents:",newdf.count())
    print("=====================================================================")
    newdf = newdf.reset_index()
    print("The distinct scents after split:", newdf['index'].tolist())
    
    
    # part C
    # distinct values Saving
    print("=====================================================================")
    print("\t\t\tPART C ANSWER")
    
    # save the results into a csv file
    print("Saving file to result as 'distinct_scent_count'!!!!!")
    try:
        newdf.to_csv("result/distinct_scent_count.csv")
        print("Saving successfull!!!")
    except Exception as e:
        print("Unsuccessfull error!!",e)

    print("=====================================================================")
    print("\t\t\tPART D ANSWER")
    # Added in a new file
    prediction = regexExtraction(df = df)
    df['quantity_prediction']= prediction['actual_val']
    try:
        print("Saving df to system!!!!")
        df.to_csv("result/final_df.csv")
        print("Successfully saved df to system!!!!")
    except Exception as e:
        print("Failed to save df to system!!!!",e)