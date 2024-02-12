import os
import json

folders = os.listdir("logger/")
for folder in folders:
    files = os.listdir("logger/{}".format(folder))
    for f in files:
        if f[-4:] == "json":
            json_file = "logger/{}/{}".format(folder, f)
    json_read = open(json_file, 'r')
    info = json.load(json_read)
    function_id = info["function_id"]
    info["function_name"] = "ManyAffine_{}".format(function_id)
    info["algorithm"]["name"] = "L-SHADE_{}".format(function_id)
    json_read.close()
    json_write = open(json_file, 'w')
    json.dump(info, json_write)
    json_write.close()
    