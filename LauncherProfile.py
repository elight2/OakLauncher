from DataManager import DataManager
from LauncherException import LauncherException

class ProfileManager(DataManager):
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

    profiles=[]

    @staticmethod
    def getProfile(profileName):
        for i in ProfileManager.profiles:
            if i["name"]==profileName:
                return i
        raise LauncherException(info=f"ProfileNotFound: {profileName}")

    @staticmethod
    def readProfiles():
        ProfileManager.readData()
        ProfileManager.profiles=ProfileManager.data["profiles"]

    @staticmethod
    def saveProfiles():
        ProfileManager.data={"profiles":ProfileManager.profiles}
        ProfileManager.saveData()

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
