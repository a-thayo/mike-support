import mikeio
import pandas as pd
import pathlib

p = list(pathlib.Path.cwd().glob("*E_SLR0*.dfs0")) # filter which scenario you want to read
key = [item.stem for item in p]

mean = []
max = []
for item in p:
  ds = mikeio.read(item)
  mean.append(ds.nanmean().to_numpy())
  max.append(ds.nanmax().to_numpy())
  if p[-1]==item:
    idx = ds.items
dictMean = dict(zip(key, mean))
dictMax = dict(zip(key, max))
dfMean = pd.DataFrame.from_dict(dictMean)
dfMax = pd.DataFrame.from_dict(dictMax)
dfMean.index = idx
dfMax.index = idx

with pd.ExcelWriter("points_comparison.xlsx", mode="w") as writer:
  dfMean.to_excel(writer, "meanCS")
  dfMax.to_excel(writer, "maxCS")
