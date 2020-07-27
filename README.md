# aps-clinica

Esse projeto foi desenvolvido como trabalho prático para a disciplina de Análise e Projeto de Software do curso 
de Ciência da Computação da Universidade Estadual do Ceará (UECE), semestre 2019.1. O objetivo é desenvolver um
sistema para uma clínica, que será utilizado pela secretária, pelos médicos e pelos pacientes.


## Features

- Utiliza o framework Django
- Trabalha o uso de Class Based View
- Utiliza User Model Customizado
- Uso de template tags
- Django admin com filtros customizados
- Utiliza Padrão Arquitetural e de Projeto

## Getting started

Você irá precisar de:

- Python >= 3.6
- Pip
- VirtualEnv

## Desenvolvimento

Para fazer alterações no projeto:

```
cd "diretorio de sua preferencia"
git clone https://github.com/Bruno-Duarte/aps.git
```

## Instalação (No Ubuntu)

1. `cd aps`
2. `virtualenv -p python3 .`
3. `source bin/activate`
4. `pip install -r requirements.txt`
5. `python manage.py migrate`
6. `python manage.py createsuperuser`
7. `python manage.py runserver`


## Deploy e Publicação

Caso queira utilizar o projeto sem fazer intalação, o projeto foi publicado online, acesse pelo [link](https://aps-clinica.herokuapp.com/).
