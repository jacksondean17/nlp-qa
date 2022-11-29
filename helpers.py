from rake_nltk import Rake
from preprocess import Preprocess as pp
from QAOptions import QAOptions
import en_core_web_sm


class Story:
    def __init__(self, story_id, headline, date, text, raw_text, options=None, spacy_model=None):
        self.options = options
        if self.options is None:
            self.options = QAOptions()

        self.spacy_model = spacy_model
        if spacy_model is None:
            self.spacy_model = en_core_web_sm.load()

        self.story_id = story_id
        self.headline = headline
        self.date = date
        self.text = text
        self.sentences = pp.sentence_tokenize(text)
        self.processed_sentences = [Sentence(s, self.options, self.spacy_model) for s in self.sentences]
        self.questions = []
        self._raw_text = raw_text

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

       # '''
        if (question.question_type == 'HUM.individual' or
                # question.question_type == 'HUM.group' or
                question.question_type[0][:3] == 'LOC' or
                question.question_type[0][:3] == 'NUM'):
            ans = self.extract_answer(question, question.candidate_sentences)
        else:
            # return highest scoring sentence without the question words
            ans = set(question.candidate_sentences[0].words) - set(question.processed_question)
        '''
        ans = set(question.candidate_sentences[0].words) - set(question.processed_question)
        '''

        return ' '.join(ans)



        return question.candidate_sentences[0].text

    def extract_answer(self, question, sentences):
        if question.question_type == 'HUM.individual':
            for i in range(self.options.num_candidate_sentences):
                for ne in sentences[i].nes:
                    if ne[1] == 'PERSON' and ne[0].lower() not in question.processed_question:
                        return [ne[0]]

#        elif question.question_type == 'HUM.group':
#            for i in range(self.options.num_candidate_sentences):
#                for ne in sentences[i].nes:
#                    if ne[1] == 'ORG' or ne[1] == 'NORP' or ne[1] == 'GPE' and ne[0].lower() not in question.processed_question:
#                        return [ne[0]]


        elif question.question_type == 'LOC.city':
            for i in range(self.options.num_candidate_sentences):
                for ne in sentences[i].nes:
                    if ne[1] == 'GPE' and ne[0].lower() not in question.processed_question:
                        return [ne[0]]
        elif question.question_type == 'LOC.country':
            for i in range(self.options.num_candidate_sentences):
                for ne in sentences[i].nes:
                    if ne[1] == 'GPE' and ne[0].lower() not in question.processed_question:
                        return [ne[0]]
        elif question.question_type == 'LOC.other':
            for i in range(self.options.num_candidate_sentences):
                for ne in sentences[i].nes:
                    if ne[1] == 'LOC' and ne[0].lower() not in question.processed_question:
                        return [ne[0]]

        elif question.question_type == 'NUM.age':
            for i in range(self.options.num_candidate_sentences):
                for ne in sentences[i].nes:
                    if ne[1] == 'DATE':
                        return [ne[0]]
        elif question.question_type == 'NUM.date':
            for i in range(self.options.num_candidate_sentences):
                for ne in sentences[i].nes:
                    if ne[1] == 'DATE' or ne[1] == 'TIME':
                        return [ne[0]]
        elif question.question_type == 'NUM.money':
            for i in range(self.options.num_candidate_sentences):
                for ne in sentences[i].nes:
                    if ne[1] == 'MONEY':
                        return [ne[0]]
        elif question.question_type == 'NUM.distance':
            for i in range(self.options.num_candidate_sentences):
                for ne in sentences[i].nes:
                    if ne[1] == 'QUANTITY':
                        return [ne[0]]
        elif question.question_type == 'NUM.period':
            for i in range(self.options.num_candidate_sentences):
                for ne in sentences[i].nes:
                    if ne[1] == 'DATE' or ne[1] == 'TIME':
                        return [ne[0]]

        return sentences[0].words

    def get_candidate_sentences(self, question):
        sentence_scores = {}
        for i, sentence in enumerate(self.processed_sentences):
            sentence_scores[i] = sentence.score(question)

        sorted_scores = sorted(sentence_scores.items(), key=lambda x: x[1], reverse=True)
        return [self.processed_sentences[i] for i, score in sorted_scores[:self.options.num_candidate_sentences]]

    def print_answers(self):
        s = ''
        for question in self.questions:
            s += f"QuestionID: {question.id}" + '\n' + f"Answer: {question.answer}" + '\n\n'
        return s

    @staticmethod
    def parse(text, sp_model=None, options=None):
        """
        Parse the original text from the *.story file into a Story object
        :param text: The text from the *.story file
        :param sp_model: A Spacy model
        :return: a Story object
        """
        lines = text.splitlines()
        headline = lines[0].split(':')[-1].strip()
        date = lines[1].split(':')[-1].strip()
        story_id = lines[2].split(':')[-1].strip()
        text = '\n'.join(lines[6:])

        return Story(story_id, headline, date, text, text, spacy_model=sp_model, options=options)


class Sentence:
    def __init__(self, text, options=None, spacy_model=None):
        self.spacy_model = spacy_model
        if spacy_model is None:
            self.spacy_model = en_core_web_sm.load()

        # replace newlines with spaces
        self.text = text.replace('\n', ' ').strip()
        self.spacy_doc = self.spacy_model(self.text)
        self.nes = [(X.text, X.label_) for X in self.spacy_doc.ents]
        self.words = pp.word_tokenize(text)
        self.tagged_words = pp.pos_tag(self.words)
        self.processed_words = pp.lemmatize(pp.remove_stopwords(self.words))
        if options is None:
            self.options = QAOptions()
        else:
            self.options = options

    def score(self, question):
        """
        Score the sentence relative to the question
        :param question: a Question object
        :return: the score of the sentence
        """
        # join all question synonyms
        sentence_synonyms = set()
        for word, syns in question.word_synonyms:
            sentence_synonyms.update(syns)

        score = 0
        # word matching
        for word in self.processed_words:
            if word in question.processed_question:
                score += self.options.sentence_scoring_weights['keyword_exact_match']
            elif word in sentence_synonyms:
                score += self.options.sentence_scoring_weights['keyword_synonym_match']

        # named entity matching
        # for ne in self.nes:
        # if ne[0] in question.nes:
        # score += self.options.sentence_scoring_weights['named_entity_match']

        if True:
            # fine-grained question type matching
            if question.question_type == 'DES.definition':
                for ne in self.nes:

                    pass
            elif question.question_type == 'DES.description':
                for ne in self.nes:
                    pass
            elif question.question_type == 'DES.reason':
                for ne in self.nes:
                    pass
            elif question.question_type == 'ENT.animal':
                for ne in self.nes:
                    pass
            elif question.question_type == 'ENT.event':
                for ne in self.nes:
                    if ne[1] == 'EVENT':
                        score += self.options.sentence_scoring_weights['q_type_ner_category_fine']['ENT.event']
                    pass
            elif question.question_type == 'ENT.other':
                for ne in self.nes:
                    pass
            elif question.question_type == 'ENT.term':
                for ne in self.nes:
                    pass
            elif question.question_type == 'HUM.description':
                for ne in self.nes:
                    if ne[1] == 'PERSON':
                        score += self.options.sentence_scoring_weights['q_type_ner_category_fine']['HUM.description']
                    pass
            elif question.question_type == 'HUM.group':
                for ne in self.nes:
                    if (ne[1] == 'ORG' or
                            ne[1] == 'NORP' or
                            ne[1] == 'GPE'):
                        score += self.options.sentence_scoring_weights['q_type_ner_category_fine']['HUM.group']
                    pass
            elif question.question_type == 'HUM.individual':
                for ne in self.nes:
                    if ne[1] == 'PERSON':
                        score += self.options.sentence_scoring_weights['q_type_ner_category_fine']['HUM.individual']
                    pass
            elif question.question_type == 'LOC.city':
                for ne in self.nes:
                    if ne[1] == 'GPE':
                        score += self.options.sentence_scoring_weights['q_type_ner_category_fine']['LOC.city']
                    pass
            elif question.question_type == 'LOC.country':
                for ne in self.nes:
                    if ne[1] == 'GPE':
                        score += self.options.sentence_scoring_weights['q_type_ner_category_fine']['LOC.country']
                    pass
            elif question.question_type == 'LOC.other':
                for ne in self.nes:
                    if ne[1] == 'LOC':
                        score += self.options.sentence_scoring_weights['q_type_ner_category_fine']['LOC.other']
                    pass
            elif question.question_type == 'NUM.age':
                for ne in self.nes:
                    if ne[1] == 'DATE':
                        score += self.options.sentence_scoring_weights['q_type_ner_category_fine']['NUM.age']
                    pass
            elif question.question_type == 'NUM.count':
                for ne in self.nes:
                    if ne[1] == 'CARDINAL':
                        score += self.options.sentence_scoring_weights['q_type_ner_category_fine']['NUM.count']
                    pass
            elif question.question_type == 'NUM.date':
                for ne in self.nes:
                    if (ne[1] == 'DATE' or
                            ne[1] == 'TIME'):
                        score += self.options.sentence_scoring_weights['q_type_ner_category_fine']['NUM.date']
                    pass
            elif question.question_type == 'NUM.distance':
                for ne in self.nes:
                    if ne[1] == 'QUANTITY':
                        score += self.options.sentence_scoring_weights['q_type_ner_category_fine']['NUM.distance']
                    pass
            elif question.question_type == 'NUM.money':
                for ne in self.nes:
                    if ne[1] == 'MONEY':
                        score += self.options.sentence_scoring_weights['q_type_ner_category_fine']['NUM.money']
                    pass
            elif question.question_type == 'NUM.other':
                for ne in self.nes:
                    if (ne[1] == 'ORDINAL' or
                            ne[1] == 'TIME' or
                            ne[1] == 'PERCENT' or
                            ne[1] == 'QUANTITY' or
                            ne[1] == 'CARDINAL'):
                        score += self.options.sentence_scoring_weights['q_type_ner_category_fine']['NUM.other']
                    pass
            elif question.question_type == 'NUM.period':
                for ne in self.nes:
                    if (ne[1] == 'DATE' or
                            ne[1] == 'TIME'):
                        score += self.options.sentence_scoring_weights['q_type_ner_category_fine']['NUM.period']
                    pass


        # match question type with named entities
        if (False):
            if question.question_type == 'HUM':
                for ne in self.nes:
                    if (ne[1] == 'PERSON' or
                            ne[1] == 'ORG' or
                            ne[1] == 'NORP'):
                        score += self.options.sentence_scoring_weights['q_type_ner_category']['HUM']
            elif question.question_type == 'NUM':
                for ne in self.nes:
                    if (ne[1] == 'DATE' or
                            ne[1] == 'TIME' or
                            ne[1] == 'PERCENT' or
                            ne[1] == 'MONEY' or
                            ne[1] == 'QUANTITY' or
                            ne[1] == 'CARDINAL' or
                            ne[1] == 'ORDINAL'):
                        score += self.options.sentence_scoring_weights['q_type_ner_category']['NUM']
            elif question.question_type == 'LOC':
                for ne in self.nes:
                    if (ne[1] == 'GPE' or
                            ne[1] == 'FAC' or
                            ne[1] == 'LOC'):
                        score += self.options.sentence_scoring_weights['q_type_ner_category']['LOC']
            elif question.question_type == 'ENT':
                for ne in self.nes:
                    if (ne[1] == 'ORG' or
                            ne[1] == 'PERSON' or
                            ne[1] == 'GPE' or
                            ne[1] == 'FAC' or
                            ne[1] == 'LOC'):
                        score += self.options.sentence_scoring_weights['q_type_ner_category']['ENT']
            elif question.question_type == 'DES':
                # no named entity matching for description questions
                # for ne in self.nes:
                    # if ne[1] == 'ORG':
                        # score += self.options.sentence_scoring_weights['q_type_ner_category']
                pass


        return score

    def __repr__(self):
        return self.text


class Question:
    def __init__(self, question_id, question, difficulty, answer, classifier=None):
        self.id = question_id
        self.question = question
        self.difficulty = difficulty
        self.answer = answer

        self.keywords = self.extract_keywords(self.question)
        self.tokenized_question = pp.word_tokenize(self.question)
        self.tagged_question = pp.pos_tag(self.tokenized_question)
        self.word_synonyms = pp.get_synonyms(pp.remove_stopwords(self.tagged_question, is_question=True))

        # self.processed_question = pp.lemmatize(pp.remove_stopwords(self.tokenized_question, is_question=True))
        self.processed_question = pp.preprocess_question(self.question)

        self.classifier = classifier
        if classifier is not None:
            self.question_type = self.classifier.classify(self.processed_question)

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
    def parse_questions(text, classifier=None):
        """
        Parse the questions from the original *.questions file
        :param text: The text of the *.questions file
        :param classifier: a QuestionClassifier object
        :return: A list of Question objects
        """
        question_text_blocks = text.split('\n\n')
        questions = []
        for block in question_text_blocks:
            if block == '':
                continue
            lines = block.splitlines()
            question_id = lines[0].split(': ')[-1].strip()
            question = lines[1].split(': ')[-1].strip()
            difficulty = lines[2].split(': ')[-1].strip()
            questions.append(Question(question_id, question, difficulty, None, classifier))

        return questions
