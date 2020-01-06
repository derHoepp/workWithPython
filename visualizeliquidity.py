import pandas as pd
import matplotlib.pyplot as plt
import os
import datetime 
import numpy as np

infile = os.path.join(os.path.dirname(__file__),"liquiverb.txt")

dataframe = pd.read_csv(infile,
                        sep="\t",
                        parse_dates=["Buc.dat."],
                        dayfirst=True,
                        thousands=",",
                        decimal="."
                        )
dataframe.dropna(axis=1, inplace=True)

def kategorie(konto):
    if str(konto).startswith("1"):
        return "LiquideMittel"
    else:
        return "Verbindlichkeiten"

dataframe["Kategorie"] = dataframe["Hauptbuch"].map(kategorie)

vodict={"LiquideMittelS":1.0,
            "LiquideMittelH":-1.0,
            "VerbindlichkeitenS":-1.0,
            "VerbindlichkeitenH":1.0}
dataframe["Vorzeichen"] = dataframe["Kategorie"].str.cat(dataframe["S/H"])
dataframe["Vorzeichen"].replace(vodict, inplace=True)
dataframe["Betrag"] = (dataframe["Betrag Hauswährung EUR"] *
                        dataframe["Vorzeichen"])

dataframe.drop(["Vorzeichen","Hauptbuch", "S/H", "Betrag Hauswährung EUR"],
               axis=1,
               inplace=True)

df = dataframe.groupby(["Buc.dat.","Kategorie"],as_index = False).sum()
v1 = df.copy()
del(dataframe)
verbi = v1.query('Kategorie=="Verbindlichkeiten"')
liqui = df.query('Kategorie=="LiquideMittel"')

verbi["kumuliert"] = verbi["Betrag"].cumsum()
liqui["kumuliert"] = liqui["Betrag"].cumsum()

verbidate = list(verbi["Buc.dat."])
verbivalu = list(verbi["kumuliert"])
liquidate = list(liqui["Buc.dat."])
liquivalu = list(liqui["kumuliert"])

fig1 = plt.figure(1)
plt.plot(verbidate, verbivalu)
plt.plot(liquidate, liquivalu)
plt.show()
