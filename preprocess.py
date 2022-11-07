from nltk import sent_tokenize, word_tokenize, pos_tag
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer


class PreProcess:
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
    def remove_stopwords(text):
        """
        Remove stopwords from the text.
        :param text: the text string
        :return: a list of tokens
        """
        return [w for w in text if w not in stopwords.words('english')]

    @staticmethod
    def lemmatize(text):
        """
        Lemmatize the text.
        :param text: the text string
        :return: a list of tokens
        """
        lemmatizer = WordNetLemmatizer()
        return [lemmatizer.lemmatize(w, 'n') for w in text]
        return [lemmatizer.lemmatize(w, 'v') for w in text]
        return [lemmatizer.lemmatize(w, 'a') for w in text]
        return [lemmatizer.lemmatize(w, 'r') for w in text]
        return [lemmatizer.lemmatize(w, 's') for w in text]
