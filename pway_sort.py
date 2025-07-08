import sys
import tempfile
import os
import time
import array
import threading
from queue import PriorityQueue

class Heap:
    def __init__(self):
        self._heap = []

    def push(self, item):
        self._heap.append(item)
        self._sift_up(len(self._heap) - 1)

    def pop(self):
        if not self._heap:
            raise IndexError("Não é possível remover de um heap vazio!")
        
        self._swap(0, len(self._heap) - 1)
        item = self._heap.pop()
        if self._heap:
            self._sift_down(0)
        return item

    def heapify(self, data):
        self._heap = list(data)
        for i in range(len(self._heap) // 2 - 1, -1, -1):
            self._sift_down(i)

    def _sift_up(self, index):
        parent_index = (index - 1) // 2
        if index > 0 and self._heap[index] < self._heap[parent_index]:
            self._swap(index, parent_index)
            self._sift_up(parent_index)

    def _sift_down(self, index):
        left_child_index = 2 * index + 1
        right_child_index = 2 * index + 2
        smallest = index
        if left_child_index < len(self._heap) and self._heap[left_child_index] < self._heap[smallest]:
            smallest = left_child_index
        if right_child_index < len(self._heap) and self._heap[right_child_index] < self._heap[smallest]:
            smallest = right_child_index
        if smallest != index:
            self._swap(index, smallest)
            self._sift_down(smallest)

    def _swap(self, i, j):
        self._heap[i], self._heap[j] = self._heap[j], self._heap[i]

    def __len__(self):
        return len(self._heap)

def gerar_runs_ordenadas(arquivo_entrada, p):
    def numeros_do_arquivo(f):
        for linha in f:
            yield from map(int, linha.split())

    start_time = time.time()
    temp_dir = None

    with open(arquivo_entrada, 'r', buffering=1024*1024) as f:
        numeros = numeros_do_arquivo(f)
        memoria = array.array('i')
        for _ in range(p):
            try:
                memoria.append(next(numeros))
            except StopIteration:
                break

        heap = Heap()
        heap.heapify(memoria)

        runs = []
        atual = float('-inf')
        congelados = array.array('i')

        while heap:
            run_temp = tempfile.NamedTemporaryFile(mode='w+t', delete=False, buffering=1024*1024)
            runs.append(run_temp.name)
            write = run_temp.write
            
            while heap:
                menor = heap.pop()
                write(f"{menor}\n")
                atual = menor
                try:
                    valor = next(numeros)
                    if valor >= atual:
                        heap.push(valor)
                    else:
                        congelados.append(valor)
                except StopIteration:
                    continue

            heap.heapify(congelados)
            congelados = array.array('i')
            run_temp.close()

    # print(f"Tempo para gerar runs ordenadas: {time.time() - start_time:.2f} segundos")
    return runs

def intercalar_grupo(grupo, temp_dir, output_list, index):
    arquivos = [open(r, 'r', buffering=1024*1024) for r in grupo]
    heap = Heap()

    for idx, arq in enumerate(arquivos):
        linha = arq.readline()
        if linha:
            heap.push((int(linha), idx))

    temp_out = tempfile.NamedTemporaryFile(mode='w+t', delete=False, buffering=1024*1024)
    output_list[index] = temp_out.name
    write = temp_out.write
    
    while heap:
        menor, origem = heap.pop()
        write(f"{menor}\n")
        linha = arquivos[origem].readline()
        if linha:
            heap.push((int(linha), origem))

    temp_out.close()
    for arq in arquivos:
        arq.close()
    for r in grupo:
        os.remove(r)

def intercalar_runs(runs, p):
    parse_count = 0
    start_time = time.time()

    temp_dir = None

    while len(runs) > 1:
        threads = []
        novos_runs = [None] * ((len(runs) + p - 1) // p)

        for i in range(0, len(runs), p):
            grupo = runs[i:i+p]
            index = i // p
            t = threading.Thread(target=intercalar_grupo, args=(grupo, None, novos_runs, index))
            threads.append(t)
            t.start()

        for t in threads:
            t.join()

        parse_count += 1
        runs = novos_runs

    # print(f"Tempo para intercalar runs: {time.time() - start_time:.2f} segundos")
    return runs[0], parse_count

def contar_registros(arquivo):
    total = 0
    with open(arquivo, 'r') as f:
        for linha in f:
            total += len(linha.split())
    return total

def main():
    if len(sys.argv) != 4:
        print("Uso: python pway_sort_with_heap.py <p> <entrada> <saida>")
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
