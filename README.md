# Teste de Latência — Pools Solo de Bitcoin ⛏️

Script em Python puro (sem dependências) que mede a latência real entre a sua
máquina e **14 pools de mineração solo de Bitcoin**: conexão TCP e handshake
stratum (`mining.subscribe`), 5 medições por pool, ranking pela mediana do
stratum — que é a latência que o seu miner sente de verdade.

Ferramenta do [Barone Club](https://x.barone.club/teste-pools).

## Rodar em 1 comando

**Mac / Linux** (Terminal):

```bash
curl -sL https://raw.githubusercontent.com/BaroneClub/teste-pools/main/teste_pools.py | python3
```

**Windows** (PowerShell, com [Python](https://www.python.org/downloads/) instalado):

```powershell
curl.exe -sL https://raw.githubusercontent.com/BaroneClub/teste-pools/main/teste_pools.py | python
```

> Nunca rode script da internet às cegas: leia o [teste_pools.py](./teste_pools.py)
> antes — são ~100 linhas que só abrem conexões, medem tempo e imprimem a tabela.

## Pools testadas

AtlasPool · CKPool EU/US · Public Pool · SoloPool.eu · ViaBTC · Parasite Pool ·
Braiins Solo · SoloHash UK · KanoPool (US/DE) · FindMyBlock EU · solo.cat ·
HF Pool BR

## Como ler o resultado

- A coluna **Stratum** é a que importa (o que o miner sente).
- Rode 2–3 vezes e ignore a primeira medição (DNS frio inflaciona).
- TCP baixo com stratum alto = pool atrás de CDN; não se engane.

Sugestões de pools? Abra uma issue. **Que o próximo bloco seja seu.**
