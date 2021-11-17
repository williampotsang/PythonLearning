
# NP iter loop
### For loop over np_height
```
for x in np_height : 
    print(str(x) + " inches")
```
### For loop over np_baseball
```
for x in np.nditer(np_baseball) :
    print(x)
```
# Pandas iter loop
### Iterate over rows of cars
```
# Code for loop that adds COUNTRY column
for lab, row in cars.iterrows() :
    cars.loc[lab, str.upper("country")] = str.upper(row["country"])
```
