import random
import pandas as pd

dfMovies = pd.read_csv('./src/movies.csv')
dfTags = pd.read_csv('./src/tags.csv')
dfTags = dfTags.groupby('movieId')['tag'].apply(lambda x: ', '.join(x)).reset_index()
dfMovies['genres'] = dfMovies['genres'].str.replace('|', ',')

df = pd.merge(dfMovies, dfTags, on='movieId', how='inner')


def recomendar_filme(filme_escolhido):
    filmes_recomendados = df[
        (df['genres'].apply(lambda x: any(genero in filme_escolhido['genres'].split(',') for genero in x.split(',')))) &
        (df['tag'].apply(lambda x: any(tag in filme_escolhido['tag'].split(',') for tag in x.split(',')))) &
        (df['title'] != filme_escolhido['title'])]

    if filmes_recomendados.empty:
        print(f'Não foi possível encontrar uma recomendação para "{filme_escolhido["title"]}"')
        return None

    filme_recomendado = random.choice(filmes_recomendados['title'].reset_index(drop=True))
    print(f"Recomendação para '{filme_escolhido['title']}': {filme_recomendado}")


def main():
    i = 0
    palavra_chave = input("Digite uma palavra-chave do filme: ")

    filmes_selecionados = df[df['title'].str.lower().str.contains(palavra_chave.lower())]
    filmes_selecionados = filmes_selecionados.sort_values(by='title')

    if filmes_selecionados.empty:
        print(f'Nenhum filme encontrado para a palavra-chave "{palavra_chave}"')
        return 'Nenhum filme encontrado para a palavra-chave'

    print("Filmes encontrados:")
    for index, filme in filmes_selecionados.iterrows():
        i += 1
        print(f"{(index + i) - index}. {filme['title']}")

    escolha_filme = int(input("Escolha o número do filme para receber uma recomendação parecida: "))

    if escolha_filme < 1 or escolha_filme > len(filmes_selecionados):
        print("Escolha inválida. Por favor, escolha um número válido.")
        return

    filme_escolhido = filmes_selecionados.iloc[escolha_filme - 1]
    recomendacao = recomendar_filme(filme_escolhido)

    if recomendacao:
       return palavra_chave, recomendacao


if __name__ == "__main__":
    main()
