def calcular_metricas(VP, VN, FP, FN):
    # Cálculo das métricas
    sensibilidade = VP / (VP + FN) if (VP + FN) != 0 else 0
    especificidade = VN / (FP + VN) if (FP + VN) != 0 else 0
    acuracia = (VP + VN) / (VP + VN + FP + FN) if (VP + VN + FP + FN) != 0 else 0
    precisao = VP / (VP + FP) if (VP + FP) != 0 else 0
    f_score = 2 * (precisao * sensibilidade) / (precisao + sensibilidade) if (precisao + sensibilidade) != 0 else 0

    # Retorna um dicionário com os resultados
    return {
        "Sensibilidade (Recall)": sensibilidade,
        "Especificidade": especificidade,
        "Acurácia": acuracia,
        "Precisão": precisao,
        "F-Score": f_score
    }

# Exemplo de uso com os valores da matriz de confusão anterior
VP = 80
VN = 105
FP = 5
FN = 10

metricas = calcular_metricas(VP, VN, FP, FN)

# Exibindo os resultados formatados em porcentagem
for nome, valor in metricas.items():
    print(f"{nome}: {valor:.2%}")