pfs = mikeio.read_pfs("TEMPLATE.log") # read template pfs for tidal prediction
cons = list(Path.cwd().glob(r"PATH TO FOLDER CONTAINING ALL YOUR .CON FILES"))
b = open(r"../BOUNDARY-COORDS.txt", 'r') # text files containing station, latitude, and longitude
d_db = {}
for line in b:
    lst = line.split()
    db = dict(
    StationName = f"BND-{lst[0]}",
    StationLatitude = float(lst[1]),
    StationLongitude = float(lst[2]))
    d_db[f"_BND-{lst[0]}_"] = db
for con in cons: # loop thru every con file (con = con file, cons = list of con files)
    c = open(con, 'r')
    no_sect = 0
    for line in c:
        lst = line.split()
        if len(lst)==4:
            dc = dict(
            Name=lst[1],
            Phase=float(lst[3]),
            Amplitude=float(lst[2])
            )
            no_sect+=1
        else:
            continue
        if isinstance(dc.get("Phase"), float) and no_sect>0:
            s = mikeio.PfsSection(dc)
            pfs.TIDHPC.Constituents[f"Constituent_{no_sect}"] = s
    pattern = r'_(.*?)_'
    match = re.search(pattern, con.stem)
    if match:
        extracted = '_' + match.group(1) + '_'
        if extracted in d_db.keys():
            s = mikeio.PfsSection(d_db[extracted])
            pfs.TIDHPC.GeneralParameters.StationName = s.StationName
            pfs.TIDHPC.GeneralParameters.StationLatitude = s.StationLatitude
            pfs.TIDHPC.GeneralParameters.StationLongitude = s.StationLongitude
    pfs.write(f"{con.stem}.pfs")

# then, run this command in cmd:
# "C:\Program Files (x86)\DHI\MIKE Zero\2024\bin\x64\tidhpc.exe" PFS_FILE_NAME.pfs
