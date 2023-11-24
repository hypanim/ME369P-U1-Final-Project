# imports
import os
import glob
import pandas as pd


# put csv data into pandas dataframe
def read_data(file_name):
    # get path to the data folder
    curr_directory = os.path.dirname(os.path.realpath(__file__))
    grade_data_path = os.path.join(curr_directory, 'data/')

    file_path = os.path.join(grade_data_path, file_name)

    # import data into pandas
    df = pd.read_csv(file_path, encoding = 'utf-16le', on_bad_lines='skip', sep = '\t')

    # semester name, course prefix, course number,
    print(df.head)

    print(df.columns.tolist())


read_data('2022_2023.csv')

