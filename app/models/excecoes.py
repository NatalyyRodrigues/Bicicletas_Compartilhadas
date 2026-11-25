"""Exceções de negócio do sistema.

Os models lançam estas exceções; as rotas (Integrante 3) as traduzem em HTTP:
    NaoEncontradoError -> 404
    ConflitoError      -> 409
    DadoInvalidoError  -> 422
"""


class ErroNegocio(Exception):
    """Base de todas as exceções de regra de negócio."""

    def __init__(self, mensagem: str):
        super().__init__(mensagem)
        self.mensagem = mensagem


class NaoEncontradoError(ErroNegocio):
    """Entidade inexistente (bicicleta, usuário ou viagem). HTTP 404."""


class ConflitoError(ErroNegocio):
    """Operação em conflito com o estado atual (ex.: bicicleta em uso). HTTP 409."""


class DadoInvalidoError(ErroNegocio):
    """Dado que viola uma regra (ex.: bateria <= 20%, minutos <= 0). HTTP 422."""
