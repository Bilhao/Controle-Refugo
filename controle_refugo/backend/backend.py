import sqlite3


class Controle:
    banco = sqlite3.connect("data/dados.db")
    cursor = banco.cursor()

    def __init__(self, codigo):
        self.codigo = codigo

    @staticmethod
    def verificar_existencia(item, codigo):
        Controle.cursor.execute(f"SELECT {item} FROM controle_refugo WHERE codigo = '{codigo}'")
        resultado = Controle.cursor.fetchone()
        if resultado is not None and resultado[0] is not None:
            return True
        else:
            return False

    @staticmethod
    def popular_dados(tree):
        tree.delete(*tree.get_children())
        Controle.cursor.execute('SELECT * FROM controle_refugo')
        rows = Controle.cursor.fetchall()
        for i, row in enumerate(rows):
            if row[4] is None:
                tree.insert('', 'end', values=(i + 1, row[0], row[1], row[2], row[3], '---'))
            else:
                tree.insert('', 'end', values=(i + 1, row[0], row[1], row[2], row[3], row[4]))

    def analisar(self):
        Controle.cursor.execute(f"SELECT * FROM controle_refugo WHERE codigo = '{self.codigo}'")
        dados = Controle.cursor.fetchall()[0]
        _, peso, comprimento, valor, quantidade = dados
        total_peso = float(quantidade) * float(peso.replace('g', ''))
        total_comprimento = float(quantidade) * float(comprimento.replace('mm', ''))
        total_valor = float(quantidade) * float(valor.replace('R$', ''))
        return peso, comprimento, valor, f"{total_peso}g", f"{total_comprimento}mm", f"R${total_valor:.2f}"

    def cadastrar(self, peso, comprimento, valor):
        Controle.cursor.execute(f"INSERT INTO controle_refugo (codigo, peso, comprimento, valor) VALUES('{self.codigo}', '{peso:.2f}g', '{comprimento:.2f}mm', 'R${valor:.2f}')")
        Controle.banco.commit()

    def atualizar(self, peso, comprimento, valor):
        Controle.cursor.execute(f"UPDATE controle_refugo SET peso = '{peso:.2f}g', comprimento = '{comprimento:.2f}mm', valor = 'R${valor:.2f}' WHERE codigo = '{self.codigo}'")
        Controle.banco.commit()

    def cadastrar_quantidade(self, quantidade):
        Controle.cursor.execute(f"UPDATE controle_refugo SET quantidade = '{quantidade}' WHERE codigo = '{self.codigo}'")
        Controle.banco.commit()

    def calcular_refugo(self, quantidade_pecas):
        Controle.cursor.execute(f"SELECT quantidade FROM controle_refugo WHERE codigo = '{self.codigo}'")
        dados = Controle.cursor.fetchone()
        quantidade = dados[0]
        refugo = int(quantidade) - int(quantidade_pecas)
        return refugo, self.codigo

    def excluir(self):
        Controle.cursor.execute(f"DELETE FROM controle_refugo WHERE codigo = '{self.codigo}'")
        Controle.banco.commit()
