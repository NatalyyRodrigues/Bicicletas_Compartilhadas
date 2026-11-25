"""Usuário do sistema de bicicletas compartilhadas."""

from app.models.excecoes import DadoInvalidoError


class Usuario:
    def __init__(self, identificador: int, nome: str):
        self._identificador = None
        self._nome = None
        self.identificador = identificador  # passam pelos setters (validação)
        self.nome = nome

    @property
    def identificador(self) -> int:
        return self._identificador

    @identificador.setter
    def identificador(self, valor: int) -> None:
        if isinstance(valor, bool) or not isinstance(valor, int) or valor <= 0:
            raise DadoInvalidoError("O identificador do usuário deve ser um inteiro positivo.")
        self._identificador = valor

    @property
    def nome(self) -> str:
        return self._nome

    @nome.setter
    def nome(self, valor: str) -> None:
        if not isinstance(valor, str) or len(valor.strip()) < 2:
            raise DadoInvalidoError("O nome do usuário deve ter pelo menos 2 caracteres.")
        self._nome = valor.strip()
