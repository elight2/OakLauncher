import profile

def getProfile(profileName):
    for profile in profile.ProfileManager.profiles:
        if profile["name"]==profileName:
            return profile
    
    raise "Profile not found"

def launch(profileName,accountName):
    profile=getProfile(profileName)
    