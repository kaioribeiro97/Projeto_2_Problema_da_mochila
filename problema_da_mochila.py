import numpy as np
import time
from tabulate import tabulate
import copy
import os



def menu():#foi decidido realizar chamadas individuais, este pode desconsiderar
    while True:
        print("---------Menu---------\n")
        print('[1] - Escolher correlação do dataset')
        print('[2] - Método por algoritmo gulosa')
        print('[3] - Método por programação dinâmica')
        print('[4] - Sair')
        a = int(input('Digite uma das quatro opções: '))
        if a == 1:
            print('[1] - Correlação fraca')
            print('[2] - Correlação moderada')
            print('[3] - Correlação forte')
            print('[4] - Voltar')
            c = int(input('Digite uma das quatro opções: '))
            caminho_peso = 'dataset/Peso_'+ str(c)+'.txt'
            caminho_valor = 'dataset/valor_'+ str(c)+'.txt'
            caminho_capacidade = 'dataset/capacidade_'+ str(c)+'.txt'
            valor = np.loadtxt(caminho_valor).astype(int)
            peso = np.loadtxt(caminho_peso).astype(int)  
            capacidade = np.loadtxt(caminho_capacidade).astype(int) 
            
        elif a == 2:
           print('---Estrategia gulosa---')
           print('---Métodos---')
           print('[1] - Menor peso')
           print('[2] - Custo beneficio')
           print('[3] - voltar')
           print('[4] - Sair')
           b = int(input('Digite a opção:'))
           if b == 1:
                print('Menor peso')
                Gulosa_menor_peso(peso,valor,capacidade)
           elif b ==2:
                print('custo beneficio')
                Gulosa_custo_beneficio(peso,valor,capacidade)
           elif b == 3:
                print('Voltando')
                menu()
           elif b == 4:
                print('saindo')
                exit()
        elif a == 3:
            saida = testes_dp(peso,valor,capacidade)
            print(saida)    
        elif a == 4:
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


def knapSack_Programming_dinnamic(valor, peso, capacidade_mochila, qtd_itens):
    memoization = [[0 for j in range(capacidade_mochila+1)]
                   for i in range(qtd_itens+1)]
    for i in range(qtd_itens):
        val = valor[i]
        p = peso[i]
        for j in range(capacidade_mochila+1):
            if peso[i] > j:
                memoization[i+1][j] = memoization[i][j]
            else:
                limitePeso = j - p
                if limitePeso < 0:
                    limitePeso = 0
                switchOff = memoization[i][j]
                switchOn = memoization[i][limitePeso] + val
                memoization[i+1][j] = max((switchOff, switchOn))
    return memoization


def testes_dp(peso,valor,capacidade):
    
    valor = valor.tolist()
    peso = peso.tolist()
    tamanho = np.loadtxt('tamanhos.txt').astype(int)
    tamanho = tamanho.tolist()
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
         memo = knapSack_Programming_dinnamic(v, p, capacidade_mochila, qtd_itens)
         print('Lucro: {}'.format(memo[qtd_itens][capacidade_mochila]))
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

def Gulosa_custo_beneficio(peso,valor,capacidade):
    saida = []
    valor = valor.tolist()
    peso = peso.tolist()
    tamanho = np.loadtxt('tamanhos.txt').astype(int)
    tamanho = tamanho.tolist()
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

def Gulosa_menor_peso(peso,valor,capacidade):
    saida = []
    valor = valor.tolist()
    peso = peso.tolist()
    tamanho = np.loadtxt('tamanhos.txt').astype(int)
    tamanho = tamanho.tolist()
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

