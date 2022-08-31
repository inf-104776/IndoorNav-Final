# Imports needed
import os

os.environ["TF_CPP_MIN_LOG_LEVEL"] = "2"
import tensorflow as tf
from tensorflow import keras

from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Conv2D, MaxPooling2D, Dropout, Flatten
from tensorflow.keras.utils import to_categorical

 
img_height = 320
img_width = 180
num_epochs = 15

batch_size = 15
nClasses_dir_floor = 37
nClasses_pos = 24
input_shape = (img_height, img_width, 1) #3 for rgb

SRC_FLOOR_DIR = "backend/training_images_dir_floor/"
SRC_POS = "backend/training_images_position/"
# Src: https://learnopencv.com/image-classification-using-convolutional-neural-networks-in-keras/


def preprocess_floor_dir():
    """creates the training and test datasets for building floor and direction model"""
    ds_train_floor_dir = tf.keras.preprocessing.image_dataset_from_directory(
        SRC_FLOOR_DIR,
        labels="inferred",
        label_mode="categorical",  #int categorical, binary
        color_mode="grayscale",
        batch_size=batch_size,
        image_size=(img_height, img_width),  # reshape if not in this size
        shuffle=True,
        seed=123,
        validation_split=0.1,
        subset="training",
    )

    ds_validation_floor_dir = tf.keras.preprocessing.image_dataset_from_directory(
        SRC_FLOOR_DIR,
        labels="inferred",
        label_mode="categorical",  # categorical, binary
        color_mode="grayscale",
        batch_size=batch_size,
        image_size=(img_height, img_width),  # reshape if not in this size
        shuffle=True,
        seed=123,
        validation_split=0.1,
        subset="validation",
    )

    return (ds_train_floor_dir, ds_validation_floor_dir)

def preprocess_pos():
    """creates the training and test datasets for position model"""
    ds_train_pos = tf.keras.preprocessing.image_dataset_from_directory(
        SRC_POS,
        labels="inferred",
        label_mode="categorical", 
        color_mode="grayscale",
        batch_size=batch_size,
        image_size=(img_height, img_width),  # reshape if not in this size
        shuffle=True,
        seed=123,
        validation_split=0.1,
        subset="training",
    )

    ds_validation_pos = tf.keras.preprocessing.image_dataset_from_directory(
        SRC_POS,
        labels="inferred",
        label_mode="categorical",
        color_mode="grayscale",
        batch_size=batch_size,
        image_size=(img_height, img_width),  # reshape if not in this size
        shuffle=True,
        seed=123,
        validation_split=0.1,
        subset="validation",
    )

    return (ds_train_pos, ds_validation_pos)


def create_model(nClasses):
    """ builds the model """
    model = Sequential()
    # The first two layers with 32 filters of window size 3x3
    model.add(Conv2D(32, (3, 3), padding='same', activation='relu', input_shape=input_shape))
    model.add(Conv2D(32, (3, 3), activation='relu'))
    model.add(MaxPooling2D(pool_size=(2, 2)))
    model.add(Dropout(0.25))

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
    model.save('./backend/models/')
    model.evaluate(ds_validation, verbose=2)



"""creates two models
one for building, floor and direction
the other for positions within the hallway"""
(ds_train_floor_dir, ds_validation_floor_dir) = preprocess_floor_dir()
(ds_train_pos, ds_validation_pos) = preprocess_pos()

model_floor_dir = create_model(nClasses_dir_floor)
train_model(model_floor_dir, ds_train_floor_dir, ds_validation_floor_dir)

model_pos = create_model(nClasses_pos)
train_model(model_pos, ds_train_pos, ds_validation_pos)

