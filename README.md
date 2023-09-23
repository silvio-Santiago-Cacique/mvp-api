#Meu Back End do MVP para Locação de Veículos

##Este é um pequeno projeto para conclusão do módulo I, referente ao **Pós-graduação em Desenvolvimento Full Stack pela PUC Rio**.
---

## Como executar 

Será necessário ter todas as libs python listadas no `requirements.txt` instaladas.

Após clonar o repositório, pelo link https://github.com/silvio-Santiago-Cacique/mvp-api, é necessário ir ao diretório raiz, pelo terminal, e executar os comandos descritos abaixo.

> É fortemente indicado o uso de ambientes virtuais do tipo [virtualenv](https://virtualenv.pypa.io/en/latest/installation.html).
Após a preparação do ambiente virtual, acesse o mesmo pelos seguintes comandos (em linux)

```
source myenv/bin/activate
```

```
(env)$ pip install -r requirements.txt
```

Este comando instala as dependências/bibliotecas, descritas no arquivo `requirements.txt`.


Para executar a API  basta executar:

```
(env)$ flask run --host 0.0.0.0 --port 5001
```

Em modo de desenvolvimento é recomendado executar utilizando o parâmetro reload, que reiniciará o servidor
automaticamente após uma mudança no código fonte. 

```
(env)$ flask run --host 0.0.0.0 --port 5001 --reload
```

Abra o [http://localhost:5001/#/](http://localhost:5001/#/) no navegador para verificar o status da API em execução.


A página ainda se comunica com uma API Externa Gratuíta BrasilApi/ViaCEP para busca de endereços por meio do CEP informado.

Comandos do docker utilizados para gerar as imagens e os containers:

Dentro do diretorio raiz da aplicação, executar:
```
docker build --pull --rm -f "Dockerfile" -t mvpveiculos:latest . #para gerar a imagem mvp_frontend

docker run --name mvpveiculos -p 5001:5001 -d -v .:/usr/share/nginx/html nginx #para rodar a imagem gerada
``

Após os comandos é só abrir o navegador no link http://127.0.0.1:5001

##Observação: A pasta src só foi adicionada devido ao fato da geração das imagens e container terem apresentado problemas sem esta pasta.
