"""
Structure:
{
    name: "Name of the Quiz",
    video_id: "YouTube Video Id",
    type: "single|multiple",
    "number_questions": number of questions in the quiz
    questions:
    [
        Question1, [Answer1_1, Answer1_2, ..., Answer1_A],
        Question2, [Answer2_1, Answer2_2, ..., Answer2_B],
        ...
        QuestionN, [AnswerN_1, AnswerN_2, ..., AnswerN_Z],
    ]
}

Each Question can have different number of answers.
"""



quizes = [
            { "name": "My First Quiz", "video_id": "Rerw3432-WewE", "type": "single", "number_questions": 5, "questions": ["Question 1", ["Answer 1","Answer 2","Answer 3"], "Question 2", ["Answer 1","Answer 2","Answer 3"], "Question 3", ["Answer 1","Answer 2","Answer 3"]]},
            { "name": "QQuiZZ Test", "video_id": "UyHi13Wr-Z8Jo", "type": "single", "number_questions": 15, "questions": ["This is question 1", ["Answer 1","Answer 2","Answer 3"], "This is question 2", ["Answer 1","Answer 2"], "This is question 3", ["Answer 1","Answer 2"], "This is Question 4", ["Answer 1","Answer 2","Answer 3", "Answer 4"]]},
            { "name": "Bitcoin Test", "video_id": "78Ujeu-weE4", "type": "multiple", "number_questions": 15, "questions": ["This is question 1", ["Answer 1","Answer 2","Answer 3","Answer 4", "Answer 5"], "This is question 2", ["Answer 1","Answer 2","Answer 3","Answer 4", "Answer 5"], "This is question 3", ["Answer 1","Answer 2","Answer 3","Answer 4", "Answer 5"], "This is question 4", ["Answer 1","Answer 2","Answer 3","Answer 4", "Answer 5"]]}
        ]


def prepare_quiz_to_insert(quiz_name: str, video_id: str, quiz_type: str, number_questions: int, questions: list[str]):
    return {"name": f"{quiz_name}", "video_id": f"{video_id}", "type": f"{quiz_type}", "number_questions": f"{number_questions}", "questions": questions}
