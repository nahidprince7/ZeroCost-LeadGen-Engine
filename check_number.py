import pandas as pd

df = pd.read_excel('results/Demo.xlsx')
print("Phone numbers in your file:")
for index, row in df.iterrows():
    print(f"{row['Name']}: '{row['Phone']}'")