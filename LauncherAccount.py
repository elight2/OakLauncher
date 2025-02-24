import webbrowser
import http.client
import urllib.parse
import json
from DataManager import DataManager
from LauncherException import LauncherException

class AccountManager(DataManager):
    FILE_NAME="./data/accounts.json"
    DEFAULT_DATA={
        "accounts":[
            {
                "name":"defaultm",
                "type":"msa",
                "username":"",
                "uuid":"",
                "access_token":"",
                "refresh_token":""
            },
            {
                "name":"defaulto",
                "type":"offline",
                "username":"user",
                "uuid":""
            }
        ]
    }

    accounts=[]

    client_id=""
    redirect_uri=""

    @staticmethod
    def getAccount(accountName):
        for i in AccountManager.accounts:
            if i["name"]==accountName:
                return i
        raise LauncherException(info=f"AccountNotFound: {accountName}")

    def openWebPage(self):
        print("<...>")
        url="https://login.microsoftonline.com/consumers/oauth2/v2.0/authorize?client_id={}&response_type=code&redirect_uri={}&response_mode=query&scope=XboxLive.signin%20offline_access"
        webbrowser.open(url.format(AccountManager.client_id,AccountManager.redirect_uri))

    def getAccessToken(self,refresh:str,url:str) -> tuple:
        authArgs=""
        if refresh=="":
            index=url.find("/?code=")
            if index==-1:
                raise LauncherException(info="URL_incorrect")
            code=url[index+7:-1]
            authArgs=urllib.parse.urlencode({
                "client_id":AccountManager.client_id,
                "code":code,
                "grant_type":"authorization_code",
                "redirect_uri":AccountManager.redirect_uri,
                "scope":"XboxLive.signin offline_access"
            })
        elif url=="":
            authArgs=urllib.parse.urlencode({
                "client_id":AccountManager.client_id,
                "refresh_token":refresh,
                "grant_type":"refresh_token",
                "scope":"XboxLive.signin offline_access"
            })

        authConnection=http.client.HTTPSConnection("login.microsoftonline.com")
        authHeaders={"Content-Type":"application/x-www-form-urlencoded"}
        authConnection.request("POST","/consumers/oauth2/v2.0/token",body=authArgs,headers=authHeaders)
        authResponse=authConnection.getresponse()

        if not authResponse.status==200:
            LauncherException(info=f"requestFailed while getAccessToken, code={authResponse.status}")
        access_token=json.loads(authResponse.read().decode("utf-8"))["access_token"]
        refresh_token=json.loads(authResponse.read().decode("utf-8"))["refresh_token"]
        return (access_token,refresh_token)

    def getLiveToken(self,accessToken:str)->tuple:
        authConnection=http.client.HTTPSConnection("user.auth.xboxlive.com")
        authHeaders={"Content-Type": "application/json",
            "Accept":"application/json"
        }
        authArgData={
            "Properties": {
                "AuthMethod": "RPS",
                "SiteName": "user.auth.xboxlive.com",
                "RpsTicket": "d={}".format(accessToken)
            },
            "RelyingParty": "http://auth.xboxlive.com",
            "TokenType": "JWT"
        }
        authArgs=json.dumps(authArgData)
        authConnection.request("POST","/user/authenticate",body=authArgs,headers=authHeaders)
        authResponse=authConnection.getresponse()

        if not authResponse.status==200:
            raise LauncherException(info=f"requestFailed while getLiveToken, code={authResponse.status}")
        token=json.loads(authResponse.read().decode("utf-8"))["Token"]
        uhs=json.loads(authResponse.read().decode("utf-8"))["DisplayClaims"]["xui"][0]["uhs"]
        return (token,uhs)

    def getXstsToken(self,liveToken:str)->list:
        authConnection=http.client.HTTPSConnection("xsts.auth.xboxlive.com")
        authHeaders={"Content-Type": "application/json",
            "Accept":"application/json"
        }
        authArgData={
            "Properties": {
                "SandboxId": "RETAIL",
                "UserTokens": [
                    liveToken
                ]
            },
            "RelyingParty": "rp://api.minecraftservices.com/",
            "TokenType": "JWT"
        }
        authArgs=json.dumps(authArgData)
        authConnection.request("POST","/xsts/authorize",body=authArgs,headers=authHeaders)
        authResponse=authConnection.getresponse()

        if not authResponse.status==200:
            raise LauncherException(info=f"requestFailed while getXstsToken, code={authResponse.status}")
        xstsToken=json.loads(authResponse.read().decode("utf-8"))["Token"]
        uhs=json.loads(authResponse.read().decode("utf-8"))["DisplayClaims"]["xui"][0]["uhs"]
        return [xstsToken,uhs]

    def getMinecraftToken(self,xstsToken,uhs)->str:
        authConnection=http.client.HTTPSConnection("api.minecraftservices.com")
        authArgData={
            "identityToken": f"XBL3.0 x={uhs};{xstsToken}"
        }
        authArgs=json.dumps(authArgData)
        authConnection.request("POST","/authentication/login_with_xbox",body=authArgs)
        authResponse=authConnection.getresponse()

        if not authResponse.status==200:
            raise LauncherException(info=f"requestFailed while getMinecraftToken, code={authResponse.status}")
        minecraftToken=json.loads(authResponse.read().decode("utf-8"))["access_token"]
        return minecraftToken

    # def checkMinecraft(self,minecraftToken)->bool:
    #     authConnection=http.client.HTTPSConnection("api.minecraftservices.com")
    #     authHeaders={"Authorization":f"Bearer {minecraftToken}"
    #     }
    #     authConnection.request("GET","/entitlements/mcstore",headers=authHeaders)
    #     authResponse=authConnection.getresponse()

    #     if not authResponse.status==200:
    #         raise "requestFailed:"+str(authResponse.status)
    #     try:
    #         if dict(json.loads(authResponse.read().decode("utf-8")))["items"][0]["name"]=="product_minecraft":
    #             return True
    #         else:
    #             return False
    #     except KeyError:
    #         return False

    def getUserInfo(self,minecraftToken)->tuple:
        authConnection=http.client.HTTPSConnection("api.minecraftservices.com")
        authHeaders={"Authorization":f"Bearer {minecraftToken}"
        }
        authConnection.request("GET","/minecraft/profile",headers=authHeaders)
        authResponse=authConnection.getresponse()

        if not authResponse.status==200:
            raise LauncherException(info=f"requestFailed while getUserInfo, code={authResponse.status}")
        if (json.loads(authResponse.read().decode("utf-8"))).get("id","ERR")=="ERR":
            return ("NOT_FOUND",)
        else:
            uuid=json.loads(authResponse.read().decode("utf-8"))["id"]
            name=json.loads(authResponse.read().decode("utf-8"))["name"]
            return (name,uuid)
    
    @staticmethod
    def readAccounts():
        AccountManager.readData()
        AccountManager.accounts=AccountManager.data["accounts"]

    @staticmethod
    def saveAccounts():
        AccountManager.data={"accounts":AccountManager.accounts}
        AccountManager.saveData()