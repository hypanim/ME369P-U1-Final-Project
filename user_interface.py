import PySimpleGUI as psg
import os
import pickle
import pandas as pd
import re
import statistics
import matplotlib as mpl
import matplotlib.pyplot as plt
mpl.use('Qt5Agg')

# load scraped course evaluation data into a pandas dataframe
def load_course_data():
    # get file path
    curr_directory = os.path.dirname(os.path.realpath(__file__))
    course_eval_dir = os.path.join(curr_directory, 'course_evaluation/data/')

    # helper function
    def course_number_regex(s):
        match = re.compile(r'(\d+)').search(s)
        return [s[:match.start()], s[match.start():]]

    # open the file and grab data
    eval_list = []

    for subdir, dirs, files in os.walk(course_eval_dir):
        for file in files:
            with open(os.path.join(subdir, file), encoding="UTF8") as f:
                for line in f:
                    d = eval(line)
                    # instructor data
                    instructor_dict = d['InstructorData'][0]
                    course = course_number_regex(instructor_dict['Course Number'])
                    year_sem = instructor_dict['Semester'].split(" ")

                    eval_list.append([instructor_dict['Last Name'], instructor_dict['First Name'], course[0], course[1],
                                      instructor_dict['Unique Number'], year_sem[0], year_sem[1], d['Table1'],
                                      d['Table2'],
                                      d['Table3']])
    # place into pandas df
    df_columns = ["lastname", "firstname", "course_prefix", "course_number", "unique_number", "semester", "year",
                  "table1", "table2", "table3"]

    global course_eval_df
    course_eval_df = pd.DataFrame(eval_list, columns=df_columns)


# check sentiment analysis and other RMP data
def sentiment(prof_firstname, prof_lastname):
    # get path to data_directory
    curr_dir = os.path.dirname(os.path.realpath(__file__))
    data_dir = os.path.join(curr_dir, "professor_sentiment/data_directory")

    # create pickle file name and open it
    prof_pkl = str(prof_firstname) + "_" + str(prof_lastname) + "_data.pkl"
    pkl_filename = os.path.join(data_dir, prof_pkl)

    # create dictionary to return
    prof_dict = {"Quality": 0.0, "Difficulty": 0.0, "Sentiment": 0.0, "Number of Ratings": 0,
                 "Other Courses Taught": [],
                 "comments": [], "tags": [], "Number of Reviews": 0}

    with open(pkl_filename, 'rb') as fp:
        reading_lists = pickle.load(fp)
        # get average quality, difficulty, sentiment analysis
        prof_dict['Quality'] = round((sum(float(i) for i in reading_lists['quality'])) / len(reading_lists['quality']),
                                     2)
        prof_dict['Difficulty'] = round(
            (sum(float(i) for i in reading_lists['difficulty'])) / len(reading_lists['difficulty']), 2)
        prof_dict['Sentiment'] = round(
            (sum(float(i) for i in reading_lists['sentimentAnalysis'])) / len(reading_lists['sentimentAnalysis']), 3)

        # other fields
        prof_dict['Number of Reviews'] = len(reading_lists['quality'])
        prof_dict['Other Courses Taught'] = reading_lists['class']
        prof_dict['comments'] = reading_lists['comment']
        prof_dict['tags'] = reading_lists['tags']

        raw_data = reading_lists

    return raw_data, prof_dict


# check course evaluations
def course_eval(prof_firstname, prof_lastname, course_prefix, course_number):
    # grab respective data
    prof_df = course_eval_df[(course_eval_df['lastname'] == prof_lastname) & (course_eval_df['firstname'] == prof_firstname) &
                 (course_eval_df['course_prefix'] == course_prefix) & (course_eval_df['course_number'] == course_number)]

    # grab table data and place in dict
    rating_dict = {"instructor_rating": [], "course_rating": [], "workload_rating": []}

    for index, row in prof_df.iterrows():
        table2_dict = row['table2']
        table3_dict = row['table3']
        # update ratings
        rating_dict['instructor_rating'].append(float(table2_dict['T2 Question 1 Score']))
        rating_dict['course_rating'].append(float(table2_dict['T2 Question 2 Score']))
        rating_dict['workload_rating'].append(float(table3_dict['Workload Score (5 = Highest, 1 = Lowest)']))

    # get raw data
    raw_data = prof_df.to_string()

    return raw_data, rating_dict


# get unique number helper function
def get_unique_num(prof_firstname, prof_lastname, course_prefix, course_number, semester, yr):
    # match to regex
    # only checking lastname, no first currently
    unique_num_df = course_eval_df[
        (course_eval_df['lastname'] == prof_lastname) & (course_eval_df['firstname'] == prof_firstname) &
        (course_eval_df['course_prefix'] == course_prefix) & (course_eval_df['course_number'] == course_number) &
        (course_eval_df['semester'] == semester) & (course_eval_df['year'] == yr)]

    return unique_num_df['unique_number'].iloc[0]

# plot some grade distributions
def grade_distribution(prof_firstname, prof_lastname, course_prefix, course_number, year, semester):
    # use helper func to get the unique number
    if semester == 'Fall':
        yr = year.split('-')[0]
    else:
        yr = year.split('-')[1]
    unique_number = get_unique_num(prof_firstname, prof_lastname, course_prefix, course_number, semester, yr)

    # get csv file name
    file_name = year.split('-')[0] + "_" + year.split('-')[1] + ".csv"

    # get path
    curr_directory = os.path.dirname(os.path.realpath(__file__))
    grade_data_path = os.path.join(curr_directory, 'grade_distribution/data/')
    file_path = os.path.join(grade_data_path, file_name)

    # populate df
    grade_df = pd.read_csv(file_path, encoding='utf-16le', on_bad_lines='skip', sep='\t')

    # convert unique number to string column
    grade_df['Section Number'] = grade_df['Section Number'].astype(str)

    # grades list
    letter_grades = ["A", "A-", "B+", "B", "B-", "C+", "C", "C-", "F", "Other"]
    grade_freq = []

    # get frequency count for each grade
    for g in letter_grades:
        search_df = grade_df[(grade_df['Section Number'] == unique_number) & (grade_df['Letter Grade'] == g)]
        if search_df.empty:
            grade_freq.append(0)
        else:
            grade_freq.append(search_df['Count of letter grade'].iloc[0])

    # plot the results!
    x_pos = [1,2,3,4,5,6,7,8,9,10]
    grade_colors = ["limegreen","limegreen","gold","gold","gold","orange","orange","orange","red","grey"]

    plt.figure()
    plt.bar(x_pos, grade_freq, color = grade_colors)
    plt.xticks(x_pos, letter_grades)

    plt.xlabel("Letter Grade")
    plt.ylabel("Frequency")

    plot_title = "{p} {pre}{num} ({s} {y})".format(p=prof_lastname, pre=course_prefix, num=course_number, s=semester,y=yr)
    plt.title(plot_title)

    plt.show(block=False)


# configure GUI
def create_gui():
    # psg settings
    psg.theme("Purple")
    psg.set_options(font=('Arial Bold', 12))

    # general layout
    gui_label = psg.Text(text='UT Course Registration Helper', font=('Arial Bold', 20), size=20, expand_x=True,
                         justification='center')

    # professor last name
    lastname_prompt = psg.Text(text='Professor Last Name', expand_x=True)
    lastname_input = psg.Input(key='professor_lastname', justification='left')

    # professor first name
    firstname_prompt = psg.Text(text='Professor First Name', expand_x=True)
    firstname_input = psg.Input(key='professor_firstname', justification='left')

    # course prefix
    course_prefix_prompt = psg.Text(text='Course Prefix (Ex: M E)', expand_x=True)
    course_prefix_input = psg.Input(key='course_prefix', justification='left')

    # course number
    course_number_prompt = psg.Text(text='Course Number (Ex: 369P)', expand_x=True)
    course_number_input = psg.Input(key='course_number', justification='left')

    # sentiment analysis
    sentiment_title = psg.Text('Sentiment Analysis (via RateMyProfessor)', justification='center', expand_x=True)
    sentiment_button = psg.Button("View Professor Data", button_color='pale green')
    sentiment_error_msg = psg.Text('', text_color='dark red')
    sentiment_raw_button = psg.Button("View Raw RMP Data", button_color='grey')
    sentiment_raw_data = ''

    # professor specific info
    # quality, difficulty, sentiment, number of reviews, other courses taught
    sentiment_analysis_title = psg.Text(text='Sentiment Analysis:')
    sentiment_val = psg.Text(text='')
    quality_title = psg.Text(text='Quality:')
    quality_val = psg.Text(text='')
    difficulty_title = psg.Text(text='Difficulty:')
    difficulty_val = psg.Text(text='')
    num_reviews_title = psg.Text(text='Number of Reviews:')
    num_reviews_val = psg.Text(text='')
    other_courses_title = psg.Text(text='Other Courses Taught:')
    other_courses_val = psg.Text(text='')

    # Course Evaluation
    course_eval_title = psg.Text('Course Evaluation', justification='center', expand_x=True)
    course_eval_button = psg.Button("View Course Evaluations", button_color='light blue')
    course_raw_button = psg.Button("View Raw CIS Data", button_color='grey')
    eval_raw_data = ''

    # ratings
    instructor_error_msg = psg.Text(text='', text_color='dark red')
    instructor_title = psg.Text(text='Instructor Rating:')
    instructor_val = psg.Text(text='')
    course_title = psg.Text(text='Course Rating:')
    course_val = psg.Text(text='')
    workload_title = psg.Text(text='Workload Rating:')
    workload_val = psg.Text(text='')

    # grade distribution
    grade_title = psg.Text('Grade Distributions', justification='center', expand_x=True)
    grade_error = psg.Text('', text_color = 'dark red')

    years = ['2010-2011', '2011-2012', '2012-2013', '2013-2014', '2014-2015', '2015-2016', '2016-2017', '2017-2018',
             '2018-2019', '2019-2020', '2020-2021', '2021-2022', '2022-2023']
    semesters = ['Fall', 'Spring', 'Summer']

    year_prompt = psg.Text(text='Select School Year', expand_x=False)
    year_combo = psg.Combo(years, key='year', expand_x=True)

    semester_prompt = psg.Text(text='Select Semester', expand_x=False)
    semester_combo = psg.Combo(semesters, key='semester', expand_x=True)

    grade_distribution_button = psg.Button("View Grade Distribution", button_color='sienna')

    # misc
    exit_button = psg.Exit(button_color='red')

    layout = [
        [gui_label],
        [lastname_prompt, lastname_input],
        [firstname_prompt, firstname_input],
        [course_prefix_prompt, course_prefix_input],
        [course_number_prompt, course_number_input],
        [psg.Text('', size=(1, 1))],  # blank line
        [course_eval_title],  # course evaluation (cade)
        [course_eval_button, instructor_error_msg],
        [instructor_title, instructor_val],
        [course_title, course_val],
        [workload_title, workload_val],
        [course_raw_button],
        [psg.Text('', size=(1, 1))],  # blank line
        [grade_title],  # grade distribution (dylan)
        [year_prompt, year_combo],
        [semester_prompt, semester_combo],
        [grade_distribution_button, grade_error],
        [psg.Text('', size=(1, 1))],  # blank line
        [sentiment_title],  # sentiment (josh)
        [sentiment_button, sentiment_error_msg],
        [sentiment_analysis_title, sentiment_val],
        [quality_title, quality_val],
        [difficulty_title, difficulty_val],
        [num_reviews_title, num_reviews_val],
        [other_courses_title, other_courses_val],
        [sentiment_raw_button],
        [psg.Text('', size=(1, 1))],  # blank line
        [exit_button],
    ]

    window = psg.Window('UT Course Registration Helper', layout, element_justification='l')

    # event handling
    while True:
        event, values = window.read()
        # print(event, values)
        if event in (None, 'Exit'):
            break

        # sentiment / RMP stuff
        elif event == sentiment_button.get_text():
            try:
                raw_data, prof_dict = sentiment(values['professor_firstname'], values['professor_lastname'])
                sentiment_error_msg.update('')
                # sentiment, quality, difficulty, number of reviews, other courses taught
                if prof_dict['Sentiment'] > 0:
                    sentiment_color = 'green'
                else:
                    sentiment_color = 'red'
                sentiment_val.update(str(prof_dict['Sentiment']), text_color=sentiment_color)

                quality_val.update(str(prof_dict['Quality']) + str('/5.00'))
                difficulty_val.update(str(prof_dict['Difficulty']) + str('/5.00'))
                num_reviews_val.update(str(prof_dict['Number of Reviews']))
                other_courses_val.update(', '.join(set(prof_dict['Other Courses Taught'])))

                sentiment_raw_data = raw_data

            except:
                # if any errors occur, display error msg
                sentiment_error_msg.update("Error! RMP data not available.")
                sentiment_val.update('')
                quality_val.update('')
                difficulty_val.update('')
                num_reviews_val.update('')
                other_courses_val.update('')

        # raw data for sentiment
        elif event == sentiment_raw_button.get_text():
            print("getting here?")
            psg.popup_scrolled(sentiment_raw_data, title='RateMyProfessor Raw Data')

        # evaluation
        elif event == course_eval_button.get_text():
            # variables: prof_firstname, prof_lastname, course_prefix, course_number
            try:
                raw_data, instructor_dict = course_eval(values['professor_firstname'], values['professor_lastname'],
                                                        values['course_prefix'],
                                                        values['course_number'])
                instructor_error_msg.update('')

                # update values
                # dictionary format: rating_dict = {"instructor_rating":[],"course_rating":[],"workload_rating":[]}
                instructor_val.update(
                    str(round(statistics.mean(instructor_dict['instructor_rating']), 2)) + str('/5.00'))
                course_val.update(str(round(statistics.mean(instructor_dict['course_rating']), 2)) + str('/5.00'))
                workload_val.update(str(round(statistics.mean(instructor_dict['workload_rating']), 2)) + str('/5.00'))

                # update raw data popup button
                eval_raw_data = raw_data

            except:
                instructor_error_msg.update('Error! Course evaluation data not available.')
                instructor_val.update('')
                course_val.update('')
                workload_val.update('')


        # course eval raw data
        elif event == course_raw_button.get_text():
            psg.popup_scrolled(eval_raw_data, title='Course Evaluation Raw Data')

        # grade distribution
        elif event == grade_distribution_button.get_text():
            try:
                grade_distribution(values['professor_firstname'], values['professor_lastname'], values['course_prefix'],
                                       values['course_number'], values['year'], values['semester'])
                grade_error.update('')
            except:
                grade_error.update('Error! Grade data not available.')

    window.close()


def main():
    # load the scraped data
    load_course_data()

    # open the user interface
    create_gui()


if __name__ == "__main__":
    main()