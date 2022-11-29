import os; import glob; import pandas as pd
def start():
    """Core function of script, sets scope of interlinked variables, 
    queries for inputs, executes functions in needed order, 
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
        'csv' : rsc2csv, 
        'json' : rsc2json,
        'html' : rsc2html,
        'sql' : rsc2sql
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

def rscselect(di_rscfiles):
    """allows user to select .rsc file from dict with int    
    Args:
     di_rscfiles=dictonary of .rsc file names  
    Returns:
     .rsc file in dict object"""
    global di_rscfile
    try:
        for key, value in di_rscfiles.items():
            print(key, ' : ', value)
        knum=input('select file key number --> ')
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

def rsc2csv(rscfile):
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
                str=line.replace('list=CountryIPBlocks\n', 'list=CountryIPBlocks ')
                rsclist.append(str)
    try:
        newdir=input('enter dir path to save .csv file --> ')
        name=input('enter name for new file --> ')
        os.chdir(newdir)
        df_rsc1=pd.DataFrame(rsclist)
        df_rsc=df_rsc1.drop(0)
        df_rsc.to_csv(name + '.csv')
    except FileNotFoundError as e:
        print('Input directory path')
        rsc2csv(rscfile)
    except PermissionError as e:
        print('Permission Error, try another path')
        rsc2csv(rscfile)
    return(df_rsc)

def rsc2json(rscfile):
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
                str=line.replace('list=CountryIPBlocks\n', 'list=CountryIPBlocks ')
                rsclist.append(str)
    try:
        newdir=input('enter dir path to save .json file --> ')
        name=input('enter name for new file --> ')
        os.chdir(newdir)
        df_rsc1=pd.DataFrame(rsclist)
        df_rsc=df_rsc1.drop(0)
        df_rsc.to_json(name + '.json')
    except FileNotFoundError as e:
        print('Input directory path')
        rsc2json(rscfile)
    except PermissionError as e:
        print('Permission Error, try another path')
        rsc2json(rscfile)
    except OSError as e:
        print('Cannot save file into a non-existent directory')
        rsc2json(rscfile)
    return(df_rsc)

def rsc2sql(rscfile):
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
                str=line.replace('list=CountryIPBlocks\n', 'list=CountryIPBlocks ')
                rsclist.append(str)
    try:
        newdir=input('enter dir path to save .db file --> ')
        sql=input('enter sql server (sqlite format) --> ')
        os.chdir(newdir)
        df_rsc1=pd.DataFrame(rsclist)
        df_rsc=df_rsc1.drop(0)
        engine = create_engine(sql)
        df_rsc.to_sql(sql, if_exists="append", chunksize=1000, con=engine)
    except FileNotFoundError as e:
        print('Input directory path')
        rsc2sql(rscfile)
    except PermissionError as e:
        print('Permission Error, try another path')
        rsc2sql(rscfile)
    return(df_rsc)

def rsc2html(rscfile):
    """Function is for use with IP-firewall-Address-List.rsc
    Converts .rsc file to .html file
    Args:
     rscfile=path and file directory
    Returns:
     writes new html file to path directory"""
    global rsclist
    global df_rsc
    rsclist=[]
    str=''
    with open(rscfile) as rsc:
        for line in rsc:
            if line.startswith('add '):
                str=line.replace('list=CountryIPBlocks\n', 'list=CountryIPBlocks ')
                rsclist.append(str)
    try:
        newdir=input('enter dir path to save .html file --> ')
        name=input('enter name for new file --> ')
        os.chdir(newdir)
        df_rsc1=pd.DataFrame(rsclist)
        df_rsc=df_rsc1.drop(0)
        df_rsc.to_html(name + '.html')
    except FileNotFoundError as e:
        print('Input directory path')
        rsc2html(rscfile)
    except PermissionError as e:
        print('Permission Error, try another path')
        rsc2html(rscfile)
    return(df_rsc)
start()
