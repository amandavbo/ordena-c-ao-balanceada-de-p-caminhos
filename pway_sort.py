import heapq
import sys
import tempfile
import os
import time
import array
import threading
from queue import PriorityQueue

def gerar_runs_ordenadas(arquivo_entrada, p):
    def numeros_do_arquivo(f):
        for linha in f:
            yield from map(int, linha.split())

    start_time = time.time()
    temp_dir = os.path.join(os.path.dirname(__file__), 'temp')
    os.makedirs(temp_dir, exist_ok=True)

    with open(arquivo_entrada, 'r', buffering=1024*1024) as f:
        numeros = numeros_do_arquivo(f)
        memoria = array.array('i')
        for _ in range(p):
            try:
                memoria.append(next(numeros))
            except StopIteration:
                break

        memoria = sorted(memoria)
        heap = list(memoria)
        heapq.heapify(heap)

        runs = []
        atual = float('-inf')
        congelados = array.array('i')

        while heap:
            run_temp = tempfile.NamedTemporaryFile(mode='w+t', delete=False, buffering=1024*1024, dir=temp_dir)
            runs.append(run_temp.name)
            write = run_temp.write
            heappop = heapq.heappop
            heappush = heapq.heappush

            while heap:
                menor = heappop(heap)
                write(f"{menor}\n")
                atual = menor
                try:
                    valor = next(numeros)
                    if valor >= atual:
                        heappush(heap, valor)
                    else:
                        congelados.append(valor)
                except StopIteration:
                    continue

            heap = list(congelados)
            congelados = array.array('i')
            heapq.heapify(heap)
            run_temp.close()

    print(f"Tempo para gerar runs ordenadas: {time.time() - start_time:.2f} segundos")
    return runs

def intercalar_grupo(grupo, temp_dir, output_list, index):
    arquivos = [open(r, 'r', buffering=1024*1024) for r in grupo]
    heap = []

    for idx, arq in enumerate(arquivos):
        linha = arq.readline()
        if linha:
            heapq.heappush(heap, (int(linha), idx))

    temp_out = tempfile.NamedTemporaryFile(mode='w+t', delete=False, buffering=1024*1024, dir=temp_dir)
    output_list[index] = temp_out.name
    write = temp_out.write
    heappush = heapq.heappush
    heappop = heapq.heappop

    while heap:
        menor, origem = heappop(heap)
        write(f"{menor}\n")
        linha = arquivos[origem].readline()
        if linha:
            heappush(heap, (int(linha), origem))

    temp_out.close()
    for arq in arquivos:
        arq.close()
    for r in grupo:
        os.remove(r)

def intercalar_runs(runs, p):
    parse_count = 0
    start_time = time.time()

    temp_dir = os.path.join(os.path.dirname(__file__), 'temp')
    os.makedirs(temp_dir, exist_ok=True)

    while len(runs) > 1:
        threads = []
        novos_runs = [None] * ((len(runs) + p - 1) // p)

        for i in range(0, len(runs), p):
            grupo = runs[i:i+p]
            index = i // p
            t = threading.Thread(target=intercalar_grupo, args=(grupo, temp_dir, novos_runs, index))
            threads.append(t)
            t.start()

        for t in threads:
            t.join()

        parse_count += 1
        runs = novos_runs

    print(f"Tempo para intercalar runs: {time.time() - start_time:.2f} segundos")
    return runs[0], parse_count

def contar_registros(arquivo):
    total = 0
    with open(arquivo, 'r') as f:
        for linha in f:
            total += len(linha.split())
    return total

def main():
    if len(sys.argv) != 4:
        print("Uso: python pway_sort.py <p> <entrada> <saida>")
        sys.exit(1)

    p = int(sys.argv[1])
    arquivo_entrada = sys.argv[2]
    arquivo_saida = sys.argv[3]

    if p < 2:
        print("Erro: p deve ser >= 2")
        sys.exit(1)

    total_regs = contar_registros(arquivo_entrada)
    runs = gerar_runs_ordenadas(arquivo_entrada, p)
    arquivo_ordenado, total_passes = intercalar_runs(runs, p)

    if os.path.exists(arquivo_saida):
        os.remove(arquivo_saida)
    os.rename(arquivo_ordenado, arquivo_saida)

    print("#Regs   Ways   #Runs   #Parses")
    print(f"{total_regs}      {p}      {len(runs)}       {total_passes}")

if __name__ == "__main__":
    main()
