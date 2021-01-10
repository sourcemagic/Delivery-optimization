# Delivery-optimization
In this project it will be solved a knapsack problem with the library PulP.  
This project comes from an exercise from a [coding challenge](https://www.get-in-it.de/coding-challenge) from [get in IT](https://www.get-in-it.de).  
The german specifications of the exercise can see at [Exercise specifications](https://github.com/sourcemagic/Delivery-optimization/blob/main/Exercise%20specifications.pdf)  

The project can be see as jupyter notebook with included documentation and results. [here](https://github.com/sourcemagic/Delivery-optimization/blob/main/Delivery%20optimization.ipynb).  

Or as python module [here](https://github.com/sourcemagic/Delivery-optimization/blob/main/delivery_optimization.py).  
It can be imported as module and used for other parameters or execute direct as script and runs with the exercise example parameters.  

### Used Requirements

- Python=3.7.6
- pandas=1.0.1
- pulp=2.4

There is a virtual environment to execute the script [here](https://github.com/sourcemagic/Delivery-optimization/tree/main/venv)  
**To run the script** type following in the console from directory Delivery-optimization:  

Linux: `~Delivery-optimization> ./venv/Scripts/python ./delivery_optimization.py`  
Windows: `~Delivery-optimization> .\venv\Scripts\python .\delivery_optimization.py`  


### Reason to use integer programming
Because the existing constraints restricted the amount of solutions a lot to be efficient. 

## Results for the exercise example

Allowed weight for truck 1 (with included driver): 1027600.0 gram or 1027.6 kg  
Allowed weight for truck 2 (with included driver): 1014300.0 gram or 1014.3 kg  

#### Result count for each item (Anzahl für jeden Gegenstand)

**Truck 1** with driver weight 72.4kg:  
Mobiltelefon Büro         =       52.0  
Mobiltelefon Heavy Duty   =      220.0  
Tablet Büro klein         =      509.0  
Tablet outdoor klein      =        4.0  

**Truck 2** with driver weight 85.7kg:  
Mobiltelefon Büro         =        8.0  
Mobiltelefon Outdoor      =      157.0  
Tablet Büro klein         =       86.0  
Tablet outdoor groß       =      370.0  

Total weight of truck 1: 1027589.0 gram or **1027.589 kg**  
Total weight of truck 2: 1014282.0 gram or **1014.282 kg**  

The total **utility (Gesamtnutzung)** value of picked items in both trucks is: **74660.0**
