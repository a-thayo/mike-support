import mikeio
from pathlib import Path

# this is to group point series into multi-item point series (or line series also can)
# in my case, i want to group it into 9 point series with either 2 or 3 items per group
# i also want to: 1) change the item name to be more descriptive, 2) add 1st timestep of value 0, 3) set item type to be Water Level
for i in range(2,11):
    bnd = list(Path.cwd().glob(f"2018_BND-{i}*.dfs0")) # customize based on your file naming conventions
    for item in bnd:
        # make the 1st timestep with data = 0
        info = mikeio.ItemInfo("PUT YOUR ITEM NAME HERE", mikeio.EUMType.Water_Level) # concat func require item names to match
        zero = mikeio.DataArray([0.0], time=pd.DatetimeIndex(["PUT YOUR 1ST TIMESTEP HERE"]), item=info)
        zero_ds = mikeio.Dataset(zero) # concat func is for dataset and not dataarray
        if item==bnd[0]:
            a = mikeio.read(item).rename({"Predicted tidal elevation": "PUT YOUR ITEM NAME HERE"})
            iteminfo = mikeio.ItemInfo(f"{item.stem}", mikeio.EUMType.Water_Level)
            a[0] = mikeio.DataArray(data=a[0].values, time=a.time, item=iteminfo)
            a = mikeio.Dataset.concat([zero_ds, a])
            merge = a.copy() # probably could get away with not copying 'a' but better safe than sorry
        else:
            b = mikeio.read(item).rename({"Predicted tidal elevation": "PUT YOUR ITEM NAME HERE"})
            iteminfo = mikeio.ItemInfo(f"{item.stem}", mikeio.EUMType.Water_Level)
            b[0] = mikeio.DataArray(data=b[0].values, time=a.time, item=iteminfo)
            b = mikeio.Dataset.concat([zero_ds, b])
            merge = mikeio.Dataset.merge([merge,b])
    merge.to_dfs("PUT YOUR FILE NAME HERE.dfs0")
