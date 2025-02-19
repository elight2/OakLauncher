import json
import os
import DataManager

class ProfileManager(DataManager.DataManager):
    FILE_NAME="./data/profiles.json"
    DEFAULT_DATA={
        "profiles":[
            {
                "name":"default",
                "version":"1.21.1",
                "java":"/usr/bin/java",
                "env":{},
                "args":[],
                "loader":""
            }
        ]
    }

    def readProfiles(self):
        DataManager.DataManager.readData(ProfileManager)

    def saveProfiles(self):
        DataManager.DataManager.saveData(ProfileManager)

    # def readFile(self):
    #     try:
    #         if not os.path.exists(self.FILE_NAME):
    #             with open(self.FILE_NAME,mode="w") as profileFile:
    #                 json.dump({"profiles":[self.DEFAULT_PROFILE]},profileFile)

    #         with open(self.FILE_NAME) as profileFile:
    #             ProfileManager.profiles=json.load(profileFile)["profiles"]
    #     except BaseException as exc:
    #         print("BaseException caught: ",exc)
    #         print("Exiting...")
