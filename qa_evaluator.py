import subprocess


class QAEvaluator:
    def __init__(self):
        print("QAEvaluator initialized")
        pass

    def evaluate(self, response_file, answer_file):
        # qa_answers: a list of answers
        # qa_gold_answers: a list of gold answers
        # return: a dictionary of metrics
        # side effect: print out the metrics
        pipe = subprocess.run(["perl", "score-answers.pl", response_file, answer_file])


        pass
