import pandas as pd
import config as co



def dataframeFormatear(estructura, dataframe):
    for (i, item) in enumerate(estructura):
        dataframe[item['nombre']]=dataframe["original"].apply(lambda x:x[item['inicio']:item['fin']])
    del dataframe["original"]
    

def quitarNull(dataframe):
    dataframe = dataframe.fillna(0)


def main():
    ESTRUCTURA_LIQUIDACION = co.ESTRUCTURA
    data_liquitacion = co.LIQUIDA
    dataframeFormatear(ESTRUCTURA_LIQUIDACION, data_liquitacion)
    quitarNull(data_liquitacion)
    print(data_liquitacion)
    # print(data_liquitacion.dtypes)

main()