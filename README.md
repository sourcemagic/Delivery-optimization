# Delivery-optimization
In this project a knapsack problem will be solved with the library PulP.  
This project results from an exercise from a [coding challenge](https://www.get-in-it.de/coding-challenge) from [get in IT](https://www.get-in-it.de).  
The german specifications of the exercise can be seen at [Exercise specifications](https://github.com/sourcemagic/Delivery-optimization/blob/main/Exercise%20specifications.pdf)  

The project can be see as jupyter notebook with included documentation and results. [here](https://github.com/sourcemagic/Delivery-optimization/blob/main/Delivery%20optimization.ipynb).  

Or as python module [here](https://github.com/sourcemagic/Delivery-optimization/blob/main/delivery_optimization.py).  
It can be imported as a module and used for other parameters or executed directly as a script and runs with the exercise example parameters.  

### Used Requirements

- Python=3.7.6
- pandas=1.0.1
- pulp=2.4

There is a virtual environment to execute the script [here](https://github.com/sourcemagic/Delivery-optimization/tree/main/venv)  
**To run the script** type following in the console from directory Delivery-optimization:  

Linux: `~Delivery-optimization> ./venv/Scripts/python ./delivery_optimization.py`  
Windows: `~Delivery-optimization> .\venv\Scripts\python .\delivery_optimization.py`  


## Results for the coding challenge exercise

**You can find the german version down below**

Allowed weight for truck 1 (with included driver): 1027600.0 gram or 1027.6 kg  
Allowed weight for truck 2 (with included driver): 1014300.0 gram or 1014.3 kg  

#### Result count for each item

**Truck 1** with driver weight 72.4kg:  
Mobile phone office = 52.0  
Mobile phone Heavy Duty = 220.0  
Tablet office small = 509.0  
Tablet outdoor small = 4.0  

**Truck 2** with driver weight 85.7kg:  
Mobile phone office = 8.0  
Mobile phone Outdoor = 157.0  
Tablet office small = 86.0  
Tablet outdoor big = 370.0  

Total weight of truck 1: 1027589.0 gram or **1027.589 kg**  
Total weight of truck 2: 1014282.0 gram or **1014.282 kg**  

The total **utility value** of picked items in both trucks is: **74660.0**  

### Ergebnisse für die Coding Challenge  

**Begründung für die Wahl des Algorithmus** integer programming (von linear programming):  
Durch die Einschränkungen für Ladegewicht der Transporter und benötigte Anzahl der Gegenstände, kann der Lösungsraum stark verkleinert werden.  
So kann das Verfahren unter Umständen auch eine bessere Performance als dynamic programming erreichen.  

Ergebnisse: 

Erlaubtes Gewicht mit enthaltenem Fahrer von Transporter 1: 1027600.0 g oder 1027.6 kg  
Erlaubtes Gewicht mit enthaltenem Fahrer von Transporter 2: 1014300.0 g oder 1014.3 kg  

#### Anzahl für jeden Gegenstand auf jeweiligem Transporter

**Transporter 1** mit Fahrer von 72.4kg:  
Mobiltelefon Büro         =       52.0  
Mobiltelefon Heavy Duty   =      220.0  
Tablet Büro klein         =      509.0  
Tablet outdoor klein      =        4.0  

**Transporter 2** mit Fahrer von 85.7kg:  
Mobiltelefon Büro         =        8.0  
Mobiltelefon Outdoor      =      157.0  
Tablet Büro klein         =       86.0  
Tablet outdoor groß       =      370.0  

Gesamtgewicht von Transporter 1: 1027589.0 g oder **1027.589 kg**  
Gesamtgewicht von Transporter 2: 1014282.0 gram or **1014.282 kg**  

Gesamter Nutzwert von Hardware auf beiden Transporter: **74660.0**
