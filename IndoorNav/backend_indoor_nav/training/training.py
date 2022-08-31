# Imports needed
import os

os.environ["TF_CPP_MIN_LOG_LEVEL"] = "2"
import tensorflow as tf
from tensorflow import keras

from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Conv2D, MaxPooling2D, Dropout, Flatten
from tensorflow.keras.utils import to_categorical

 
IMG_HEIGHT_TRAIN = 320
IMG_WIDTH_TRAIN = 180

num_epochs = 15
batch_size = 15
nClasses = 355
input_shape = (IMG_HEIGHT_TRAIN, IMG_WIDTH_TRAIN, 1) #3 for rgb

SRC_DIR = "backend_indoor_nav\\training\\one_category\\"

# Src: https://learnopencv.com/image-classification-using-convolutional-neural-networks-in-keras/

def preprocess():
    """creates the training and test datasets"""
    ds_train = tf.keras.preprocessing.image_dataset_from_directory(
        SRC_DIR,
        labels="inferred",
        label_mode="categorical", 
        color_mode="grayscale",
        batch_size=batch_size,
        image_size=(IMG_HEIGHT_TRAIN, IMG_WIDTH_TRAIN),  # reshape if not in this size
        shuffle=True,
        seed=123,
        validation_split=0.1,
        subset="training",
    )

    ds_validation = tf.keras.preprocessing.image_dataset_from_directory(
        SRC_DIR,
        labels="inferred",
        label_mode="categorical", 
        color_mode="grayscale",
        batch_size=batch_size,
        image_size=(IMG_HEIGHT_TRAIN, IMG_WIDTH_TRAIN),  # reshape if not in this size
        shuffle=True,
        seed=123,
        validation_split=0.1,
        subset="validation",
    )

    return (ds_train, ds_validation)

def create_model():
    """ builds the model """
    model = Sequential()
    # The first two layers with 32 filters of window size 3x3
    model.add(Conv2D(32, (3, 3), padding='same', activation='relu', input_shape=input_shape))
    model.add(Conv2D(32, (3, 3), activation='relu'))
    model.add(MaxPooling2D(pool_size=(2, 2)))
    model.add(Dropout(0.25)) #prevents overfitting

    model.add(Conv2D(64, (3, 3), padding='same', activation='relu'))
    model.add(Conv2D(64, (3, 3), activation='relu'))
    model.add(MaxPooling2D(pool_size=(2, 2)))
    model.add(Dropout(0.25))

    model.add(Conv2D(64, (3, 3), padding='same', activation='relu'))
    model.add(Conv2D(64, (3, 3), activation='relu'))
    model.add(MaxPooling2D(pool_size=(2, 2)))
    model.add(Dropout(0.25))

    model.add(Flatten())
    model.add(Dense(512, activation='relu'))
    model.add(Dropout(0.5))
    model.add(Dense(nClasses, activation='softmax'))

    return model

def train_model(model, ds_train, ds_validation):
    """ trains the model """
    model.compile(optimizer='rmsprop', loss='categorical_crossentropy', metrics=['accuracy'])

    model.summary()

    model.fit(ds_train, epochs=num_epochs, verbose=2)
    model.save('./backend_indoor_nav/training/models/')
    model.evaluate(ds_validation, verbose=2)



"""creates a model to detect all positions"""
(ds_train, ds_validation) = preprocess()

model = create_model()
train_model(model, ds_train, ds_validation)