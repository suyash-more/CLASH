from django.test import TestCase
from .models import Questions

class QuestionTestCase(TestCase):
    def testQuestion(self):
        question = Questions(question="Which laptop is good?", option_A="dell", option_B="hp", option_C="lenovo", option_D="acer", 
        correct_answer="hp")
        self.assertEqual(question.question, "Which laptop is good?")
        self.assertEqual(question.option_A, "dell")
        self.assertEqual(question.option_B, "hp")
        self.assertEqual(question.option_C, "lenovo")
        self.assertEqual(question.option_D, "acer")
        self.assertEqual(question.correct_answer, "hp")

