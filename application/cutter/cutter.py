import os
from application import app
from application.util import print_time
import uuid
import thulac

cutter = None

cutter = thulac.thulac(seg_only=True, model_path=app.config["THULAC_MODEL_PATH"])


def thulac_cutone(text):
    data = cutter.cut(text)
    result = []
    for x in data:
        result.append(x[0])
    return result


def cut(text):
    print("One cut begin")
    print_time()
    if isinstance(text, str):
        text = [text]

    result = []
    for line in text:
        result.append(thulac_cutone(line))

    print("One cut end")
    print_time()
    return result
