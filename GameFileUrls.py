class Urls:
    versionManifest=""
    versionJson=""

    @staticmethod
    def getVersionJsonUrl(oriUIrl:str):
        return oriUIrl.replace("piston-meta.mojang.com",Urls.versionJson)
    
class Official(Urls):
    versionManifest="http://launchermeta.mojang.com/mc/game/version_manifest.json"
    versionJson="piston-meta.mojang.com"
    versionJar="piston-data.mojang.com"

class Bmclapi(Urls):
    versionManifest="https://bmclapi2.bangbang93.com/mc/game/version_manifest.json"
    versionJson="bmclapi2.bangbang93.com"
    versionJar="bmclapi2.bangbang93.com"

urlList=[Official(),Bmclapi()]