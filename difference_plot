import mikeio
import pathlib

p = list(pathlib.Path.cwd().glob("*F_SLR0.70_10000*.dfsu"))
base = mikeio.read("base case.dfsu")

for item in p:
  ds = mikeio.read(item)
  diff = ds[1] - base[1]
  diff.to_dfs(f"diff_{item.stem}.dfsu")
