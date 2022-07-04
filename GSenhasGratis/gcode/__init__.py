

class GCode:
    def __init__(self):
        # Variaveis de Configuração
        self.config = {"tema": "scidblue", "status_visible": 0, "altentic": 0}
        self.keys = None

    # Salvar as Chaves
    def key_save(self):
        """
        -> Salvar as Chaves
        :return: None
        """
        return "123456"

    def key_load(self, keys):
        """
        -> Carregar as Senhas na Memoria
        :param keys: cahves para descriptogrfar
        :return: None
        """
        self.keys = keys

    def crip(self, texto, keys):
        """
        -> Descriptografar
        key: Chave gerada pela função key_save
        texto: Texto(str) que sera criptografado
        return: Conteúdo Criptografado
        """
        return texto

    def desc(self, crip, keys):
        """
        -> Descriptografar
        key: Chave gerada pela função key_save
        crip: Conteúdo Criptografado
        return: conteúdo descriptogrfado
        """
        return crip

    def valid(self, valor1, valor2):
        """
        -> Validar um Senha
        valor1: Conteúdo para comparação
        valor2: Conteúdo para comparação
        return: True/false
        """
        if valor1 == valor2:
            return True
        else:
            return False

    @staticmethod
    def reconver_cod():
        return "new123"