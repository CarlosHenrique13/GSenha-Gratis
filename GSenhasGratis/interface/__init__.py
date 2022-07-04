import sys
from tkinter import *
from tkinter import ttk, messagebox
from ttkthemes import ThemedTk
import pyperclip as cp
import json
from GSenhasGratis import *


class Interface:
    def __init__(self):
        # variaveis Padrão
        self.gcode = None
        self.help = """[F5]     Atualiza a tabela de senhas 
[Del]    Deleta uma senha
[TAB]    Trocar de campo de digitação
[Enter]  Envia resultado dependendo do campo que for \npresionado
[Ctrl+s] Salvar nova senha ou altera senha antiga
[Ctrl+l] Limpar caixas de textos"""

        # Temas
        self.temas = ('scidblue', 'equilux', 'adapta', 'default', 'itft1', 'clearlooks',
                      'radiance', 'vista', 'yaru')
        # Acessando o banco de dados
        self.gsenha = GSenha("")

        # Configurações pelo Json
        self.config = {"tema": "scidblue", "status_visible": 0}
        self.config = self._json_get()
        self._visible = self.config["status_visible"]

        # Definindos Items para o __INIT__
        self.id = None
        self.user = None
        self.pswd = None
        self.tema = None
        self.site = None
        self.nome = None
        self.busca = None
        self.senha = None
        self.email = None
        self.style = None
        self.code_r = None
        self.tabela = None
        self.iflogin = None
        self.ifbusca = None
        self.colunas = None
        self.usuario = None
        self.bnt_ocult = None
        self.login_style = None
        self.login_janela = None
        self.senha_janela = None
        self.senha_confirma = None
        self.janela_principal = None
        self.cadastra_janela = None

        # Chamando Interface de Login
        self.login()

    # INTERFACE DE LOGIN
    def login(self):
        """
        -> Janela de Login
        :return: None
        """
        # Interface de Login
        self.login_janela = ThemedTk(theme='scidblue')
        self.login_janela.resizable(False, False)

        try:
            self.login_style = ttk.Style(self.login_janela)
            self.login_style.theme_use(self.config['tema'])
        except TclError:
            self.config['tema'] = 'scidblue'
            self.login_style.theme_use(self.config['tema'])
            self._json_save()
            self.config = self._json_get()

        self.login_janela.title("GSenha")
        lado, cima = (self.login_janela.winfo_screenwidth()), (self.login_janela.winfo_screenheight())
        self.login_janela.geometry(f"350x200+{int((lado - 350) / 2)}+{int((cima - 200) / 3)}")
        self.iflogin = ttk.Frame(self.login_janela, width=350, height=200)
        self.iflogin.pack()

        # Usuario
        self.user = self._entry(self.iflogin, "Usuário ou E-mail", 5, 50, 150, 50, self.valida)
        self.user.focus()
        # Senha
        self.pswd = self._entry(self.iflogin, "Senha", 5, 90, 150, 90, self.valida)
        self.pswd['show'] = '*'
        # Envia
        btn_submit = ttk.Button(self.iflogin, text="Login", command=lambda: self.valida())
        btn_submit.place(x=180, y=125)
        # Cadastra Novo Usuario
        btn_cadastra = ttk.Button(self.iflogin, text="Cadastrar", command=lambda: self.cadastra())
        btn_cadastra.place(x=50, y=125)
        # Esqueseu a Senha
        btn_senha_troca = ttk.Button(self.iflogin, text="Esqueceu a sua Senha? ", command=lambda: self.nova_senha())
        btn_senha_troca.place(x=100, y=160)
        self.login_janela.bind("<Return>", self.valida)
        self.login_janela.mainloop()

    # INTERFACE DE CADASTRO DENOVO USUARIO
    def cadastra(self):
        """
        -> Janela de cadastro de novo Usuario
        :return: None
        """
        self.login_janela.destroy()
        # Janela de Cadastro
        self.cadastra_janela = ThemedTk(theme='scidblue')
        self.cadastra_janela.title("GSenha Cadastro")
        self.cadastra_janela.resizable(False, False)
        login = ttk.Style(self.cadastra_janela)
        login.theme_use(self.config['tema'])
        lado, cima = (self.cadastra_janela.winfo_screenwidth()), (self.cadastra_janela.winfo_screenheight())
        self.cadastra_janela.geometry(f"350x180+{int((lado - 350) / 2)}+{int((cima - 180) / 3)}")
        cadastra = ttk.Frame(self.cadastra_janela, width=350, height=180)
        cadastra.pack()
        # Email
        self.email = self._entry(cadastra, 'Email', 5, 5, 150, 5, self._new_user)
        self.email.focus()
        # usuario
        self.usuario = self._entry(cadastra, 'Nome de Usuario', 5, 35, 150, 35, self._new_user)
        # Senha
        self.senha = self._entry(cadastra, 'Senha', 5, 65, 150, 65, self._new_user)
        self.senha['show'] = '*'
        # Repetir Senha
        self.senha_confirma = self._entry(cadastra, 'Confirma a Senha', 5, 95, 150, 95, self._new_user)
        self.senha_confirma['show'] = '*'
        btn = ttk.Button(cadastra, text="Cadastra", command=lambda: self._new_user())
        btn.place(x=150, y=125)
        self.cadastra_janela.bind("<Return>", self._new_user)
        self.cadastra_janela.mainloop()
        self.login()

    # INTERFACE DE NOVA SENHA
    def nova_senha(self):
        self.login_janela.destroy()
        # Jane de Altera Senha
        self.senha_janela = ThemedTk(theme='scidblue')
        self.senha_janela.title("GSenha Trocar Senha")
        self.senha_janela.resizable(False, False)
        login = ttk.Style(self.senha_janela)
        login.theme_use(self.config['tema'])
        login.theme_use(self.config['tema'])
        lado, cima = (self.senha_janela.winfo_screenwidth()), (self.senha_janela.winfo_screenheight())
        self.senha_janela.geometry(f"400x180+{int((lado - 350) / 2)}+{int((cima - 180) / 3)}")
        tela = ttk.Frame(self.senha_janela, width=400, height=180)
        tela.pack()
        # Formulario
        self.usuario = self._entry(tela, 'Usuário ou E-mail', 5, 5, 200, 5, self._new_pswd)
        self.usuario.focus()
        self.code_r = self._entry(tela, 'Chave de Recuperação', 5, 35, 200, 35, self._new_pswd)
        self.senha = self._entry(tela, 'Nova Senha', 5, 65, 200, 65, self._new_pswd)
        self.senha['show'] = '*'
        self.senha_confirma = self._entry(tela, 'Digite Novamente a Senha', 5, 95, 200, 95, self._new_pswd)
        self.senha_confirma['show'] = '*'
        btn = ttk.Button(tela, text="Altera a Senha", command=lambda: self._new_pswd())
        btn.place(x=150, y=125)
        self.senha_janela.mainloop()
        self.login()

    # Cadastrar Novo usuario
    def _new_user(self, event=None):
        """
        -> Responsavel por Cadastra Novo Usuario
        :return: None
        """
        if self.senha.get() == self.senha_confirma.get():
            if self.gsenha.new_user(nome=self.usuario.get(), email=self.email.get(), senha=self.senha.get()):
                messagebox.showinfo("GSenha Cadastro", "Usuário Cadastrado com Sucesso!")
                self.cadastra_janela.destroy()
            else:
                messagebox.showinfo("GSenha Cadastro", "Usuário já Existente, ou e-mail já Cadastrado!!")

    # Alterando Senha
    def _new_pswd(self, event=None):
        if self.senha.get() == self.senha_confirma.get():
            status, chave = self.gsenha.user_new_pswd(user=self.usuario.get(), pswd=self.senha.get(),
                                                      chave=self.code_r.get())
            if status:
                messagebox.showinfo("GSenha Nova Senha", f"Sua Nova senha foi alterada com Sucesso!\n"
                                    f"Sua Nova Chave: {chave}")
                self.senha_janela.destroy()
            else:
                messagebox.showinfo("GSenha Nova Senha", "Não foi possivel altera a sua senha,"
                                    " verifique se os dados estão corretos")

    # Campos de texto do cadastra
    @staticmethod
    def _entry(iframe, txt, x1, y1, x2, y2, funcao):
        """
        -> Criar Linha de Cadastra
        :param iframe: Tela onde Ficara o Objeto(IFrame)
        :param txt: Nome do Objeto e Nome que aparecera para o usuário como identificado
        :param x1: local x para o texto
        :param y1: local y para o texto
        :param x2: local x para o caixa de texto
        :param y2: local y para o caixa de texto
        :return: O Objeto Criado
        """
        ttk.Label(iframe, text=f"{txt}: ").place(x=x1, y=y1)
        txt = ttk.Entry(iframe)
        txt.place(x=x2, y=y2)
        txt.bind("<Return>", funcao)
        return txt

    # Salvar Json
    def _json_save(self):
        with open("interface.json", 'w+') as file_json:
            json.dump(self.config, file_json)

    # Pegar Json
    def _json_get(self):
        try:
            with open("interface.json", 'r') as file_json:
                return json.load(file_json)
        except FileNotFoundError:
            self._json_save()
            return self._json_get()

    # Menu da Tabela
    def _menu(self):
        """
        -> Responsavel pela criação do menu da tabela (clique do mouse)
        :return: None
        """
        self.tabela_m = Menu(self.tabela, tearoff=0)
        self.tabela_m.add_command(label="Copiar", command=lambda: self._copy_table())
        self.tabela_m.add_command(label="Deleta", command=lambda: self._delete_senha())

    # Limpar Entradad de dados de usuário
    def _clear_entry(self, event=None):
        """
        -> Limpar as caixas de Entrada
        :return: None
        """
        self.id['text'] = '0'
        self.nome.delete(0, 'end')
        self.usuario.delete(0, 'end')
        self.site.delete(0, 'end')
        self.senha.delete(0, 'end')
        self.nome.focus()

    # Fazer uma Busca pela senha
    def _buscar(self, event=None):
        """
        -> Responsavel por Fazer a buscar de Informações das senha apartir do nome
        :return: None
        """
        self._clear_table()
        for row in self.gsenha.buscar(nome=self.busca.get(), retrono=True):
            self.tabela.insert("", "end", values=(row[0], row[1],
                                                  self.gcode.desc(row[2], self.gcode.keys),
                                                  self.gcode.desc(row[3], self.gcode.keys),
                                                  self.gcode.desc(row[4], self.gcode.keys)))

    # Criar Linha de Texto com Campo de Digitação
    def _entry_line(self, iframe, txt, x1, y1, x2, y2):
        """
        -> Criar Linha de Cadastra
        :param iframe: Tela onde Ficara o Objeto(IFrame)
        :param txt: Nome do Objeto e Nome que aparecera para o usuário como identificado
        :param x1: local x para o texto
        :param y1: local y para o texto
        :param x2: local x para o caixa de texto
        :param y2: local y para o caixa de texto
        :return: O Objeto Criado
        """
        ttk.Label(iframe, text=f"{txt}: ").place(x=x1, y=y1)
        txt = ttk.Entry(iframe)
        txt.place(x=x2, y=y2)
        txt.bind("<Return>", self._salva)
        txt.bind("<Control-s>", self._salva)
        txt.bind("<Control-l>", self._clear_entry)
        txt.bind('<Control-KeyRelease-a>', self.callback)
        return txt

    # Altera o Tema
    def _tema_mode(self, event=None):
        tema = self.tema.get()
        self.style.theme_use(tema)
        self.config['tema'] = tema
        self._json_save()

    # INTERFACE PRINCIPAL DO PROGRAMA
    def interface(self):
        """
        -> Interface Principal
        :return: None
        """
        # try:

        min_midth = 650
        min_height = 500
        self.janela_principal = ThemedTk(theme='scidblue')
        self.style = ttk.Style(self.janela_principal)
        self.style.theme_use(self.config['tema'])
        self.janela_principal.title("GSenha")
        lado, cima = (self.janela_principal.winfo_screenwidth()), (self.janela_principal.winfo_screenheight())
        self.janela_principal.geometry(f"{min_midth}x{min_height}+{int((lado - min_midth) / 2)}+"
                                       f"{int((cima - min_height) / 3)}")
        self.janela_principal.resizable(False, False)

        # buscar Senha
        self.ifbusca = ttk.Frame(self.janela_principal, width=min_midth, height=40)
        self.ifbusca.place(x=0, y=0)
        # Texto de Buscar Senha
        ttk.Label(self.ifbusca, text="Buscar: ").place(x=5, y=5)
        # Campo de Buscar senha
        self.busca = ttk.Entry(self.janela_principal, width=50)
        self.busca.place(x=70, y=5)
        self.busca.focus()
        # Butão de Busca
        buscar_img = PhotoImage(file=r"./icon/database-search.png")
        img_buscar = buscar_img.subsample(3, 3)
        btn_buscar = ttk.Button(self.ifbusca, text="Buscar", image=img_buscar, width=6, command=lambda: self._buscar())
        btn_buscar.place(x=480, y=5)
        self.busca.bind('<Control-KeyRelease-a>', self.callback)
        self.busca.bind("<Return>", self._buscar)
        # Butão de Deslogar
        ttk.Button(self.ifbusca, text="Sair", width=4, command=lambda: self._deslogar()).place(x=580, y=5)

        # Adicionar Senha/Altera
        ifadd = ttk.Frame(self.janela_principal, width=min_midth, height=200)
        ifadd.place(x=0, y=40)

        # Ajuda
        ttk.Label(ifadd, text=self.help).place(x=270, y=40)

        # Id
        ttk.Label(ifadd, text="ID: ").place(x=0, y=0)
        self.id = ttk.Label(ifadd, text="0")
        self.id.place(x=80, y=0)

        # Nome
        self.nome = self._entry_line(iframe=ifadd, txt='Nome', x1=0, y1=30, x2=80, y2=30)

        # Usuario
        self.usuario = self._entry_line(iframe=ifadd, txt='Usuário', x1=0, y1=60, x2=80, y2=60)

        # Senha
        self.senha = self._entry_line(iframe=ifadd, txt="Senha", x1=0, y1=90, x2=80, y2=90)

        # Site
        self.site = self._entry_line(iframe=ifadd, txt="Site", x1=0, y1=120, x2=80, y2=120)

        # Botoẽs
        btn_clear = ttk.Button(ifadd, text="Limpar", width=6, command=lambda: self._clear_entry())
        btn_clear.place(x=5, y=150)
        btn_delete = ttk.Button(ifadd, text="Deleta", width=6, command=lambda: self._delete_senha())
        btn_delete.place(x=90, y=150)
        btn_update = ttk.Button(ifadd, text="Salvar", width=6, command=lambda: self._salva())
        btn_update.place(x=175, y=150)

        # Temas
        self.tema = ttk.Combobox(ifadd, values=self.temas)
        self.tema.place(x=360, y=0)
        self.tema.current(self.temas.index(self.config['tema']))
        self.tema.bind('<<ComboboxSelected>>', self._tema_mode)

        # Tabela de Senha
        iftabela = ttk.Frame(self.janela_principal, width=600, height=250)
        iftabela.place(x=0, y=230)
        self.colunas = ('ID', 'NOME', 'SITE', 'USUARIO', 'SENHA')
        self.tabela = ttk.Treeview(iftabela, columns=self.colunas, show="headings", height=12)

        # Definindo as Colunas
        self.tabela.column("ID", minwidth=0, width=50)
        self.tabela.column("NOME", minwidth=0, width=120)
        self.tabela.column("SITE", minwidth=0, width=200)
        self.tabela.column("USUARIO", minwidth=0, width=150)
        self.tabela.column("SENHA", minwidth=0, width=130)
        self.tabela.heading('ID', text='ID')
        self.tabela.heading('NOME', text='NOME')
        self.tabela.heading('SITE', text='SITE')
        self.tabela.heading('USUARIO', text='USUÁRIO')
        self.tabela.heading('SENHA', text='SENHA')

        # Ocultar Senha
        btn_img = PhotoImage(file=r"./icon/eye-outline.png")
        img_btn_outline = btn_img.subsample(3, 3)
        self.bnt_ocult = ttk.Button(self.ifbusca, image=img_btn_outline, command=lambda: self._list_table())
        self.bnt_ocult.place(x=520, y=5)

        # Inserindo os dados na Tabela
        self._list_table()

        # Menu Mouse da Tabela
        self._menu()

        # Interação com a Tabela
        self.tabela.bind("<Double-1>", self._tabela_click)
        self.tabela.bind("<Button-1>", self._invisible_menu_table)
        self.tabela.bind("<Button-3>", self._menu_tabela)
        self.tabela.bind("<Delete>", self._delete_senha)
        # Possicionar a tabela
        self.tabela.pack()

        # Manter Janela em Exeução
        self.janela_principal.bind("<Button-1>", self._invisible_menu_table)
        self.janela_principal.bind("<Control-l>", self._clear_entry)
        self.janela_principal.bind("<Control-s>", self._salva)
        self.janela_principal.bind("<Delete>", self._delete_senha)
        self.janela_principal.bind("<F5>", self._list_table)

        self.janela_principal.mainloop()
        # finalizando a Interface
        try:
            self.tabela_m.destroy()
            self.login_janela.destroy()
        except TclError:
            pass
        # except AttributeError:

    @staticmethod
    def callback(event):
        """
        -> Seleciona o Texto da Caix de Texto
        :param event: Gerado pelo Teclado
        :return: None
        """
        # select text
        event.widget.select_range(0, 'end')
        # move cursor to the end
        event.widget.icursor('end')

    # Deslogar
    def _deslogar(self):
        """
        -> Deslogar
         - detroi janela pricipal e reconstroi o login
        :return: None
        """
        self.janela_principal.destroy()
        self.login()

    # Salvar dados
    def _salva(self, event=None):
        """
        -> Salvar Uma Nova Senha
        :return: None
        """
        nome = self.nome.get()
        if nome != '':
            if self.id.cget('text') == '0':
                status = self.gsenha.new_senha(nome=nome,
                                               site=self.site.get(),
                                               usuario=self.usuario.get(),
                                               senha=self.senha.get(),
                                               keys=self.gcode.keys)
                self._clear_table()
                self._list_table()
                self._clear_entry()
                self.nome.focus()
                if status:
                    # Criar Um popup de Avisso de Adicionado com sucesso
                    pass
            elif self.id.cget('text') >= '1':
                status = self.gsenha.update(idd=self.id.cget('text'), nome=nome,
                                            site=self.site.get(),
                                            usuario=self.usuario.get(),
                                            senha=self.senha.get())
                self._clear_table()
                self._list_table()
                self._clear_entry()
                self.nome.focus()
                if status:
                    # Criar Um popup de Avisso de Adicionado com sucesso
                    pass

    # Deletar Senha
    def _delete_senha(self, event=None):
        """
        -> Removera o registro da Senha
        :return: None
        """
        try:
            item = self.tabela.item(self.tabela.focus())['values'][0]
            self.id['text'] = item
            self.gsenha.delete(self.id.cget('text'))
            self._clear_table()
            self._list_table()
        except IndexError:
            pass

    # Limpar tabela
    def _clear_table(self):
        """
        -> Apagar visualização de todos os dados da Tabela
        :return: None
        """
        for item in self.tabela.get_children():
            self.tabela.delete(item)

    # Exibir a Senha e Usuario
    def _list_table(self, event=None):
        """
        -> Mostrara as senha e usuario ou deixara oculto as informações
        :return: None
        """
        if self._visible == 0:
            self._clear_table()
            # Inserindo os dados na Tabela
            for row in self.gsenha.listar(True):
                self.tabela.insert("", "end", values=(row[0], row[1],
                                                      self.gcode.desc(row[2],
                                                      self.gcode.keys), "***", "***"))
            self._visible = 1
            self.config["status_visible"] = 0
            self._json_save()
        elif self._visible == 1:
            self._clear_table()
            for row in self.gsenha.listar(True):
                self.tabela.insert("", "end", values=(row[0], row[1],
                                                      self.gcode.desc(row[2], self.gcode.keys),
                                                      self.gcode.desc(row[3], self.gcode.keys),
                                                      self.gcode.desc(row[4], self.gcode.keys)))
            self._visible = 0
            self.config["status_visible"] = 1
            self._json_save()

    # Remover o menu de click do mouse
    def _invisible_menu_table(self, event=None):
        """
        -> Responsavel por remover o menu do mouse
        :return: None
        """
        try:
            item = self.tabela.item(self.tabela.focus(), 'values')[0]
            self.id['text'] = item
        except IndexError:
            pass
        self.tabela_m.destroy()
        self._menu()

    # Pegar valor do Item espesifco da uma linha
    def _ident_items_table(self):
        """
        -> Retorna a conteúdo da linha na possição da coluna que foi clicado
        :return: Texto da Tabela que foi selecionado
        """
        try:
            cur_item = self.tabela.item(self.tabela.focus())
            col = self.tabela.identify_column(self.clickdireito.x)
            # Verificar qual coluna foi clicada da linha
            for iten in range(1, len(self.colunas) + 1):
                if col == f"#{iten}":
                    return str(cur_item['values'][iten - 1])
        except IndexError:
            pass

    # Copiar para Are a Tranferencia
    def _copy_table(self):
        """
        -> Copiar o dado da Coluna de Uma linha espesifica ao clicar
        :return: None
        """
        cp.copy(str(self._ident_items_table()))

    # Menu da Tabela ao Clik com Direito do mouse
    def _menu_tabela(self, event):
        """
        -> Menu ao Clicar com o Mouse (Botão Direito)
        :param event: Evento que e Gerdado do Click
        :return: None
        """
        self.clickdireito = event
        try:
            self.tabela_m.tk_popup(event.x_root, event.y_root)
        except IndexError:
            pass
        finally:
            self.tabela_m.grab_release()

    # Tabela Duplo Click para altera dados
    def _tabela_click(self, event=None):
        """
        -> Pegar dados aoa Duplo Click em Linha da Tabela
        :return: None
        """
        self._clear_entry()
        item = self.tabela.selection()[0]
        itens = self.tabela.item(item, 'values')

        self.id['text'] = itens[0]
        self.nome.insert(0, itens[1])
        self.site.insert(0, itens[2])
        self.usuario.insert(0, itens[3])
        self.senha.insert(0, itens[4])

    # Validar Usuario para Login
    def valida(self, event=None):
        user = self.user.get()
        pswd = self.pswd.get()
        try:
            status, db_user = self.gsenha.user_valid(user=user, pasw=pswd)
            if status:
                self.login_janela.destroy()
                # Acessando o banco de dados
                self.gcode = self.gsenha.gcode
                self.gsenha = GSenha(f"{db_user}.db")
                self.interface()
            else:
                messagebox.showinfo("GSenha Login", "Usuário ou Senha Invalido")
        except KeyboardInterrupt:
            sys.exit()
