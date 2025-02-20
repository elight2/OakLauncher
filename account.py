import webbrowser
import http.client
import urllib.parse
import json
import DataManager

class AccountManager(DataManager.DataManager):
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

    client_id=""
    redirect_uri=""
    urls=[
        "https://login.microsoftonline.com/consumers/oauth2/v2.0/authorize?client_id={}&response_type=code&redirect_uri={}&response_mode=query&scope=XboxLive.signin%20offline_access"
    ]

    def openWebPage(self):
        print("<...>")
        webbrowser.open(AccountManager.urls[0].format(AccountManager.client_id,AccountManager.redirect_uri))

    def getAccessToken(self,refresh:str,url:str) -> list:
        authArgs=""
        if refresh=="":
            index=url.find("/?code=")
            if index==-1:
                raise "URL_incorrect"
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
            raise "requestFailed:"+str(authResponse.status)
        access_token=json.loads(authResponse.read().decode("utf-8"))["access_token"]
        refresh_token=json.loads(authResponse.read().decode("utf-8"))["refresh_token"]
        return [access_token,refresh_token]

    def getLiveToken(self,accessToken:str)->list:
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
            raise "requestFailed:"+str(authResponse.status)
        token=json.loads(authResponse.read().decode("utf-8"))["Token"]
        uhs=json.loads(authResponse.read().decode("utf-8"))["DisplayClaims"]["xui"][0]["uhs"]
        return [token,uhs]

    def getXstsToken(self,liveToken:str)->str:
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
            raise "requestFailed:"+str(authResponse.status)
        xstsToken=json.loads(authResponse.read().decode("utf-8"))["Token"]
        return xstsToken
    
    def readAccounts(self):
        DataManager.DataManager.readData(AccountManager)

    def saveAccounts(self):
        DataManager.DataManager.saveData(AccountManager)