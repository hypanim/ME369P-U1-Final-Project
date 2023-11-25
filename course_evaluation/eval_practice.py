import re
import pandas as pd


def course_number_regex(s):
    return list(filter(None, re.split(r'(\d+)', s)))

def parse_instructor_data(filename):
    # create data list
    eval_list = []
    # open the file and append
    with open(filename, encoding="UTF8") as f:
        for line in f:
            d = eval(line)
            # instructor data
            instructor_dict = d['InstructorData'][0]
            course = course_number_regex(instructor_dict['Course Number'])
            year_sem = instructor_dict['Semester'].split(" ")

            eval_list.append([instructor_dict['Last Name'], instructor_dict['First Name'], course[0], course[1],
                              instructor_dict['Unique Number'], year_sem[0], year_sem[1], d['Table1'], d['Table2'],
                              d['Table3']])
    # place into pandas df
    df_columns = ["lastname", "firstname", "course_prefix", "course_number", "unique_number", "semester", "year",
                  "table1", "table2", "table3"]
    df = pd.DataFrame(eval_list, columns=df_columns)
    print(df.columns.tolist())
    print(df.head())
parse_instructor_data("instructor_data1a.txt")
