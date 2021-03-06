

""" Deutlich abweichender Ansatz
    Geeignet, um "geschlossene" Bereiche zu erkennen, also z.B. Kreise im zweidimenisonalen 
    Raum oder Cluster im Allgemeinen. 
    Der RBF-Kernel ist sehr nützlich, wenn man wenige Merkmale und eine moderate Anzahl 
    von Samples hat, da viele Merkmale den Algorithmus drastisch verlangsamen können. 
    Außerdem, wird dieser Kernel häufiger verwendet, weil normalierweise nichtlineare 
    Kernel genauer als lineare sind. """


## ##########################
## Teil 0: Einlesen der Daten
## ##########################

import pandas as pd

df = pd.read_csv("./Python_Training/Machine Learning/Klassifikation/CSV/classification.csv")


## ################################################################
## Teil 1: Aufteilung in Trainings- und Testdaten (hier: 75% / 25%)
## ################################################################

from sklearn.model_selection import train_test_split

# Welche Spalten sollen zur Vorhersage verwendet werden
X = df[["age", "interest"]].values

""" Oder: Die Spalte "success" soll nicht zur Vorhersage verwendet werden:
    X = df.drop("success", axis = 1).values """

y = df["success"].values

X_train, X_test, y_train, y_test = train_test_split(X, y, random_state = 0, test_size = 0.25)


## #######################
## Teil 2: Daten skalieren
## #######################

from sklearn.preprocessing import StandardScaler

scaler = StandardScaler()
scaler.fit(X_train)

X_train = scaler.transform(X_train)
X_test = scaler.transform(X_test)


## #####################
## Teil 3: Anwendung SVC
## #####################

from sklearn.svm import SVC
import numpy as np

""" gamma = Gewichtung Sigma, Parameter C = Gewichtung einzelner Punkte """
model = SVC(kernel = "rbf", gamma = 0.2, C = 1)
model.fit(X_train, y_train)

print(model.score(X_test, y_test))


## ##########################
## Teil 4: Ergebnisse plotten
## ##########################

""" Hinweis: Benötigt plot_classifier.py """

from Support.plot_classifier import plot_classifier

# Trainings-Daten plotten
plot_classifier(model, X_train, y_train, proba = False, xlabel = "Alter", ylabel = "Interesse")

# Testdaten plotten
plot_classifier(model, X_test, y_test, proba = False, xlabel = "Alter", ylabel = "Interesse")


