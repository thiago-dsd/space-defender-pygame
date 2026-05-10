# Plano de Desenvolvimento — Space Defender (Demo)
## Linguagem de Programação Aplicada — Atividade Prática

---

## Tema
Jogo de nave espacial 2D. O jogador controla uma nave, destrói asteroides e tenta sobreviver até atingir a pontuação de vitória.

---

## Estrutura de arquivos

```
space_defender/
├── main.py          # ponto de entrada, loop principal e máquina de estados
├── entities.py      # classes: Player, Asteroid, Bullet
└── (sem pasta assets — todos os visuais desenhados via pygame.draw)
```

> Sem arquivos de imagem/som externos. Tudo é desenhado com pygame.draw,
> tornando o projeto auto-contido e sem dependência de assets baixados.

---

## Estados do jogo (State Machine)

```
MENU → PLAYING → GAME_OVER
                → VICTORY
```

| Estado    | Descrição                              |
|-----------|----------------------------------------|
| MENU      | Tela inicial com título e controles    |
| PLAYING   | Loop de jogo ativo                     |
| GAME_OVER | Jogador perdeu todas as vidas          |
| VICTORY   | Jogador atingiu 500 pontos             |

---

## Requisitos atendidos

| Requisito              | Solução                                      |
|------------------------|----------------------------------------------|
| Controle do jogador    | ← → move a nave, SPACE atira                 |
| Desafio                | Asteroides aumentam em velocidade e frequência com o tempo |
| Condição de vitória    | Atingir 500 pontos destruindo asteroides     |
| Condição de derrota    | Perder as 3 vidas por colisão com asteroide  |
| Menu com controles     | Tela de menu exibe os controles na tela      |
| Jogo 2D (não console)  | Janela pygame 800x600                        |

---

## Entidades (entities.py)

### Player
- Posição fixa na parte inferior da tela
- Move horizontalmente com ← →
- Atira para cima com SPACE (cooldown de 0.3s)
- 3 vidas, pisca ao ser atingido (invencibilidade temporária)

### Asteroid
- Spawna no topo da tela em posição X aleatória
- Cai em velocidade aleatória (aumenta com o tempo)
- Tamanho aleatório (raio entre 15 e 40px)
- Destrói ao sair da tela (sem penalidade) ou ao ser baleado

### Bullet
- Dispara da posição da nave
- Sobe em alta velocidade
- Remove ao sair da tela ou colidir com asteroide

---

## Progressão de dificuldade

| Tempo (segundos) | Velocidade base dos asteroides | Intervalo de spawn |
|------------------|--------------------------------|--------------------|
| 0–20             | 2                              | 1.5s               |
| 20–40            | 3                              | 1.2s               |
| 40+              | 4                              | 0.9s               |

---

## Tela de Menu
```
╔══════════════════════════════╗
║      SPACE DEFENDER          ║
║                              ║
║   Pressione ENTER para jogar ║
║                              ║
║   Controles:                 ║
║   ← → ......... Mover nave   ║
║   SPACE ........ Atirar      ║
║   ESC .......... Sair        ║
╚══════════════════════════════╝
```

---

## Compilação (entrega)

1. Rodar `pyinstaller --onefile main.py` na pasta do projeto
2. Copiar pasta `assets/` ao lado do `main.exe` na pasta `dist/` (se houver assets)
3. Zipar a pasta `dist/` → entregar o `.zip`

> Como não há assets externos, apenas o `main.exe` precisa estar no ZIP.

---

## Ordem de implementação

- [ ] 1. Esqueleto do main.py com loop e estados
- [ ] 2. Classe Player com movimento e disparo
- [ ] 3. Classe Asteroid com spawn e movimento
- [ ] 4. Classe Bullet com colisão
- [ ] 5. Sistema de vidas, score e progressão de dificuldade
- [ ] 6. Telas: Menu, Game Over, Victory
- [ ] 7. Testes e ajustes de gameplay
- [ ] 8. Compilação com PyInstaller
