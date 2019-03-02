import os 

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

'''
getFilePath: return the path of the folder or file which is 
    specified.
'''
def getFilePath(foldername,filename=None,create=False):
    try:
        assert type(foldername) is list
        path = os.path.join(BASE_DIR,foldername[0])
        for sub_fold in foldername[1:]:
            path = os.path.join(path,sub_fold)
    except:
        path = os.path.join(BASE_DIR,foldername)
    
    
    if create and not os.path.exists(path):
        os.makedirs(path)
        
    if filename is not None:
        path = os.path.join(path,filename)
        
    return path

'''
checkRequiredFiles: get a type dict
    if exec is true raise exception
    else just return bool
'''
def checkRequiredFiles(files,exec=True):
    for file in files.values():
        if not os.path.exists(file):
            if exec:
                raise FileExistsError("dataset file %s missing !"
                    % (file))
            else:
                return False
    return True
