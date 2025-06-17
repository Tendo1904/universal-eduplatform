from .models import Test, Question, Answer, Solutions, Result


def formula_1(id_result):
    """
    Calculate the total points scored based on the user's answers to questions.

        This method retrieves the result associated with a given ID, filters the questions
        related to the test corresponding to that result, and calculates the total points
        earned by the user for their answers. It considers correct and incorrect answers
        along with the points assigned to each question.

        Args:
            id_result: The identifier for the result entry which links to the test and answers.

        Returns:
            The total points scored by the user, calculated based on their responses to the questions.
    """
    result = Result.objects.get(pk=id_result)
    questions = Question.objects.filter(id_test=result.id_test)
    points_total = 0
    for question in questions:
        points_question = 0
        correct_answers = [
            answer.answer_text
            for answer in Answer.objects.filter(
                id_question=question.pk, is_correct=True
            )
        ]
        num_right = len(correct_answers)
        num_all = Answer.objects.filter(id_question=question.pk).count()
        solutions = Solutions.objects.filter(
            id_result=id_result, id_question=question.pk
        )
        for solution in solutions:
            if solution.user_answer in correct_answers:
                points_question += 1 / num_right
            else:
                points_question -= 1 / num_all
        points_question *= question.question_points
        points_question = round(points_question, 2)
        points_total += points_question
    return points_total
