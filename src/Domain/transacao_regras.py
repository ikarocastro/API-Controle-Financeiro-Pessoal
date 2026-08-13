def validar_error(valor):
    if (valor < 0):
        raise ValueError("O numero digitado não é aceito por ser negativo!")
   