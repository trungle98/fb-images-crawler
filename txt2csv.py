# importing pandas as pd
import pandas as pd

# list of name, degree, score
nme = ["aparna", "pankaj", "sudhir", "Geeku"]
deg = ["MBA", "BCA", "M.Tech", "MBA"]


# dictionary of lists 
dict = {'images': nme, 'avatar': deg}

df = pd.DataFrame(dict)

# saving the dataframe
df.to_csv('file1.csv')