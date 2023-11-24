import PySimpleGUI as psg


# check sentiment analysis
def sentiment():
    pass

# check course_evaluations
def course_eval():
    pass

# check grade distributions
def grade_distribution():
    pass

# configure GUI
def create_gui():
    # psg settings
    psg.theme("Purple")
    psg.set_options(font=('Arial Bold', 12))

    # general layout
    gui_label = psg.Text(text='UT Course Registration Helper',font=('Arial Bold', 20), size=20,expand_x=True,justification='center')

    # professor last name
    lastname_prompt = psg.Text(text='Professor Last Name', expand_x=True)
    lastname_input = psg.Input(key='professor_last_name', justification='left')

    # course prefix
    course_prefix_prompt = psg.Text(text='Course Prefix (Ex: M E)', expand_x=True)
    course_prefix_input = psg.Input(key='course_prefix', justification='left')

    # course number
    course_number_prompt = psg.Text(text='Course Number (Ex: 369P)', expand_x=True)
    course_number_input = psg.Input(key='course_number', justification='left')

    # sentiment analysis
    sentiment_title = psg.Text('Sentiment Analysis (via RateMyProfessor)', justification='center', expand_x=True)
    sentiment_button = psg.Button("Check Professor Sentiment", button_color='pale green')
    sentiment_result = psg.Text('josh sentiment analysis stuff go here', text_color='grey30')

    # Course Evaluation
    course_eval_title = psg.Text('Course Evaluation', justification='center', expand_x=True)
    course_eval_button = psg.Button("View Professor Course Evaluation", button_color='light blue')
    course_eval_result = psg.Text('cade course eval results go here', text_color='grey30')

    # grade distribution
    grade_title = psg.Text('Grade Distributions', justification='center', expand_x=True)

    years = ['2010-2011','2011-2012','2012-2013','2013-2014','2014-2015','2015-2016','2016-2017','2017-2018','2018-2019','2019-2020','2020-2021','2021-2022','2022-2023']
    semesters = ['Fall', 'Spring', 'Summer']

    year_prompt = psg.Text(text='Select School Year', expand_x=False)
    year_combo = psg.Combo(years, key='year', expand_x=True)

    semester_prompt = psg.Text(text='Select Semester', expand_x=False)
    semester_combo = psg.Combo(semesters, key='semester', expand_x=True)

    grade_distribution_button = psg.Button("View Grade Distribution", button_color='sienna')
    # course evaluation stuff

    # misc
    exit_button = psg.Exit(button_color = 'red')

    layout = [
        [gui_label],
        [lastname_prompt, lastname_input],
        [course_prefix_prompt, course_prefix_input],
        [course_number_prompt, course_number_input],
        [psg.Text('', size=(1, 1))], # blank line
        [sentiment_title],
        [sentiment_button],
        [sentiment_result],
        [psg.Text('', size=(1, 1))],  # blank line
        [course_eval_title],
        [course_eval_button],
        [course_eval_result],
        [psg.Text('', size=(1, 1))],  # blank line
        [grade_title],
        [year_prompt, year_combo],
        [semester_prompt, semester_combo],
        [grade_distribution_button],
        [psg.Text('', size=(1, 1))],  # blank line
        [exit_button],
        ]

    window = psg.Window('UT Course Registration Helper', layout, element_justification='c')

    # event handling
    while True:
        event, values = window.read()
        print(event, values)
        if event in (None, 'Exit'):
            break


    window.close()

create_gui()