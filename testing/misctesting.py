import copy
class test:
    def __init__(self, val):
        self.hi = val



class bigTest:
    def __init__(self, num):
        self.myself =  [test(i) for i in range(num)]

    def copyself(self):
        return self.myself

testers = bigTest(20)
testers2 = copy.deepcopy(testers)

for i in testers2.myself:
    i.hi = 10

for i in testers.myself:
    print(i.hi)
