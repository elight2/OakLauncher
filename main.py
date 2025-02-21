

def readKey():
    key=input()
    return key

def printHelp():
    pass

registeredFunc={
    "h":printHelp,
    "l":
}

if __name__=="__main__":
    print("Oak Launcher")
    print("Use h to get help")

    try:
        while(True):
            key=readKey()
            func=registeredFunc.get(key,"notFound")
            if func=="notFound":
                print("Unknown command")
            else:
                func()

    except BaseException as exc:
        print("BaseException caught: ",exc)
        print("Exiting...")