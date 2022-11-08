from rake_nltk import Rake
from preprocess import Preprocess as pp
from QAOptions import QAOptions


class Story:
    def __init__(self, story_id, headline, date, text, raw_text, options=None):
        self.story_id = story_id
        self.headline = headline
        self.date = date
        self.text = text
        self.sentences = pp.sentence_tokenize(text)
        self.processed_sentences = [Sentence(s) for s in self.sentences]
        self.questions = []
        self._raw_text = raw_text

        if options is None:
            self.options = QAOptions()
        else:
            self.options = options

    def __str__(self):
        return f"StoryID: {self.story_id}\n" \
               f"Headline: {self.headline}\n" \
               f"Text: {self.text[0:75]}...\n"

    def answer_questions(self):
        answers = {}
        for question in self.questions:
            question.answer = self.answer_question(question)
            answers[question.id] = question.answer
        return answers

    def answer_question(self, question):
        question.candidate_sentences = self.get_candidate_sentences(question)
        return question.candidate_sentences[0].text

    def get_candidate_sentences(self, question):
        sentence_scores = {}
        for i, sentence in enumerate(self.processed_sentences):
            sentence_scores[i] = sentence.score(question.processed_question)

        sorted_scores = sorted(sentence_scores.items(), key=lambda x: x[1], reverse=True)
        return [self.processed_sentences[i] for i, score in sorted_scores[:self.options.num_candidate_sentences]]

    def print_answers(self):
        s = ''
        for question in self.questions:
            s += f"QuestionID: {question.id}" + '\n' + f"Answer: {question.answer}" + '\n\n'
        return s

    @staticmethod
    def parse(text):
        """
        Parse the original text from the *.story file into a Story object
        :param text: The text from the *.story file
        :return: a Story object
        """
        lines = text.splitlines()
        headline = lines[0].split(':')[-1].strip()
        date = lines[1].split(':')[-1].strip()
        story_id = lines[2].split(':')[-1].strip()
        text = '\n'.join(lines[6:])

        return Story(story_id, headline, date, text, text)


class Sentence:
    def __init__(self, text):
        # replace newlines with spaces
        self.text = text.replace('\n', ' ').strip()
        self.words = pp.word_tokenize(text)
        self.processed_words = pp.lemmatize(pp.remove_stopwords(self.words))

    def score(self, keywords):
        """
        Score the sentence based on the number of matching keywords
        :param keywords: a list of keywords
        :return: the score of the sentence
        """
        score = 0
        for word in self.processed_words:
            if word in keywords:
                score += 1
        return score

    def __repr__(self):
        return self.text


class Question:
    def __init__(self, question_id, question, difficulty, answer):
        self.id = question_id
        self.question = question
        self.difficulty = difficulty
        self.answer = answer

        self.keywords = self.extract_keywords(self.question)
        self.tokenized_question = pp.word_tokenize(self.question)
        self.processed_question = pp.lemmatize(pp.remove_stopwords(self.tokenized_question))

        self.candidate_sentences = []

    def __str__(self):
        return f"QuestionID: {self.id}\n" \
               f"Question: {self.question}\n" \
               f"Answer: {self.answer}\n" \
               f"Difficulty: {self.difficulty}"

    @staticmethod
    def extract_keywords(question):
        """
        Extract keywords from the question
        :param question: the question text
        :return: a list of keywords
        """
        # this has a ton of options that I might want to play with later
        r = Rake(max_length=3)
        r.extract_keywords_from_text(question)
        return r.get_ranked_phrases()  # maybe only return the top 5 or 10?

    @staticmethod
    def parse_questions(text):
        """
        Parse the questions from the original *.questions file
        :param text: The text of the *.questions file
        :return: A list of Question objects
        """
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
