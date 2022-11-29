import subprocess


class QAEvaluator:
    def __init__(self):
        pass

    def evaluate(self, response_file, answer_file):
        # qa_answers: a list of answers
        # qa_gold_answers: a list of gold answers
        # return: a dictionary of metrics
        # side effect: print out the metrics
        pipe = subprocess.run(["perl", "score-answers.pl", response_file, answer_file])

        pass

    def evaluate_quiet(self, response_file, answer_file):
        # qa_answers: a list of answers
        # qa_gold_answers: a list of gold answers
        # return: a dictionary of metrics
        # side effect: print out the metrics
        pipe = subprocess.run(["perl", "score-answers-quiet.pl", response_file, answer_file], stdout=subprocess.PIPE)
        res = float(pipe.stdout.decode('utf-8'))
        return res

