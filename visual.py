import matplotlib
matplotlib.use('agg')

import matplotlib.pyplot as plt
import keras
import numpy as np
import utils

MODEL_NAME = "LSTM_CNN"
FOLDER_NAME = "training"

<<<<<<< HEAD
TRAINING_IMG = utils.getFilePath(
    foldername=[FOLDER_NAME,MODEL_NAME],
    create=True
)
=======
MODEL_NAME = "default"
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TRAINING_IMG = os.path.join(BASE_DIR,'training')
TRAINING_IMG = os.path.join(TRAINING_IMG,MODEL_NAME)
>>>>>>> bf2b4ef115818a186ebc39a0b859ee08b2b49175

class TrainingPlot(keras.callbacks.Callback):

    # This function is called when the training begins
    def on_train_begin(self, logs={}):
        # Initialize the lists for holding the logs, losses and accuracies
        self.losses = []
        self.acc = []
        self.val_losses = []
        self.val_acc = []
        self.logs = []

    # This function is called at the end of each epoch
    def on_epoch_end(self, epoch, logs={}):

        # Append the logs, losses and accuracies to the lists
        self.logs.append(logs)
        self.losses.append(logs.get('loss'))
        self.acc.append(logs.get('acc'))
        self.val_losses.append(logs.get('val_loss'))
        self.val_acc.append(logs.get('val_acc'))

        # Before plotting ensure at least 2 epochs have passed
        if len(self.losses) > 1:

            N = np.arange(0, len(self.losses))
            plt.figure()
            plt.plot(N, self.losses, label = "train_loss")
            plt.plot(N, self.acc, label = "train_acc")
            plt.plot(N, self.val_losses, label = "val_loss")
            plt.plot(N, self.val_acc, label = "val_acc")
            plt.title("Training Loss and Accuracy [Epoch {}]".format(epoch))
            plt.xlabel("Epoch #")
            plt.ylabel("Loss/Accuracy")
            plt.legend()
<<<<<<< HEAD
           
            plt.savefig(utils.getFilePath(TRAINING_IMG,'Epoch-{}.png'\
                .format(epoch)))
            plt.close()
=======
            # Make sure there exists a folder called output in the current directory
            # or replace 'output' with whatever direcory you want to put in the plots
            plt.savefig(os.path.join(TRAINING_IMG,'Epoch-{}.png'\
                    .format(epoch)))
            plt.close()
>>>>>>> bf2b4ef115818a186ebc39a0b859ee08b2b49175
