## Como utilizar a solução desenvolvida

A solução desenvolvida está disponível no formato de imagem Docker no repositório do projeto no Docker Hub. Então para a utilização dos programas é necessário ter o Docker instalado no dispositivo no qual o programa será executado.

### 1º etapa - Baixando a imagem Docker

Primeiramente é preciso baixar a imagem disponível no repositório nas respectivas máquinas que serão utilizadas, para isso basta abrir o terminal e executar o comando abaixo nas máquinas que serão utilizadas.

```bash
docker pull lfrcintra/clock:latest
```

### 2º etapa - Executando a imagem baixada

Com a imagem *bank* baixada em cada uma das máquinas é possível instanciar cada um dos bancos através do Docker. Para isso basta executar cada um dos comandos abaixo em uma máquina diferente.

**Obs:** Nos argumentos *host*, *clock2_host* e *clock3_host* é necessário preencher com o ip da máquina onde o respectivo banco está sendo executado.

```bash
docker run -p 12001:12001 --rm -it -e host="0.0.0.0" -e clock2_host="ip_da_maquina" -e clock3_host="ip_da_maquina" lfrcintra/clock
```

```bash
docker run -p 12001:12001 --rm -it -e host="0.0.0.0" -e clock2_host="ip_da_maquina" -e clock3_host="ip_da_maquina" lfrcintra/clock
```

```bash
docker run -p 12001:12001 --rm -it -e host="0.0.0.0" -e clock2_host="ip_da_maquina" -e clock3_host="ip_da_maquina" lfrcintra/clock
```

### 3º etapa - Acessando o sistema

A partir do momento que o programa é iniciado o tempo começa a contar, para mudar o drift basta apertar a tecla `ENTER` e colocar um valor e apertar `ENTER` para confirmar.