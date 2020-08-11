from src.brain import brain
import random
import copy
class gen:
    def __init__(self, instructions, start=[0, 0]):
        self.instructions = instructions
        self.brains = []
        self.start = start
        self.population = 1
        self.boundries = []
        self.goalx = 0
        self.goaly = 0
        self.lossfun = lambda x, y, exptx, expty: ((exptx-x)**2 + (expty-y)**2)

    def populate(self, population):
        self.population = population
        for i in range(population):
            self.brains.append(brain(self.instructions, self.start[0], self.start[1]))

    def move(self):
        for i in range(self.population):
            self.brains[i].adjust(self.boundries)

    def create_boundry(self, x1, y1, x2, y2, out=False):
        if out:
            bound = lambda posx, posy: posx<x1 or posx>x2 or posy<y1 or posy>y2
        else:
            bound = lambda posx, posy: posx>x1 and posx<x2 and posy>y1 and posy<y2
        self.boundries.append(bound)

    def goal(self, x, y):
        self.goalx = x
        self.goaly = y
        self.boundries.append(lambda posx, posy: posx==x and posy==y)

    def sort(self, x):
        ''' sort an array of arrays in decending order based off the second item '''
        not_ordered = True
        while not_ordered:
            not_ordered = False
            for i in range(len(x)-1):
                if x[i][1] < x[i+1][1]:
                    temp = x[i]
                    x[i] = x[i+1]
                    x[i+1]= temp
                    not_ordered = True
        return x

    def new(self):
        rankings = []
        for i in range(self.population):
            score = self.brains[i].score(self.goalx, self.goaly, self.lossfun)
            rankings.append([self.brains[i], score])
        rankings = self.sort(rankings)
        weighted_rankings = copy.deepcopy(rankings)
        for rank in range(len(rankings)):
            for j in range(rank):
                weighted_rankings.append(rankings[rank])
        new_generation = []
        new_generation.append(rankings[-1][0].reset())
        for new_populant in range(self.population-1):
            fittest = random.randint(0, len(weighted_rankings)-1)
            baby = copy.deepcopy(weighted_rankings[fittest][0])
            baby.mutate(0.1)
            new_generation.append(baby)
        self.brains = new_generation
        return new_generation
