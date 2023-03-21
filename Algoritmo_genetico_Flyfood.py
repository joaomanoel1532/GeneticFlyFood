from typing import List, Tuple, Callable
from random import randint, random, shuffle
from math import cos, radians
import time


def gerar_populacao_inicial(lista: List[list], numero_individuo: int) -> List[List[list]]:
  if len(lista) <= 1 or numero_individuo == 1:
    return [lista]
  
  lista_aux = []
  for i, atual in enumerate(lista):
    elementos_restantes = lista[:i] + lista[i+1:]
    for p in gerar_populacao_inicial(elementos_restantes, numero_individuo):
      
      lista_aux.append([atual] + p)
      if len(lista_aux) == numero_individuo:
        shuffle(lista_aux) 
        return lista_aux
      
  shuffle(lista_aux)  
  
  return lista_aux


def roleta(lista: list[float]) -> int:
  rand = random() * sum(lista)
  soma = 0
  for i, apt in enumerate(lista):
    soma += apt
    if soma >= rand:
      return i


def calcular_dois_pontos(ponto1, ponto2):
  distPontos = ((((ponto1[0] - ponto2[0]) ** 2)+((ponto1[1] - ponto2[1]) ** 2)) ** 0.5)
  return distPontos


def calcular_todas_distancias(lista_cidades: List[List[list]]) -> List[float]:
    distancia_rotas = [None] * len(lista_cidades)
    for i,rota in  enumerate(lista_cidades):
        distancia = 0
        for index, _ in enumerate(rota):
            if index < len(rota)-1:
                distancia += calcular_dois_pontos(rota[index], rota[index + 1])
        distancia += calcular_dois_pontos(rota[-1], rota[0])
        distancia_rotas[i] = distancia
    return distancia_rotas


def escala_apt(lista: list[float]) -> float:
    varlor_minimo = min(lista)
    valor_maximo = max(lista)
    lista_escalada = [(x - varlor_minimo +1) / (valor_maximo - varlor_minimo +1) for x in lista]
    return lista_escalada


def torneio(aptidao: List[float]) -> int:
  pai1 = randint(0, len(aptidao) - 1)
  pai2 = randint(0, len(aptidao) - 1)
  return pai1 if aptidao[pai1] > aptidao[pai2] else pai2
    

def mutacao_genes(lista_populacao: list[list[object]], taxa_mutacao: float):
    for i, elemento in enumerate(lista_populacao):
        if random() <= taxa_mutacao:
            a = randint(0, len(elemento) - 1)
            b = randint(0, len(elemento) - 1)
            lista_populacao[i][a], lista_populacao[i][b] = lista_populacao[i][b], lista_populacao[i][a]
    return lista_populacao


def aptidao(lista_populacao: List[float]) -> List[float]:
  lista_aptidao = [None] * len(lista_populacao)
  for index, el in enumerate(lista_populacao):
    lista_aptidao[index] = cos(el*radians(90))
  return lista_aptidao

def selecao_pais(lista_populacao: List[list[list]], aptidao: List[float], sel_func: Callable) -> List[List[list]]:
  lista_pais: List = [None] * len(lista_populacao)
  for i in range(0, len(lista_populacao), 2):
    idx_pai1_selecionado = sel_func(aptidao)
    idx_pai2_selecionado = sel_func(aptidao[:idx_pai1_selecionado] + aptidao[idx_pai1_selecionado + 1:])
    lista_pais[i] = lista_populacao[idx_pai1_selecionado]
    lista_pais[i+1] = lista_populacao[idx_pai2_selecionado]
  return lista_pais

def PMX(father1, father2):
  cutpoint1 = randint(0, len(father1) - 1)
  cutpoint2 = randint(0, len(father1) - 1)
  if cutpoint1 > cutpoint2:
    cutpoint1, cutpoint2 = cutpoint2, cutpoint1
  
  sons = father1[:]
  
  for i in range(cutpoint1, cutpoint2):
    if father2[i] not in sons[cutpoint1:cutpoint2]:
      j = father1.index(father2[i])
      sons[i], sons[j] = sons[j], sons[i]
  
  for i in range(cutpoint1, cutpoint2):
    if father2[i] not in sons[cutpoint1:cutpoint2]:
      j = father1.index(father2[i])
      sons[j], sons[i] = sons[i], sons[j]

  return sons

def cruzamento_dois_pais(pai1, pai2, taxa_cruzamento) -> Tuple:
  if random() < taxa_cruzamento:
    return PMX(pai1, pai2), PMX(pai2, pai1)
  return pai1, pai2


def cruzamento_todos_pais(lista_pais: List, taxa_cruzamento: float) -> List:
  lista_filho = [None] * len(lista_pais)
  for i in range(0, len(lista_pais), 2):
    lista_filho[i], lista_filho[i + 1]  = cruzamento_dois_pais(lista_pais[i], lista_pais[i + 1], taxa_cruzamento)
  return lista_filho


def evolucao(lista_populacao: List, numero_individuo: int,numero_geracoes: int,
             taxa_cruzamento: float, taxa_mutacao: float, sel_func: Callable) -> Tuple[List[List[list]], List[float]]:
  
  populacao_inicial = gerar_populacao_inicial(lista_populacao, numero_individuo)
  menor_caminho = float('inf')
  for geracao in range(numero_geracoes):
    distancia = calcular_todas_distancias(populacao_inicial)
    melhor_individuo = distancia[distancia.index(min(distancia))]
    print(f'Geração: {geracao}º Menor distância:',melhor_individuo)
    parentes = selecao_pais(populacao_inicial,aptidao(escala_apt(distancia)), sel_func)
    sons = cruzamento_todos_pais(parentes, taxa_cruzamento)
    filhos_mutados = mutacao_genes(sons, taxa_mutacao)
    populacao_inicial = filhos_mutados[:]
    if melhor_individuo < menor_caminho:
      menor_caminho = melhor_individuo
  print(f"menor caminho de todas as gerações {menor_caminho}")
    
  return populacao_inicial, distancia
    

lista = []
a = 'berlin52.tsp'
b ='d198.tsp'
c = 'bayg29.tsp'
with open (c) as obj_file:
  text =obj_file.readlines()
  
for i, el in enumerate(text[6:-1]):
  line = []
  for index, x in enumerate(el.replace('\n', ' ').split(' ')):
    if (x != ''):
      line.append(float(x))
  lista.append((line[1], line[2], str(int(line[0]))))
ini = time.time()
evolucao(
  lista_populacao = lista,
  numero_individuo = 20,
  numero_geracoes = 2000,
  taxa_cruzamento = 0.8,
  taxa_mutacao = 0.1,
  sel_func=torneio
  
)
fim = time.time()
print("Tempo gasto:", round(fim - ini, 3))
