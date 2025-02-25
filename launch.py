from LauncherAccount import AccountManager
from LauncherProfile import ProfileManager
from LauncherSettings import SettingManager
from LauncherException import LauncherException
from LauncherDownloader import downloadFile
from GameFileUri import GameFileUris

import json
from pathlib import Path
import hashlib

# class GameDirs:
#     def __init__(self,minecraftPrefix:str):
#         self.minecraftPrefix=Path(minecraftPrefix)
#         self.versionManifest=self.minecraftPrefix/Path("version_manifest.json")

#     def generate(self,version:str):
#         self.versionJson=self.minecraftPrefix/Path("versions")/Path(version)/Path(version+".json")
#         self.versionJar=self.minecraftPrefix/Path("versions")/Path(version)/Path(version+".jar")

# def getCurUrls():
#     return urlList[SettingManager.settings["mirror"]]

def checkExistAndDownload(dir,url:str,parseJson=False,size=0,sha1:str=""):
    # check and download
    if not Path(dir).exists():
        downloadFile(url,dir)
    # optional check
    if size!=0:
        if Path(dir).stat().st_size!=size:
            raise LauncherException(info="FileSizeNotMatch")
    if sha1!="":
        with open(dir,mode="rb") as f:
            fileSha1=hashlib.sha1()
            fileSha1.update(f.read())
            if fileSha1.hexdigest().lower()!=sha1.lower():
                raise LauncherException(info="FileSha1NotMatch")
    if parseJson:
        # read
        with open(dir) as f:
            data=json.load(f)
            return data
    else:
        return {}

def getVersionManifest(uri:GameFileUris):
    return checkExistAndDownload(uri.versionManifestDir,uri.getVersionManifestUrl(),parseJson=True)

def getVersionJson(uri:GameFileUris,version:str,manifest):
    # for check sum use v2 manifest
    for i in manifest["versions"]:
        if i["id"]==version:
            return checkExistAndDownload(uri.versionJsonDir,uri.genVersionJsonUrl(i["url"]),parseJson=True)
    raise LauncherException(info="VersionNotInManifest")

def checkVersionJar(uri:GameFileUris,versionJsonData):
    clientInfo=versionJsonData["downloads"]["client"]
    checkExistAndDownload(uri.versionJarDir,uri.genVersionJarUrl(clientInfo["url"]),size=int(clientInfo["size"]),sha1=clientInfo["sha1"])

def checkLibraries(uri:GameFileUris,versionJsonData,osType):
    for libEntry in versionJsonData["libraries"]:
        # check rules
        rules=libEntry.get("rules",0)
        if rules!=0:
            skip=False
            for ruleEntry in rules:
                # os check
                os=ruleEntry.get("os",0)
                if os!=0:
                    if os!=osType:
                        skip=True
                        break
            if skip:
                continue

        # check and download


def launch(profileName,accountName):
    # get info
    ProfileManager.readProfiles()
    AccountManager.readAccounts()
    SettingManager.readSettings()
    profileInfo=ProfileManager.getProfile(profileName)
    accountInfo=AccountManager.getAccount(accountName)
    settingsInfo=SettingManager.settings
    uriInfo=GameFileUris(settingsInfo["dir"])
    uriInfo.setUrlGroup(settingsInfo["mirror"])

    # check java
    if not Path(profileInfo["java"]).exists():
        raise LauncherException(info=f"Java executable not found: {profileInfo["java"]}")

    versionManifest=getVersionManifest(uriInfo)

    # check official version
    if not any(i["id"]==profileInfo["version"] for i in versionManifest["versions"]) and profileInfo["loader"]=="":
        raise LauncherException(info="UnofficialVersionWithoutLoader")

    uriInfo.generateDir(profileInfo["version"])
    
    versionJson=getVersionJson(uriInfo,profileInfo["version"],versionManifest)

    checkVersionJar(uriInfo,versionJson)

    checkLibraries(uriInfo,versionJson)
    