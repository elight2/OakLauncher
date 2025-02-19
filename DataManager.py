import os
import json

class DataManager:
    FILE_NAME=""
    DEFAULT_DATA={}
    data={}

    @classmethod
    def readData(cls):
        try:
            if not os.path.exists(cls.FILE_NAME):
                with open(cls.FILE_NAME,mode="w") as dataFile:
                    json.dump(cls.data,dataFile)

            with open(DataManager.FILE_NAME) as dataFile:
                cls.data=json.load(dataFile)
        except BaseException as exc:
            print("BaseException caught while reading json: ",exc)

    @classmethod
    def saveData(cls):
        with open(cls.FILE_NAME,mode="w") as dataFile:
            json.dump(cls.data,dataFile)

