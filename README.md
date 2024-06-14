# TCC-RaspClient

**TCC-RaspClient** é um projeto baseado em Python projetado para rodar em um Raspberry Pi, servindo como um cliente para um sistema maior de controle universal de dispositivos IoT.

## Objetivos

- **Desenvolver um dispositivo central de controle que integre diversos dispositivos IoT.**
- **Criar um repositório online para compartilhamento de comandos e dispositivos.**
- **Implementar suporte para múltiplos protocolos de comunicação IoT.**
- **Testar e validar a integração com dispositivos de marcas diferentes.**

## Recursos

- **Comunicação:** Envio de dados processados para um servidor central.
- **Interface Web:** Interface web para monitoramento e controle.

## Instalação

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

## Contato
Para qualquer dúvida ou problema, por favor, abra uma issue no GitHub.
