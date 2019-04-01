'''
from keras.models import Sequential
from keras.layers import Dense,Dropout,Activation,Flatten,Conv1D,Input,Embedding,MaxPooling1D,LSTM
from keras.wrappers.scikit_learn import KerasClassifier
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import KFold
from keras.layers import GlobalAveragePooling1D, Embedding
from keras.models import Model

import tensorflow as tf
tf.logging.set_verbosity(tf.logging.ERROR)
import preprocessing as pre

import visual
import time
import utils
import dirs
'''
import pandas as pd
import pickle as pk
from sklearn import svm
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import accuracy_score
from sklearn.linear_model import PassiveAggressiveClassifier

#plot_losses = visual.TrainingPlot()
#start_time = time.time()

'''
TODO :Generate appropriate dataset files

    getSantizeStanceTrain  = pre.GetSanitizeStanceData(load="train")
    getSantizeStanceTest  = pre.GetSanitizeStanceData(load="test")

    getSantizeStanceTrain.merge(filename=dirs.MERGE_TRAIN_FILE,preprocess=True,commit=True)
    getSantizeStanceTest.merge(filename=dirs.MERGE_TEST_FILE,preprocess=True,commit=True)

    getSantizeStanceTrain.fit_tfidf_trainsform(filename='tf-idf_vector.pickle')

'''

#Hyper parmeters
nb_epoch = 25
nb_classes = 4
batch_size = 128

def baseline_model(input_size):
    #1 dense layer sequential model : [OVERFITTED] valid acc : 50.4% still down
    def seq_model():
        model = Sequential()
        model.add(Dense(62,input_dim=(1,input_size)))
        model.add(Activation('relu'))

        model.add(Dense(64))
        model.add(Activation('relu'))

        model.add(Dense(nb_classes))
        model.add(Activation('softmax'))
        model.compile(
            loss='categorical_crossentropy', 
            optimizer='adam', metrics=['accuracy']
        )

        return model

    def CBOW_model():
        sequence_input = Input(shape=(500,), dtype='int32')
        embedding_layer = Embedding(50000, 50,
                            input_length=500,
                            trainable=True)
        embedded_sequences = embedding_layer(sequence_input)

        average = GlobalAveragePooling1D()(embedded_sequences)
        predictions = Dense(nb_classes, activation='softmax')(average)

        model = Model(sequence_input, predictions)
        model.compile(loss='categorical_crossentropy',
              optimizer='adam', metrics=['acc'])

        return model

    def LSTM_CNN():
        sequence_input = Input(shape=(500,), dtype='int32')
        embedding_layer = Embedding(50000, 50,
                            input_length=500,
                            trainable=True)
        embedded_sequences = embedding_layer(sequence_input)

        x = Conv1D(64, 5)(embedded_sequences)
        x = MaxPooling1D(5)(x)
        x = Dropout(0.2)(x)
        x = Conv1D(64, 5)(x)
        x = MaxPooling1D(5)(x)
        x = Dropout(0.2)(x)
        x = LSTM(64)(x)
        predictions = Dense(nb_classes, activation='softmax')(x)

        model = Model(sequence_input, predictions)
        model.compile(loss='categorical_crossentropy',
              optimizer='adam',
              metrics=['acc'])
        return model

    return LSTM_CNN

def train_model(getSantizeStanceData):
    x_train,y_train,x_test,y_test = getSantizeStanceData.getTrainTestData()
    
    model = baseline_model(x_train)()
    
    print("[==] Model Summary")
    print(model.summary())

    print("[+] Training model")
    
    estimator = model.fit(
        x_train, y_train, validation_data=(x_test, y_test),
        batch_size=batch_size,callbacks=[plot_losses],
        epochs=nb_epoch, verbose=2
    )

    print("[==] Saving model")

    model.save(utils.getFilePath('pickled',visual.MODEL_NAME))
    
    print("--- %s seconds ---" % (time.time() - start_time))

if __name__ == "__main__":
    #supply this to generate all the required dataset files
    #embedding type specifies the vector formation whether tokenizer or tf_idf
    # pipline = pre.StanceDataPipeline(embedding_type='tokenizer')
    #specify the name of of the pickle file 
    #pipline.startPipeline(pickled_filename="word2vec_filename.pkl")
    '''
    getStanceData = pre.GetStanceData(
        path_to_vec_pkl=utils.getFilePath(['pickled','word2vec'],filename='word2vec_filename.pkl'),
        embedding_type='tokenizer'
    )
    getStanceData.getTrainTestData(shuffle=True)
    #train_model(getSantizeStanceData=getStanceData)
    '''
