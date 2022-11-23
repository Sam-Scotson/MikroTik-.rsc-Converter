import os; import glob; import pandas as pd; import time

def start():
    """Core function of script, sets scope of interlinked variables, 
    queries for inputs, executes .rsc file gather functions in needed order, 
    allows selection of file conversion function
    
    Args:
     none
     
    Returns:
     selected file conversion function output to selected directory path
     .rsc file contents in panda df"""
    global inputdir
    global rscfiles
    global rscfile
    global outputfile
    global df_rsc
    ori=os.getcwd()
    try:
        inputdir=input('enter .rsc file path --> ')
    except FileNotFoundError as e:
        print('Input directory path')
        start()
    rscfiles=getrscfiles(inputdir)
    rscfile=rscselect(di_rscfiles)
    contooldict={ 
        'csv' : ipfirersc2csv, 
        'json' : ipfirersc2json,
        'sql' : ipfirersc2sql
        }
    for key, value in contooldict.items():
        print(key, ' : ', value)
    try:
        selectformat=input('enter file conversion function (i.e. csv)--> ')
        outputfile=contooldict[selectformat](rscfile)
    except KeyError as e:
        print('Input function file key')
        selectformat=input('enter file format function -->')
        outputfile=contooldict[selectformat](rscfile)
    finally:
        print(df_rsc)
    os.chdir(ori)
    print('Conversion Successful!')

time.sleep(0.1)

def getrscfiles(inputdir):
    """change dir to .rsc file path, 
    picks up files places them in a dict
    
    Args:
     directory path(str)
     
    Returns: 
     Panda DataFrame"""
    global di_rscfiles
    try:
        os.chdir(inputdir)
    except FileNotFoundError as e:
        print('Input correct path directory')
        start()
    rscfiles=glob.glob(inputdir + '\\*.rsc')
    di_rscfiles={ i : rscfiles[i] for i in range(0, len(rscfiles) ) }
    return(di_rscfiles)
 
time.sleep(0.1)

def rscselect(di_rscfiles):
    """allows user to select .rsc file from dict with int
        
    Args:
     di_rscfiles=dictonary of .rsc file names
         
    Returns:
     .rsc file in dict object"""
    global di_rscfile
    for key, value in di_rscfiles.items():
        print(key, ' : ', value)
    try:
        knum=input('select key number --> ')
        inum=int(knum)
        di_rscfile=di_rscfiles[inum]
    except ValueError as e:
        print('Input correct key number')
        rscselect(di_rscfiles)
    except IndexError as e:
        print('Input correct key number')
        rscselect(di_rscfiles) 
    except KeyError as e:
        print('Input correct key number')
        rscselect(di_rscfiles)   
    return(di_rscfile)

time.sleep(0.1)

def ipfirersc2csv(rscfile):
    """Function is for use with IP-firewall-Address-List.rsc
    Converts .rsc file to .csv file

    Args:
     rscfile=path and file directory

    Returns:
     writes new csv file to .rsc path directory"""
    global rsclist
    global df_rsc
    rsclist=[]
    str=''
    with open(rscfile) as rsc:
        for line in rsc:
            if line.startswith('add '):
                str=line.replace('add ', '[add ').replace(
                    'list=CountryIPBlocks\n', 'list=CountryIPBlocks]')
            rsclist.append(str)
    try:
        newdir=input('enter dir path to save .csv file --> ')
        name=input('enter name for new file --> ')
        os.chdir(newdir)
        df_rsc=pd.DataFrame(rsclist)
        df_rsc.to_csv(name + '.csv')
    except FileNotFoundError as e:
        print('Input directory path')
        ipfirersc2csv(rscfile)
    except PermissionError as e:
        print('Permission Error, try another path')
        ipfirersc2csv(rscfile)
    return(df_rsc)

time.sleep(0.1)

def ipfirersc2json(rscfile):
    """Function is for use with IP-firewall-Address-List.rsc
    Converts .rsc file to .json file

    Args:
     rscfile=path and file directory

    Returns:
     writes new json file to path directory"""
    global rsclist
    global df_rsc
    rsclist=[]
    str=''
    with open(rscfile) as rsc:
        for line in rsc:
            if line.startswith('add '):
                str=line.replace('add ', '[add ').replace(
                    'list=CountryIPBlocks\n', 'list=CountryIPBlocks]')
            rsclist.append(str)
    try:
        newdir=input('enter dir path to save .json file --> ')
        name=input('enter name for new file --> ')
        os.chdir(newdir)
        df_rsc=pd.DataFrame(rsclist)
        df_rsc.to_json(name + '.json')
    except FileNotFoundError as e:
        print('Input directory path')
        ipfirersc2json(rscfile)
    except PermissionError as e:
        print('Permission Error, try another path')
        ipfirersc2json(rscfile)
    return(df_rsc)

time.sleep(0.1)

def ipfirersc2sql(rscfile):
    """Function is for use with IP-firewall-Address-List.rsc
    Converts .rsc file to sql .db file

    Args:
     rscfile=path and file directory

    Returns:
     writes new .db file to path directory"""
    from sqlalchemy import create_engine
    global df_rsc
    global rsclist
    rsclist=[]
    str=''
    with open(rscfile) as rsc:
        for line in rsc:
            if line.startswith('add '):
                str=line.replace('add ', '[add ').replace(
                    'list=CountryIPBlocks\n', 'list=CountryIPBlocks]')
            rsclist.append(str)
    try:
        newdir=input('enter dir path to save .db file --> ')
        sql=input('enter sql sever (sqlite format) --> ')
        os.chdir(newdir)
        df_rsc=pd.DataFrame(rsclist)
        engine = create_engine(sql)
        df_rsc.to_sql(sql, if_exists="append", chunksize=1000, con=engine)
    except FileNotFoundError as e:
        print('Input directory path')
        ipfirersc2sql(rscfile)
    except PermissionError as e:
        print('Permission Error, try another path')
        ipfirersc2sql(rscfile)
    return(df_rsc)
start()
