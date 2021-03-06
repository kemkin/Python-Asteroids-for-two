'''
Written on 02.12.2010 by Andrej Cizov

Defines the functions that read the object's data for Modules.Object.Loader
'''
from Modules.Config import get
import io
import sys
import os
def read_loader_config ( name ):
        '''
        reads the loader config to a tuple
        Arguments:
        - name: the name of the file to read, according to "Objects" configuration name
        '''
        path = "{0}/{1}/{2}{3}".format(get("Objects"), get("Objects Configs"), name,  get("Objects Suffix"))
        r = [] # variable returned to the caller
        try:
                
                cfg = io.open( path )
                
                lines = cfg.readlines( )
                # Some pretty sketchy code to read the files
                for line in lines:
                        if line[0] != '#': #do not read the comments
                                try:
                                        line = line.rstrip(" "+os.linesep)
                                        line_parts = line.split('=')
                                        
                                        r+=[[line_parts[0], line_parts[1]]]
                                except:
                                        pass
        except Exception as e:
                print (e)
                sys.exit ( "!!! Modules.Config.LoaderConfigReader.read_loader_config Could not load the file: '{0}'".format( path ) )
        return r
