class Story:
    def __init__(self, story_id, headline, date, text, raw_text):
        self.story_id = story_id
        self.headline = headline
        self.date = date
        self.text = text
        self.questions = []
        self._raw_text = raw_text

    def __str__(self):
        return f"StoryID: {self.story_id}\n" \
               f"Headline: {self.headline}\n" \
               f"Text: {self.text[0:75]}...\n"

    @staticmethod
    def parse(text):

        lines = text.splitlines()
        headline = lines[0].split(':')[-1].strip()
        date = lines[1].split(':')[-1].strip()
        story_id = lines[2].split(':')[-1].strip()
        text = '\n'.join(lines[6:])

        return Story(story_id, headline, date, text, text)


class Question:
    def __init__(self, question_id, question, difficulty, answer):
        self.id = question_id
        self.question = question
        self.difficulty = difficulty
        self.answer = answer

    def __str__(self):
        return f"QuestionID: {self.id}\n" \
               f"Question: {self.question}\n" \
               f"Answer: {self.answer}\n" \
               f"Difficulty: {self.difficulty}"

    @staticmethod
    def parse_questions(text):
        question_text_blocks = text.split('\n\n')
        questions = []
        for block in question_text_blocks:
            if block == '':
                continue
            lines = block.splitlines()
            question_id = lines[0].split(': ')[-1].strip()
            answer = lines[1].split(': ')[-1].strip()
            difficulty = lines[2].split(': ')[-1].strip()
            questions.append(Question(question_id, answer, difficulty, None))

        return questions
