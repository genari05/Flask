# Usa uma imagem oficial do Python como base
FROM python:3.10

# Define o diretório de trabalho dentro do container
WORKDIR /App

# Copia os arquivos do projeto para dentro do container
COPY . /App

# Instala as dependências do projeto
RUN pip install --no-cache-dir -r requirements.txt

# Expõe a porta que o Flask vai rodar
EXPOSE 5000

# Comando para rodar a aplicação Flask
CMD ["python", "App/app.py"]
