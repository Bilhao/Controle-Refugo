from backend.backend import *
from tkinter import ttk
import customtkinter as ctk
import ctypes

escala = ctypes.windll.shcore.GetScaleFactorForDevice(0) / 100
ctk.set_appearance_mode("dark")


def centralizar(parent, w, h, *args):
    if "main" in args:
        centro_x = parent.winfo_x() + int((parent.winfo_screenwidth() + w) / 2 - w)
        centro_y = parent.winfo_y() + int((parent.winfo_screenheight() + h) / 2 - h) - 30
    else:
        centro_x = parent.winfo_x() + int((parent.winfo_width() + w)/2 - w)
        centro_y = parent.winfo_y() + int((parent.winfo_height() + h) / 2 - h)
    return f"{w}x{h}+{centro_x}+{centro_y}"


class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Controle de refugo")
        self.geometry(f"{centralizar(self, 750, 550, 'main')}")
        self.resizable(False, False)
        self.iconbitmap('assets/icon.ico')

        Label(self).label(260, 17, text="Análise de produção", font=("Inter", 25))
        Label(self).label(42, 84, text="Escolha uma opção:", font=("Inter", 15))

        Frame(self, 30, 55, 690, 1, border_width=2, border_color="#FFFFFF", fg_color="#FFFFFF")

        Button(self).verde(91, 115, 161, 40, text='Analisar produção', command=lambda: TopAnalisar(self, self.pegar_valor()))
        Button(self).verde(293, 115, 161, 40, text='Cadastrar novo material', command=lambda: TopCadastrar(self))
        Button(self).verde(498, 115, 161, 40, text='Atualizar dados', command=lambda: TopAtualizar(self, self.pegar_valor()))
        Button(self).verde(91, 168, 161, 40, text='Cadastrar quantidade', command=lambda: TopCastrarQuantidade(self, self.pegar_valor()))
        Button(self).verde(293, 168, 161, 40, text='Calcular refugo', command=lambda: TopCalcularRefugo(self, self.pegar_valor()))
        Button(self).verde(498, 168, 161, 40, text='Excluir um material', command=lambda: TopExcluir(self, self.pegar_valor()))
        Button(self).verde(15, 510, 121, 28, text='Sincronizar', command=lambda: Controle.popular_dados(self.treeview))
        Button(self).branco(667, 521, 70, 18, text='Sair', command=lambda: (Controle.banco.close(), self.destroy())[0])

        self.treeview = Treeview(self, 25, 235, 700, 255, ('id', 'codigo', 'peso', 'comprimento', 'valor', 'quantidade'))
        self.treeview.bind("<Delete>", lambda event: self.excluir())
        self.valores = ctk.Variable()

    def excluir(self):
        for itens in self.treeview.selection():
            TopSenha(self, command=lambda: Controle(self.treeview.item(itens)['values'][1]).excluir())
        self.popular()

    # Atualiza os itens do Treeview
    def popular(self):
        Controle.popular_dados(self.treeview)

    def pegar_valor(self):
        self.valores.set(self.treeview.item(self.treeview.focus())['values'])
        return self.valores.get()


class Label(ctk.CTkLabel):
    def __init__(self, parent):
        super().__init__(parent)

    def label(self, x, y, font=("Inter", 13), **kwargs):
        self.configure(font=font, **kwargs)
        self.place(x=x, y=y)

    def label_erro(self, relx, y, font=("Inter", 14 * -1), **kwargs):
        self.configure(font=font, text_color="#ff1a1a", height=0, **kwargs)
        self.place(relx=relx, y=y, anchor='center')

    def label_success(self, relx, y, font=("Inter", 14 * -1), **kwargs):
        self.configure(font=font, **kwargs)
        self.place(relx=relx, y=y, anchor='center')


class Frame(ctk.CTkFrame):
    def __init__(self, parent, x, y, w, h, **kwargs):
        super().__init__(parent)
        self.configure(width=w, height=h, **kwargs)
        self.place(x=x, y=y)


class Entry(ctk.CTkEntry):
    def __init__(self, parent, x, y, w, h, **kwargs):
        super().__init__(parent)
        self.configure(width=w, height=h, **kwargs)
        self.place(x=x, y=y)


class Button(ctk.CTkButton):
    def __init__(self, parent):
        super().__init__(parent)

    def verde(self, x, y, w, h, text, command):
        self.configure(width=w, height=h, text=text, command=command, corner_radius=12, border_width=2,
                       border_color='#181818', fg_color='#519654', hover_color='#47854a')
        self.place(x=x, y=y)

    def branco(self, x, y, w, h, text, command):
        self.configure(width=w, height=h, text=text, command=command, text_color="#181818", corner_radius=12,
                       border_width=2, border_color='#181818', fg_color='#949292', hover_color='#c0bfbf')
        self.place(x=x, y=y)


class Treeview(ttk.Treeview):
    def __init__(self, parent, x, y, w, h, columns: tuple, **kwargs):
        super().__init__(parent)
        self.configure(columns=columns, show='headings', selectmode="extended", **kwargs)
        self.place(x=x * escala, y=y * escala, width=w * escala, height=h * escala)

        self.heading('id', text='ID', command=lambda: self.ordenar_colunas(self, 'id', False))
        self.heading('codigo', text='Código do material', command=lambda: self.ordenar_colunas(self, 'codigo', False))
        self.heading('peso', text='Peso unitário', command=lambda: self.ordenar_colunas(self, 'peso', False))
        self.heading('comprimento', text='Comprimento', command=lambda: self.ordenar_colunas(self, 'comprimento', False))
        self.heading('valor', text='Valor equivalente', command=lambda: self.ordenar_colunas(self, 'valor', False))
        self.heading('quantidade', text='Quantidade', command=lambda: self.ordenar_colunas(self, 'quantidade', False))

        self.column('id', width=50)
        self.column('codigo', width=140)
        self.column('peso', width=120)
        self.column('comprimento', width=140)
        self.column('valor', width=130)
        self.column('quantidade', width=120)

        # Estilo do treeview
        style = ttk.Style()
        style.theme_use('default')
        style.configure('Treeview', borderwidth=0, background='#181818', foreground='#FFFFFF', rowheight=int(30 * escala), fieldbackground="#181818", font=('Inter', int(10 * escala)))
        style.configure('Treeview.Heading', borderwidth=1, background='#519654', foreground='#FFFFFF', rowheight=int(30 * escala), fieldbackground="#519654", font=('Inter', int(10 * escala)))
        style.map('Treeview', background=[('selected', '#519654')], foreground=[('selected', '#FFFFFF')])
        style.map('Treeview.Heading', background=[('selected', '#47854a')], foreground=[('selected', '#FFFFFF')])

        # Adiciona um scroll bar ao treeview
        scrollbar = ctk.CTkScrollbar(self, command=self.yview, bg_color="#181818")
        scrollbar.pack(side='right', fill='y')
        self.configure(yscrollcommand=scrollbar.set)

        Controle.popular_dados(self)

    @staticmethod
    # Função para ordenar as colunas
    def ordenar_colunas(tree, coluna, reverse):
        lista = [(tree.set(k, coluna), k) for k in tree.get_children('')]
        if coluna == 'id':
            lista.sort(reverse=reverse, key=lambda x: int(x[0]))
        elif coluna == 'peso':
            lista.sort(reverse=reverse, key=lambda x: float(x[0][:-1]))
        elif coluna == 'comprimento':
            lista.sort(reverse=reverse, key=lambda x: float(x[0][:-2]))
        elif coluna == 'valor':
            lista.sort(reverse=reverse, key=lambda x: float(x[0][2:]))
        else:
            lista.sort(reverse=reverse)

        for index, (valor, posicao) in enumerate(lista):
            tree.move(posicao, '', index)

        tree.heading(coluna, command=lambda _coluna=coluna: tree.ordenar_colunas(tree, _coluna, not reverse))


class TopLevels(ctk.CTkToplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.iconbitmap('assets/icon.ico')
        self.transient(parent)
        self.grab_set()
        self.resizable(False, False)

        self.erro_message = ctk.StringVar()
        self.success_message = ctk.StringVar()

        self.validador = ctk.BooleanVar()


class TopAnalisar(TopLevels):
    def __init__(self, parent, valores):
        super().__init__(parent)
        self.title(f"Controle de refugo - Analisar produção")
        self.geometry(centralizar(self.parent, 650, 285))
        string_vars = [ctk.StringVar() for _ in range(6)]

        Label(self).label(26, 24, text="Digite o código do material de analise:")
        Label(self).label_erro(0.5, 232, textvariable=self.erro_message)

        entry_codigo = Entry(self, 260, 27, 161, 15)
        frame = Frame(self, 10, 67, 630, 150)

        if valores != "":
            entry_codigo.insert(0, valores[1])

        Label(frame).label(10, 5, text="Dados do material:")
        Label(frame).label(33, 40, text="Peso unitário  =")
        Label(frame).label(33, 70, text="Comprimento  =")
        Label(frame).label(33, 100, text="Valor equivalente  =")
        Label(frame).label(310, 40, text="Quantidade total do peso  =")
        Label(frame).label(310, 70, text="Quantidade total do comprimento  =")
        Label(frame).label(310, 100, text="Quantidade total do valor  =")
        Label(frame).label(135, 40, textvariable=string_vars[0])
        Label(frame).label(135, 70, textvariable=string_vars[1])
        Label(frame).label(155, 100, textvariable=string_vars[2])
        Label(frame).label(481, 40, textvariable=string_vars[3])
        Label(frame).label(525, 70, textvariable=string_vars[4])
        Label(frame).label(480, 100, textvariable=string_vars[5])

        Button(self).verde(485, 25, 107, 28, text="Analisar", command=lambda: self.pegar_analisar(string_vars, entry_codigo.get()))
        Button(self).branco(271.5, 246, 107, 28, text="Voltar", command=lambda: self.destroy())

        self.bind("<Return>", lambda event: self.pegar_analisar(string_vars, entry_codigo.get()))
        self.wait_window(self)

    def pegar_analisar(self, string_vars, codigo):
        try:
            self.erro_message.set("")
            if codigo == "":
                raise Exception("Preencha todos os campos!")
            if not Controle.verificar_existencia("codigo", codigo):
                raise sqlite3.Error(f"'{codigo}' não existe no banco de dados")
            if not Controle.verificar_existencia("quantidade", codigo):
                raise sqlite3.Error(f"quantidade não cadastrada no banco de dados")
            [var.set("") for index, var in enumerate(string_vars)]
            [var.set(Controle(str(codigo)).analisar()[index]) for index, var in enumerate(string_vars)]
            App.popular(self.parent)
        except (sqlite3.Error, Exception) as erro:
            self.erro_message.set(f"Erro ao analisar: {erro}")
            [var.set("") for index, var in enumerate(string_vars)]


class TopCadastrar(TopLevels):
    def __init__(self, parent):
        super().__init__(parent)
        self.title(f"Controle de refugo - Cadastrar novo material")
        self.geometry(centralizar(self.parent, 520, 210))

        Label(self).label(26, 24, text="Digite o CÓDIGO do material para cadastrar:")
        Label(self).label(26, 53, text="Digite o PESO UNITÁRIO do material  em gramas:")
        Label(self).label(26, 82, text="Digite o COMPRIMENTO do material em milímetros:")
        Label(self).label(26, 111, text="Digite o VALOR EQUIVALENTE do material em R$:")
        Label(self).label_erro(0.5, 155, textvariable=self.erro_message)
        Label(self).label_success(0.5, 155, textvariable=self.success_message)

        entry_codigo = Entry(self, 332, 27, 161, 15)
        entry_peso = Entry(self, 332, 56, 161, 15)
        entry_comprimento = Entry(self, 332, 85, 161, 15)
        entry_valor = Entry(self, 332, 114, 161, 15)

        Button(self).verde(26, 170, 107, 28, text="Confirmar", command=lambda: self.pegar_cadastrar([entry_codigo, entry_peso, entry_comprimento, entry_valor]))
        Button(self).branco(386, 170, 107, 28, text="Voltar", command=lambda: self.destroy())

        self.bind("<Return>", lambda event: self.pegar_cadastrar([entry_codigo, entry_peso, entry_comprimento, entry_valor]))
        self.wait_window(self)

    def pegar_cadastrar(self, entrys):
        try:
            self.erro_message.set("")
            self.success_message.set("")
            if any(entry.get() == '' for entry in entrys):
                raise Exception("Preencha todos os dados!")
            if Controle.verificar_existencia("codigo", entrys[0].get()):
                raise sqlite3.Error(f"'{entrys[0].get()}' já cadastrado")
            entrys[1:] = [float(entry.get().replace(',', '.')) for entry in entrys[1:]]
            Controle(entrys[0].get()).cadastrar(*entrys[1:])
            App.popular(self.parent)
            self.success_message.set("Dados cadastrados com sucesso!")
        except (sqlite3.Error, Exception) as erro:
            self.erro_message.set(f"Erro ao cadastrar: {erro}")


class TopAtualizar(TopLevels):
    def __init__(self, parent, valores):
        super().__init__(parent)
        self.title(f"Controle de refugo - Atualizar dados")
        self.geometry(centralizar(self.parent, 520, 210))

        Label(self).label(26, 24, text="Digite o CÓDIGO do material para atualizar:")
        Label(self).label(26, 53, text="Digite o PESO UNITÁRIO do material  em gramas:")
        Label(self).label(26, 82, text="Digite o COMPRIMENTO do material em milímetros:")
        Label(self).label(26, 111, text="Digite o VALOR EQUIVALENTE do material em R$:")
        Label(self).label_erro(0.5, 155, textvariable=self.erro_message)
        Label(self).label_success(0.5, 155, textvariable=self.success_message)

        entry_codigo = Entry(self, 332, 27, 161, 15)
        entry_peso = Entry(self, 332, 56, 161, 15)
        entry_comprimento = Entry(self, 332, 85, 161, 15)
        entry_valor = Entry(self, 332, 114, 161, 15)

        if valores != "":
            entry_codigo.insert(0, valores[1])
            entry_peso.insert(0, valores[2][:-1])
            entry_comprimento.insert(0, valores[3][:-2])
            entry_valor.insert(0, valores[4][2:])

        Button(self).verde(26, 170, 107, 28, text="Confirmar", command=lambda: self.pegar_atualizar([entry_codigo, entry_peso, entry_comprimento, entry_valor]))
        Button(self).branco(386, 170, 107, 28, text="Voltar", command=lambda: self.destroy())

        self.bind("<Return>", lambda event: self.pegar_atualizar([entry_codigo, entry_peso, entry_comprimento, entry_valor]))
        self.wait_window(self)

    def pegar_atualizar(self, entrys):
        try:
            self.erro_message.set("")
            self.success_message.set("")
            self.validador.set(False)
            if any(entry.get() == '' for entry in entrys):
                raise Exception("Preencha todos os dados!")
            if not Controle.verificar_existencia("codigo", entrys[0].get()):
                raise sqlite3.Error(f"'{entrys[0].get()}' não existe no banco de dados")
            entrys[1:] = [float(entry.get().replace(',', '.')) for entry in entrys[1:]]
            TopSenha(self, command=lambda: Controle(entrys[0].get()).atualizar(*entrys[1:]))
            if self.validador.get():
                App.popular(self.parent)
                self.success_message.set("Dados atualizados com sucesso!")
        except (sqlite3.Error, Exception) as erro:
            self.erro_message.set(f"Erro ao atualizar: {erro}")


class TopCastrarQuantidade(TopLevels):
    def __init__(self, parent, valores):
        super().__init__(parent)
        self.title(f"Controle de refugo - Cadastrar quantidade")
        self.geometry(centralizar(self.parent, 520, 175))

        Label(self).label(26, 24, text="Digite o CÓDIGO do material:")
        Label(self).label(26, 53, text="Digite a QUANTIDADE estimada de material:")
        Label(self).label_erro(0.5, 110, textvariable=self.erro_message)
        Label(self).label_success(0.5, 110, textvariable=self.success_message)

        entry_codigo = Entry(self, 340, 27, 161, 15)
        entry_quantidade = Entry(self, 340, 56, 161, 15)

        if valores != "":
            entry_codigo.insert(0, valores[1])

        Button(self).verde(26, 135, 107, 28, text="Confirmar", command=lambda: self.pegar_cadastrar_quantidade([entry_codigo, entry_quantidade]))
        Button(self).branco(386, 135, 107, 28, text="Voltar", command=lambda: self.destroy())

        self.bind("<Return>", lambda event: self.pegar_cadastrar_quantidade([entry_codigo, entry_quantidade]))
        self.wait_window(self)

    def pegar_cadastrar_quantidade(self, entrys):
        try:
            self.erro_message.set("")
            self.success_message.set("")
            self.validador.set(False)
            if any(entry.get() == '' for entry in entrys):
                raise Exception("Preencha todos os dados!")
            if not Controle.verificar_existencia("codigo", entrys[0].get()):
                raise sqlite3.Error(f"'{entrys[0].get()}' não existe no banco de dados")
            TopSenha(self, command=lambda: Controle(entrys[0].get()).cadastrar_quantidade(entrys[1].get()))
            if self.validador.get():
                App.popular(self.parent)
                self.success_message.set("Quantidade cadastrada com sucesso!")
        except (sqlite3.Error, Exception) as erro:
            self.erro_message.set(f"Erro ao cadastrar: {erro}")


class TopCalcularRefugo(TopLevels):
    def __init__(self, parent, valores):
        super().__init__(parent)
        self.title(f"Controle de refugo - Calcular refugo")
        self.geometry(centralizar(self.parent, 520, 175))
        refugo = ctk.StringVar()

        Label(self).label(26, 24, text="Digite o CÓDIGO do material para calcular o refugo:")
        Label(self).label(26, 53, text="Digite a QUANTIDADE de peças produzidas:")
        Label(self).label_erro(0.5, 110, textvariable=self.erro_message)
        Label(self).label_success(0.5, 110, textvariable=refugo)

        entry_codigo = Entry(self, 340, 27, 161, 15)
        entry_quantidade = Entry(self, 340, 56, 161, 15)

        if valores != "":
            entry_codigo.insert(0, valores[1])

        Button(self).verde(26, 135, 107, 28, text="Calcular", command=lambda: self.pegar_calcular_refugo(refugo, [entry_codigo, entry_quantidade]))
        Button(self).branco(386, 135, 107, 28, text="Voltar", command=lambda: self.destroy())

        self.bind("<Return>", lambda event: self.pegar_calcular_refugo(refugo, [entry_codigo, entry_quantidade]))
        self.wait_window(self)

    def pegar_calcular_refugo(self, refugo, entrys):
        try:
            refugo.set("")
            if any(entry.get() == '' for entry in entrys):
                raise Exception("Preencha todos os campos!")
            if not Controle.verificar_existencia("codigo", entrys[0].get()):
                raise sqlite3.Error(f"'{entrys[0].get()}' não existe no banco de dados")
            elif not Controle.verificar_existencia("codigo", entrys[0].get()):
                raise sqlite3.Error(f"quantidade não cadastrada no banco de dados")
            conclusao, codigo = Controle(entrys[0].get()).calcular_refugo(entrys[1].get())
            if conclusao == 0:
                refugo.set(f"Não houve refugo no processamento do material {codigo}.")
            elif conclusao > 0:
                refugo.set(f"Houve um refugo de {conclusao} no processamento do material {codigo}.")
            else:
                refugo.set("Quantidade de peças maior do que a estimada.")
        except (sqlite3.Error, Exception) as erro:
            self.erro_message.set(f"Erro ao atualizar: {erro}")


class TopExcluir(TopLevels):
    def __init__(self, parent, valores):
        super().__init__(parent)
        self.title(f"Controle de refugo - Excluir um material")
        self.geometry(centralizar(self.parent, 520, 127))

        Label(self).label(26, 24, text="Digite o CÓDIGO do material para excluir:")
        Label(self).label_erro(0.5, 70, textvariable=self.erro_message)
        Label(self).label_success(0.5, 70, textvariable=self.success_message)

        entry_codigo = Entry(self, 340, 27, 161, 15)

        if valores != "":
            entry_codigo.insert(0, valores[1])

        Button(self).verde(26, 87, 107, 28, text="Excluir", command=lambda: self.pegar_excluir(entry_codigo.get()))
        Button(self).branco(386, 87, 107, 28, text="Voltar", command=lambda: self.destroy())

        self.bind("<Return>", lambda event: self.pegar_excluir(entry_codigo.get()))
        self.wait_window(self)

    def pegar_excluir(self, codigo):
        try:
            self.erro_message.set("")
            self.success_message.set("")
            self.validador.set(False)
            if codigo == "":
                raise Exception("Preencha todos os campos!")
            if not Controle.verificar_existencia("codigo", codigo):
                raise sqlite3.Error(f"'{codigo}' não existe no banco de dados")
            TopSenha(self, command=lambda: Controle(codigo).excluir())
            if self.validador.get():
                App.popular(self.parent)
                self.success_message.set("Item excluido com sucesso!")
        except (sqlite3.Error, Exception) as erro:
            self.erro_message.set(f"Erro ao atualizar: {erro}")


class TopSenha(TopLevels):
    def __init__(self, parent, command):
        super().__init__(parent)
        self.title("Autenticação")
        self.geometry(centralizar(self.parent, 300, 120))

        Label(self).label(20, 20, text="Digite sua senha:")
        Label(self).label_erro(0.5, 65, textvariable=self.erro_message)

        entry_senha = Entry(self, 130, 23, 150, 15, show="*")

        Button(self).verde(26, 81, 107, 28, text="Confirmar", command=lambda: self.validar_senha(entry_senha, command))
        Button(self).branco(170, 81, 107, 28, text="Cancelar", command=lambda: self.destroy())

        self.bind("<Return>", lambda event: self.validar_senha(entry_senha, command))
        self.wait_window(self)

    def validar_senha(self, entry_senha, command):
        try:
            self.erro_message.set("")
            self.validador.set(False)
            if entry_senha.get() == open("data/senha", "r").read().splitlines()[0]:
                self.destroy()
                command()
                self.validador.set(True)
            else:
                entry_senha.delete(0, 'end')
                raise Exception("Senha incorreta")
        except (sqlite3.Error, Exception) as erro:
            self.erro_message.set(f"{erro}")


if __name__ == '__main__':
    app = App()
    app.mainloop()
