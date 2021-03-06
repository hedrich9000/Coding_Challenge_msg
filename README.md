# .msg Coding Challenge

![Graph](solve_coding_challenge/docs/graph.gif) |
:----:
Animierte Grafik, welche die Schritte des Algorithmus zur Lösung des Problems darstellt ([Interaktive Version](https://msg-coding-solution-graph.site44.com/)) |

## Ausführung des Codes
Getestet mit Python in einer Virtual Environment mit:
* Python Version 3.8.2 auf Ubuntu 20.04 LTS
* Python Version 3.8.2 auf Windows 10 (10.0.18363)

Zur Visualisierung des Ergebnis ist Firefox empfehlenswert (als Default Browser einstellen!).

### Installieren der benötigten Packages
```script
$ python setup.py build
$ python setup.py install
$ pip install -r requirements.txt
```
### Ausführen des Codes (kurzes Beispiel)
Ausführen des Beispiels mit beigefügter .csv-Datei:
```script
$ cd solve_coding_challenge/
$ python main.py -m -g
```
### Ausführen des Codes (Ausführlich)
```script
$ cd solve_coding_challenge/
$ python main.py -h
usage: main.py [-h] [-l LOAD] [-i ITERATIONS] [-s SCORE] [-m] [-g]

Import CSV-File and get a solution for the TSP problem. If nothing is set, the
program will set the csv-path to "msg_standorte_deutschland.csv" and the
iterations to 5.

optional arguments:
  -h, --help            show this help message and exit
  -l LOAD, --load LOAD  Load CSV-File in the stated form (default: False)
  -i ITERATIONS, --iterations ITERATIONS
                        [OPTIONAL] Set the wanted iterations with random initial routes for the algorithm (default: False)
  -s SCORE, --score SCORE
                        [OPTIONAL] Set score, where the algorithms ends the optimization. (default: False)
  -m, --vis_map         [OPTIONAL] Enable visualization of the cities on a map using your webbrowser. (default: False)
  -g, --vis_graph       [OPTIONAL] Enable visualization of the algorithm steps as a graph using your webbrowser. (default: False)
```
Beispielanwendung in der Kommandozeile, falls eine individuelle CSV-Datei geladen werden soll:
```script
$ python main.py -l /path/to/file/file.csv -i 20 -s 0.001 -m -g
```
Hier kann individuell eine eigene CSV-Datei eingegeben werden (**[-l]**), die Anzahl der Iterationen mit zufälliger
Startroute gesetzt werden (**[-i]**) und der Score zur ausreichenden Optimierung angepasst werden (**[-s]**). Die
CSV-Datei muss dabei im gleichen Format wie die Vorlage gegeben sein.
## Berechnung der Distanzen
Die Distanz zwischen den Städten wurde mittels der Geokoordinaten als Kreisbogen über 
die Erdkugel berechnet. Somit entspricht die Distanz der "Luftlinie" zwischen den Orten.

## Optimierung des Problems
Zur Optimierung wurde der 2-opt Ansatz gewählt, da dieser einen guten Kompromiss zwischen 
Zeitaufwand und der Minimierung der Gesamtdistanz darstellt.
 


## Lösung/Ergebnisse

Die Lösung wird im Folgenden sowohl als Auflistung der Städte als auch als Visualisierung der Städte 
anhand eines interaktiven Graphen sowie einer interaktiven Karte gezeigt.

Zum Öffnen der Visualisierungen stehen folgende Links zur Verfügung:
* [Interaktiver Graph](https://msg-coding-solution-graph.site44.com/)
* [Interaktive Karte](https://msg-coding-solution-map.site44.com/)

Diese Visualisierungen lassen sich mittels der tags **[-m]** und **[-g]** von *main.py* generieren.
Dabei sollte sich beim Ausführen der Funktion automatisch der Default Browser öffnen und 
die Visualierungen in zwei neuen Tabs anzeigen. Die Ergebnisse in Textform werden im Folgenden gezeigt.



### Geringste gefundene Distanz
Die geringste gefundene Distanz in Kilometern beträgt:
 ```script
Distanz: 2333.4124 km
 ```

### Reihenfolge der Standorte
Die Reihenfolge mit Start- und Endpunkt in Ismaning ergibt sich folgendermaßen:

```script
Ismaning/München (Hauptsitz)
Ingolstadt
Nürnberg
Stuttgart
St. Georgen
Bretten
Walldorf
Frankfurt
Köln/Hürth
Düsseldorf
Essen
Münster
Lingen (Ems)
Schortens/Wilhelmshaven
Hamburg
Hannover
Braunschweig
Berlin
Görlitz
Chemnitz
Passau
Ismaning/München (Hauptsitz)
```
### Ergebnisse auf der Karte
![Map showing the resulting route to cities](solve_coding_challenge/docs/result_map.png) |
:----:
Lösung des Problems dargestellt auf einer Landkarte ([Interaktive Version](https://msg-coding-solution-map.site44.com/)) |


