import random, math, copy
from operator import attrgetter

GENE_LENGTH = 50

class Individual:
  def __init__(self):
      self.gene = [random.randrange(-1, 2, 2) for _ in range(GENE_LENGTH)]  # -1 or 1
      self.MUTATION_RATE = 0.05
      self.fitness = self.computeFittness()     # 小さい値ほど良い個体

  def computeFittness(self):
    fitness = 0.0
    for i in range(GENE_LENGTH):
      fitness += self.gene[i] * math.sqrt(i + 1)
    fitness = abs(fitness)
    return fitness
    
  def mutate(self):
    # MUTATION_RATEの確率で変異
    for i in range(GENE_LENGTH):
      if random.random() < self.MUTATION_RATE:
        self.gene[i] = self.gene[i] * (-1)
    # 適応度を再計算
    self.fitness = self.computeFittness()


class Population:
  def __init__(self, number):
    self.number = number
    self.individuals = [Individual() for _ in range(number)]

  def selectParents(self):
    return self.individuals[random.randrange(0, self.number)]    # 暫定版

  def crossover(self, individual1, individual2):
    next_individual = Individual()
    type = random.randint(1, 2)
    # 一点交差の場合
    if type == 1:
      point = random.randint(0, 100000000) % (GENE_LENGTH - 1)
      for i in range(GENE_LENGTH):
        if i <= point:
          next_individual.gene[i] = individual1.gene[i]
        else:
          next_individual.gene[i] = individual2.gene[i]
    # 二点交差の場合
    if type == 2:
      point1 = random.randint(0, 100000000) % (GENE_LENGTH - 1)
      point2 = (point1 + (random.randint(0, 100000000) % (GENE_LENGTH - 2) + 1)) % (GENE_LENGTH - 1)
      if point1 > point2: 
        point1, point2 = point2, point1
      for i in range(GENE_LENGTH):
        if i <= point1:
          next_individual.gene[i] = individual1.gene[i]
        elif i <= point2:
          next_individual.gene[i] = individual2.gene[i]
        else:
          next_individual.gene[i] = individual1.gene[i]
    # 適応度を再計算
    next_individual.fitness = next_individual.computeFittness()
    return next_individual

  def evolve(self):
    next_individuals = []
    self.individuals.sort(key=attrgetter('fitness'))
    for i in range(len(self.individuals)):
      # エリート保存戦略（半分はこれで決める）
      if i < self.number // 2:
        next_individuals.append(copy.deepcopy(self.individuals[i]))
      # 交差によって新しい個体を作成（残り半分）
      else:
        individual1 = copy.deepcopy(self.selectParents())
        individual2 = copy.deepcopy(self.selectParents())
        next_individuals.append(self.crossover(individual1, individual2))
    # 突然変異
    for next_individual in next_individuals:
      next_individual.mutate()
    # 世代のスケール
    self.individuals = copy.deepcopy(next_individuals)

  def getBest(self):
    self.individuals.sort(key=attrgetter('fitness'))
    return self.individuals[0]

    
class Main:
  def __init__(self, population_size):
    self.best_gene = [0 for _ in range(GENE_LENGTH)]
    self.best_fitness = 10000000000000000.0
    self.population_size = population_size

  def solve(self, cycle):
    population = Population(self.population_size)
    for _ in range(cycle):
      population.evolve()
      best = population.getBest()
      if best.computeFittness() < self.best_fitness:
        self.best_gene = best.gene[:]
        self.best_fitness = best.computeFittness()
      # print(self.best_fitness)   #####
  
  def result(self):
    A = []
    B = []
    for i in range(len(self.best_gene)):
      if self.best_gene[i] == 1:
        A.append(i + 1)
      else:
        B.append(i + 1)
    print(f'A: {A}')
    print(f'B: {B}')
    print(f'fitness: {self.best_fitness}')


if __name__ == '__main__':
  main = Main(10)     # 個体数を指定
  main.solve(1000)    # 進化の回数を指定
  main.result()
