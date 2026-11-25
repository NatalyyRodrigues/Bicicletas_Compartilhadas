"""Hierarquia de bicicletas: Bicicleta (abstrata) -> Comum, Eletrica, Cargueira."""

from abc import ABC, abstractmethod

from app.models.excecoes import ConflitoError, DadoInvalidoError


class Bicicleta(ABC):
    """Classe abstrata: define o que toda bicicleta precisa ter e saber fazer."""

    TIPO = "abstrata"  # cada filha sobrescreve; usado no filtro ?tipo= e na criação

    def __init__(self, identificador: int):
        self._identificador = None
        self._em_uso = False
        self.identificador = identificador  # passa pela validação do setter

    # ---------- encapsulamento ----------
    @property
    def identificador(self) -> int:
        return self._identificador

    @identificador.setter
    def identificador(self, valor: int) -> None:
        if isinstance(valor, bool) or not isinstance(valor, int) or valor <= 0:
            raise DadoInvalidoError("O identificador da bicicleta deve ser um inteiro positivo.")
        self._identificador = valor

    @property
    def em_uso(self) -> bool:
        return self._em_uso

    @property
    def status(self) -> str:
        return "em_uso" if self._em_uso else "disponivel"

    # ---------- polimorfismo ----------
    @abstractmethod
    def tarifa(self, minutos: int) -> float:
        """Valor a cobrar por uma viagem de `minutos` minutos. Cada tipo calcula do seu jeito."""

    # ---------- regras de uso ----------
    def iniciar_uso(self) -> None:
        """Marca a bicicleta como em uso, se as regras permitirem (método-modelo)."""
        self._validar_saida()
        self._em_uso = True

    def liberar(self) -> None:
        """Devolve a bicicleta (fim da viagem)."""
        self._em_uso = False

    def validar_remocao(self) -> None:
        """RN: bicicleta em uso não pode ser retirada do sistema."""
        if self._em_uso:
            raise ConflitoError(f"A bicicleta {self._identificador} está em uso e não pode ser retirada.")

    def _validar_saida(self) -> None:
        """Condições para a bicicleta sair para uma viagem. As filhas podem estender."""
        if self._em_uso:
            raise ConflitoError(f"A bicicleta {self._identificador} já está em uso.")

    @staticmethod
    def validar_minutos(minutos: int) -> None:
        if isinstance(minutos, bool) or not isinstance(minutos, int) or minutos <= 0:
            raise DadoInvalidoError("Os minutos da viagem devem ser um inteiro maior que zero.")


class Comum(Bicicleta):
    """Bicicleta comum: cobra apenas por minuto."""

    TIPO = "comum"
    VALOR_MINUTO = 0.50  # RN: R$ 0,50 por minuto

    def __init__(self, identificador: int):
        super().__init__(identificador)

    def tarifa(self, minutos: int) -> float:
        self.validar_minutos(minutos)
        return round(minutos * self.VALOR_MINUTO, 2)


class Cargueira(Bicicleta):
    """Bicicleta cargueira: cobra apenas por minuto, em valor maior que a comum."""

    TIPO = "cargueira"
    VALOR_MINUTO = 0.80  # RN: R$ 0,80 por minuto

    def __init__(self, identificador: int):
        super().__init__(identificador)

    def tarifa(self, minutos: int) -> float:
        self.validar_minutos(minutos)
        return round(minutos * self.VALOR_MINUTO, 2)


class Eletrica(Bicicleta):
    """Bicicleta elétrica: tem bateria, cobra por minuto + taxa de desbloqueio."""

    TIPO = "eletrica"
    VALOR_MINUTO = 1.00      # RN: R$ 1,00 por minuto
    TAXA_DESBLOQUEIO = 3.00  # RN: R$ 3,00 por viagem
    BATERIA_MINIMA = 20      # RN: só sai com bateria ACIMA de 20%

    def __init__(self, identificador: int, bateria: int = 100):
        super().__init__(identificador)
        self._bateria = None
        self.bateria = bateria  # passa pela validação do setter

    @property
    def bateria(self) -> int:
        return self._bateria

    @bateria.setter
    def bateria(self, valor: int) -> None:
        if isinstance(valor, bool) or not isinstance(valor, int) or not 0 <= valor <= 100:
            raise DadoInvalidoError("A bateria deve ser um inteiro entre 0 e 100.")
        self._bateria = valor

    def tarifa(self, minutos: int) -> float:
        self.validar_minutos(minutos)
        return round(minutos * self.VALOR_MINUTO + self.TAXA_DESBLOQUEIO, 2)

    def _validar_saida(self) -> None:
        super()._validar_saida()  # primeiro a regra comum: não pode estar em uso
        if self._bateria <= self.BATERIA_MINIMA:
            raise DadoInvalidoError(
                f"Bateria em {self._bateria}%: a elétrica só sai com bateria acima de {self.BATERIA_MINIMA}%."
            )
