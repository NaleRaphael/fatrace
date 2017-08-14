class Singleton:
    __single = None
    def __new__(clz):
        if not Singleton.__single:
            Singleton.__single = object.__new__(clz)
        return Singleton.__single
        
    def doSomething(self):
        print("do something...XD")

if __name__ == '__main__':
    singleton = Singleton()
    singleton.doSomething()
