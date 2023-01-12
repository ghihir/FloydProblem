import random, math, copy
from operator import attrgetter

GENE_LENGTH = 50

class Individual:
  def __init__(self):
      self.gene = [random.randint(-1,1) for _ in range(GENE_LENGTH)]
      self.MUTATION_RATE = 0.05
      self.fitness = self.computeFittness()

  def computeFittness(self):
    fitness = 0.0
    for i in range(GENE_LENGTH):
      fitness += abs(self.gene[i] * math.sqrt(i + 1))
    return fitness
    
  def mutate(self):
    for i in range(GENE_LENGTH):
      if random.random() < self.MUTATION_RATE:
        self.gene[i] = self.gene[i] * (-1)

  def printInfo(self):
    a = [] ; b = []
    for i, g in enumerate(self.gene):
      if  g == 1: a.append(i + 1)
      else: b.append(i + 1)
    print(f'a: {a}')
    print(f'b: {b}')
    print(f'fitness: {self.fitness}\n')


class Population:
  def __init__(self, number):
    self.number = number
    self.individuals = [Individual() for _ in range(number)]
    self.next_individuals = [Individual() for _ in range(number)]

  def selectParents(self):
    pass

  def crossover(self, individual1, individual2):
    pass

  def evolve(self):
    i = 0
    # エリート保存戦略（半分はこれで決める）
    self.individuals.sort(key=attrgetter('fitness'), reverse=True)
    while i < self.number // 2:
      self.next_individuals[i] = self.individuals[i]
      i += 1
    # 交差によって新しい個体を作成（残り半分）
    while i < self.number:
      individual1 = self.select()
      individual2 = self.select()
      self.next_individuals[i] = self.crossover(individual1, individual2)
      i += 1
    # 突然変異
    for next_individual in self.next_individuals:
      next_individual.mutate()
    self.individuals = self.next_individuals[:]

    

class Main:
  def __init__(self):
    self.best_gene = [0 for _ in range(GENE_LENGTH)]
    self.best_fitness = 10000000

  def solve(self):
    pass


i = Individual()
i.printInfo()
