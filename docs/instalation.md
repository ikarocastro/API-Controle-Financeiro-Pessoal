# Processo de intalacão 

1. Instalar o python3
2. Recriar o (venv)
- ``Para recriar``:

```
python3 -m venv venv
```

- ``Para ativar``:

- No Mac é diferente 
- No Mac/Linux, é assim ``(não é .ps1, é .sh, e usa source)``:
````
source venv/bin/activate
````

3. Instalar as dependências — de uma vez, usando o ``requirements.txt``

```
pip install -r requirements.txt
```

- Aqui está a vantagem de ter versionado esse arquivo: em vez de instalar ``psycopg2-binary`` e ``python-dotenv`` um por um manualmente, você roda um único comando:

4. Instalar o FastAPI

```
python3 -m pip install fastapi
```

- O `FastAPI`, sozinho, só define como construir a API — mas pra ela realmente `"rodar"` e `"escutar"` requisições, você precisa de um servidor por baixo. O mais comum, e que a documentação oficial do FastAPI recomenda, é o `uvicorn.` Instala ele também:

```
python3 -m pip install "uvicorn[standard]"
```

- e não esquecer do freeze para salvar a dependência

```
python3 -m pip freeze > requirements.txt
```

