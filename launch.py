from account import AccountManager
from LauncherProfile import ProfileManager
from LauncherException import LauncherException
from LauncherDownloader import downloadFile
import GameFileUrls

import os
import json

minecraftPrefix="./minecraft/"
versionManifestDir=minecraftPrefix+"version_manifest.json"
urlInUse=GameFileUrls.Official()

def getVersionManifest():
    # version manifest
    if not os.path.exists(versionManifestDir):
        downloadFile(urlInUse.versionManifest,versionManifestDir)
    with open(versionManifestDir) as versionManifestFile:
        versionManifest=json.load(versionManifestFile)
        return versionManifest

def launch(profileName,accountName):

    # get info
    ProfileManager.readProfiles()
    AccountManager.readAccounts()
    profileInfo=ProfileManager.getProfile(profileName)
    accountInfo=AccountManager.getAccount(accountName)

    # check java
    if not os.path.exists(profileInfo["java"]):
        raise LauncherException(info=f"Java executable not found: {profileInfo["java"]}")

    # check official version
    officialVersion=False
    versionManifest=getVersionManifest()
    for i in versionManifest["versions"]:
        if i["id"]==profileInfo["version"]:
            officialVersion=True
            break
    if not officialVersion and profileInfo["loader"]=="":
        raise LauncherException(info="UnofficialVersionWithoutLoader")
    