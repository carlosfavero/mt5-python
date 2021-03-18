# - Link oficial do exemplo:
# - https://www.mql5.com/pt/docs/integration/python_metatrader5/mt5copyratesfrom_py
# - MT5CopyRatesFrom(
# -    symbol,       // nome do símbolo
# -    timeframe,    // período gráfico
# -    from,         // data de abertura da barra inicial
# -    count         // número de barras
# -    )

import MetaTrader5 as mt5
from pytz import timezone
from datetime import datetime, timedelta
import pandas as pd

# display data on the MetaTrader 5 package
print("MetaTrader5 package author: ",mt5.__author__)
print("MetaTrader5 package version: ",mt5.__version__)

# - Passso - 01
# - Inicializando a conexão co MT5 e buscando os dados do ativo.
def inicializa(Ativo, Ano,Mes,Dia,QtdeBar,TimeFrame, mt5):
    utc_tz = timezone("America/Recife") #timezone("UTC")
    try:
        #MT5Initialize()
        # establish connection to MetaTrader 5 terminal
        if not mt5.initialize():
            print("initialize() failed, error code =",mt5.last_error())
            quit()
        #MT5WaitForTerminal()
        #mt5.wait()
        
        utc_from = datetime(Ano, Mes, Dia, tzinfo=utc_tz)        
        #ticksAtivo =  MT5CopyRatesFrom(Ativo, TimeFrame, utc_from, QtdeBar)
        barsAtivo =  mt5.copy_rates_from(Ativo, TimeFrame, utc_from, QtdeBar)       
        
        #MT5Shutdown()
        mt5.shutdown()
        return barsAtivo
    except Exception as e:
        raise e

# - Passso - 02
def prepareData(Ativo, Ano,Mes,Dia, QtdeBar, TimeFrame, mt5):  
    try:
        barsAtivo = inicializa(Ativo,Ano,Mes,Dia, QtdeBar, TimeFrame, mt5)
        
        df = pd.DataFrame(data=barsAtivo)
        # - Somente formatando a data para que Dataframe entenda a coluna como um objeto de datetime.
        df['time'] = pd.to_datetime(df.time,  unit='s', origin='unix')  
        #Renomeando coluna
        df.rename(columns = {'time':'date'}, inplace = True)
        # - Ajustando o horario UTC.
        #df['time'] += timedelta(hours=3)
        # - Ordenando os dados do mais novo para o mais antigo.
        df.set_index('date',inplace=True)
        df.sort_index(ascending=False, inplace=True) 
        
 
    except Exception as e:
        raise e
    df.symbol = Ativo
    return df

# - Ativo
_Ativo = "MGLU3"

# - Data inicio da busca dos dados historicos
_Ano = 2020
_Mes = 2
_Dia = 16  
# - Quantidade de barras solicitadas.
# - Pega 30 barras fechadas para traz da data solicitada. 
_QtdeBar = 30

# - Tempo grafico - M1, M5, M15, M30, H1, D1 etc...
# - Timeframe diario.
_TimeFrame = mt5.TIMEFRAME_D1

# - DataFrame do Pandas para armazenar os dados do MT5 - _Df_Ativo
# - Buscando os dados do MT5
_Df_Ativo = prepareData(_Ativo, _Ano,_Mes, _Dia, _QtdeBar, _TimeFrame, mt5)

# - Imprimindo na tela os 10 primeiros registros.
print(_Df_Ativo.head(10))