import flet as ft

def main(page: ft.Page):
    #impostazioni base della pagina
    page.window.width = 1200
    page.window.height = 900
    page.title = "Test del quoziente intellettivo"
    page.vertical_alignment = ft.MainAxisAlignment.START
    
    def carica_domanda(n_domanda): #per ogni domanda prende immagini e risposte
        avanti = False
        try:
            f = open("percorsi_foto.txt", "r", encoding="utf-8")
            avanti = True
        except FileNotFoundError:
            print("file non trovato")
            
        if avanti:
            percorsi = []
            x = 0
            # con questo ciclo si contano i pipe (|) per trovare la posizione dei percorsi
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
    
    def carica_dati(range_eta): #prende i dati dei test qi già svolti
        errore = True
        try:
            f = open("risultati.txt", "r", encoding="utf-8")
            errore = False
        except:
            print("errore: file non trovato")
        
        if not(errore):
            tot = []
            tot_eta = []
            
            #questo ciclo aggiunge alla lista tot tutti i risulati e alla lista tot_eta tutti i risultati del range d'età preso come parametro
            for r in f:
                r = r.replace("\n", "")
                dati = r.split("|")
                tot.append(int(dati[0]))
                if dati[1] == range_eta:
                    tot_eta.append(int(dati[0]))
            f.close()
            
            # calcolo qi medio generale e nel range d'età
            somma = 0
            for i in tot:
                somma += i
            media_tot = somma // len(tot)
            somma = 0
            
            for i in tot_eta:
                somma += i
            media_eta = somma // len(tot_eta)
            
            return media_tot, media_eta
    
    def salva_dati(punteggio, range_eta): # aggiunge sul file il risultato del test eseguito con il range d'età selezionato all'inizio
        errore = True
        try:
            f = open("risultati.txt", "a", encoding="utf-8")
            errore = False
        except:
            print("errore: file non trovato")
        
        if not(errore):
            f.write(str(punteggio) + "|" + range_eta + "\n")
            f.close()
        
    def crea_domanda(n_domanda): # prende le domande e mette i loro percorsi come src delle immagini
        percorsi = carica_domanda(n_domanda)
        img_domanda.src = percorsi[0]
        
        for i in range(len(img_opzioni)):
            img_opzioni[i].visible = True
            img_opzioni[i].src = percorsi[i + 1]
    
        risposte_corrette.append(percorsi[7]) # salva la risposta corretta
    
    def attiva_inizio(e): # una volta scelto il range d'età attiva il pulsante inizio
        if e.data != None:
            inizio.disabled = False
            inizio.update()
        
    def start(e): # rimuove gli elementi mostrati all'inizio e mostra quelli necessari per svolgere il test
        titolo1.visible = False
        testo1.visible = False
        testo2.visible = False
        inizio.visible = False
        range_età.visible = False
        testo_domanda.visible = True
        domanda.visible = True
        img_domanda.visible = True
        opzioni.visible = True
        successivo.visible = True
        precedente.visible = True
        termina.visible = True
        crea_domanda(domanda.value) # prende i percorsi della prima domanda e li applica alle immagini
        for i in range(len(img_opzioni)):
            img_opzioni[i].visible = True
        page.update()
        
    def succ(e): # passa alla domanda successiva salvando la risposta selezionata dall'utente
        if opzioni.value == None:
            opzioni.value = ""
        if opzioni.value != "":
            risposte_utente[domanda.value - 1] = opzioni.value
            
        domanda.value += 1
        opzioni.value = risposte_utente[domanda.value - 1]
        crea_domanda(domanda.value)
        
        # se si trova alla domanda 20 disabilita il pulsante successivo, se si sposta dalla domanda 1 attiva il pulsante precedente
        if domanda.value == 20:
            successivo.disabled = True
        if domanda.value > 1:
            precedente.disabled = False
        page.update()
    
    def prec(e): # passa alla domanda precedente salvando la risposta selezionata dall'utente
        if opzioni.value == None:
             opzioni.value = ""
        if opzioni.value != "":
            risposte_utente[domanda.value - 1] = opzioni.value
            
        domanda.value -= 1
        opzioni.value = risposte_utente[domanda.value - 1]
        crea_domanda(domanda.value)
        
        # se si trova alla domanda 1 disabilita il pulsante precedente, se si sposta dalla domanda 20 attiva il pulsante successivo
        if domanda.value == 1:
            precedente.disabled = True
        if domanda.value < 20:
            successivo.disabled = False
        page.update()
        
    def controlla_termina(e): # verifica che l'utente abbia risposto a tutte le domanda prima di finire il test
        if opzioni.value == None:
             opzioni.value = ""
        if opzioni.value != "":
            risposte_utente[domanda.value - 1] = opzioni.value

        if "" in risposte_utente: # se ci sono delle domande senza risposta viene aperto un popup che indica quali domande mancano
            apri_popup(e)
        
        else:
            risultati(e)
            fine(e)

        page.update()
        
    def apri_popup(e): # funzione che apre il popup
        # con questo ciclo vengono trovate le domande a cui non si ha ancora risposto
        testo = "Non hai risposto alle domande: "
        for i in range(len(risposte_utente)):
            if risposte_utente[i] == "":
                testo += str(i + 1) + ", "
        testo = testo[:-2]
        popup.content = ft.Text(testo, size = 16)
         
        page.open(popup)
        page.update()
        
    def risultati(e): # calcola il qi in base alle riosposte e prende i dati del file per fornire dei valori medi di confronto
        # calcolo punteggio
        punteggio = 0
        for i in range(len(risposte_utente)):
            if risposte_utente[i] == risposte_corrette[i]:
                punteggio += 3

        # i minori di 16 anni e le persone nel range 16 - 20 hanno un piccolo aumento del risulato in quanto le domade sono realizzate per persone adulte e non in fase di sviluppo
        if range_età.value == "< 16": 
            punteggio += punteggio * 0.25
        elif range_età.value == "16 - 20":
            punteggio += punteggio * 0.15
        punteggio = int(round(punteggio, 0))
        punteggio += 70
        
        qi.value = f"Il tuo QI è {punteggio}"
        salva_dati(punteggio, range_età.value) # salva il punteggio
        
        #prende i risultati medi
        media_tot, media_eta = carica_dati(range_età.value)
        
        qi_medio.value = f"QI medio: {media_tot}"
        qi_medio_eta.value = f"QI medio nel range d'età {range_età.value} : {media_eta}"
        
        if media_tot > punteggio:
            qi_medio.color = "red"
        else:
            qi_medio.color = "green"
        if media_eta > punteggio:
            qi_medio_eta.color = "red"
        else:
            qi_medio_eta.color = "green"
        
    def fine(e): # rimuove gli elementi del test per mostrare i dati finali
        testo_domanda.visible = False
        domanda.visible = False
        img_domanda.visible = False
        opzioni.visible = False
        successivo.visible = False
        precedente.visible = False
        termina.visible = False
        riepilogoText.visible = True
        riepilogoText.value = "Test completato con successo!"
        qi.visible = True
        qi_medio.visible = True
        qi_medio_eta.visible = True
        for i in range(len(img_opzioni)):
            img_opzioni[i].visible = False
        page.vertical_alignment = ft.MainAxisAlignment.CENTER
        page.update()
    
    # schermata iniziale
    titolo1 = ft.Text("Test del QI: cos'è e a cosa serve", size=40)
    testo1 = ft.Text(size=20, width = 1000, text_align=ft.TextAlign.CENTER, value="Il test del quoziente intellettivo (QI) è uno strumento pensato per misurare le capacità cognitive di una persona, cioè il modo in cui ragiona, comprende concetti, risolve problemi e apprende nuove informazioni.\nIl suo scopo principale è quello di offrire un'indicazione generale dell'intelligenza, confrontando i risultati di una persona con la media della popolazione, che è fissata a un punteggio di 100.\nDurante il test vengono proposti diversi tipi di esercizi che coinvolgono il ragionamento logico, la memoria, l’abilità nel riconoscere schemi, la comprensione del linguaggio e la capacità di lavorare con numeri o immagini.\nNon serve conoscere nozioni specifiche: si tratta più di capire come pensi e quanto velocemente riesci a elaborare le informazioni.\nIl risultato del test può essere utile per varie ragioni: da un lato, aiuta a conoscere meglio se stessi e a scoprire i propri punti di forza mentali, dall’altro, può offrire un’indicazione utile per chi sta cercando di capire quale tipo di studio o percorso lavorativo potrebbe essere più adatto.\nIn alcuni casi, è anche semplicemente un modo per sfidare la propria mente in modo stimolante e divertente.")
    testo2 = ft.Text(size=25, width = 1000, text_align=ft.TextAlign.CENTER, value="Importante: i risultati di questo test sono delle stime non scientifiche in quanto vengono utilizzati dati e criteri non ufficiali.\n", weight=ft.FontWeight.BOLD)
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
    
    # elementi domande test
    risposte_utente = ["", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", ""]
    risposte_corrette = []
    domanda = ft.Text(1, size=40, visible=False)
    testo_domanda = ft.Text("Domanda", size=40, visible=False)
    img_domanda = ft.Image(src="immagini\d1\domanda1.png", visible=False, width=400, height=400)
    img_opzioni = [
            ft.Image(src="immagini\d1\d1_risposta_A.png", visible=False, width=128, height=128),
            ft.Image(src="immagini\d1\d1_risposta_B.png", visible=False, width=128, height=128),
            ft.Image(src="immagini\d1\d1_risposta_C.png", visible=False, width=128, height=128),
            ft.Image(src="immagini\d1\d1_risposta_D.png", visible=False, width=128, height=128),
            ft.Image(src="immagini\d1\d1_risposta_E.png", visible=False, width=128, height=128),
            ft.Image(src="immagini\d1\d1_risposta_F.png", visible=False, width=128, height=128)
        ]
    opzioni = ft.RadioGroup(visible=False, content=ft.Row([
            ft.Radio(value="A", label="A                     ", scale=1.2),
            ft.Radio(value="B", label="B                     ", scale=1.2),
            ft.Radio(value="C", label="C                     ", scale=1.2),
            ft.Radio(value="D", label="D                     ", scale=1.2),
            ft.Radio(value="E", label="E                     ", scale=1.2),
            ft.Radio(value="F", label="F         ", scale=1.2)
        ]))
    successivo = ft.Button(text="Successivo", on_click=succ, width=150, height=50, style=ft.ButtonStyle(text_style=ft.TextStyle(size=20)), bgcolor="#ffff66", disabled=False, visible=False)
    precedente = ft.Button(text="Precedente", on_click=prec, width=150, height=50, style=ft.ButtonStyle(text_style=ft.TextStyle(size=20)), bgcolor="#ffff66", disabled=True, visible=False)
    termina = ft.Button(text="Termina", on_click=controlla_termina, width=150, height=50, style=ft.ButtonStyle(text_style=ft.TextStyle(size=20)), bgcolor="#ffff66", disabled=False, visible=False)
    
    popup = ft.AlertDialog(
        modal=True,
        title=ft.Text("Attenzione"),
        content=ft.Text("Non hai risposto a tutte le domande", size = 16),
        actions=[
            ft.TextButton("Ok", on_click=lambda e: page.close(popup), scale=1.3)
        ],
    )
    
    # dati finali
    riepilogoText = ft.Text(color="green", size=40, visible=False, weight=ft.FontWeight.BOLD)
    qi = ft.Text("", size=40, visible=False)
    qi_medio = ft.Text("", size=40, visible=False)
    qi_medio_eta = ft.Text("", size=40, visible=False)

    # messa a schermo elementi
    page.add(
        ft.Row(
            [
                ft.Column(
                    [
                        titolo1, testo1, testo2, range_età, inizio
                    ],
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER
                ),
                ft.Column(
                    [
                        ft.Row([testo_domanda, domanda]), img_domanda, opzioni, ft.Row(img_opzioni), ft.Row([precedente, successivo, termina]), riepilogoText
                    ],
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER
                ),
                ft.Column(
                    [
                        riepilogoText, qi, qi_medio, qi_medio_eta
                    ],
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER
                ),
            ],
            alignment=ft.MainAxisAlignment.CENTER
        )
    )

ft.app(main)

#TODO mettere il timer