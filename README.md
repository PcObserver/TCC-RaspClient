# Projeto Elegos
![Imagem do Projeto](https://github.com/PcObserver/assets/blob/main/elegos_image.png)

Com o rápido avanço da tecnologia, a quantidade de dispositivos IoT vem crescendo exponencialmente. Diversos sistemas oferecem soluções para operar esses dispositivos, mas a maioria deles dá suporte apenas aos da própria marca, criando dificuldades em construir ecossistemas IoT com controle unificado. O projeto “Elegos” consiste de um controle universal de dispositivos IoT que visa unificar o gerenciamento desses dispositivos em uma única plataforma.

Utilizando um hub baseado em Raspberry Pi 3 modelo B, o sistema detecta automaticamente dispositivos na rede local e permite o envio de comandos, mesmo sem conexão com a internet. Além disso, um repositório online de comandos permite a adição e o compartilhamento de novos dispositivos de forma colaborativa, permitindo a inclusão de novos dispositivos e comandos, bem como avaliação das contribuições criadas pelos usuários pela própria comunidade utilizando um sistema de avaliação por votos positivos.

## Repositórios Associados
- [Back-end da Comunidade de Dispositivos IoT](https://github.com/PcObserver/iot-commands-hub)
- [Front-end da Comunidade de Dispositivos IoT](https://github.com/PcObserver/TCC-iot-hub)
- [Sistema do Raspberry Pi](https://github.com/PcObserver/TCC-RaspClient)

## Objetivo

O objetivo deste repositório é entregar um projeto baseado em Python projetado para rodar em um Raspberry Pi, servindo como um cliente para um sistema maior de controle universal de dispositivos IoT. O Raspberry Pi será usado no projeto, juntamente com a implementação do software desenvolvido neste repositório, como uma central de controle que integre diversos dispositivos IoT por meio de uma interface web para monitoramente e controle dos dispositivos configurados.

## Tecnologias Utilizadas

- Python 3.7
- Flask 3.0.3
- SQLite
- SQL Alchemy

## Configuração do Projeto

### Pré-requisitos

- Python 3.7 ou superior
- Raspberry Pi com Raspbian OS

### Passos

1. **Clone o Repositório**
    ```bash
    git clone https://github.com/PcObserver/TCC-RaspClient.git
    cd TCC-RaspClient
    ```

2. **Crie e Ative um Ambiente Virtual**
    ```bash
    python -m venv venv
    source venv/bin/activate
    ```

3. **Instale as Dependências**
    ```bash
    pip install -r requirements.txt
    ```

## Configuração do Banco de Dados
### Inicialize o Banco de Dados
```
flask --app application db init
```
### Aplique as Migrações
```
flask --app application db migrate -m "Initial migration."
```
## Executando o Servidor
Inicie o servidor Flask com o seguinte comando:
```
flask --app application run
```

### Executando como um Serviço
Para rodar o TCC-RaspClient como um serviço no Raspberry Pi, siga estes passos:

### Crie um Arquivo de Serviço Systemd
 ```
sudo nano /etc/systemd/system/tcc-raspclient.service
 ```
### Adicione o seguinte conteúdo ao arquivo:

 ```
[Unit]
Description=TCC-RaspClient Service
After=network.target

[Service]
User=pi
WorkingDirectory=/home/pi/TCC-RaspClient
Environment="PATH=/home/pi/TCC-RaspClient/venv/bin"
ExecStart=/home/pi/TCC-RaspClient/venv/bin/flask --app application run --host=0.0.0.0

[Install]
WantedBy=multi-user.target
 ```

### Recarregue o Systemd e Inicie o Serviço

 ```
sudo systemctl daemon-reload
sudo systemctl start tcc-raspclient.service
sudo systemctl enable tcc-raspclient.service
 ```

### Verifique o Status do Serviço

 ```
sudo systemctl status tcc-raspclient.service
 ```
## Estrutura do projeto
* api/: Contém wrappers de API para endpoints remotos.
* data/: Armazena arquivos de dados SQLite.
* migrations/: Scripts de migração de banco de dados.
* models/: Modelos de banco de dados.
* static/: Arquivos estáticos (CSS, JS, imagens).
* templates/: Templates HTML.
* utils/: Funções utilitárias.
* views/: Funções de visualização para a interface web.

