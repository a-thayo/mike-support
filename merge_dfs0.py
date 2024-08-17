import mikeio
from pathlib import Path

# this is to group point series into multi-item point series (or line series also can)
# in my case, i want to group it into 9 point series with either 2 or 3 items per group
for i in range(2,11):
    bnd = list(Path.cwd().glob(f"2018_BND-{i}*.dfs0")) # customize based on your filen naming conventions
    for item in bnd:
        if item==bnd[0]:
            print(item.stem) # just to check if its reading the correct file
            a = mikeio.read(item).rename({"Predicted tidal elevation": f"{item.stem}"})
            merge = a.copy() # probably could get away with not copying 'a' but better safe than sorry
        else:
            print(item.stem)
            b = mikeio.read(item).rename({"Predicted tidal elevation": f"{item.stem}"})
            merge = mikeio.Dataset.merge([merge,b])
    merge.to_dfs(f"{bnd[0].stem[:-2]}.dfs0")
