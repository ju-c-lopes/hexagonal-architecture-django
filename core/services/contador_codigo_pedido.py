from datetime import date, datetime, time, timedelta


class ContadorDiario:
    contador = 0

    def __init__(self, fim_expediente: time = time(6, 0)):
        self.fim_expediente = fim_expediente
        self.data_atual = self._dia_referencia()

    def _dia_referencia(self) -> date:
        """
        Retorna a data de referência para o contador com base no fim do expediente.
        Se o horário atual for antes do fim do expediente, usa o dia anterior como referência.
        """
        agora = datetime.now()
        if agora.time() < self.fim_expediente:
            return (agora - timedelta(days=1)).date()
        return agora.date()

    def obter_proximo(self) -> int:
        """
        Incrementa e retorna o próximo número do contador.
        Reseta o contador se a data de referência mudou.
        """
        dia_referencia = self._dia_referencia()
        if self.data_atual != dia_referencia:
            self.data_atual = dia_referencia
            ContadorDiario.contador = 0
        ContadorDiario.contador += 1
        return ContadorDiario.contador
