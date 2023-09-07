from flask import Blueprint, render_template, request, redirect, url_for
import csv
from pathlib import Path

quiz_blueprint = Blueprint('quiz', __name__, template_folder='templates')

# use for store path of quiz file, quiz score and question No
class quizConfig():
    # quiz file store path
    QUIZ_DIR = Path(__file__).resolve().parent.parent.joinpath('quiz.txt')
    f = csv.reader(open(QUIZ_DIR, "r"))
    questions = list()
    for i in f:
        questions.append(i)

    quiz_score = 0
    question_no = 0


# add new object for new quiz
quiz_config = quizConfig()


# view quiz
@quiz_blueprint.route('/quiz', methods=['GET', 'POST'])
def quiz():
    quiz_btn_txt = "Next"
    return render_template('quiz.html', question=quiz_config.questions[0][0], question_no=quiz_config.question_no + 1,
                           ans1=quiz_config.questions[0][1], ans2=quiz_config.questions[0][2],
                           ans3=quiz_config.questions[0][3], quiz_btn_txt=quiz_btn_txt,
                           link=quiz_config.questions[0][4],
                           score=quiz_config.quiz_score)


# if click new question
@quiz_blueprint.route('/next_question', methods=['GET', 'POST'])
def next_question():
    # if user not give answer for checkbox, refresh page
    if not request.form.get("answer"):
        return render_template('quiz.html',
                               question=quiz_config.questions[quiz_config.question_no][0],
                               question_no=quiz_config.question_no + 1,
                               ans1=quiz_config.questions[quiz_config.question_no][1],
                               ans2=quiz_config.questions[quiz_config.question_no][2],
                               ans3=quiz_config.questions[quiz_config.question_no][3],
                               quiz_btn_txt="Next",
                               link=quiz_config.questions[quiz_config.question_no][4],
                               answer_txt="Please choose one choice!",
                               score=quiz_config.quiz_score)
    # question move to next one
    quiz_config.question_no += 1
    answer_txt = ""
    # check answer is correct or not, then move to next question
    if quiz_config.question_no < 5:
        if request.form["answer"] == "1":
            answer_txt = "Correct answer!"
            quiz_config.quiz_score += 1
        else:
            answer_txt = "Incorrect answer!"
        return render_template('quiz.html',
                               question=quiz_config.questions[quiz_config.question_no][0],
                               question_no=quiz_config.question_no + 1,
                               ans1=quiz_config.questions[quiz_config.question_no][1],
                               ans2=quiz_config.questions[quiz_config.question_no][2],
                               ans3=quiz_config.questions[quiz_config.question_no][3],
                               quiz_btn_txt="Next",
                               link=quiz_config.questions[quiz_config.question_no][4],
                               answer_txt=answer_txt,
                               score=quiz_config.quiz_score)
    # if finish quiz, show score and answer text
    elif quiz_config.question_no == 5:
        temp_score = 0
        if request.form["answer"] == "1":
            temp_score = quiz_config.quiz_score + 1
        quiz_config.quiz_score = 0
        quiz_config.question_no = 0
        answer_txt = "Congratulations on completing the test!"
        return render_template('quiz.html', score=temp_score, answer_txt=answer_txt,
                               quiz_btn_txt="Finish")
