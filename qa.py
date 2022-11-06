import sys
from qa_evaluator import QAEvaluator

class QA:
    def __init__(self, input_file):
        print("QA initialized")
        self.input_file = input_file


if __name__ == '__main__':
    input_file = sys.argv[1]

    QA = QA(input_file)

    evaluator = QAEvaluator()