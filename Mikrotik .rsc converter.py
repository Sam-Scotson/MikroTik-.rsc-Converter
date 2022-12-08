import os; import glob; import pandas as pd
def start():
    """Core function of script, sets scope of interlinked variables, 
    queries for inputs, executes functions in needed order, 
    opens file and stores contents as a list, allows selection of file conversion function    
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
    global cxlist
    ori=os.getcwd()
    try:
        inputdir=input('enter .rsc file path --> ')
    except FileNotFoundError as e:
        print('Input directory path')
        start()
    rscfiles=getrscfiles(inputdir)
    rscfile=rscselect(di_rscfiles) 
    cxlist=cxfile(rscfile) 
    cxtooldict={ 
        'csv' : rsc2csv, 
        'json' : rsc2json,
        'html' : rsc2html,
        'sql' : rsc2sql
        }
    for key, value in cxtooldict.items():
        print(key, ' : ', value)
    try:
        selectformat=input('enter file conversion function (i.e. csv)--> ')
        outputfile=cxtooldict[selectformat](rscfile)
    except KeyError as e:
        print('Input function file key')
        selectformat=input('enter file format function -->')
        outputfile=cxtooldict[selectformat](rscfile)
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
     dict"""
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
    """allows user to select .rsc file from dict
    Args:
     di_rscfiles=dictonary of .rsc file names  
    Returns:
     .rsc file in list object"""
    global di_rscfile
    for key, value in di_rscfiles.items():
        print(key, ' : ', value)
    try:
        knum=input('select file key number --> ')
        i=int(knum)
        di_rscfile=di_rscfiles[i]
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

def cxfile(rscfile):
    global rsclist
    rsclist=[]
    str1=''
    with open(rscfile) as rsc:
        for line in rsc:
            if line.startswith('add '):
                str1=line.replace('list=CountryIPBlocks\n', 'list=CountryIPBlocks ')
                rsclist.append(str1)
    return(rsclist)

def rsc2csv(cxlist):
    """for use with IP-firewall-Address-List.rsc
    changes dir, creates pd-df from rsclist, 
    converts to .csv file
    Args:
     rscfile=path and file directory
    Returns:
     writes new .csv file to path directory"""
    global df_rsc
    try:
        newdir=input('enter dir path to save .csv file --> ')
        name=input('enter name for new file --> ')
        os.chdir(newdir)
        df_rsc1=pd.DataFrame(cxlist)
        df_rsc=df_rsc1.drop(0)
        df_rsc.to_csv(name + '.csv')
    except FileNotFoundError as e:
        print('Input directory path')
        rsc2csv(rscfile)
    except PermissionError as e:
        print('Permission Error, try another path')
        rsc2csv(rscfile)
    return(df_rsc)

def rsc2json(cxlist):
    """for use with IP-firewall-Address-List.rsc
    changes dir, creates pd-df from rsclist, 
    converts to .json file
    Args:
     rscfile=path and file directory
    Returns:
     writes new .json file to path directory"""
    global df_rsc
    try:
        newdir=input('enter dir path to save .json file --> ')
        name=input('enter name for new file --> ')
        os.chdir(newdir)
        df_rsc1=pd.DataFrame(cxlist)
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

def rsc2sql(cxlist):
    """for use with IP-firewall-Address-List.rsc
    changes dir, creates pd-df from rsclist, 
    converts to .db file
    Args:
     rscfile=path and file directory
    Returns:
     writes new db file to path directory"""
    from sqlalchemy import create_engine
    global df_rsc
    try:
        newdir=input('enter dir path to save .db file --> ')
        sql=input('enter sql server (sqlite format) --> ')
        os.chdir(newdir)
        df_rsc1=pd.DataFrame(cxlist)
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

def rsc2html(cxlist):
    """for use with IP-firewall-Address-List.rsc
    changes dir, creates pd-df from rsclist, 
    converts to .html file
    Args:
     rscfile=path and file directory
    Returns:
     writes new html file to path directory"""
    global df_rsc
    try:
        newdir=input('enter dir path to save .html file --> ')
        name=input('enter name for new file --> ')
        os.chdir(newdir)
        df_rsc1=pd.DataFrame(cxlist)
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
def rsc2pdf(rsclist):
    """for use with IP-firewall-Address-List.rsc
    changes dir, creates pd-df from rsclist, 
    converts to .pdf file
    Args:
     rscfile=path and file directory
    Returns:
     writes new pdf file to path directory"""









