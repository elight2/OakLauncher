import urllib.request

# 0: dir is file 1: 
def downloadFile(url:str,dir,filename:str="",type:int=0):
    urllib.request.urlretrieve(url,dir)