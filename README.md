# 📦 Ordenação Balanceada de p-Caminhos

Trabalho da disciplina **MATA54 - Estrutura de Dados e Algoritmos II – 2025.1**  

---
## 🎯 Objetivo

Consolidar o conhecimento sobre **ordenação externa**, implementando uma solução prática capaz de ordenar arquivos contendo inteiros, respeitando limites de memória e de arquivos simultaneamente abertos. O programa:

- 📂 Ordena números inteiros de um arquivo de entrada;
- 🧠 Usa no máximo `p` registros na memória principal;
- 🔄 Manipula até `2p` arquivos por vez.

---

## ⚙️ Método de Ordenação

O algoritmo implementa a técnica de **ordenação balanceada de p-caminhos (p-way merge sort)** com as seguintes fases:

### 🧩 1. Substituição por Seleção
- Inicializa um heap com `p` inteiros;
- Gera as **runs ordenadas iniciais** escritas em arquivos temporários;
- Valores fora de ordem são "congelados" e usados nas próximas runs.

### ♻️ 2. Intercalação com Heap Mínima
- Junta até `p` runs simultaneamente com **heap mínima**;
- Cria novas runs intermediárias até obter 1 única ordenada.

---

## 🖥️ Interface de Entrada e Saída

O programa é executado via terminal com:

```bash
python pway_sort.py <p> <arquivo_entrada> <arquivo_saida>
```

📌 Exemplo:
```bash
python pway_sort.py 3 input.txt output.txt
```

### 📥 Exemplo de entrada (`input.txt`):
```
18
7
3
24
15
5
20
25
16
14
21
19
1
4
13
9
22
11
23
8
17
6
12
2
10
```

### 📤 Exemplo de saída (`output.txt`):
```
1
2
3
4
5
6
7
8
9
10
11
12
13
14
15
16
17
18
19
20
21
22
23
24
25
```

📊 Saída no terminal:
```
#Regs Ways #Runs #Parses
25    3    5     2
```

---


## ✅ Critérios

- ✅ Ordenação **sem uso de sort interno** (nem mesmo no buffer inicial, apenas heap);
- ✅ Leitura e escrita apenas via **arquivos externos**;
- ✅ Compatível com arquivos grandes;
- ✅ Não usa estruturas que armazenem tudo na RAM;
- ✅ Não usa bibliotecas de ordenação pronta;


---

## 🔬 Testes Esperados

Utilizando o `input.txt` com 25 valores e o `input2.txt` com 10.000 valores:

| Comando                                  | Saída Esperada        |
|------------------------------------------|------------------------|
| `python pway_sort.py 2 input.txt output1.txt`    | `25  2  7  3`          |
| `python pway_sort.py 3 input.txt output2.txt`    | `25  3  5  2`          |
| `python pway_sort.py 4 input.txt output3.txt`    | `25  4  4  1`          |
| `python pway_sort.py 3 input2.txt output4.txt`    | `10000  3  1667  7 `          |


---

## 🛠️ Como Rodar Localmente

### 1. Clone o Repositório
```bash
git clone https://github.com/seuusuario/ordena-pway.git
cd ordena-pway
```

### 2. Crie o arquivo `input.txt`
Com valores inteiros, um por linha:
```
18
7
3
...
```

### 3. Execute o script principal
```bash
python pway_sort.py 3 input.txt output.txt
```

### 4. Veja os resultados
- O arquivo `output.txt` conterá os valores ordenados;
- O terminal exibirá as estatísticas do processo.

---


## ℹ️ Observação sobre a Leitura dos Dados

Inicialmente, o programa foi implementado para ler apenas arquivos em que cada número inteiro estava em uma linha separada, conforme o exemplo clássico de entrada:

```
18
7
3
...
```

No entanto, após o professor fornecer o arquivo `input2.txt` (com 10.000 inteiros separados por espaço em uma única linha), a implementação foi adaptada para aceitar **qualquer formato de entrada** em que os inteiros estejam separados por espaço ou quebra de linha, como:

```
18 7 3 24 15 5 20 ...
```

### 🆕 Como funciona a nova leitura

- O programa lê cada linha do arquivo e, para cada linha, separa todos os inteiros usando `linha.split()`.


---

## 🧠 Lógica de Implementação

- **Heap mínima** é usada tanto para gerar runs iniciais quanto para intercalar arquivos;
- A função `gerar_runs_ordenadas()` lê `p` valores e grava sequências ordenadas até esvaziar o arquivo;
- A função `intercalar_runs()` combina `p` arquivos por vez, criando runs intermediárias até restar um único arquivo ordenado.

---

## 📚 Licença
Uso acadêmico — desenvolvido exclusivamente para a disciplina MATA54 - UFBA.
