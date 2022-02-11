import random
import pandas as pd
from pumpwood_communication.microservices import PumpWoodMicroService

microservice = PumpWoodMicroService(
    server_url="http://0.0.0.0:8000/",
    username="pumpwood", password="pumpwood")
microservice.login()


texto_exemplo = """
Os candidatos à Prefeitura de Macapá se viram obrigados a lidar com um novo e
surpreendente elemento na disputa: a “humilhação” a que foram submetidos os
eleitores em razão do apagão no Amapá desde o último dia 3.
A palavra é reiteradamente dita pelos moradores da capital amapaense para
resumir o que sentem desde que ficaram no escuro.
O problema está longe de ser resolvido, a ponto de o TRE (Tribunal Regional
Eleitoral) do Amapá pedir ao TSE (Tribunal Superior Eleitoral) o adiamento
das eleições em Macapá, sem definição de uma nova data. O pedido foi aceito
pela corte em Brasília.
A medida vale apenas para a capital. Nas outras 15 cidades do estado, a
votação está prevista para ocorrer neste domingo (15).
Os primeiros dias sem energia e o posterior racionamento a que foram
submetidos, com imprevisibilidade de horários em algumas regiões da cidade,
provocaram a fúria dos moradores de Macapá.

A animosidade não se resume aos protestos, que seguem ocorrendo praticamente
todas as noites, em distintos bairros da cidade. A Folha presenciou diversas
situações em que comunidades não aceitam a presença de cabos eleitorais.
É assim, por exemplo, nas chamadas áreas de ressaca, que são as extensões de
alguns bairros sobre áreas de lago. Ao lado de estreitas pontes de madeira,
favelas sobre a água foram erguidas. Um único bairro, Congós, tem 30 mil
moradores vivendo nessas “baixadas”. É muito frequente encontrar moradores
refratários à presença de cabos eleitorais e distribuidores de santinhos.
Cabos eleitorais também não são bem recebidos em comunidades mais afastadas.
O mau humor na cidade —para dizer o mínimo— é generalizado diante da falta
de solução para o problema e dos transtornos com a falta de energia. Já são
nove dias de apagão. O impacto na disputa eleitoral é inevitável, com a
população buscando culpados para o problema no meio político.
São os casos, por exemplo, de comunidades quilombolas próximas ao núcleo
urbano de Macapá.
A última pesquisa Ibope, feita dos dias 9 a 11 —ou seja, já durante o apagão—
e divulgada nesta quarta (11), aponta uma possível alteração de cenários.
"""
palavras = pd.Series(texto_exemplo.split())
index_filter = 4 <= palavras.str.len()
palavras = palavras[index_filter].tolist()


def gerador_de_lero_lero(n: int):
    return " ".join(random.choices(palavras, k=n))


for i in range(5):
    microservice.save({
        "model_class": "DescriptionExperimentTeam",
        "description": gerador_de_lero_lero(5),
        "notes": gerador_de_lero_lero(20)})
