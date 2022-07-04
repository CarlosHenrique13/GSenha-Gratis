import os
import sqlite3

from GSenhasGratis.gcode import GCode


class GSenha:
    def __init__(self, con=''):
        self.gcode = GCode()
        self.gsenha_con = sqlite3.connect('GSenha.db')
        self.gsenha_cur = self.gsenha_con.cursor()
        self._new_table()

        self.diretoria_usuario = self.gcode.crip('users', self.gcode.keys)
        if not os.path.isdir(self.diretoria_usuario):
            os.makedirs(self.diretoria_usuario)

        if con != '':
            # Dados do Usuário
            self.con = sqlite3.connect(f'./{self.diretoria_usuario}/{con}')
            self.cur = self.con.cursor()

            self.new_table()

    # Criar tebale de Registro de Usuários
    def _new_table(self):
        try:
            self.gsenha_cur.execute('''CREATE TABLE IF NOT EXISTS users
                              (id INTEGER PRIMARY KEY ,name blob UNIQUE, email blob UNIQUE UNIQUE,
                               pasword blob, cod_rec blob, keys blob )''')
            return True
        except sqlite3.OperationalError:
            return False

    # Criar tebale de senhas
    def new_table(self):
        try:
            self.cur.execute('''CREATE TABLE IF NOT EXISTS paswords
                           (id INTEGER PRIMARY KEY ,name blob, site blob, user blob, psword blob )''')
            return True
        except sqlite3.OperationalError:
            return False

    # Cadastra uma nova senha
    def new_senha(self, nome: str, site: str, usuario: str, senha: str, keys: dict):
        try:
            self.cur.execute(
                f'INSERT INTO paswords (name,site,user,psword) VALUES ("{nome}",?,?,?)',
                (self.gcode.crip(site, keys), self.gcode.crip(usuario, keys),
                 self.gcode.crip(senha, keys)))
            self.con.commit()
            return True
        except sqlite3.OperationalError:
            self.new_table()
            self.cur.execute(
                f'INSERT INTO paswords (name,site,user,psword) VALUES ("{nome}",?,?,?)',
                (self.gcode.crip(site, keys), self.gcode.crip(usuario, keys),
                 self.gcode.crip(senha, keys)))
            self.con.commit()
            return True

    # Apagar registro de Senha
    def delete(self, idd=0):
        self.cur.execute(f"DELETE from paswords where id={idd}")
        self.con.commit()

    # Listar senhas
    def listar(self, retrono=False):
        if retrono:
            return self.cur.execute('SELECT * FROM paswords ')
        print(" §\033[1;34mListando Senhas\033[m:")
        try:
            for row in self.cur.execute('SELECT * FROM paswords '):
                print(
                    f"   - \033[1;35mId\033[m: \033[1;36m{row[0]}\033[m, \033[1;"
                    f"35mNome\033[m: \033[92m {row[1]} \033[m, "
                    f"\033[1;35mSite\033[m: \033[92m{self.gcode.desc(row[2], self.gcode.keys)}\033[m, \033[1;"
                    f"35mUsuario\033[m: \033[92m{self.gcode.desc(row[3], self.gcode.keys)}\033[m, "
                    f"\033[1;35mSenha\033[m: \033[92m{self.gcode.desc(row[4], self.gcode.keys)}\033[m")
        except sqlite3.OperationalError:
            self.new_table()

    # Atualizar Informação
    def update(self, idd: int, nome: str, usuario: str, senha: str, site: str):
        """
        -> Atualizar Informação de Senha
        :param idd: Identificador
        :param nome: Novo Nome
        :param usuario: Novo Nome de Usuairo
        :param senha: Nova Senha
        :param site: Url do site de onde e a senha
        :return: True/False
        """
        self.cur.execute(f'UPDATE paswords SET name="{nome}",site=?,user=?,psword=? WHERE id="{idd}"',
                         (self.gcode.crip(site, self.gcode.keys), self.gcode.crip(usuario, self.gcode.keys),
                          self.gcode.crip(senha, self.gcode.keys)))
        self.con.commit()
        return True

    # Cadastra Novo Usuario
    def new_user(self, nome: str, email: str, senha: str):
        """
        -> Cadastra um Novo Usuário
        :param email: Email do usuário
        :param nome: Nome do usuário
        :param senha: Senha do Usuário
        :return: None
        """
        try:
            if nome != '' and senha != '' and '@' in email:
                self.gsenha_cur.execute(
                    f'INSERT INTO users (name,email,pasword,cod_rec,keys) VALUES ("{nome}",?,?,?,?)',
                    [self.gcode.crip(email, self.gcode.keys), self.gcode.crip(senha, self.gcode.keys),
                     self.gcode.reconver_cod(), self.gcode.key_save()])
                self.gsenha_con.commit()
                return True
            else:
                return False
        except sqlite3.IntegrityError:
            return False

    # Deletar o Usuário:
    def del_user(self, name):
        self.gsenha_cur.execute(f'DELETE from users where nome="{name}"')
        self.gsenha_con.commit()
        try:
            os.remove(f'./{self.diretoria_usuario}/{self.gcode.crip(self.user, self.gcode.keys)}.db')
        except FileNotFoundError:
            print('\033[91m ARQUIVO DE USUÁRIO NÃO LOCALIZADO')

    # Validar Usuario
    def user_valid(self, user: str, pasw: str):
        """
        -> Validar Credencia de Usaurio
        :param user: Nome de Usuario ou E-mail
        :param pasw: Senha do Usuario
        :return: True/False
        """
        dados = None
        # Logar via E-mail
        if '@' in user:
            user = self.gcode.crip(user, self.gcode.keys)
            for user_dados in self.gsenha_cur.execute(f'SELECT * FROM users WHERE email="{user}" '):
                dados = user_dados
            if (user == dados[2]) and self.gcode.valid(dados[3], self.gcode.crip(pasw, self.gcode.keys)):
                self.gcode.key_load(dados[5])
                return True, self.gcode.desc(self.gcode.crip(dados[1], self.gcode.keys), self.gcode.keys)
            else:
                return False, False
        # Logar via Nome de usuario
        else:
            for user_dados in self.gsenha_cur.execute(f'SELECT * FROM users WHERE name="{user}" '):
                dados = user_dados
            try:
                if (user == dados[1]) and self.gcode.valid(dados[3], self.gcode.crip(pasw, self.gcode.keys)):
                    self.gcode.key_load(dados[5])
                    return True, self.gcode.desc(self.gcode.crip(dados[1], self.gcode.keys), self.gcode.keys)
                else:
                    return False, False
            except TypeError:
                return False, False

    # Altera a Senha do Usuario
    def user_new_pswd(self, user: str, pswd: str, chave: str):
        """
        -> Altera a senha do Usuário casso ele esqueça
        :param user: Nome de Usuário ou Email
        :param pswd: Nova senha do Usuário
        :param chave: Chave que Valida que o usuário e o usuário
        :return: True/False
        """

        dados = None
        # Logar via E-mail
        if '@' in user:
            user = self.gcode.crip(user, self.gcode.keys)
            for user_dados in self.gsenha_cur.execute(f'SELECT * FROM users WHERE email=? ', [user]):
                dados = user_dados
            if (user == dados[2]) and (dados[4] == chave):
                pswd = self.gcode.crip(pswd, self.gcode.keys)
                recover = self.gcode.reconver_cod()
                self.gsenha_cur.execute(
                        f'UPDATE users SET pasword=?, cod_rec=? WHERE id="{dados[0]}"',
                        (pswd, recover))
                self.gsenha_con.commit()
                return True, recover
            else:
                return False, False
        # Logar via Nome de usuario
        else:
            for user_dados in self.gsenha_cur.execute(f'SELECT * FROM users WHERE name="{user}" '):
                dados = user_dados
            if (user == dados[1]) and (dados[4] == chave):
                pswd = self.gcode.crip(pswd, self.gcode.keys)
                recover = self.gcode.reconver_cod()
                self.gsenha_cur.execute(
                    f'UPDATE users SET pasword=?, cod_rec=? WHERE id="{dados[0]}"',
                    (pswd, recover))
                self.gsenha_con.commit()
                return True, recover
            else:
                return False, False

    # Buscar senhas
    def buscar(self, nome: str, retrono=False):
        if retrono:
            return self.cur.execute(f'SELECT * FROM paswords WHERE name LIKE "%{nome}%" ')
        print(" §\033[1;34mResultado da Busca\033[m: ")
        for row in self.cur.execute(f'SELECT * FROM paswords WHERE name LIKE "%{nome}%" '):
            print(
                f"   - \033[1;35mNome\033[m: \033[92m{row[1]}\033[m,"
                f" \033[1;35mSite\033[m: \033[92m{self.gcode.desc(row[2], self.gcode.keys)}\033[m, "
                f"\033[1;35mUsuario\033[m: \033[92m{self.gcode.desc(row[3], self.gcode.keys)}\033[m,"
                f" \033[1;35mSenha\033[m: \033[92m{self.gcode.desc(row[4], self.gcode.keys)}\033[m")

    # Menu Texto
    @staticmethod
    def _menu():
        print(f""" \033[1;97m {'='*5} \033[1;92mMENU\033[m {'='*5} \033[m
    [\033[1;93mhelp\033[m] \033[1;37mAbrir o Menu \033[m
    [\033[1;93mnew-user \033[m] \033[1;37mCriar um novo usuário \033[m
    [\033[1;93mcls\033[m]  \033[1;37mLimpar o Terminal \033[m
    [\033[1;93mlogin\033[m] \033[1;37mTrocar de Usuário \033[m
    [\033[1;93mdel-user\033[m] \033[1;37mExcluir a conta de um usuário \033[m

    [\033[1;93mnew\033[m]  \033[1;37mCadastra uma nova senha \033[m
    [\033[1;93mlist\033[m] \033[1;37mListar as senhas \033[m
    [\033[1;93mbusc <nome> \033[m] \033[1;37mBuscar por uma senha pelo nome \033[m
    [\033[1;93mdel <id> \033[m] \033[1;37mDeletar Senha pelo id da linha \033[m
    [\033[1;93mdel-my\033[m] \033[1;37mApagar minhan conta e meus dados \033[m
    [\033[1;93mupdate <id> \033[m] \033[1;37mAtualizar iformação da linha pelo id \033[m
    [\033[1;91mclose\033[m] \033[1;37mFinalizar o Programa \033[m
    """)

    def _interface_login(self):
        print("\033[1;36m=\033[1;35m-\033[1;36m=\033[m"*5,
              "\033[1;92mGSenha Terminal\033[m",
              "\033[1;36m=\033[1;35m-\033[1;36m=\033[m"*5)
        try:
            self.user = str(input("\033[1;32mNome de Usuário\033[1;97m:\033[m\033[93m "))
            senha = str(input("\033[1;32mSenha\033[1;97m:\033[m\033[93m "))
            status, db_name = self.user_valid(self.user, senha)
            if status:
                self.con = sqlite3.connect(f'./{self.diretoria_usuario}/{db_name }.db')
                self.cur = self.con.cursor()
                return True
            else:
                return False
        except KeyboardInterrupt:
            return False

    def interface(self):
        if self._interface_login():
            self._menu()
            while True:
                try:
                    resp = str(input("\033[1;32mGSenhas\033[1;97m>>\033[m\033[93m ")).split(" ")

                    # Listando Menu
                    if resp[0] == 'help':
                        self._menu()

                    # Criar um Novo Usuário
                    elif resp[0] == 'new-user':
                        estatus = self.new_user(nome=str(input("\033[1;35mNome\033[m:\033[93m")),
                                                email=str(input("\033[1;35mEmail\033[m:\033[93m")),
                                                senha=str(input("\033[1;35mSenha\033[m:\033[93m")))
                        os.system("clear")
                        if estatus:
                            print("\033[1;94mUsuário Cadastrado com Sucesso.\033[m")
                        else:
                            print("\033[1;91mUsuário Não Cadastrado ja Existente ou Dados Invalidos.\033[m")
                    # Finalizar o Programa
                    elif resp[0] == 'close':
                        break

                    # Limpar o Terminal windows(cls) Linux(clear)
                    elif resp[0] == "cls":
                        os.system("clear")

                    # trocar de usuario
                    elif resp[0] == "login":
                        self.interface()
                        break

                    # Novo cadastro de senha
                    elif resp[0] == "new":
                        try:
                            nome = str(input("\033[1;35mNome\033[m: \033[93m"))
                            usuario = str(input("\033[1;35mUsuario\033[m: \033[93m"))
                            site = str(input("\033[1;35mSite\033[m: \033[93m"))
                            senha = str(input("\033[1;35mSenha\033[m: \033[93m"))
                            self.new_senha(nome=nome, usuario=usuario, site=site, senha=senha, keys=self.gcode.keys)
                        except KeyboardInterrupt:
                            pass

                    # Listar todas as senhas
                    elif resp[0] == "list":
                        self.listar()

                    # Deletar Minha Conta
                    elif resp[0] == "del-my":
                        self.del_user(name=self.user)
                        break

                    # Deletar Usuário
                    elif f"{resp[0]} {resp[1]}" == f"del-user {resp[1]}":
                        self.del_user(name=resp[1])

                    # Buscar por senha espesifica
                    elif f"{resp[0]} {resp[1]}" == f"busc {resp[1]}":
                        self.buscar(nome=resp[1])

                    # Deletar Senha pelo ID da linha
                    elif f"{resp[0]} {resp[1]}" == f"del {resp[1]}":
                        self.delete(idd=int(resp[1]))

                    # Atualizar os dados de uma linha
                    elif f"{resp[0]} {resp[1]}" == f"update {resp[1]}":
                        nome = str(input("\033[1;35mNome\033[m:\033[93m"))
                        estatus = self.update(idd=int(resp[1]),
                                              nome=nome,
                                              usuario=str(input("\033[1;35mUsuário\033[m:\033[93m")),
                                              senha=str(input("\033[1;35mSenha\033[m:\033[93m")),
                                              site=str(input("\033[1;35mSite\033[m:\033[93m")))
                        os.system("clear")
                        if estatus:
                            print(f"\033[1;94mDados Atualizados ID: \033[1;97m{resp[1]}\033[m")
                        else:
                            print(f"\033[1;91mFalha ao Atualizar os Dados do ID:\033[1;97 {resp[1]}.\033[m")
                except IndexError:
                    # Comando Invalido
                    print("\033[91mComando Invalido!\033[m")
                except KeyboardInterrupt:
                    break
        else:
            print("\033[91mUsuário ou Senha Invalidos!!\033[m")

        print("\033[97mFinalizado.")
