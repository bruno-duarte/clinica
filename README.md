# aps-clinica

Esse projeto foi desenvolvido como trabalho prático para a disciplina de Análise e Projeto de Software do curso 
de Ciência da Computação da Universidade Estadual do Ceará (UECE), semestre 2019.1. O objetivo é desenvolver um
sistema para uma clínica, que será utilizado pela secretária, pelos médicos e pelos pacientes. O sistema deve
possuir as seguintes funcionalidades:

- O sistema deve permitir que a secretária cadastre, edite, e busque médicos. Os médicos têm nome, CPF, e sua 
especialidade (clínica geral, oculista, pediatra, obstetra...). Ela só pode remover um médico caso este ainda 
não tenha feito consulta.
- Os pacientes podem se cadastrar diretamente no sistema informando nome, data de nascimento e CPF. Eles também 
podem editar, buscar e remover seus dados, mas este último apenas se não tiverem sido consultados.
- O paciente pode agendar uma consulta pelo sistema. Para tanto, ele faz uma busca por especialidade e verifica 
a disponibilidade de horários no dia desejado da consulta. Os médicos atendem em três horários: de 8h-9h, 9h-10h, 
10h-11h. O sistema informa o nome do médico disponível em cada horário. Se houver vaga, ele agenda a consulta para 
o dia e horário marcado. Caso não haja vaga, o paciente pode opcionalmente entrar em uma lista de espera para 
aquele dia com o médico escolhido. Um paciente não pode agendar uma consulta para um mesmo médico se já houver uma 
consulta agendada para este médico mas ainda não realizada.
- O paciente pode desmarcar a consulta através do sistema. Para isso, ele localiza as consultas por ele agendadas, 
seleciona a que deseja cancelar, preencho o motivo, e solicita o cancelamento. Este só pode ser feito com pelo 
menos um dia de antecedência à consulta.
- Caso algum paciente desmarque a consulta e tenha lista de espera para aquele médico naquele dia, o sistema 
notifica o primeiro paciente da lista, que pode aceitar o agendamento ou sair da lista. Neste caso, a notificação 
vai para o segundo na lista de espera, e assim sucessivamente até a lista ter sido toda consultada.
- O médico pode verificar os agendamentos dele para cada dia, bem como as consultas já realizadas.
- Em cada consulta, o médico preenche os sintomas do paciente (em um campo) e informa a lista de remédios que o 
paciente tem que tomar (em outro campo). Opcionalmente, o médico pode solicitar os exames (raio-x, tomografia, 
exame de sangue...). O mesmo exame pode ser solicitado em diferentes consultas para o mesmo paciente.
- O médico pode imprimir o relatório da consulta, com os dados que foram inseridos, bem como remédios e exames 
prescritos.

A secretária pode também solicitar os seguintes relatórios:

- ver todos os pacientes cadastrados, ver só os que já tiveram consultas, e ver só os que não tiveram consulta.
- imprimir a lista de médicos, agrupados por especialidade, e a quantidade de consultas realizadas em um 
determinado período.


## Features

- Utiliza o framework Django
- Trabalha o uso de Class Based View
- Utiliza User Model Customizado
- Uso de Template tags
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
