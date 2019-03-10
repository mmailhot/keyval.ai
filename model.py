from keras.layers import Input, Dense
from keras.models import Model
from keras.optimizers import SGD
import numpy as np
import random
import string

def string_to_bin_n_char(b, n):
    arr = np.zeros(n * 8)
    for i in range(min(len(b), n)):
        c = b[i]
        for j in range(8):
            arr[(8 * i) + j] = float((c >> (7 - j)) & 1)
    return arr

def bin_arr_to_string(b):
    res = bytearray()
    for i in range(len(b) // 8):
        c = 0
        for j in range(8):
            c = c << 1
            c = c | int(round((b[(8 * i) + j])))
        res.append(c)
    return res.partition(b'\0')[0]

inputs = Input(shape=(256,))
x = Dense(256, activation='relu')(inputs)
# x = Dense(2048, activation='relu')(x)
# x = Dense(2048, activation='relu')(x)
x = Dense(2048, activation='relu')(x)
predictions = Dense(2048, activation='sigmoid')(x)

model = Model(inputs=inputs, outputs=predictions)
model.compile(optimizer='rmsprop',
              loss='binary_crossentropy',
              metrics=['accuracy'])

all_keys = set()

def insert(key, value, epochs):
    if key in all_keys:
        all_keys.remove(key)
    if len(all_keys) == 0:
        i_bin = string_to_bin_n_char(key, 32)
        o_bin = string_to_bin_n_char(value, 256)
        idata = np.array([i_bin for _ in range(25)])
        odata = np.array([o_bin for _ in range(25)])
    else:
        keys_tuple = tuple(all_keys)
        prev_idata = np.array([string_to_bin_n_char(random.choice(keys_tuple), 32) for _ in range(25)])
        prev_odata = np.rint(model.predict(prev_idata))
        i_bin = string_to_bin_n_char(key, 32)
        o_bin = string_to_bin_n_char(value, 256)
        new_idata = np.array([i_bin for _ in range(25)])
        new_odata = np.array([o_bin for _ in range(25)])
        idata = np.concatenate((prev_idata, new_idata))
        odata = np.concatenate((prev_odata, new_odata))

    all_keys.add(key)
    model.fit(idata, odata, epochs=epochs)

def get(key):
    return bin_arr_to_string(model.predict(np.array([string_to_bin_n_char(key, 32)]))[0])
