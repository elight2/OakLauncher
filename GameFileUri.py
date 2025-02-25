from pathlib import Path

class GameFileUris:
    __urls=[
        {
            "versionManifest":"http://launchermeta.mojang.com/mc/game/version_manifest.json",
            "versionJson":"piston-meta.mojang.com",
            "versionJar":"piston-data.mojang.com",
            "libraries":"libraries.minecraft.net"
        },
        {
            "versionManifest":"https://bmclapi2.bangbang93.com/mc/game/version_manifest.json",
            "versionJson":"bmclapi2.bangbang93.com",
            "versionJar":"bmclapi2.bangbang93.com",
            "libraries":"bmclapi2.bangbang93.com/maven"
        }
    ]

    def __init__(self,minecraftPrefix) -> None:
        self.__urlGroup=0
        self.minecraftPrefix=Path(minecraftPrefix)
        self.versionManifestDir=self.minecraftPrefix/Path("version_manifest.json")
        self.librariesRoot=self.minecraftPrefix/Path("libraries")

    def generateDir(self,version):
        self.versionJsonDir=self.minecraftPrefix/Path("versions")/Path(version)/Path(version+".json")
        self.versionJarDir=self.minecraftPrefix/Path("versions")/Path(version)/Path(version+".jar")

    def genLibraryDir(self,libraryPath:str):
        return self.librariesRoot/Path(libraryPath)

    def setUrlGroup(self,group:int):
        self.__urlGroup=group

    def curUrlGroup(self):
        return self.__urls[self.__urlGroup]

    def genVersionJsonUrl(self,oriUIrl:str):
        return oriUIrl.replace("piston-meta.mojang.com",self.curUrlGroup()["versionJson"])
    def genVersionJarUrl(self,oriUIrl:str):
        return oriUIrl.replace("piston-data.mojang.com",self.curUrlGroup()["versionJar"])
    def getVersionManifestUrl(self):
        return self.curUrlGroup()["versionManifest"]
    def genLibraryUrl(self,oriUIrl:str):
        return oriUIrl.replace("libraries.minecraft.net",self.curUrlGroup()["libraries"])