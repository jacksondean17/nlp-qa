import sys
from qa_evaluator import QAEvaluator
from helpers import Question, Story
from QAOptions import QAOptions
from question_classifier import QuestionClassifier


class QA:
    def __init__(self, input_file, options=QAOptions()):
        self.input_file = input_file
        self.input_dir = None
        self.story_ids = []
        self.stories = {}
        self.question_classifier = QuestionClassifier('./test-files/question_training.txt')
        self.parse_input_file()
        self.parse_stories()
        self.parse_questions()
        self.options = options

    def parse_input_file(self):
        with open(self.input_file, 'r') as story_list:
            self.input_dir = story_list.readline().strip()
            for line in story_list:
                self.story_ids.append(line.strip())

    def parse_stories(self):
        for story_id in self.story_ids:
            with open(self.input_dir + '/' + story_id + '.story', 'r') as story_file:
                self.stories[story_id] = Story.parse(story_file.read())

        pass

    def parse_questions(self):
        for story_id in self.story_ids:
            with open(self.input_dir + '/' + story_id + '.questions', 'r') as question_file:
                self.stories[story_id].questions = Question.parse_questions(question_file.read(), classifier=self.question_classifier)
        pass

    def answer_questions(self):
        # return: a dict of question_id to answer
        # side effect: print out the answers in the format of
        #     QuestionID: <question_id>
        #     Answer: <answer>

        for story in self.stories.values():
            story.answer_questions()

    def print_answers(self):
        s = ''
        for story in self.stories.values():
            s += story.print_answers()
        return s

    def save_answers(self, filename):
        with open(filename, 'w') as f:
            f.write(self.print_answers())


if __name__ == '__main__':
    input_file = sys.argv[1]
    output_file = None
    if len(sys.argv) > 2:
        output_file = sys.argv[2]

    answer_file = None
    if len(sys.argv) > 3:
        answer_file = sys.argv[3]

    QA = QA(input_file)
    QA.answer_questions()
    # save to file if specified, otherwise print to stdout
    if output_file:
        QA.save_answers(output_file)
    else:
        print(QA.print_answers())

    # evaluate if answer file is specified
    if answer_file:
        evaluator = QAEvaluator()
        evaluator.evaluate(output_file, answer_file)
