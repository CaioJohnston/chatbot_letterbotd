import random
import pandas as pd

# Leitura dos dados
dfMovies = pd.read_csv('./src/movies.csv')
dfTags = pd.read_csv('./src/tags.csv')

# Agrupamento das tags por movieId
dfTags = dfTags.groupby('movieId')['tag'].apply(lambda x: ', '.join(x)).reset_index()

# Remover separadores "|" dos gêneros
dfMovies['genres'] = dfMovies['genres'].str.replace('|', ',')

# Mesclagem dos DataFrames
df = pd.merge(dfMovies, dfTags, on='movieId', how='inner')

def recomendar_filme(filme_escolhido):
    # Filtrar filmes com pelo menos um gênero em comum e pelo menos uma tag igual ao filme escolhido
    filmes_recomendados = df[(df['genres'].apply(lambda x: any(genero in filme_escolhido['genres'].split(',') for genero in x.split(',')))) &
                             (df['tag'].apply(lambda x: any(tag in filme_escolhido['tag'].split(',') for tag in x.split(',')))) &
                             (df['title'] != filme_escolhido['title'])]

    if filmes_recomendados.empty:
        return f'Não foi possível encontrar uma recomendação para "{filme_escolhido["title"]}"'
    else:
        filme_recomendado = random.choice(filmes_recomendados['title'].reset_index(drop=True))
        print(f"Recomendação para '{filme_escolhido['title']}': {filme_recomendado}")
        return f"Recomendação para '{filme_escolhido['title']}': {filme_recomendado}"

def recommend_keyword_movie(keyword):
    # Filtrar filmes que contêm a palavra-chave no título
    filmes_selecionados = df[df['title'].str.lower().str.contains(keyword.lower())]
    filmes_selecionados = filmes_selecionados.sort_values(by='title')
    return [filme['title'] for _, filme in filmes_selecionados.iterrows()]

def recommend_movie_from_list(movies, user_choice):
    # Verifica se a escolha do usuário está dentro dos limites
    escolha_filme = int(user_choice)
    if 1 <= escolha_filme <= len(movies):
        filme_escolhido = df[df['title'] == movies[escolha_filme - 1]].iloc[0]
        return recomendar_filme(filme_escolhido)
    else:
        return "Escolha inválida. Por favor, escolha um número válido."

if __name__ == "__main__":
    # Teste da função recommend_keyword_movie
    keyword = input("Digite uma palavra-chave para encontrar filmes: ")
    movies_with_keyword = recommend_keyword_movie(keyword)
    print(f"Filmes com a palavra-chave '{keyword}': {movies_with_keyword}")

    # Teste da função recommend_movie_from_list
    user_choice = input("Escolha um número para o filme que você gosta: ")
    movies_list = recommend_keyword_movie(keyword)  # Use a mesma palavra-chave para gerar a lista
    recommendation_result = recommend_movie_from_list(movies_list, user_choice)
    print(recommendation_result)

