from nltk import sent_tokenize, word_tokenize, pos_tag
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from rake_nltk import Rake
from preprocess import PreProcess as pp


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
        self.text = text
        self.words = word_tokenize(text)


class Question:
    def __init__(self, question_id, question, difficulty, answer):
        self.id = question_id
        self.question = question
        self.difficulty = difficulty
        self.answer = answer

        self.keywords = self.extract_keywords(self.question)
        self.tokenized_question = pp.word_tokenize(self.question)
        self.processed_question = pp.lemmatize(pp.remove_stopwords(self.tokenized_question))

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
