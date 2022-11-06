import sys
from qa_evaluator import QAEvaluator
from helpers import Question, Story


class QA:
    def __init__(self, input_file):
        print("QA initialized")
        self.input_file = input_file
        self.input_dir = None
        self.story_ids = []
        self.stories = {}
        self.parse_input_file()
        self.parse_stories()
        self.parse_questions()

    def parse_input_file(self):
        with open(self.input_file, 'r') as story_list:
            self.input_dir = story_list.readline().strip()
            for line in story_list:
                self.story_ids.append(line.strip())

            print(self.input_dir)
            print(self.story_ids)

    def parse_stories(self):
        for story_id in self.story_ids:
            with open(self.input_dir + '/' + story_id + '.story', 'r') as story_file:
                self.stories[story_id] = Story.parse(story_file.read())

        pass

    def parse_questions(self):
        for story_id in self.story_ids:
            with open(self.input_dir + '/' + story_id + '.questions', 'r') as question_file:
                self.stories[story_id].questions = Question.parse_questions(question_file.read())
        pass

    def answer_questions(self):
        pass


if __name__ == '__main__':
    input_file = sys.argv[1]

    QA = QA(input_file)

    evaluator = QAEvaluator()
