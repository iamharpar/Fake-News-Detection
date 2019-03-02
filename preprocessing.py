from sklearn.feature_extraction.text import TfidfVectorizer
from nltk.tokenize import word_tokenize,WhitespaceTokenizer
from nltk.stem import WordNetLemmatizer 
from keras.utils.np_utils import to_categorical
from keras.preprocessing.text import Tokenizer
from keras.preprocessing.sequence import pad_sequences
import scipy.sparse

import pandas as pd
import numpy as np 
import pickle as pk
import dirs as dr
import utils as ut

'''
    execute 
    >>>import nltk
    >>>nltk.download("punkt")
    >>>nltk.download("stopwords")
    >>nltk.download('words')
    >>>nltk.download('wordnet')
'''

label_ref = {'agree': 0, 'disagree': 1, 'discuss': 2, 'unrelated': 3}
label_ref_rev = {0: 'agree', 1: 'disagree', 2: 'discuss', 3: 'unrelated'}
col_ref = {'body':'articleBody','headline':'Headline','id':'Body ID','stance':'Stance'}
STOP_WORDS_SET = [
        "a", "about", "above", "across", "after", "afterwards", "again", "against", "all", "almost", "alone", "along",
        "already", "also", "although", "always", "am", "among", "amongst", "amoungst", "amount", "an", "and", "another",
        "any", "anyhow", "anyone", "anything", "anyway", "anywhere", "are", "around", "as", "at", "back", "be",
        "became", "because", "become", "becomes", "becoming", "been", "before", "beforehand", "behind", "being",
        "below", "beside", "besides", "between", "beyond", "bill", "both", "bottom", "but", "by", "call", "can", "co",
        "con", "could", "cry", "de", "describe", "detail", "do", "done", "down", "due", "during", "each", "eg", "eight",
        "either", "eleven", "else", "elsewhere", "empty", "enough", "etc", "even", "ever", "every", "everyone",
        "everything", "everywhere", "except", "few", "fifteen", "fifty", "fill", "find", "fire", "first", "five", "for",
        "former", "formerly", "forty", "found", "four", "from", "front", "full", "further", "get", "give", "go", "had",
        "has", "have", "he", "hence", "her", "here", "hereafter", "hereby", "herein", "hereupon", "hers", "herself",
        "him", "himself", "his", "how", "however", "hundred", "i", "ie", "if", "in", "inc", "indeed", "interest",
        "into", "is", "it", "its", "itself", "keep", "last", "latter", "latterly", "least", "less", "ltd", "made",
        "many", "may", "me", "meanwhile", "might", "mill", "mine", "more", "moreover", "most", "mostly", "move", "much",
        "must", "my", "myself", "name", "namely", "neither", "nevertheless", "next", "nine", "nobody", "now", "nowhere",
        "of", "off", "often", "on", "once", "one", "only", "onto", "or", "other", "others", "otherwise", "our", "ours",
        "ourselves", "out", "over", "own", "part", "per", "perhaps", "please", "put", "rather", "re", "same", "see",
        "serious", "several", "she", "should", "show", "side", "since", "sincere", "six", "sixty", "so", "some",
        "somehow", "someone", "something", "sometime", "sometimes", "somewhere", "still", "such", "system", "take",
        "ten", "than", "that", "the", "their", "them", "themselves", "then", "thence", "there", "thereafter", "thereby",
        "therefore", "therein", "thereupon", "these", "they", "thick", "thin", "third", "this", "those", "though",
        "three", "through", "throughout", "thru", "thus", "to", "together", "too", "top", "toward", "towards", "twelve",
        "twenty", "two", "un", "under", "until", "up", "upon", "us", "very", "via", "was", "we", "well", "were", "what",
        "whatever", "when", "whence", "whenever", "where", "whereafter", "whereas", "whereby", "wherein", "whereupon",
        "wherever", "whether", "which", "while", "whither", "who", "whoever", "whole", "whom", "whose", "why", "will",
        "with", "within", "without", "would", "yet", "you", "your", "yours", "yourself", "yourselves","at",
        ]

lemmatizer = WordNetLemmatizer()
w_tokenizer = WhitespaceTokenizer()

BODY_KEY = "body"
STANCE_KEY = "stance"
HEADLINE_KEY = 'headline'

nb_words = 500

def lemmatize_text(text):
    return ' '.join([lemmatizer.lemmatize(w) for w in w_tokenizer.tokenize(text)])

def remove_nonASCII(text):
    return ''.join([" " if ord(i) < 32 or ord(i) > 126 else i for i in text])

def remove_stopWords(text):
    return ' '.join(["" if i in STOP_WORDS_SET else i for i in text.split(' ')])

def remove_longWords(text):
    return ' '.join(["" if len(i) > 30 else i for i in text.split(' ')])

def remove_numbers(text):
    return ' '.join(s for s in text.split() if not any(c.isdigit() for c in s) and len(s)>0)

def to_lower(text):
    return text.lower()

preprocess_funcs = [
    to_lower,remove_nonASCII,
    remove_stopWords,remove_longWords,
    remove_numbers,lemmatize_text
]

'''
    takes in arguments the type of empbedding_type
    path to the training and test stance and body
    file should be defined in the dirs file

'''

class StanceDataPipeline(object):
    def __init__(self,embedding_type='tf_idf'):
        '''
            df_train or df_test [0] == 'stances'
            df_train or df_test [1] == 'bodies'
        '''
        self.df_train = [None,None]
        self.df_test = [None,None]
        self.word_vectorizer = None
        self.embedding_type = embedding_type

        for index,(train_file,test_file) in enumerate(
            zip(dr.TRAIN_DATASET_FILES.values(),
                dr.TEST_DATASET_FILES.values())):

            self.df_train[index] = pd.read_csv(train_file)
            self.df_test[index] = pd.read_csv(test_file)

    def get_unique_training_words(self):

        return len(self.df_train[1][col_ref['headline']].unique().tolist()) + \
                len(self.df_train[0][col_ref['body']].unique().tolist())

    def __preprocess(self):
        preprocess_count = 0
        df = [self.df_train,self.df_test]

        for preprocess_data in df:
            for func in preprocess_funcs:
                preprocess_data[1][col_ref['headline']] =  preprocess_data[1]\
                    [col_ref['headline']].apply(func)

                preprocess_data[0][col_ref['body']] =  preprocess_data[0]\
                    [col_ref['body']].apply(func)
            
            preprocess_count = preprocess_count + 1
            print("[+] pre-processing for %d/2 done !" % (preprocess_count))

    def __embbed_dataset(self,filename):
        body = self.df_train[0][col_ref['body']].values, 
        headline =  self.df_train[1][col_ref['headline']].values

        concated_corpus = np.concatenate([body[0],headline])

        if self.embedding_type is 'tf_idf':
            self.word_vectorizer = TfidfVectorizer(stop_words=STOP_WORDS_SET)
            self.word_vectorizer.fit(concated_corpus)

        elif self.embedding_type is 'tokenizer':
            self.word_vectorizer = Tokenizer(num_words=20000)
            self.word_vectorizer.fit_on_texts(concated_corpus)
        else:
            pass
        
        print("[+] Transformation of word2vec done with %s" 
            % (self.embedding_type))

        pk.dump(self.word_vectorizer,open(filename,"wb"))
        print("[+] Fitted Corpus %s committed" % (filename))

        return self.word_vectorizer

    def __merge(self):

        DATA_ATTR = [
            self.df_train,
            self.df_test,
        ]

        SAVE_TO_ATTR = [
            dr.MERGE_TRAIN_FILE,
            dr.MERGE_TEST_FILE
        ]

        ITER_ATTR = zip(DATA_ATTR,SAVE_TO_ATTR)

        for dataset_file,save_to in ITER_ATTR:
            temp_df = pd.merge(
                dataset_file[1],dataset_file[0],on=col_ref['id']
            )

            temp_df.to_csv(save_to)
            print("[+] %s data Commited Successfully..." % (save_to))

    '''
        Pass the name of the pickled word2vec file
    '''
    def startPipeline(self,pickled_filename):
        self.__preprocess()
        self.__embbed_dataset(ut.getFilePath(
            ['pickled','word2vec'],
            pickled_filename,create=True
        ))
        self.__merge()
        

class GetStanceData(object):
    '''
        Takes in argumnet the path to merge file 
        which is defined in the dirs file
    '''
    def __init__(self,path_to_vec_pkl=None,embedding_type="tf_idf",):
        self.df_train = pd.read_csv(dr.MERGE_TRAIN_FILE)
        self.df_test = pd.read_csv(dr.MERGE_TEST_FILE)

        self.path_to_vec_pkl = path_to_vec_pkl
        self.embedding_type = embedding_type

        assert self.path_to_vec_pkl is not None
        self.word_vectorizer = pk.load(open(self.path_to_vec_pkl,"rb"))
    
    def __vecTransform(self,corpus):
        if self.embedding_type is 'tf_idf':
            return self.word_vectorizer.transform(corpus)
        
        if self.embedding_type is 'tokenizer':
            return self.word_vectorizer.texts_to_sequences(corpus)

        raise NameError("%s no such option available" % (self.embedding_type))


    def getTrainTestData(self,shuffle=True):
        if ut.checkRequiredFiles(dr.TRAIN_DATASET_NUMPY,exec=False) and \
            ut.checkRequiredFiles(dr.TEST_DATASET_NUMPY,exec=False):

            train_stance = np.load(dr.TRAIN_DATASET_NUMPY[STANCE_KEY])
            train_headline = np.load(dr.TRAIN_DATASET_NUMPY[HEADLINE_KEY])
            train_body = np.load(dr.TRAIN_DATASET_NUMPY[BODY_KEY])
            
            test_stance = np.load(dr.TEST_DATASET_NUMPY[STANCE_KEY])
            test_headline = np.load(dr.TEST_DATASET_NUMPY[HEADLINE_KEY])
            test_body = np.load(dr.TEST_DATASET_NUMPY[BODY_KEY])
            
            print("[+] Loaded numpy matrices")
        else:
            print("[-] Unable to load numpy matrices")

            train_stance = self.df_train[col_ref['stance']]\
                .apply(lambda x: label_ref[x]).values 

            train_stance = to_categorical(train_stance)

            train_body = self.__vecTransform(corpus= \
                self.df_train[col_ref['headline']].values)

            train_headline = self.__vecTransform(corpus= \
                self.df_train[col_ref['body']].values)

            print("[+] Converted word2Vec for training data")

            np.save(dr.TRAIN_DATASET_NUMPY[HEADLINE_KEY],train_headline)
            np.save(dr.TRAIN_DATASET_NUMPY[BODY_KEY],train_body)
            np.save(dr.TRAIN_DATASET_NUMPY[STANCE_KEY],train_stance)

            print("[+] Committed all the training numpy matrices")

            test_stance = self.df_test[col_ref['stance']]\
                .apply(lambda x: label_ref[x]).values 

            test_stance = to_categorical(test_stance)

            test_body = self.__vecTransform(corpus= \
                self.df_test[col_ref['headline']].values)

            test_headline = self.__vecTransform(corpus= \
                self.df_test[col_ref['body']].values)
            
            print("[+] Converted word2Vec for testing data")
            
            np.save(dr.TEST_DATASET_NUMPY[HEADLINE_KEY],test_headline)
            np.save(dr.TEST_DATASET_NUMPY[BODY_KEY],test_body)
            np.save(dr.TEST_DATASET_NUMPY[STANCE_KEY],test_stance)

            print("[+] Committed all the testing numpy matrices")

        
        if shuffle and self.embedding_type is 'tf_idf':
            index = np.arange(np.shape(train_body)[0])
            np.random.shuffle(index)

            train_body,train_headline,train_stance = \
                train_body[index, :],train_headline[index, :],train_stance[index,:]

            print("[+] Training dataset shuffled")

            index = np.arange(np.shape(test_body)[0])
            np.random.shuffle(index)
            
            test_body,test_headline,test_stance = \
                test_body[index, :],test_headline[index, :],test_stance[index,:]

            print("[+] Testing dataset shuffled")
            
        elif shuffle and self.embedding_type is 'tokenizer':
            train_body = pad_sequences(train_body,maxlen=500)
            train_headline = pad_sequences(train_headline,maxlen=500)

            test_headline = pad_sequences(test_headline,maxlen=500)
            test_body = pad_sequences(test_body,maxlen=500)

            index = np.arange(np.shape(train_body)[0])
            np.random.shuffle(index)

            train_body,train_headline,train_stance = \
                train_body[index, :],train_headline[index, :],train_stance[index,:]

            print("[+] Training dataset shuffled")

            index = np.arange(np.shape(test_body)[0])
            np.random.shuffle(index)

            test_body,test_headline,test_stance = \
                test_body[index, :],test_headline[index, :],test_stance[index,:]

            print("[+] Testing dataset shuffled")

        return train_body + train_headline, train_stance, \
                test_body + test_headline , test_stance
