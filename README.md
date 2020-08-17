# ze-api

API baseada em Geolocalização escrita em Python, Flask, Postgres e Postgis.

Com a ze-API é possível [criar um parceiro](#criar-um-parceiro-cup), [carregar parceiro pelo id](#carregar-parceiro-pelo-id-cppi) e [buscar parceiro](#buscar-parceiro-bp).

# Table of contents
   * [Configurando o ambiente local](#configurando-o-ambiente-local)
   * [API Documentação](#api-documentação)
      * [Descrição](#descrição)
      * [Cabeçalho](#cabeçalho)
      * [Criar um parceiro (CUP)](#criar-um-parceiro-cup)
		* [Exemplo CUP](#exemplo-cup)
      * [Carregar parceiro pelo id (CPPI)](#carregar-parceiro-pelo-id-cppi)
		* [Exemplo CPPI](#exemplo-cppi)
      * [Buscar parceiro (BP)](#buscar-parceiro-bp)
		* [Exemplo BP](#exemplo-bp)
   * [References](#references)

# Configurando o ambiente local

Uma vez que o docker está instalado em seu computador, execute os seguintes passos:

clonar o projeto

    git clone git@github.com:danilolmoura/ze-api.git

criar e executar a imagem localmente

    cd ze-api
    docker-compose build
    docker-compose up -d

Após o passo anterior, a aplicação poderá ser acessada no endereço http://127.0.0.1:5000/

Os logs de execução da aplicação podem ser visualizados através dos comandos abaixo

	docker ps
	docker logs <container_id>

# API Documentação

## Descrição

A ze-API é uma interface que utiliza o padrão `HTTP REST`.

## Cabeçalho

Para cada requisição realizada para a API, **é necessário** adicionar o `Content-type` conforme o exemplo abaixo:
```json
{
	"Content-Type": "application/json"
}
```


## Criar um parceiro (CUP)

Através deste recurso é possível criar um novo parceiro, considerando os pontos abaixo:

- Não é necessário adicionar o `id` do parceiro em sua criação.
- Todos os campos são obrigatórios, exceto o `id`
- Não é possível cadastrar um parceiro com o mesmo `document`.

### Exemplo CUP

```json
POST /api/v1/partner
{
	"address": { 
	  "type": "Point",
	  "coordinates": [-46.57421, -21.785741]
	},
	"coverageArea": { 
		"type": "MultiPolygon", 
		"coordinates": [
			[[[30, 20], [45, 40], [10, 40], [30, 20]]], 
			[[[15, 5], [40, 10], [10, 20], [5, 10], [15, 5]]]
		]
	},
	"document": "1432132123891/0001",
	"ownerName": "Zé da Silva",
	"tradingName": "Adega da Cerveja - Pinheiros"
}
```

Na resposta, serão retornados os dados do parceiro recém-criado:
```json
HTTP Response 200
{
	"$id": 1,
	"address": {
		"coordinates": [-46.57421, -21.785741],
		"type": "Point"
	},
	"coverageArea": {
		"coordinates": [
			[
				[[30.0, 20.0], [45.0, 40.0], [10.0, 40.0]],
				[[15.0, 5.0], [40.0, 10.0], [10.0, 20.0], [5.0, 10.0]]
			]
		],
		"type": "MultiPolygon"
	},
	"document": "1432132123891/0001",
	"ownerName": "Zé da Silva",
	"tradingName": "Adega da Cerveja - Pinheiros"
}
```

Ou, retornará uma exceção caso o `document` seja duplicado:

```json
HTTP Response 409
{
  "message": "Conflict",
  "status": 409
}
```

## Carregar parceiro pelo id (CPPI)

Através desse recurso, é possível buscar informações de um parceiro já cadastrado utilizando deu `id`, considerando os pontos abaixo:

- É necessário adicionar à URL da requição um `id` de parceiro já existente, caso contrário uma exceção será lançada.

### Exemplo CPPI

```json
HTTP GET /api/v1/partner/1
```

Na resposta, serão retornados os dados do parceiro solicitado:
```json
HTTP Response 200
{
	"$id": 1,
	"address": {
	"coordinates": 
		[-46.57421, -21.785741],
		"type": "Point"
	},
	"coverageArea": {
		"coordinates": [
			[
				[
					[-43.36556, -22.99669],
					[-43.36539, -23.01928],
					[-43.26583, -23.01802],
					[-43.25724, -23.00649],
					[-43.23355, -23.00127]
				],
				[
					[15.0, 5.0],
					[40.0, 10.0],
					[10.0, 20.0],
					[5.0, 10.0]
				]
			]
		],
		"type": "MultiPolygon"
	},
	"document": "1432132123891/0001",
	"ownerName": "Zé da Silva",
	"tradingName": "Adega da Cerveja - Pinheiros"
}
```

Ou, retornará uma exceção caso o `id` seja inválido, no seguinte formato:
```json
HTTP Response 404
{
	"item": {
		"$id": 278,
		"$type": "partner"
	},
	"message": "Not Found",
	"status": 404
}
```

## Buscar parceiro (BP)

Através desse recurso, é possível encontrar o parceiro mais próximo e cuja área de cobertura abranje a coordenada enviada, considerando os pontos abaixo:

- É necessário o envio da coordenada geográfica (long, lat), onde queremos buscar o parceiro.
- Uma vez recebedida as coordenada geográfica, é localizado o parceiro cuja área de cobertura engloba a coordenada enviada na requisição.
- Caso mais de um parceiro seja encontrado no item anterior, é escolhido o parceiro cujo endereço é o mais próximo da coordenada enviada na requisição.
- Caso nenhum parceiro possua área de cobertura que englobe o ponto enviado, o resultado será vazio.

### Exemplo BP

```json
HTTP GET /api/v1/partner/nearest
{
	"long": -43.311675,
	"lat": -23.010202
}
```

Na resposta, serão retornados os dados do parceiro mais próximo:
```json
HTTP Response 200
{
	"$id": 1,
	"address": {
	    "coordinates": [-43.297337, -23.013538],
	    "type": "Point"
	},
	"coverageArea": {
	    "coordinates": [
	        [
	            [
	                [-43.36556, -22.99669],
	                [-43.36539, -23.01928],
	                [-43.26583, -23.01802],
	                [-43.25724, -23.00649],
	                [-43.23355, -23.00127]
	            ]
	        ]
	    ],
	    "type": "MultiPolygon"
	},
  	"document": "1432132123891/0001",
	"ownerName": "Joao Silva",
	"tradingName": "Bar do Ze"
}
```

Ou, na resposta será retornado `null` caso nenhum parceiro cubra o ponto geográfico enviado:
```json
HTTP Response 200

null
```

# References

* [Docker](https://www.docker.com/get-started)
* [Flask](http://flask.palletsprojects.com/en/1.1.x/)
* [SQLAlchemy](https://www.sqlalchemy.org/)
* [GeoAlchemy2](https://geoalchemy-2.readthedocs.io/en/latest/)
