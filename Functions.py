import traceback



def printException():
    """Prints caught exception traceback
    """
    print("\n--------------- CAUGHT EXCEPTION ---------------\n" 
        + traceback.format_exc() + "------------------------------------------------\n")