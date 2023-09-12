from funcoes import *
import os

while True:
    os.system("@echo off")
    os.system("cls")
    opcao = input("""Controle de Refugo

Escolha uma opção:
1 -> Analizar produção
2 -> Cadastrar quantidade de material
3 -> Calcular refugo da produção
4 -> Cadastrar um novo material
5 -> Atualizar dados de um material
6 -> Excluir um material
7 -> Ver dados cadastrados
8 -> Sair
$: """)
    try:
        if opcao == '1':
            codigo = input("Digite o CÓDIGO do material de analise: ")
            calcular(codigo)
        elif opcao == '2':
            codigo = input("Digite o CÓDIGO do material para cadastrar a quantidade: ")
            quantidade = input(f"Digite a QUANTIDADE estimada do material {codigo}: ")
            inserir_quantidade(codigo, quantidade)
        elif opcao == '3':
            codigo = input("Digite o CÓDIGO do material para se calcular o refugo: ")
            quantidade_pecas = input("Digite a QUANTIDADE de peças produzidas: ")
            calcular_refugo(codigo, quantidade_pecas)
        elif opcao == '4':
            codigo = input("Digite o CÓDIGO do material para cadastrar: ")
            inserir(codigo)
        elif opcao == '5':
            codigo = input("Digite o CÓDIGO do material para atualizar: ")
            atualizar(codigo)
        elif opcao == '6':
            codigo = input("Digite o CÓDIGO do material para excluir: ")
            excluir(codigo)
        elif opcao == '7':
            visualizar()
        elif opcao == '8':
            exit()
        else:
            input("\nOpção inválida. Aperte ENTER para continuar...")
            continue
        input("\nAperte ENTER para continuar...")
    except ValueError as erro:
        print(erro)
        input("\nValor inserido é inválido. Tente novamente.")
        continue
