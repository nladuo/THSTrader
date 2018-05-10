import numpy as np
from PIL import Image
import pickle
import os


def get_model():
    model_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "captcha_model.pickle")
    with open(model_path, "rb") as f:
        return pickle.load(f)


def captcha_recognize(path):
    model = get_model()
    
    pix = np.array(Image.open(path).convert("L"))
    # threshold image
    pix = (pix < 200) * 255

    col_ranges = [
        [2, 2 + 9],
        [18, 18 + 9],
        [34, 34 + 9],
        [50, 50 + 9]
    ]
    # split and save
    letters = []
    for col_range in col_ranges:
        letter = pix[:, col_range[0]: col_range[1]]
        letters.append(letter.reshape(9*23))
        
    res = model.predict(letters)
    return "".join([str(ch) for ch in res])
