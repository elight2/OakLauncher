from LauncherAccount import AccountManager
from LauncherProfile import ProfileManager
from LauncherSettings import SettingManager
from LauncherException import LauncherException
from LauncherDownloader import downloadFile
from GameFileUrls import urlList

import json
from pathlib import Path

class GameDirs:
    def __init__(self,minecraftPrefix:str):
        self.minecraftPrefix=Path(minecraftPrefix)
        self.versionManifest=self.minecraftPrefix/Path("version_manifest.json")

    def generate(self,version:str):
        self.versionJson=self.minecraftPrefix/Path("versions")/Path(version)/Path(version+".json")
        self.versionJar=self.minecraftPrefix/Path("versions")/Path(version)/Path(version+".jar")

def getCurUrls():
    return urlList[SettingManager.settings["mirror"]]

def checkExistAndDownload(dir,url:str):
    # check and download
    if not Path(dir).exists():
        downloadFile(urlList[SettingManager.settings["mirror"]].versionManifest,dir)
    # read
    with open(dir) as f:
        data=json.load(f)
        return data

def getVersionManifest(dirs:GameDirs):
    return checkExistAndDownload(dirs.versionManifest,getCurUrls().versionManifest)

def getVersionJson(dirs:GameDirs,version:str,manifest):
    # for check sum use v2 manifest
    dirs.generate(version)
    for i in manifest["versions"]:
        if i["id"]==version:
            return checkExistAndDownload(dirs.versionJson,getCurUrls().getVersionJsonUrl(i["url"]))
    raise LauncherException(info="VersionNotInManifest")

def checkVersionJar(dirs:GameDirs,data,version):
    dirs.generate(version)
    checkExistAndDownload(dirs.versionJar,)

def launch(profileName,accountName):
    # get info
    ProfileManager.readProfiles()
    AccountManager.readAccounts()
    SettingManager.readSettings()
    profileInfo=ProfileManager.getProfile(profileName)
    accountInfo=AccountManager.getAccount(accountName)
    settingsInfo=SettingManager.settings
    dirs=GameDirs(settingsInfo["dir"])

    # check java
    if not Path(profileInfo["java"]).exists():
        raise LauncherException(info=f"Java executable not found: {profileInfo["java"]}")

    versionManifest=getVersionManifest(dirs)

    # check official version
    if not any(i["id"]==profileInfo["version"] for i in versionManifest["versions"]) and profileInfo["loader"]=="":
        raise LauncherException(info="UnofficialVersionWithoutLoader")
    
    getVersionJson(dirs,profileInfo["version"],versionManifest)

