from DataManager import DataManager
from LauncherException import LauncherException

class SettingManager(DataManager):
    FILE_NAME="./data/settings.json"
    DEFAULT_DATA={
        "dir":"./minecraft/",
        "mirror":0
    }

    settings={}

    @staticmethod
    def readSettings():
        SettingManager.readData()
        SettingManager.settings=SettingManager.data

    @staticmethod
    def saveSettings():
        SettingManager.data=SettingManager.settings
        SettingManager.saveData()