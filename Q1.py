import random
import os
import matplotlib.pyplot as plt

random.seed(42)

# Parâmetros
total_referencias = 1000
total_paginas = 10
tamanho_workset = 4
prob_workset = 0.9

paginas = list(range(total_paginas)) 
workset = paginas[:tamanho_workset]   
restantes = paginas[tamanho_workset:] 

# Geração das referências
referencias = []
for _ in range(total_referencias):
    if random.random() < prob_workset:
        referencia = random.choice(workset)
    else:
        referencia = random.choice(restantes)
    referencias.append(referencia)

nome_arquivo = "referencias_paginacao.txt"

# Só cria o arquivo se ele ainda não existir
if not os.path.exists(nome_arquivo):
    with open(nome_arquivo, "w") as arquivo:
        for ref in referencias:
            arquivo.write(f"{ref}\n")
    print(f"Arquivo '{nome_arquivo}' criado com sucesso!")
else:
    print(f"Arquivo '{nome_arquivo}' já existe. Nenhuma ação tomada.")


def simulacao_fifo(referencias, num_quadros):
    quadros = []
    faltas = 0
    for pagina in referencias:
        if pagina not in quadros:
            faltas += 1
            if len(quadros) >= num_quadros:
                quadros.pop(0)
            quadros.append(pagina)
    return faltas

def simulacao_aging(referencias, num_quadros, bits=8):
    quadros = []
    contadores = {}
    referencias_bit = {}
    faltas = 0

    for pagina in referencias:
        for p in quadros:
            contadores[p] >>= 1
            if referencias_bit.get(p, False):
                contadores[p] |= (1 << (bits - 1))
            referencias_bit[p] = False

        if pagina not in quadros:
            faltas += 1
            if len(quadros) < num_quadros:
                quadros.append(pagina)
                contadores[pagina] = 0
            else:
                pagina_substituir = min(quadros, key=lambda p: contadores[p])
                quadros.remove(pagina_substituir)
                del contadores[pagina_substituir]
                del referencias_bit[pagina_substituir]
                quadros.append(pagina)
                contadores[pagina] = 0

        referencias_bit[pagina] = True

    return faltas

def gerar_grafico_comparativo(molduras, fifo, aging, caminho_saida="grafico_faltas_paginacao.png"):
    plt.figure(figsize=(10, 6))
    plt.plot(molduras, fifo, marker='o', label='FIFO', linestyle='-', color='blue')
    plt.plot(molduras, aging, marker='s', label='Aging', linestyle='--', color='green')
    plt.title("Comparação de Faltas de Página: FIFO vs. Aging")
    plt.xlabel("Número de Molduras")
    plt.ylabel("Número de Faltas de Página")
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.savefig(caminho_saida)
    print(f"Gráfico salvo como '{caminho_saida}'")

def main():
    molduras_testar = [2, 3, 5, 8, 10]

    fifo_resultados = []
    aging_resultados = []

    print(f"{'Molduras':<10} {'Faltas FIFO':<15} {'Faltas Aging':<15}")
    print("-" * 40)

    for molduras in molduras_testar:
        faltas_fifo = simulacao_fifo(referencias, molduras)
        faltas_aging = simulacao_aging(referencias, molduras)
        fifo_resultados.append(faltas_fifo)
        aging_resultados.append(faltas_aging)
        print(f"{molduras:<10} {faltas_fifo:<15} {faltas_aging:<15}")

    gerar_grafico_comparativo(molduras_testar, fifo_resultados, aging_resultados)

if __name__ == "__main__":
    main()
