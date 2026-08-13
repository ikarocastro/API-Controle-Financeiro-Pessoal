from dataclasses import dataclass
from enum import Enum
from datetime import date

class TipoTransacao(Enum):
    ENTRADA = "Entrada"
    SAIDA = "saida"

@dataclass
class Transacao:
    id: int
    valor: float
    descricao: str
    categoria: str
    data: date
    tipo: TipoTransacao