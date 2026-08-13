from dataclasses import dataclass

@dataclass
class Conta:
    id: int
    nome: str
        
Conta1 = Conta(id=1, nome="ikaro")