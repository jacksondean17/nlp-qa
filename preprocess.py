from nltk import sent_tokenize, word_tokenize, pos_tag
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.corpus import wordnet
from nltk.wsd import lesk


class Preprocess:
    @staticmethod
    def word_tokenize(text):
        """
        Tokenize the text into a list of words.
        Also removes punctuation and normalize the case.
        :param text: the text string
        :return: a list of tokens
        """
        # tokenize
        t = word_tokenize(text)
        # remove punctuation
        t = [w for w in t if w.isalnum()]
        # normalize
        t = [w.lower() for w in t]
        return t

    @staticmethod
    def sentence_tokenize(text):
        """
        Tokenize the text into a list of sentences.
        :param text: the text string
        :return: a list of sentences
        """
        return sent_tokenize(text)

    @staticmethod
    def remove_stopwords(text, is_question=False):
        """
        Remove stopwords from the text.
        :param text: a list of tokens OR a list of tagged tokens (word, tag)
        :return: a list of tokens OR a list of tagged tokens (word, tag)
        """
        if is_question:
            # keep the question words
            stop_words = set(stopwords.words('english')) - {'what', 'when', 'where', 'why', 'how', 'which', 'who'}
        else:
            stop_words = set(stopwords.words('english'))

        if len(text) == 0:
            return text
        if isinstance(text[0], tuple):
            # remove stopwords from a list of tagged tokens
            return [(w, t) for w, t in text if w not in stop_words]
        else:
            # remove stopwords from a list of tokens
            return [w for w in text if w not in stop_words]

    @staticmethod
    def lemmatize(text):
        """
        Lemmatize the text.
        :param text: a list of tokens
        :return: a list of lemmatized tokens
        """
        lemmatizer = WordNetLemmatizer()
        l = [lemmatizer.lemmatize(w, 'n') for w in text]
        l = [lemmatizer.lemmatize(w, 'v') for w in l]
        l = [lemmatizer.lemmatize(w, 'a') for w in l]
        l = [lemmatizer.lemmatize(w, 'r') for w in l]
        return [lemmatizer.lemmatize(w, 's') for w in l]

    @staticmethod
    def pos_tag(tokenized_sentence):
        """
        POS tag the tokenized sentence.
        :param tokenized_sentence: a list of tokens
        :return: a list of tuples (token, tag)
        """
        return pos_tag(tokenized_sentence)

    @staticmethod
    def get_sense(words, word, tag):
        if tag.startswith('NN'):
            syn = lesk(words, word, 'n')
        elif tag.startswith('VB'):
            syn = lesk(words, word, 'v')
        elif tag.startswith('JJ'):
            syn = lesk(words, word, 'a')
        elif tag.startswith('RB'):
            syn = lesk(words, word, 'r')
        else:
            syn = []
        return syn

    @staticmethod
    def get_synonyms(tagged_words):
        """
        Get the synonyms of the words in the tagged sentence.
        :param tagged_words: the tagged sentence
        :return: a list of tuples (word, synonyms)
        """

        '''
        # If I want to disambiguate the word sense first
        words = [w for w, t in tagged_words]
        synonyms = []
        for word, tag in tagged_words:
            syn = Preprocess.get_sense(words, word, tag)
            if syn:
                synonyms.append((word, [l.name() for l in syn.lemmas()]))

        return synonyms
        '''

        '''
        # If I just want synonyms for all senses and all POS
        synonyms = []
        for word, tag in tagged_words:
            syns = wordnet.synsets(word)
            word_syns = set()
            for syn in syns:
                word_syns.update([l.name() for l in syn.lemmas()])
            word_syns.discard(word)
            synonyms.append((word, word_syns))

        return synonyms
        '''

        # If I just want synonyms for all senses
        synonyms = []
        for word, tag in tagged_words:
            if tag.startswith('NN'):
                syns = wordnet.synsets(word, 'n')
            elif tag.startswith('VB'):
                syns = wordnet.synsets(word, 'v')
            elif tag.startswith('JJ'):
                syns = wordnet.synsets(word, 'a')
            elif tag.startswith('RB'):
                syns = wordnet.synsets(word, 'r')
            else:
                syns = wordnet.synsets(word)

            word_syns = set()
            for syn in syns:
                word_syns.update([l.name() for l in syn.lemmas()])
            word_syns.discard(word)
            synonyms.append((word, word_syns))
        return synonyms



    @staticmethod
    def get_antonyms(word):
        """
        Get the antonyms of a word.
        :param word: the word
        :return: a list of antonyms
        """
        antonyms = set()
        for syn in wordnet.synsets(word):
            for l in syn.lemmas():
                if l.antonyms():
                    antonyms.add(l.antonyms()[0].name())
        return antonyms

