import heapq
import sys
import tempfile
import os

#gera runs iniciais com substituicao por selecao
def gerar_runs_ordenadas(arquivo_entrada, p):
    heap = []
    runs = []
    memoria = []
    congelados = []

    #cria um iterador de números do arquivo -> independentemente de quebra de linha
    def numeros_do_arquivo(f):
        for linha in f:
            for num in linha.strip().split():
                yield int(num)

    with open(arquivo_entrada, 'r') as f:
        numeros = numeros_do_arquivo(f)
        # leitura inicial de p registros
        for _ in range(p):
            try:
                memoria.append(next(numeros))
            except StopIteration:
                break

        memoria.sort()
        heap = [(val, False) for val in memoria]
        heapq.heapify(heap)

        atual = float('-inf')

        while heap:
            run_temp = tempfile.NamedTemporaryFile(mode='w+t', delete=False)
            runs.append(run_temp.name)

            while heap:
                menor, congelado = heapq.heappop(heap)
                run_temp.write(f"{menor}\n")
                atual = menor

                try:
                    valor = next(numeros)
                except StopIteration:
                    continue

                if valor >= atual:
                    heapq.heappush(heap, (valor, False))
                else:
                    congelados.append((valor, True))

            heap = congelados
            congelados = []
            heapq.heapify(heap)

            run_temp.close()

    return runs


#intercala p arquivos usando heap minima
def intercalar_runs(runs, p):
    parse_count = 0

    while len(runs) > 1:
        novos_runs = []

        for i in range(0, len(runs), p):
            grupo = runs[i:i+p]
            arquivos = [open(r, 'r') for r in grupo]
            heap = []

            for idx, arq in enumerate(arquivos):
                linha = arq.readline()
                if linha:
                    heapq.heappush(heap, (int(linha.strip()), idx))

            temp_out = tempfile.NamedTemporaryFile(mode='w+t', delete=False)
            novos_runs.append(temp_out.name)

            while heap:
                menor, origem = heapq.heappop(heap)
                temp_out.write(f"{menor}\n")
                linha = arquivos[origem].readline()
                if linha:
                    heapq.heappush(heap, (int(linha.strip()), origem))

            temp_out.close()
            for arq in arquivos:
                arq.close()
            for r in grupo:
                os.remove(r)

        parse_count += 1  

        runs = novos_runs

    return runs[0], parse_count


def contar_registros(arquivo):
    with open(arquivo, 'r') as f:
        return sum(1 for linha in f for _ in linha.strip().split())

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

    os.rename(arquivo_ordenado, arquivo_saida)

    print("#Regs   Ways   #Runs   #Parses")
    print(f"{total_regs}      {p}      {len(runs)}       {total_passes}")

if __name__ == "__main__":
    main()