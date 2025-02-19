import json
import os
import DataManager

class AccountManager(DataManager.DataManager):
    FILE_NAME="./data/accounts.json"
    DEFAULT_DATA={
        "accounts":[
            {
                "name":"default",
                "type":"offline",
                "username":"user",
                "uuid":""
            }
        ]
    }

    urls=[
        "https://login.microsoftonline.com/consumers/oauth2/v2.0/authorize?client_id=%s&response_type=code&redirect_uri=%s&response_mode=query&scope=XboxLive.signin%20offline_access"
    ]

    def openWebPage(self):
        pass

    def code2Token(self):
        pass

    def readAccounts(self):
        DataManager.DataManager.readData(AccountManager)

    def saveAccounts(self):
        DataManager.DataManager.saveData(AccountManager)