import numpy as np
import time
from tabulate import tabulate
import copy
import os



def menu():#foi decidido realizar chamadas individuais, este pode desconsiderar
    while True:
        print("---------Menu---------\n")
        print('[1] - Método por algoritmo gulosa')
        print('[2] - Método por programação dinâmica')
        print('[3] - Sair')
        a = int(input('Digite uma das quatro opções: '))
        if a == 1:
           print('---Estrategia gulosa---')
           print('---Métodos---')
           print('[1] - Menor peso')
           print('[2] - Custo beneficio')
           print('[3] - voltar')
           print('[4] - Sair')
           b = int(input('Digite a opção:'))
           if b == 1:
                print('Menor peso')
                Gulosa_menor_peso()
           elif b ==2:
                print('custo beneficio')
                Gulosa_custo_beneficio()
           elif b == 3:
                print('Voltando')
                menu()
           elif b == 4:
                print('saindo')
                exit()
        elif a == 2:
            saida = testes_dp()
            print(saida)    
        elif a == 3:
            print('exit')
            exit()


def pesagem(item):
    return item[2]


def valores(item):
    return item[1]
    
def custo_beneficio(item):
    return float(valores(item))/pesagem(item)

def menorpeso(item):
    return (100/pesagem(item))


def knapSack_Programming_dinnamic(W, wt, val, n):
   K = [[0 for x in range(W + 1)] for x in range(n + 1)]
   #Table in bottom up manner
   for i in range(n + 1):
      for w in range(W + 1):
         if i == 0 or w == 0:
            K[i][w] = 0
         elif wt[i-1] <= w:
            K[i][w] = max(val[i-1] + K[i-1][w-wt[i-1]], K[i-1][w])
         else:
            K[i][w] = K[i-1][w]
   return K[n][W]

def testes_dp():
    valor = np.loadtxt('valores.txt').astype(int)
    peso = np.loadtxt('pesos.txt').astype(int)
    valor = valor.tolist()
    peso = peso.tolist()
    tamanho = np.loadtxt('tamanhos.txt').astype(int)
    tamanho = tamanho.tolist()
    capacidade = np.loadtxt('capacidade.txt').astype(int)
    capacidade = capacidade.tolist()
    saida = []
    for i in range(0, 7):
         qtd_itens = tamanho[i]
         capacidade_mochila = capacidade[i]
         print('Qtd de itens', qtd_itens)
         print('Capacidade da mochila',capacidade_mochila)
         v = valor[:qtd_itens]
         p = peso[:qtd_itens]
         a = time.time()
         print('Lucro: {}'.format( knapSack_Programming_dinnamic(capacidade_mochila, p, v, qtd_itens)))
         b = time.time()
         saida.append([i, b-a])
         print('Tempo: {}'.format(b-a))
         capacidade = capacidade * 10
         print('----------')
    return saida

def knapsack_ga(items, capacidade, keyFunc=custo_beneficio):
    knapsack = []
    knapsack_peso = 0
    knapsack_valor = 0
    # itens_ordenados = sorted(items, key=keyFunc)
    itens_ordenados = sorted(items,key = keyFunc)
    while len(itens_ordenados) > 0:
        item = itens_ordenados.pop()
        if pesagem(item) + knapsack_peso <= capacidade:
            knapsack.append(item)
            knapsack_peso += pesagem(knapsack[-1])
            knapsack_valor += valores(knapsack[-1])
        else:
            break
    return knapsack, knapsack_peso, knapsack_valor

def Gulosa_custo_beneficio():
    saida = []
    valor = np.loadtxt('valores.txt').astype(int)
    peso = np.loadtxt('pesos.txt').astype(int)
    valor = valor.tolist()
    peso = peso.tolist()
    tamanho = np.loadtxt('tamanhos.txt').astype(int)
    tamanho = tamanho.tolist()
    capacidade = np.loadtxt('capacidade.txt').astype(int)
    capacidade = capacidade.tolist()

    itens = []
    for i in range(len(valor)):
        itens.append([i, valor[i], peso[i]])
        
    for i in range(0, 7):
        qtd_itens = tamanho[i]
        bagagem = itens[:qtd_itens]
        print(qtd_itens)
        capacidade_mochila = capacidade[i]
        print('capacidade Mochila:',capacidade_mochila)
        a = time.time()
        mochila, moc_peso, lucro = knapsack_ga(bagagem, capacidade_mochila)
        b = time.time()
        saida.append([qtd_itens, b-a, lucro])
        print('Lucro: {}'.format(lucro))
        print('tempo {}'.format(b-a))
        print('--------')
    return saida


def knapsack_ga_menorpeso(items, capacidade, keyFunc=menorpeso):
    knapsack = []
    knapsack_peso = 0
    knapsack_valor = 0
    itens_ordenados = sorted(items, key=keyFunc)
    # itens_ordenados = sorted(items,key = keyFunc)
    # print(itens_ordenados)
    while len(itens_ordenados) > 0:
        item = itens_ordenados.pop()
        if pesagem(item) + knapsack_peso <= capacidade:
            knapsack.append(item)
            knapsack_peso += pesagem(knapsack[-1])
            knapsack_valor += valores(knapsack[-1])
        else:
            break
    return knapsack, knapsack_peso, knapsack_valor

def Gulosa_menor_peso():
    saida = []
    valor = np.loadtxt('valores.txt').astype(int)
    peso = np.loadtxt('pesos.txt').astype(int)
    valor = valor.tolist()
    peso = peso.tolist()
    tamanho = np.loadtxt('tamanhos.txt').astype(int)
    tamanho = tamanho.tolist()
    capacidade = np.loadtxt('capacidade.txt').astype(int)
    capacidade = capacidade.tolist()

    itens = []
    for i in range(len(valor)):
        itens.append([i, valor[i], peso[i]])

    for i in range(0, 7):
        qtd_itens = tamanho[i]
        bagagem = itens[:qtd_itens]
        print(qtd_itens)
        capacidade_mochila = capacidade[i]
        print('capacidadeMochila',capacidade_mochila)
        a = time.time()
        mochila, moc_peso, lucro = knapsack_ga_menorpeso(bagagem, capacidade_mochila)
        b = time.time()
        saida.append([qtd_itens, b-a,lucro])
        print('Lucro: {}'.format(lucro))
        print('tempo {}'.format(b-a))
        print('moc_peso: {}'.format(moc_peso))
        print('--------')
    return saida

