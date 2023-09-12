import sqlite3
import pandas as pd


def conectar():
    try:
        banco = sqlite3.connect(r"..\data\dados_material.db")
        cursor = banco.cursor()
        return banco, cursor
        # cursor.execute("CREATE TABLE controle_refugo (codigo text, peso text, comprimento text, valor text, quantidade text)")
    except sqlite3.Error as erro:
        print("Erro: ", erro)


def verificar_existencia(item, codigo):
    banco, cursor = conectar()
    cursor.execute(f"SELECT {item} FROM controle_refugo WHERE codigo = '{codigo}'")
    resultado = cursor.fetchone()
    if resultado is not None and resultado[0] is not None:
        return True
    else:
        return False


def pegar_validar_valores(codigo):
    while True:
        try:
            peso = float(input(f"Digite o PESO UNITÁRIO do material {codigo} em gramas: "))
            comprimento = float(input(f"Digite o COMPRIMENTO do material {codigo} em milímetros: "))
            valor = float(input(f"Digite o VALOR EQUIVALENTE do material {codigo} em R$: "))
            return peso, comprimento, valor
        except ValueError or TypeError as erro:
            print("Valor inválido: ", erro, "\nTente novamente\n")
            continue


def inserir(codigo):
    banco, cursor = conectar()
    try:
        if verificar_existencia("codigo", codigo):
            raise sqlite3.Error(f"{codigo} já inserido")
        peso, comprimento, valor = pegar_validar_valores(codigo)
        cursor.execute(f"INSERT INTO controle_refugo (codigo, peso, comprimento, valor) VALUES('{codigo}', '{peso:.2f}g', '{comprimento:.2f}mm', 'R${valor:.2f}')")
        banco.commit()
        print("Dados inseridos com sucesso")
    except sqlite3.Error or ValueError or TypeError as erro:
        print("Erro ao inserir: ", erro)
    banco.close()


def inserir_quantidade(codigo, quantidade):
    banco, cursor = conectar()
    try:
        if not verificar_existencia("codigo", codigo):
            raise sqlite3.Error(f"{codigo} não existe no banco de dados")
        cursor.execute(f"UPDATE controle_refugo SET quantidade = '{quantidade}' WHERE codigo = '{codigo}'")
        banco.commit()
        print("Dados inseridos com sucesso")
    except sqlite3.Error or ValueError as erro:
        print("Erro ao inserir: ", erro)
    banco.close()


def atualizar(codigo):
    banco, cursor = conectar()
    try:
        if not verificar_existencia("codigo", codigo):
            raise sqlite3.Error(f"{codigo} não existe no banco de dados")
        peso, comprimento, valor = pegar_validar_valores(codigo)
        cursor.execute(f"UPDATE controle_refugo SET peso = '{peso}g', comprimento = '{comprimento}mm', valor = 'R${valor}' WHERE codigo = '{codigo}'")
        banco.commit()
        print("Dados atualizados com sucesso")
    except sqlite3.Error or ValueError as erro:
        print("Erro ao atualizar: ", erro)
    banco.close()


def excluir(codigo):
    banco, cursor = conectar()
    try:
        if not verificar_existencia("codigo", codigo):
            raise sqlite3.Error(f"{codigo} não existe no banco de dados")
        cursor.execute(f"DELETE FROM controle_refugo WHERE codigo = '{codigo}'")
        banco.commit()
        print("Dados removidos com sucesso")
    except sqlite3.Error or ValueError as erro:
        print("Erro ao excluir: ", erro)
    banco.close()


def calcular(codigo):
    banco, cursor = conectar()
    try:
        if not verificar_existencia("codigo", codigo):
            raise sqlite3.Error(f"{codigo} não existe no banco de dados")
        if not verificar_existencia("quantidade", codigo):
            raise sqlite3.Error(f"quantidade não cadastrada no banco de dados")
        cursor.execute(f"SELECT * FROM controle_refugo WHERE codigo = '{codigo}'")
        dados = cursor.fetchall()[0]
        _, peso, comprimento, valor, quantidade = dados
        total_peso = float(quantidade) * float(peso.replace('g', ''))
        total_comprimento = float(quantidade) * float(comprimento.replace('mm', ''))
        total_valor = float(quantidade) * float(valor.replace('R$', ''))
        print(f"""\nDados do material {codigo}:\n
- Peso unitário = {peso} -> Quantidade total de peso = {total_peso}g
- Comprimento = {comprimento} -> Quantidade total de comprimento = {total_comprimento}mm
- Valor equivalente = {valor} -> Quantidade total do valor = R${total_valor:.2f}""")
    except sqlite3.Error or ValueError or TypeError as erro:
        print("Erro ao calcular: ", erro)
    banco.close()


def calcular_refugo(codigo, quantidade_pecas):
    banco, cursor = conectar()
    try:
        if not verificar_existencia("codigo", codigo):
            raise sqlite3.Error(f"{codigo} não existe no banco de dados")
        elif not verificar_existencia("quantidade", codigo):
            raise sqlite3.Error(f"quantidade não cadastrada no banco de dados")
        cursor.execute(f"SELECT quantidade FROM controle_refugo WHERE codigo = '{codigo}'")
        dados = cursor.fetchone()
        quantidade = dados[0]
        refugo = int(quantidade) - int(quantidade_pecas)
        if refugo == 0:
            print(f"\nNão houve refugo no processamento do material {codigo}.")
        elif refugo > 0:
            print(f"\nHouve um refugo de {refugo} no processamento do material {codigo}.")
        else:
            print("\nQuantidade de peças maior do que a estimada.")
    except sqlite3.Error or ValueError as erro:
        print("Erro ao calcular: ", erro)
    banco.close()


def visualizar():
    banco, cursor = conectar()
    try:
        cursor.execute("SELECT * FROM controle_refugo ORDER BY codigo ASC")
        data = cursor.fetchall()
        df = pd.DataFrame(data, columns=['Código do material', 'Peso unitário', 'Comprimento', 'Valor equivalente', 'Quantidade']).fillna("---")
        print("\nDados de produção\n\n", df.to_string())
    except sqlite3.Error as erro:
        print("Erro: ", erro)
    banco.close()
