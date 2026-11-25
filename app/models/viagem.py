"""Viagem: composição de uma Bicicleta e um Usuario."""

from app.models.bicicleta import Bicicleta
from app.models.excecoes import ConflitoError, DadoInvalidoError
from app.models.usuario import Usuario


class Viagem:
    def __init__(self, identificador: int, bicicleta: Bicicleta, usuario: Usuario):
        if isinstance(identificador, bool) or not isinstance(identificador, int) or identificador <= 0:
            raise DadoInvalidoError("O identificador da viagem deve ser um inteiro positivo.")
        self._identificador = identificador
        self._bicicleta = bicicleta   # composição: a viagem guarda os objetos
        self._usuario = usuario
        self._minutos = None
        self._finalizada = False

    @property
    def identificador(self) -> int:
        return self._identificador

    @property
    def bicicleta(self) -> Bicicleta:
        return self._bicicleta

    @property
    def usuario(self) -> Usuario:
        return self._usuario

    @property
    def minutos(self):
        return self._minutos

    @property
    def finalizada(self) -> bool:
        return self._finalizada

    def iniciar(self) -> None:
        """Inicia a viagem. A bicicleta decide se pode sair (em uso -> 409; bateria baixa -> 422)."""
        self._bicicleta.iniciar_uso()

    def finalizar(self, minutos: int) -> None:
        """Registra a duração e libera a bicicleta."""
        if self._finalizada:
            raise ConflitoError(f"A viagem {self._identificador} já foi finalizada.")
        Bicicleta.validar_minutos(minutos)
        self._minutos = minutos
        self._finalizada = True
        self._bicicleta.liberar()

    def calcular_valor(self) -> float:
        """Valor da viagem. Polimorfismo: quem sabe calcular é a bicicleta, sem if por tipo."""
        if not self._finalizada:
            raise ConflitoError("A viagem ainda não foi finalizada; não há valor a calcular.")
        return self._bicicleta.tarifa(self._minutos)
