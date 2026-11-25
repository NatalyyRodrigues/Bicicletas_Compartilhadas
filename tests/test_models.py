"""Testes das regras de negócio em app/models (sem HTTP, sem arquivo JSON)."""

import pytest

from app.models import (
    Bicicleta,
    Cargueira,
    Comum,
    ConflitoError,
    DadoInvalidoError,
    Eletrica,
    ErroNegocio,
    NaoEncontradoError,
    Usuario,
    Viagem,
)


# ---------- requisito 1: classe abstrata ----------
def test_bicicleta_abstrata_nao_pode_ser_instanciada():
    with pytest.raises(TypeError):
        Bicicleta(1)


# ---------- requisito 2: herança ----------
@pytest.mark.parametrize("classe", [Comum, Eletrica, Cargueira])
def test_filhas_herdam_de_bicicleta(classe):
    bike = classe(1)
    assert isinstance(bike, Bicicleta)
    assert bike.identificador == 1
    assert bike.status == "disponivel"


# ---------- requisito 3: polimorfismo da tarifa ----------
def test_tarifa_comum_e_cargueira_por_minuto():
    assert Comum(1).tarifa(10) == 5.00
    assert Cargueira(2).tarifa(10) == 8.00


def test_tarifa_eletrica_inclui_taxa_de_desbloqueio():
    assert Eletrica(1, bateria=80).tarifa(10) == 13.00  # 10 x 1,00 + 3,00


def test_valor_da_viagem_usa_tarifa_polimorfica_sem_if_por_tipo():
    usuario = Usuario(1, "Ana")
    esperado = {Comum: 5.00, Cargueira: 8.00, Eletrica: 13.00}
    for classe, valor in esperado.items():
        viagem = Viagem(1, classe(1), usuario)
        viagem.iniciar()
        viagem.finalizar(10)
        assert viagem.calcular_valor() == valor


# ---------- regra do tema: bicicleta em uso ----------
def test_bicicleta_em_uso_nao_inicia_outra_viagem():
    bike = Comum(1)
    usuario = Usuario(1, "Ana")
    Viagem(1, bike, usuario).iniciar()
    with pytest.raises(ConflitoError):
        Viagem(2, bike, usuario).iniciar()


def test_bicicleta_em_uso_nao_pode_ser_retirada():
    bike = Comum(1)
    bike.iniciar_uso()
    with pytest.raises(ConflitoError):
        bike.validar_remocao()


def test_bicicleta_liberada_pode_ser_retirada():
    bike = Comum(1)
    bike.iniciar_uso()
    bike.liberar()
    bike.validar_remocao()  # não lança
    assert bike.status == "disponivel"


# ---------- regra do tema: bateria da elétrica ----------
@pytest.mark.parametrize("bateria", [0, 15, 20])
def test_eletrica_com_bateria_ate_20_nao_sai(bateria):
    bike = Eletrica(1, bateria=bateria)
    with pytest.raises(DadoInvalidoError):
        bike.iniciar_uso()
    assert bike.em_uso is False


def test_eletrica_com_bateria_acima_de_20_sai():
    bike = Eletrica(1, bateria=21)
    bike.iniciar_uso()
    assert bike.em_uso is True


# ---------- requisito 4: encapsulamento e validação ----------
def test_bateria_fora_de_0_a_100_e_invalida():
    with pytest.raises(DadoInvalidoError):
        Eletrica(1, bateria=101)
    with pytest.raises(DadoInvalidoError):
        Eletrica(1, bateria=-1)


def test_identificador_invalido():
    with pytest.raises(DadoInvalidoError):
        Comum(0)
    with pytest.raises(DadoInvalidoError):
        Comum("abc")


def test_em_uso_nao_pode_ser_alterado_de_fora():
    bike = Comum(1)
    with pytest.raises(AttributeError):
        bike.em_uso = True


def test_usuario_valida_nome_e_identificador():
    assert Usuario(1, "  Ana  ").nome == "Ana"
    with pytest.raises(DadoInvalidoError):
        Usuario(1, " ")
    with pytest.raises(DadoInvalidoError):
        Usuario(-5, "Ana")


# ---------- minutos e ciclo da viagem ----------
@pytest.mark.parametrize("minutos", [0, -3, 2.5, "10"])
def test_minutos_invalidos(minutos):
    with pytest.raises(DadoInvalidoError):
        Comum(1).tarifa(minutos)


def test_finalizar_libera_bicicleta_e_registra_minutos():
    bike = Comum(1)
    viagem = Viagem(1, bike, Usuario(1, "Ana"))
    viagem.iniciar()
    assert bike.em_uso is True
    viagem.finalizar(30)
    assert bike.em_uso is False
    assert viagem.minutos == 30 and viagem.finalizada is True


def test_nao_calcula_valor_de_viagem_nao_finalizada():
    viagem = Viagem(1, Comum(1), Usuario(1, "Ana"))
    viagem.iniciar()
    with pytest.raises(ConflitoError):
        viagem.calcular_valor()


def test_nao_finaliza_duas_vezes():
    viagem = Viagem(1, Comum(1), Usuario(1, "Ana"))
    viagem.iniciar()
    viagem.finalizar(5)
    with pytest.raises(ConflitoError):
        viagem.finalizar(5)


# ---------- requisito 6: hierarquia de exceções ----------
@pytest.mark.parametrize("filha", [NaoEncontradoError, ConflitoError, DadoInvalidoError])
def test_excecoes_filhas_herdam_de_erro_negocio(filha):
    assert issubclass(filha, ErroNegocio)
    assert filha("msg").mensagem == "msg"
