# Othello ⚫⚪

INF01048 - Inteligência Artificial - 2022/2

Léo Hernandes de Vasconcelos - 323961<br>
Jose Henrique Lima Marques - 324502<br>
Vítor Caruso Rodrigues Ferrer - 327023

## Heurísticas 🗒️

Nos baseamos no artigo [*An Analysis of Heuristics in Othello*](https://courses.cs.washington.edu/courses/cse573/04au/Project/mini1/RUSSIA/Final_Paper.pdf) de *Vaishnavi Sannidhanam* e *Muthukaruppan Annamalai* que analise diferentes heurísticas e suas melhores combinações. No artigo, são citadas 4 heurísticas principais, das quais 3 implementamos.

### 1. Heurística de paridade de peças 
A mais simples e mais ineficiente quando usada sozinha, simplesmente é feita a contagem das nossas peças, subtraindo as do adversário. Ela se torna muito importante no final do jogo, em que focamos em jogadas que ganham mais peças, afinal esse é o objetivo principal.

### 2. Heurística de mobilidade
Um pouco mais sofisticada, nela fazemos uma contagem dos nossos movimentos possíveis e subtraímos os movimentos possíveis do adversário. A intenção é valorizar movimentos que nos liberam bastante espaço de escolha no tabuleiro enquanto que limitamos a flexibilidade do jogo do oponente.

### 3. Heurísticas de cantos
Há uma grande relação entre cantos capturados e a vitória no jogo, pois os cantos do tabuleiro são posições sem flanqueamento e que geram grande estabilidade durante a partida. Nela, damos valor a jogadas que capturam cantos, porém mais importante que isso, penalizamos bastante jogadas que irão favorecer a captura de cantos para o adversário. Pela nossa experiência de testes, é mais importante que o adversário não possua cantos capturados do que nós termos algum.

## Condição de parada 🛑

Desde o início, assumimos compromisso em gastar poder computacional no cálculo de heurísticas melhores do que em algoritmos sofisticados de navegação pela árvore de jogadas possíveis. Devido a isso, assumimos uma profundidade limite igual a 4 para o algoritmo Minimax, visto que a profundidade 5 estrapolava o tempo de espera estipulado.

## Melhorias 📈

### 1. Threads
Para termos certeza de que nosso agente não seria desclassificado por falta de tempo em casos muito específicos em que o jogo possui uma quantidade enorme de possibilidades (árvore muito grande), implementamos o uso de threads para calcularem os valores estimados dos estados do jogo paralelamente. Pelos testes que fizemos, em alguns casos estávamos ganhando quase 1 segundo de execução utilizando threads, o que nos tranquilizou bastante.

### 2. Pesos dinâmicos para heurísticas
Inicialmente fizemos uma combinação linear estática das três heurísticas descritas com pesos que foram testados para avaliar os estados do jogo. Mas como é citado no artigo, idealmente as táticas do jogo mudam de acordo com o estado da partida. Devido a isso, mantemos um controle do progresso do jogo contando quantas posições vazias ainda restam para modificar os pesos de acordo com limiares estipulados.
Iniciamos o jogo focando em prender o adversário e limitar seus movimentos. No meio da partida focamos em conquistar os cantos do tabuleiro, já que muito provavelmente já estamos perto de alguns. Finalmente nos útlimos movimentos damos muito valor à quantidade de peças que possuimos em relação às que o adversário possui.

## Bibliografia 📚
[An Analysis of Heuristics in Othello](https://courses.cs.washington.edu/courses/cse573/04au/Project/mini1/RUSSIA/Final_Paper.pdf)

[How to write an Othello AI with Alpha-Beta search](https://medium.com/@gmu1233/how-to-write-an-othello-ai-with-alpha-beta-search-58131ffe67eb)
