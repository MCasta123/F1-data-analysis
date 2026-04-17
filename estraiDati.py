#Scarica dati della formula 1 tramite fastf1 e li esporta in un file CSV
import pandas as pd
import fastf1
import os
import sys

#configurazione cache locale
CACHE_DIR = "./f1_cache"
os.makedirs(CACHE_DIR, exist_ok=True)
fastf1.Cache.enable_cache(CACHE_DIR)

#definizioni funzioni di base per estrarre i dati

def scegli_anno():
    anniDisponibili=[2018,2019,2020,2021,2022,2023,2024]
    print("="*50)
    while True:
        anno=input('Che anno ti interessa? (2018-2024) ')
        try:
            anno=int(anno)
            if anno in anniDisponibili:
                print('Anno trovato')
                break
            else:
                print('Inserire un anno giusto!')
        except:
            print('Inserire un anno!')
    return anno

def scegli_gara(anno):
    print(f'Le gare dell anno {anno} sono: ')
    schedule = fastf1.get_event_schedule(anno,include_testing=False)
    eventi=schedule['EventName'].tolist()
    i=1
    for ev in eventi:
        print(f'{i} : {ev}')
        i=i+1
    while True:
        garaScelta=input('Inserire il numero della gara desiderata: ')
        try:
            garaScelta=int(garaScelta)
            if garaScelta>0 and garaScelta<=i:
                break
            else:
                print('Inserire un numero adeguato')
        except:
            print('Errore riprovare')
    return eventi[garaScelta-1]

def scegli_sessione(anno,gara):
    session=fastf1.get_event(anno,gara)
    print('Per questo weekend di gara, le sessioni sono: ')
    listaSessioni=[]
    for i in range(1,6):
        listaSessioni.append(session[f'Session{i}'])
        print(f'{i} : '+session[f'Session{i}'])
    while True:
        sessioneScelta=input('A quale sessione sei interessato? (1-5) ')
        try:
            sessioneScelta=int(sessioneScelta)
            if sessioneScelta in range(1,6):
                return listaSessioni[sessioneScelta-1]
            else:
                print('Seleziona una sessione disponibile')
        except:
            print('ERRORE, riprovare!')




        






annoScelto=scegli_anno()
garaScelta=scegli_gara(anno=annoScelto)
sessioneScelta=scegli_sessione(anno=annoScelto,gara=garaScelta)

#session = fastf1.get_session(2021, 'Monza', 'Qualifying')

