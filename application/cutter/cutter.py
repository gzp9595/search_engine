import os
from application import app
from application.util import print_time
import uuid
import jieba

cutter = None

if not ("THULAC" in app.config and os.path.exists(app.config["THULAC"])):
    import thulac

    cutter = thulac.thulac(seg_only=True)


def thulac_cutone(text):
    data = cutter.cut(text)
    result = []
    for x in data:
        result.append(x[0])
    return result


def cut(text):
    print "One cut begin"
    print_time()
    if isinstance(text, basestring):
        text = [text]

    if app.config["USING_JIEBA"]:
        result = []
        for x in text:
            result.append(" ".join(jieba.cut_for_search(x)))

        return result

    result = []

    if cutter is None:
        temp_path = os.path.join(app.config["TEMP_DIR"], str(uuid.uuid4()) + ".txt")
        temp_path2 = os.path.join(app.config["TEMP_DIR"], str(uuid.uuid4()) + ".txt")
        f = open(temp_path, "w")
        for line in text:
            print >> f, line.replace("\n", "").replace(" ", "")
        f.close()

        os.system(app.config["THULAC"] + "thulac -model_dir " + app.config[
            "THULAC"] + "models -seg_only -t2s < " + temp_path + " > " + temp_path2)
        # print(app.config["THULAC"] + "thulac -model_dir " + app.config[
        #    "THULAC"] + "models -seg_only -t2s < " + temp_path + " > " + temp_path2)

        f = open(temp_path2, "r")
        cnt = 0
        for line in f:
            cnt += 1
            if cnt == 1:
                continue
            data = line.replace("\n", " ").replace("%", " ").split(" ")
            data = data[0:len(data) - 1]
            result.append(data)
    else:
        result = []
        for line in text:
            result.append(thulac_cutone(line))

    print "One cut end"
    print_time()
    return result
