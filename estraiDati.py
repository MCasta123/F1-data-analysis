#Scarica dati della formula 1 tramite fastf1 e li esporta in un file CSV
import pandas as pd
import fastf1
import os
import matplotlib.pyplot as plt
import fastf1.plotting

fastf1.set_log_level('ERROR')
#definizioni funzioni di base per estrarre i dati

def scegli_anno():
    anniDisponibili=[2018,2019,2020,2021,2022,2023,2024,2025,2026]
    print("="*50)
    while True:
        anno=input('Che anno ti interessa? (2018-2026) ')
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

def formatta_tempo(secondi):
            if pd.isna(secondi): # Se il pilota non ha un tempo (es. giro di rientro)
                return "Box/Out"
            minuti = int(secondi // 60)
            sec = secondi % 60
            # Formatta con 2 cifre per i secondi e 3 per i millesimi (es. 05.123)
            return f"{minuti}:{sec:06.3f}"

class F1DataExtractor:

    def __init__(self,anno,gara,sessione,cartella_base='dati_csv'):
        self.anno=anno
        self.gara=gara
        self.sessione=sessione
        self.cartella_base=cartella_base

        #configurazione cache locale
        CACHE_DIR = "./f1_cache"
        os.makedirs(CACHE_DIR, exist_ok=True)
        fastf1.Cache.enable_cache(CACHE_DIR)
        #caricamento sessione
        self.session=fastf1.get_session(self.anno,self.gara,self.sessione)
        print('Loading...')
        try:
            self.session.load()
        except:
            print('Si è verificato un errore, è possibile che i dati di questa sessione non siano ancora stati caricati')

    def __scegli_pilota(self,stampa_lista_piloti=True):
        risultati=self.session.results
        pilotiNellaSessione=risultati['Abbreviation'].copy()
        pilotiNellaSessione=list(pilotiNellaSessione)
        colonne=['BroadcastName','Abbreviation']
        listaPiloti=risultati[colonne]
        if stampa_lista_piloti:
            print('La lista di piloti che partecipano a questa sessione è ')
            print(listaPiloti)
            print('-'*75)
        while True:
            pilotaScelto=input('Inserire l\'abbreviazione del pilota che si vuole scegliere: ')
            pilotaScelto=pilotaScelto.upper()
            if pilotaScelto in pilotiNellaSessione:
                return pilotaScelto
            else:
                print('Scelta errata, riprovare')
        
    def __estraiGiriSessione(self):
        #accedo ai tempi sul giro
        giri=self.session.laps
        try:
            
            giri['LapTime']=giri['LapTime'].dt.total_seconds()
            giri['Sector1Time']=giri['Sector1Time'].dt.total_seconds()
            giri['Sector2Time']=giri['Sector2Time'].dt.total_seconds()
            giri['Sector3Time']=giri['Sector3Time'].dt.total_seconds()
        except:
            print('Attenzione ai dati')
        return giri

    def printLapOfPilot(self):
        pilota=self.__scegli_pilota()
        giriPilota=self.session.laps.pick_drivers(pilota).copy()
        try:
            
            giriPilota['LapTime']=giriPilota['LapTime'].dt.total_seconds()
            giriPilota['Sector1Time']=giriPilota['Sector1Time'].dt.total_seconds()
            giriPilota['Sector2Time']=giriPilota['Sector2Time'].dt.total_seconds()
            giriPilota['Sector3Time']=giriPilota['Sector3Time'].dt.total_seconds()

            giriPilota['LapTime'] = giriPilota['LapTime'].apply(formatta_tempo)
            giriPilota['Sector1Time'] = giriPilota['Sector1Time'].apply(formatta_tempo)
            giriPilota['Sector2Time'] = giriPilota['Sector2Time'].apply(formatta_tempo)
            giriPilota['Sector3Time'] = giriPilota['Sector3Time'].apply(formatta_tempo)
        except:
            print('Attenzione ai dati')

        colonne=['Driver','Stint','LapTime','Sector1Time','Sector2Time','Sector3Time','Compound','TyreLife']
        giriPilota=giriPilota[colonne].to_string(index=False)
        print(giriPilota)
        
    def risultati_sessione(self):
        risultati=self.session.results
        colonne=['Position','FullName','Abbreviation','DriverNumber','TeamName','Points','Laps','BestLap']
        risultati['BestLap']=None
        risultati=risultati[colonne].copy()
        abbreviazionePiloti=risultati['Abbreviation']    
        
        for pilota in abbreviazionePiloti:
            giriPilota=self.session.laps.pick_drivers(pilota)
            if not giriPilota.empty:
                bestLap=giriPilota.pick_fastest()
                if bestLap is not None and pd.notna(bestLap['LapTime']):
                    bestLap=bestLap['LapTime'].total_seconds()
                    bestLap=formatta_tempo(bestLap)
                    condizione=abbreviazionePiloti==pilota
                    risultati.loc[condizione,'BestLap']=bestLap

        risultati=risultati.to_string(index=False)
        print(risultati)

    def fastestLapPilota(self):
        risultati=self.session.results
        abbreviazionePiloti=risultati['Abbreviation']
        colonne=['Abbreviation','FullName','BestLap']
        risultati['BestLap']=None
        risultati=risultati[colonne].copy()
        for pilota in abbreviazionePiloti:
            giriPilota=self.session.laps.pick_drivers(pilota)
            if not giriPilota.empty:
                bestLap=giriPilota.pick_fastest()
                if bestLap is not None and pd.notna(bestLap['LapTime']):
                    bestLap=bestLap['LapTime'].total_seconds()
                    bestLap=formatta_tempo(bestLap)
                    condizione=abbreviazionePiloti==pilota
                    risultati.loc[condizione,'BestLap']=bestLap
        risultati=risultati.sort_values(by='BestLap')
        risultati=risultati.to_string(index=False)
        print(risultati)
    
    def __estraiTelemetriaPilota(self,pilota):
        giriPilota=self.session.laps.pick_drivers(pilota)
        if giriPilota.empty:
            print(f"Attenzione: Nessun dato in pista per {pilota}.")
            return None
        giroVeloce=giriPilota.pick_fastest()
        if giroVeloce is None or pd.isna(giroVeloce['LapTime']):
            print(f'Il pilota {pilota} non ha giri validi in questa sessione')
        try:
            telemetria=giroVeloce.get_telemetry()
        except Exception as e:
            print(f"Errore durante il download della telemetria: {e}")
            return None
        colonne_utili = ['Distance', 'Speed', 'Throttle', 'Brake', 'nGear', 'RPM']
        telemetria_pulita = telemetria[colonne_utili].copy()
        return telemetria_pulita


    def stampaTelemetria(self):
        self.__estraiTelemetriaPilota('LEC')
        """ fastf1.plotting.setup_mpl(mpl_timedelta_support=True, color_scheme=None)
        while True:
            numPiloti=input('Scegli di quanti piloti vedere la telemetria: (max 4) ')
            try:
                numPiloti=int(numPiloti)
                if numPiloti<=0 or numPiloti>4:
                    print('Inserire un numero corretto')
                else:
                    break
            except:
                print('Inserire un numero')
        
        pilotiScelti=[]
        pilota=self.__scegli_pilota()
        pilotiScelti.append(pilota)
        i=0
        while numPiloti>1 and i<numPiloti-1:
            pilota=self.__scegli_pilota(stampa_lista_piloti=False)
            pilotiScelti.append(pilota)
            i=i+1 """
        






annoScelto=scegli_anno()
garaScelta=scegli_gara(anno=annoScelto)
sessioneScelta=scegli_sessione(anno=annoScelto,gara=garaScelta)
estraiDati=F1DataExtractor(anno=annoScelto,gara=garaScelta,sessione=sessioneScelta)
estraiDati.stampaTelemetria()


