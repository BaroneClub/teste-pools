#!/usr/bin/env python3
# Teste de latencia para pools de mineracao solo de Bitcoin
# Mede: 1) tempo de conexao TCP  2) tempo do handshake stratum (mining.subscribe)
# O ranking usa o STRATUM, que e a latencia que o minerador sente de verdade.
# Funciona em Mac, Linux e Windows (Python 3.6+, sem dependencias externas).
# Uso: python3 teste_pools.py   (no Windows: python teste_pools.py)

import socket
import json
import time
import statistics

POOLS = [
    ("AtlasPool",        "solo.atlaspool.io",        3333),
    ("CKPool EU",        "eusolo.ckpool.org",        3333),
    ("CKPool US",        "solo.ckpool.org",          3333),
    ("Public Pool",      "public-pool.io",           21496),
    ("SoloPool.eu BTC",  "btc.solopool.eu",          3337),
    ("ViaBTC",           "btc.viabtc.io",            3333),
    ("Parasite Pool",    "parasite.wtf",             42069),
    ("Braiins Solo",     "solo.stratum.braiins.com", 3333),
    ("SoloHash UK",      "solo.solohash.co.uk",      3333),
    ("KanoPool",         "stratum.kano.is",          3333),
    ("KanoPool DE",      "de.kano.is",               3333),
    ("FindMyBlock EU",   "eu.findmyblock.xyz",       3335),
    ("solo.cat",         "solo.cat",                 3333),
    ("HF Pool BR",       "stratum.hfpool.com.br",    3333),
]

RUNS = 5          # quantas medicoes por pool
TIMEOUT = 5.0     # segundos

SUBSCRIBE = json.dumps({
    "id": 1,
    "method": "mining.subscribe",
    "params": ["teste-latencia/1.0"]
}) + "\n"


def testar(host, porta):
    """Retorna (tcp_ms, stratum_ms) ou lanca excecao."""
    t0 = time.perf_counter()
    s = socket.create_connection((host, porta), timeout=TIMEOUT)
    tcp_ms = (time.perf_counter() - t0) * 1000
    try:
        t1 = time.perf_counter()
        s.sendall(SUBSCRIBE.encode())
        s.settimeout(TIMEOUT)
        buf = b""
        while b"\n" not in buf:
            chunk = s.recv(4096)
            if not chunk:
                break
            buf += chunk
        stratum_ms = (time.perf_counter() - t1) * 1000
    finally:
        s.close()
    return tcp_ms, stratum_ms


def main():
    print("=" * 62)
    print("TESTE DE LATENCIA - POOLS SOLO DE BITCOIN")
    print(f"{RUNS} medicoes por pool | timeout {TIMEOUT:.0f}s")
    print("=" * 62)

    resultados = []
    for nome, host, porta in POOLS:
        tcps, strats = [], []
        erro = None
        for _ in range(RUNS):
            try:
                tcp_ms, stratum_ms = testar(host, porta)
                tcps.append(tcp_ms)
                strats.append(stratum_ms)
            except Exception as e:
                erro = str(e)
            time.sleep(0.3)
        if tcps:
            resultados.append((nome, host, statistics.median(tcps),
                               min(tcps), max(tcps),
                               statistics.median(strats)))
            print(f"  ok  {nome:<16} testado")
        else:
            print(f"  X   {nome:<16} falhou: {erro}")

    if not resultados:
        print("\nNenhum pool respondeu. Verifique sua conexao/firewall.")
        return

    # Ordena pelo STRATUM (mediana): e o que o minerador sente de verdade.
    # Pools atras de CDN podem ter TCP baixo mas stratum alto - nao se engane.
    resultados.sort(key=lambda r: r[5])
    print()
    print(f"{'#':<3}{'Pool':<17}{'Host':<26}{'Stratum (mediana)':<19}{'TCP':<11}{'Min-Max TCP'}")
    print("-" * 90)
    for i, (nome, host, med, mn, mx, st) in enumerate(resultados, 1):
        print(f"{i:<3}{nome:<17}{host:<26}{st:>10.1f} ms     "
              f"{med:>6.1f} ms  {mn:>5.1f}-{mx:<6.1f} ms")

    print()
    print(f"Vencedor (menor latencia stratum): {resultados[0][0]} ({resultados[0][5]:.1f} ms)")
    print("Dica: rode 2-3 vezes e ignore a primeira medicao (DNS frio inflaciona).")


if __name__ == "__main__":
    main()
