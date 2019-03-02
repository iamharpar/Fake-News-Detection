from keras.models import Sequential
from keras.layers import Dense,Dropout,Activation,Flatten,Conv1D
from keras.wrappers.scikit_learn import KerasClassifier
import preprocessing as pre
import tensorflow as tf
from keras.utils.np_utils import to_categorical
import visual
import time

start_time = time.time()

plot_losses = visual.TrainingPlot()
tf.logging.set_verbosity(tf.logging.ERROR)

nb_epoch = 10
nb_classes = 4
batch_size = 10

def baseline_model(input_size):
    model = Sequential()
    model.add(Dense(32,input_dim=input_size))
    model.add(Activation('relu'))
    model.add(Dropout(.2))

    model.add(Dense(nb_classes))
    model.add(Activation('softmax'))
    model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])

    return model


if __name__ == "__main__":
    getSantizeStanceData  = pre.GetSanitizeStanceData(load=True)
    tfidf_train = getSantizeStanceData.fit_tfidf_trainsform()

    x_train,y_train = getSantizeStanceData.getTrainingData()
    x_test,y_test = getSantizeStanceData.getTestingData()
    
    y_train = to_categorical(y_train)
    y_test = to_categorical(y_test)

    print(y_test)
    #(1, 17163) (1, 17163)

    model = baseline_model(x_train[0].shape[1])
    
    print("[==] Model Summary [==]")
    print(model.summary())
    
    print("[+] Training model")

    estimator = model.fit(
        x_train, y_train, validation_data=(x_test, y_test),
        batch_size=batch_size,callbacks=[plot_losses],
        epochs=nb_epoch, verbose=2
    )
    
    print("[==] Saving model [==]")
    model.save("single_layer.h5")
    
    
    print("--- %s seconds ---" % (time.time() - start_time))
    '''
    K-nn classifier    
    Training Accuracy:   95.980  %
    Validation Accuracy:   68.634  %
    '''

