from tkinter import *
from PIL import Image, ImageTk
from dataframe import main
import unicodedata

root = Tk()
path = 4
stage = 0
fails = 0
interaction = 0
profile = []


def remove_accents(b):
    normalized = unicodedata.normalize('NFKD', b)
    return ''.join([c for c in normalized if not unicodedata.combining(c)])


def click(event=None):
    global path
    global stage
    global fails
    global interaction
    global profile

    welcome_message = ('Olá! Vai ser um prazer ajudar!' + '\n' + 'Você deseja uma recomendação por filme ou por perguntas?')

    send = 'Você: ' + a.get()
    text.insert(END, '\n' + send)
    user_input = a.get().lower()
    user_input = remove_accents(user_input)

    path1_keywords = ['perguntas', 'pergunta']
    path2_keywords = ['filme', 'filmes', 'titulo', 'titulos']
    hello_keywords = ['ola', 'oi', 'eai', 'salve', 'tudo bom?', 'tudo bem?']
    bye_keywords = ['tchau', 'valeu', 'obrigado', 'ajudou', 'falou', 'ate']
    goback_keywords = ['mudei de ideia', 'voltar', 'volta', 'recomecar', 'reiniciar', 'de novo', 'do comeco']

    if interaction == 0:
        if any(keyword in user_input for keyword in hello_keywords):
            interaction = 1
            path = 0
        else:
            text.insert(END, '\n' + 'Bot: Se precisar de algo é só me dar um Oi.')

    if path == 0:
        if any(keyword in user_input for keyword in path1_keywords):
            path = 1
            text.insert(END, '\n' + 'Bot: Qual seu gênero favorito?')
        elif any(keyword in user_input for keyword in path2_keywords):
            path = 2
            text.insert(END, '\n' + 'Bot: Digite uma palavra chave do filme (em inglês):')
        elif any(keyword in user_input for keyword in bye_keywords):
            text.insert(END, '\n' + 'Bot: Foi um prazer ajudar! Volte sempre.')
        elif any(keyword in user_input for keyword in hello_keywords):
            if interaction == 0:
                text.insert(END, '\n')
            else:
                text.insert(END, '\n' + 'Olá! Vai ser um prazer ajudar!' + '\n' + 'Você deseja uma recomendação por filme ou por perguntas?')
        elif any(keyword in user_input for keyword in goback_keywords):
            if fails == 5:
                text.insert(END, '\n' + 'Bot: Parece que você está com dificuldades para utilizar o chat...' + '\n' + 'Entre em contato com nosso supervisor: https://chat.openai.com/')
            else:
                fails += 1
                profile = []
                text.delete('1.0', END)
                canvas.delete('all')
                text.insert(END, 'Bot: Sem problemas! Vamos do começo...' + '\n' + '\n')
                text.insert(END, welcome_message)
        else:
            text.insert(END, '\n' + 'Bot: Desculpe, não entendi o que você quis dizer.')
    elif path == 1:
        genres_keywords = ['animacao', 'drama', 'romance', 'ficcao', 'cientifica']
        duration_keywords = ['curto', 'medio', 'longo', 'curtos', 'medios', 'longos']
        release_keywords = ['antes de 2000', 'depois de 2000', 'antes', 'depois', 'velho', 'novo', 'antigo', 'antes dos anos 2000', 'depois dos anos 2000']
        if stage == 0:
            if any(keyword in user_input for keyword in genres_keywords):
                if 'animacao' in user_input:
                    user_input = 'animacao'
                elif 'drama' in user_input:
                    user_input = 'drama'
                elif 'romance' in user_input:
                    user_input = 'romance'
                elif any(keyword in user_input for keyword in ['ficcao', 'cientifica']):
                    user_input = 'ficcao'
                profile.append(user_input)
                stage = 1
                text.insert(END, '\n' + 'O filme precisa ser longo, médio ou curto?')

            elif any(keyword in user_input for keyword in goback_keywords):
                path = 0
                stage = 0
                profile = []
                text.delete('1.0', END)
                text.insert(END, '\n' + 'Bot: Sem problemas! Vamos do começo...' + '\n' + '\n')
                text.insert(END, welcome_message)
            else:
                text.insert(END, '\n' + 'Bot: Desculpe, ainda não temos boas recomendações para esse gênero.' + '\n' + 'Experimente uma recomendação com base em um filme de sua escolha!')
        elif stage == 1:
            if any(keyword in user_input for keyword in duration_keywords):
                if any(keyword in user_input for keyword in ['medio', 'longo', 'medios', 'longos']):
                    user_input = 'longo'
                elif any(keyword in user_input for keyword in ['curto', 'curtos']):
                    user_input = 'curto'
                profile.append(user_input)
                stage = 2
                text.insert(END, '\n' + 'O filme precisa ter sido lançado antes ou depois dos anos 2000?')
            elif any(keyword in user_input for keyword in goback_keywords):
                path = 0
                stage = 0
                profile = []
                text.delete('1.0', END)
                text.insert(END, '\n' + 'Bot: Sem problemas! Vamos do começo...' + '\n' + '\n')
                text.insert(END, welcome_message)
            else:
                text.insert(END, '\n' + 'Bot: Desculpe, não entendi o que você quis dizer.')
        elif stage == 2:
            if any(keyword in user_input for keyword in release_keywords):
                if any(keyword in user_input for keyword in ['antes de 2000', 'antes', 'velho', 'antes dos anos 2000', 'antigo']):
                    user_input = 'antigo'
                elif any(keyword in user_input for keyword in ['depois de 2000', 'depois', 'depois dos anos 2000', 'novo']):
                    user_input = 'novo'
                text.insert(END, '\n' + 'Achamos um filme para você...')
                profile.append(user_input)
                print(profile)
                display_image(recommend_movie(profile))
                path = 0
                stage = 0
                fails = 0
                text.insert(END, '\n')

            elif any(keyword in user_input for keyword in goback_keywords):
                path = 0
                stage = 0
                profile = []
                text.insert(END, '\n' + 'Bot: Sem problemas! Vamos do começo...' + '\n' + '\n')
                text.insert(END, welcome_message)
            else:
                text.insert(END, '\n' + 'Bot: Desculpe, não entendi o que você quis dizer.')
        else:
            path = 0
            stage = 0
            profile = [0] * len(profile)
            text.insert(END, '\n' + 'Bot: Algo deu errado mas sem problemas! Vamos do começo...' + '\n' + '\n')
            text.insert(END, welcome_message)
    elif path == 2:
        if 'algo diferente' in user_input:
            text.insert(END, '\n' + 'Bot: Resposta específica para algo diferente no path2')
        else:
            text.insert(END, '\n' + 'Bot: Outra resposta no path2')

    text.yview(END)
    a.delete(0, 'end')


def recommend_movie(profile):
    movies = {
        'drama_curto_antigo': 'Reservoir Dogs',
        'drama_curto_novo': 'Nightcrawler',
        'drama_longo_antigo': 'GoodFellas',
        'drama_longo_novo': 'Inglourious Basterds',
        'romance_curto_antigo': 'When Harry Met Sally...',
        'romance_curto_novo': '(500) Days of Summer',
        'romance_longo_antigo': 'The Age of Innocence',
        'romance_longo_novo': 'La La Land',
        'ficcao_curto_antigo': 'Blade Runner',
        'ficcao_curto_novo': 'Ex Machina',
        'ficcao_longo_antigo': 'Star Wars: Episode VI - Return of the Jedi',
        'ficcao_longo_novo': 'Blade Runner 2049',
        'animacao_curto_antigo': 'Beauty and the Beast',
        'animacao_curto_novo': 'Up',
        'animacao_longo_antigo': 'Akira',
        'animacao_longo_novo': 'Spider-Man: Into the Spider-Verse'
    }
    key = '_'.join(profile)
    if key in movies:
        recommendation = movies[key]
        text.insert(END, '\n' + '---' + recommendation + '---')
        display_image(recommendation)
    else:
        text.insert(END, '\n' + 'Não achamos nenhum filme para você!')

    return recommendation


def display_image(recomendation):
    canvas.delete('all')

    posters = {
        'Reservoir Dogs': './src/Reservoir Dogs.jpg',
        'Nightcrawler': './src/Nightcrawler.jpg',
        'GoodFellas': './src/GoodFellas.jpg',
        'Inglourious Basterds': './src/Inglourious Basterds.jpg',
        'When Harry Met Sally...': './src/When Harry Met Sally.jpg',
        '(500) Days of Summer': './src/(500) Days of Summer.jpg',
        'The Age of Innocence': './src/The Age of Innocence.jpg',
        'La La Land': './src/LaLaLand.jpg',
        'Blade Runner': './src/Blade Runner.jpg',
        'Ex Machina': './src/Ex Machina.jpg',
        'Star Wars: Episode VI - Return of the Jedi': './src/Star Wars Episode VI Return of the Jedi.jpg',
        'Blade Runner 2049': './src/Blade Runner 2049.jpg',
        'Beauty and the Beast': './src/Beauty and the Beast.jpg',
        'Up': './src/Up.jpg',
        'Akira': './src/Akira.jpg',
        'Spider-Man: Into the Spider-Verse': './src/Spider-Man Into the Spider-Verse.jpg'
    }

    poster_path = posters[recomendation]
    image = Image.open(poster_path)
    image = image.resize((360, 590), Image.BICUBIC)
    tk_image = ImageTk.PhotoImage(image)
    canvas.image = tk_image
    canvas.create_image(0, 0, anchor='nw', image=tk_image)


# config do chat
text = Text(root, bg='#333333', fg='white', highlightbackground='gray')
text.configure(font=('Arial', 18))
text.grid(row=0, column=0, columnspan=2)

canvas = Canvas(root, bg='#333333', width=360, height=590)
canvas.grid(row=0, column=2, sticky="nsew")

a = Entry(root, width=40)
a.grid(row=1, column=0, sticky="nsew")
Button(root, text='Enviar', bg='white', width=20, command=click).grid(row=1, column=1)

root.title('Letterbotd')
root.bind('<Return>', click)
root.resizable(True, True)
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)

root.mainloop()
