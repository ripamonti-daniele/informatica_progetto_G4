import flet as ft

def carica_domanda(n_domanda):
    avanti = False
    try:
        f = open("percorsi_foto.txt", "r", encoding="utf-8")
        avanti = True
    except FileNotFoundError:
        print("file non trovato")
        
    if avanti:
        percorsi = []
        x = 0
        for r in f:
            r = r.strip("\n")
            if r == "|":
                x += 1
            if x == n_domanda:
                for i in range(8):
                    percorsi.append(f.readline().strip("\n"))
                break        
                
        f.close()
        return percorsi

def main(page: ft.Page):
    page.window.width = 1200
    page.window.height = 900
    page.title = "Test del quoziente intellettivo"
    page.vertical_alignment = ft.MainAxisAlignment.START
    
    def crea_domanda(n_domanda):
        percorsi = carica_domanda(n_domanda)
        img_domanda.src = percorsi[0]
        
        for i in range(len(img_opzioni)):
            img_opzioni[i].visible = True
            img_opzioni[i].src = percorsi[i + 1]
    
        risposte_corrette.append(percorsi[7])
    
    def attiva_inizio(e):
        if e.data != None:
            inizio.disabled = False
            inizio.update()
        
    def start(e):
        titolo1.visible = False
        testo1.visible = False
        inizio.visible = False
        range_età.visible = False
        testo_domanda.visible = True
        domanda.visible = True
        img_domanda.visible = True
        opzioni.visible = True
        successivo.visible = True
        precedente.visible = True
        termina.visible = True
        for i in range(len(img_opzioni)):
            img_opzioni[i].visible = True
        page.update()
        
    def succ(e):
        if opzioni.value == None:
            opzioni.value = ""
        if opzioni.value != "":
            risposte_utente[domanda.value - 1] = opzioni.value
        #print(risposte_utente)
        domanda.value += 1
        opzioni.value = risposte_utente[domanda.value - 1]
        crea_domanda(domanda.value)
        if domanda.value == 20:
            successivo.disabled = True
        if domanda.value > 1:
            precedente.disabled = False
        page.update()
    
    def prec(e):
        if opzioni.value == None:
            opzioni.value = ""
        if opzioni.value != "":
            risposte_utente[domanda.value - 1] = opzioni.value
        # print(risposte_utente)
        domanda.value -= 1
        opzioni.value = risposte_utente[domanda.value - 1]
        crea_domanda(domanda.value)
        if domanda.value == 1:
            precedente.disabled = True
        if domanda.value < 20:
            successivo.disabled = False
        page.update()
        
    def attiva_termina(e):
        risposte_vuote = risposte_utente.count("")
        if risposte_vuote == 1 and opzioni.value != "":
            termina.disabled = False
        termina.update()
        
    def fine(e):
        testo_domanda.visible = False
        domanda.visible = False
        img_domanda.visible = False
        opzioni.visible = False
        successivo.visible = False
        precedente.visible = False
        termina.visible = False
        for i in range(len(img_opzioni)):
            img_opzioni[i].visible = False
        page.update()
    
    # schermata iniziale
    titolo1 = ft.Text("Test del QI: cos'è e a cosa serve", size=40)
    testo1 = ft.Text(size=20, width = 1000, text_align=ft.TextAlign.CENTER, value="Il test del quoziente intellettivo (QI) è uno strumento pensato per misurare le capacità cognitive di una persona, cioè il modo in cui ragiona, comprende concetti, risolve problemi e apprende nuove informazioni.\nIl suo scopo principale è quello di offrire un'indicazione generale dell'intelligenza, confrontando i risultati di una persona con la media della popolazione, che è fissata a un punteggio di 100.\nDurante il test vengono proposti diversi tipi di esercizi che coinvolgono il ragionamento logico, la memoria, l’abilità nel riconoscere schemi, la comprensione del linguaggio e la capacità di lavorare con numeri o immagini.\nNon serve conoscere nozioni specifiche: si tratta più di capire come pensi e quanto velocemente riesci a elaborare le informazioni.\nIl risultato del test può essere utile per varie ragioni: da un lato, aiuta a conoscere meglio se stessi e a scoprire i propri punti di forza mentali, dall’altro, può offrire un’indicazione utile per chi sta cercando di capire quale tipo di studio o percorso lavorativo potrebbe essere più adatto.\nIn alcuni casi, è anche semplicemente un modo per sfidare la propria mente in modo stimolante e divertente.\n")
    inizio = ft.Button(text="Inizia", on_click=start, width=150, height=50, style=ft.ButtonStyle(text_style=ft.TextStyle(size=20)), bgcolor="#ffff66", disabled=True)
    range_età = ft.Dropdown(
        width=300,
        label="Inserisci la tua età",
        options=[
            ft.dropdown.Option(i)
            for i in ["< 16", "16 - 20", "21 - 30", "31 - 40", "41 - 50", "51 - 60", "> 60"]
        ],
        on_change=attiva_inizio
    )
    
    # domande test
    risposte_utente = ["", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", ""]
    risposte_corrette = []
    domanda = ft.Text(1, size=40, visible=False)
    testo_domanda = ft.Text("Domanda", size=40, visible=False)
    img_domanda = ft.Image(src="immagini\d1\domanda1.png", visible=False)
    img_opzioni = [
            ft.Image(src="immagini\d1\d1_risposta_A.png", visible=False),
            ft.Image(src="immagini\d1\d1_risposta_B.png", visible=False),
            ft.Image(src="immagini\d1\d1_risposta_C.png", visible=False),
            ft.Image(src="immagini\d1\d1_risposta_D.png", visible=False),
            ft.Image(src="immagini\d1\d1_risposta_E.png", visible=False),
            ft.Image(src="immagini\d1\d1_risposta_F.png", visible=False)
        ]
    opzioni = ft.RadioGroup(visible=False, on_change=attiva_termina, content=ft.Row([
            ft.Radio(value="A", label="A                     ", scale=1.2),
            ft.Radio(value="B", label="B                     ", scale=1.2),
            ft.Radio(value="C", label="C                     ", scale=1.2),
            ft.Radio(value="D", label="D                     ", scale=1.2),
            ft.Radio(value="E", label="E                     ", scale=1.2),
            ft.Radio(value="F", label="F                  ", scale=1.2)
        ]))
    img_domanda = ft.Image(src="immagini\d1\domanda2.png", visible=False)
    img_opzioni = [
            ft.Image(src="immagini\d1\d1_risposta_A.png", visible=False),
            ft.Image(src="immagini\d1\d1_risposta_B.png", visible=False),
            ft.Image(src="immagini\d1\d1_risposta_C.png", visible=False),
            ft.Image(src="immagini\d1\d1_risposta_D.png", visible=False),
            ft.Image(src="immagini\d1\d1_risposta_E.png", visible=False),
            ft.Image(src="immagini\d1\d1_risposta_F.png", visible=False)
        ]
    opzioni = ft.RadioGroup(visible=False, on_change=attiva_termina, content=ft.Row([
            ft.Radio(value="A", label="A                     ", scale=1.2),
            ft.Radio(value="C", label="B                     ", scale=1.2),
            ft.Radio(value="B", label="C                     ", scale=1.2),
            ft.Radio(value="D", label="D                     ", scale=1.2),
            ft.Radio(value="E", label="E                     ", scale=1.2),
            ft.Radio(value="F", label="F                  ", scale=1.2)
        ]))
    successivo = ft.Button(text="Successivo", on_click=succ, width=150, height=50, style=ft.ButtonStyle(text_style=ft.TextStyle(size=20)), bgcolor="#ffff66", disabled=False, visible=False)
    precedente = ft.Button(text="Precedente", on_click=prec, width=150, height=50, style=ft.ButtonStyle(text_style=ft.TextStyle(size=20)), bgcolor="#ffff66", disabled=True, visible=False)
    termina = ft.Button(text="Termina", on_click=fine, width=150, height=50, style=ft.ButtonStyle(text_style=ft.TextStyle(size=20)), bgcolor="#ffff66", disabled=True, visible=False)
        
    page.add(
        ft.Row(
            [
                ft.Column(
                    [
                        titolo1, testo1, range_età, inizio
                    ],
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER
                ),
                ft.Column(
                    [
                        ft.Row([testo_domanda, domanda]), img_domanda, opzioni, ft.Row(img_opzioni), ft.Row([precedente, successivo, termina])
                    ],
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER
                )
            ],
            alignment=ft.MainAxisAlignment.CENTER
        )
    )

ft.app(main)