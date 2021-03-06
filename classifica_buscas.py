from collections import Counter
import pandas as pd

# teste inicial: home, busca, logado => comprou
# busca: 85.71% (7 testes)
df = pd.read_csv('buscas.csv')
Y_df = df['comprou']
X_df = df[['home', 'busca', 'logado']]
Xdummies_df = pd.get_dummies(X_df)
Ydummies_df = Y_df

X = Xdummies_df.values
Y = Ydummies_df.values

porcentagem_de_treino = 0.8
porcentagem_de_teste = 0.1

tamanho_de_treino = porcentagem_de_treino * len(Y)
tamanho_de_teste = porcentagem_de_teste * len(Y)
tamanho_de_validacao = len(Y) - tamanho_de_treino - tamanho_de_teste

tamanho_de_treino = int( tamanho_de_treino )
tamanho_de_teste = int( tamanho_de_teste )

treino_dados = X[0:tamanho_de_treino]
treino_marcacoes = Y[0:tamanho_de_treino]

fim_de_teste = tamanho_de_treino + tamanho_de_teste
teste_dados = X[tamanho_de_treino:fim_de_teste]
teste_marcacoes = Y[tamanho_de_treino:fim_de_teste]

validacao_dados = X[fim_de_teste:]
validacao_marcacoes = Y[fim_de_teste:] 

# a eficacia do algoritmo que chuta
# tudo um unico valor
acerto_base = max(Counter(validacao_marcacoes).itervalues())
taxa_de_acerto_base = 100.0 * acerto_base / len(validacao_marcacoes)

print("Taxa de acerto base: %f" % taxa_de_acerto_base)

def fit_and_predict(nome, modelo, treino_dados, treino_marcacoes, teste_dados, teste_marcacoes):
    modelo.fit(treino_dados, treino_marcacoes)

    resultado = modelo.predict(teste_dados)
    acertos = (resultado == teste_marcacoes)
    total_de_acertos = sum(acertos)
    total_de_elementos = len(teste_dados)
    taxa_de_acerto = 100.0 * total_de_acertos / total_de_elementos

    print("Taxa de acerto do algoritmo {0} : {1} ".format(nome, taxa_de_acerto))
    return taxa_de_acerto

from sklearn.naive_bayes import MultinomialNB
modeloMultinomial = MultinomialNB()

resultadoMultinomial = fit_and_predict("MultinomialNB", modeloMultinomial, treino_dados, treino_marcacoes, teste_dados, teste_marcacoes)

from sklearn.ensemble import AdaBoostClassifier
modeloAdaBoost = AdaBoostClassifier()

resultadoAdaBoost = fit_and_predict("AdaBoostClassifier", modeloAdaBoost, treino_dados, treino_marcacoes, teste_dados, teste_marcacoes)

if(resultadoMultinomial > resultadoAdaBoost):
    vencedor = modeloMultinomial
else:
    vencedor = modeloAdaBoost

resultado = vencedor.predict(validacao_dados)

acertos = (resultado == validacao_marcacoes)
total_de_acertos = sum(acertos)
total_de_elementos = len(validacao_marcacoes)
taxa_de_acerto = 100.0 * total_de_acertos / total_de_elementos

print("Taxa de acerto do algoritmo vencedor entre os dois algoritmos no mundo real : {0} ".format(taxa_de_acerto))


print("Total de elementos : %d" % len(Y))
