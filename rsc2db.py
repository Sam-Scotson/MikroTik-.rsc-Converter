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
    global df_rsc
    ori=os.getcwd()
    try:
        inputdir=input('enter .rsc file path --> ')
    except FileNotFoundError as e:
        print('Input directory path')
        start()
    rscfiles=getrscfiles(inputdir)
    rscfile=rscselect(di_rscfiles)
    csv2sql()
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

def ipfirersc2csv(rscfile):
    """Function is for use with IP-firewall-Address-List.rsc
    Converts .rsc file to .csv file
    Args:
     rscfile=path and file directory
    Returns:
     writes new csv file to .rsc path directory"""
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
        newdir=input('enter dir path to save .csv file --> ')
        name=input('enter name for new file --> ')
        os.chdir(newdir)
        df_rsc1=pd.DataFrame(rsclist)
        df_rsc=df_rsc1.drop(0)
        df_rsc.to_csv(name + '.csv')
    except FileNotFoundError as e:
        print('Input directory path')
        ipfirersc2csv(rscfile)
    except PermissionError as e:
        print('Permission Error, try another path')
        ipfirersc2csv(rscfile)
    return(df_rsc)

def csv2sql():
    from sqlalchemy import create_engine
    from sqlalchemy import Column, Integer, String
    from sqlalchemy.orm import Session
    from sqlalchemy.orm import declarative_base

    engine = create_engine("postgresql+psycopg2://dcstudent:S3cretPassw0rd@localhost:5432/campdata-prod")
    session = Session(engine)
    Base=rscRawAll()

    class rscRawAll(Base):
        __table__=".rsc_raw_all"
        id=Column(int, primary_key=table)
        IPinfo=Column(String(255))