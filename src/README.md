Tiago Afonso Salgueiro up201704006
Daniel Santos up201305674

# Relatório projecto final

## Objectivos/introdução
Este projecto tem como objectivo a criação de um protótipo que se serve das funcionalidades do microprocessador ESP32 e de um sensor LIDAR para medir distâncias, mostrando-as num site em tempo real.

## Princípios gerais de funcionamento
O protótipo físico consiste na placa com os componentes fornecidos aos alunos no âmbito da cadeira, acrescido do sensor LIDAR que comunica diretamente com o ESP32 através do protocolo UART. Para além destes dois componentes principais, incorporamos também os botões e LEDs presentes na placa de forma a enriquecer o protótipo com algum nível de controlo extra.

Torna-se agora importante explicar sucintamente o modo de operação do sensor LIDAR. Como foi referido, este sensor utiliza o protocolo de comunicação em série UART e transmite para o ESP32 dois sinais: signal strength e distance. O primeiro corresponde a um valor no intervalo [0,3000] que é menor para valores maiores de distância medida e também menor para superfícies-alvo com refletividade baixa. O segundo corresponde à distância ao alvo em cm.
Essa informação, assim como frame headers importantes para verificar o funcionamento próprio do sensor, é enviada com a seguinte estrutura:

![](https://lh4.googleusercontent.com/TVWI5IDa2AG0UOkJygZQ7jWRJ7kP4cC4XG51f39dB2RPMU4N1VlFSMrnsGPfZ0rNvZeuVGAVdkLphMzUEic7lPwgcozrlSmKLDiea0eqA_WRhKqwnRQall8t2-FSypxoml3LOPUL)

Então, uma maneira eficiente de recolher esses dados é depois de encontrar o frame header inicial, lêr 8 bytes e desempacotar esses dados com a seguinte linha:

    frame, dist, strength, mode, _, checksum = struct.unpack("<BHHBBB", data)

O LIDAR utilizado (TF mini LIDAR range finder) mede distâncias ponto a ponto, num cone de medição de 2.3º. Quando este cone apanha duas superfícies com distâncias diferentes, como um pequeno desnível no pavimento, retorna a média das duas distâncias. O sensor apresenta uma refresh rate de 100Hz, o que, teoricamente, permitiria atualizar o gráfico no site em intervalos de 10ms,  mais do que suficiente e mais do que aquilo a que podemos chegar com o software utilizado.

Voltando ao resto dos componentes da placa, estando esclarecido o funcionamento geral do sensor, segue uma lista com cada componente e a sua função:

-   LEDs: funcionam como indicadores extra para a força do sinal, usando um esquema intuitivo, no qual o led vermelho corresponde a uma força do sinal mais perto de zero, o amarelo a valores intermédios e o verde a um intervalo de valores superior;
    
-   Botão esquerdo: enquanto premido, ativa o funcionamento dos LEDs;
    
-   Botão direito: Deep sleep;
    
-   Adicionalmente, o dispositivo “acorda” de novo ao passar o dedo pelo pin 4.
   
Quanto ao software, este apresenta três componentes principais que funcionam em conjunto para obter o resultado final: o programa boot.py que faz o setup da ligação wi-fi; o programa main.py que se serve da biblioteca MicroWebServ2 para criar servidor de páginas web e recebe os dados do sensor que envia para dois ficheiros txt, um a um; e o ficheiro index.html que descreve a página web onde são apresentados os gráficos que são actualizados em tempo real num intervalo pré-definido. Há também o ficheiro credentials.py, com user e password do WiFi.

## Resultados/bugs/melhorias possíveis:

Ligando efectivamente o protótipo e utilizando num contexto real, observa-se que este desempenha as funções pretendidas, não estando, no entanto, livre de alguns problemas.  

Um destes problemas é que o browser armazena automaticamente os sites visitados em cache, o que culmina em que por vezes o site deixa de atualizar com novos pontos. Ou melhor, atualiza, mas não o vemos porque o browser está a mostrar a versão do site que se visitou anteriormente. Para contornar isto é necessário  utilizar as ferramentas de programador para desligar a cache. Tentou-se implementar nas primeiras linhas do ficheiro .html um código de cache control que deveria contornar automaticamente este problema, desativando a cache, mas o mesmo não se conseguiu ainda o efeito pretendido, sendo este um ponto a melhorar no futuro.

Para além disto tivemos alguns problemas de fiabilidade com o sensor em si que, embora não seja do âmbito da cadeira, necessitou de alguma atenção e medidas no código para minorar alguns erros do sensor.

Adicionalmente, como objectivo para melhoria futura, seria ideal conseguir transmitir os dados para um site público onde uma pessoa em qualquer sítio com acesso à internet conseguisse observar os gráficos ou até controlar o estado dos LEDs e dos botões. Não foi possível fazê-lo já nesta iteração. Será necessário fazer uma pesquisa mais profunda sobre o tópico, que apenas foi abordado superficialmente, como introdução.

(A ideia aqui subjacente seria usar um API que a partir do qual pudéssemos obter o IP público do ESP32)

## Conclusão
Concluímos que globalmente o projecto foi bem sucedido. Não temos o código mais streamlined possível, e deixamos muito espaço aberto para melhoria, no entanto consideramos que conseguimos idealizar e concretizar um projecto que se serve de uma grande parte dos conhecimentos lecionados na cadeira e que neste aspecto fomos além das expectativas. Iremos continuar a trabalhar neste projecto fora do âmbito da cadeira, sendo o nosso objectivo final que o protótipo possa ser implementado na assistência a invisuais, através de feedback háptico ou sonoro. O trabalho que desenvolvemos para a cadeira de EDM corresponde à ferramenta de testes e calibração para esse projecto.
