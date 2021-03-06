import random
class brain:
    def __init__(self,instructions, x,y):
        ''' initialise brain values '''
        self.start = [x, y]
        self.x = x
        self.y = y
        self.speed = 10
        self.xmov = 0
        self.ymov = 0
        self.movements = []
        self.itter = 0
        self.canvasobj = None
        self.colour = "#"+"".join([hex(random.randint(17, 255)).replace("0x", "").upper() for i in range(3)])
        self.alive = True
        for i in range(instructions):
            self.movements.append([random.randint(-1*self.speed, 1*self.speed) for j in range(2)])

    def adjust(self, boundries):
        ''' move brain when called '''
        if self.alive:
            self.xmov = self.movements[self.itter][0]
            self.ymov = self.movements[self.itter][1]
            self.x += self.xmov
            self.y += self.ymov
            self.itter += 1
            for bound in boundries:
                if bound(self.x, self.y):
                    self.alive = False

    def score(self, goalx, goaly, cost):
        ''' calculates the score for this brain, given a fitness algorithm '''
        self.cost = cost(self.x, self.y, goalx, goaly)
        return self.cost

    def mutate(self, chance):
        ''' mutates its instuctions '''
        for i in range(len(self.movements)):
            if random.random() <= chance:
                self.movements[i] = [random.randint(-1*self.speed, 1*self.speed) for j in range(2)]
        return self.reset()

    def reset(self):
        ''' resets its values '''
        self.itter = 0
        self.xmov = 0
        self.ymov = 0
        self.x = self.start[0]
        self.y = self.start[1]
        self.alive = True
        self.canvasobj = None
        return self
