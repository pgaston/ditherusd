#%%

import os
import numpy as np
import argparse
import yaml
from pathlib import Path

from modifyStage import modifyStage

#%%


def define_arguments():
    """ Define command line arguments. """
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", default="parameters/warehouse.yaml", help="Path to input parameter file")
    parser.add_argument(
        "--num", "--num", type=int, default=1, help="Num variants to create."
    )
    return parser

'''
    Functions to support - based on https://docs.omniverse.nvidia.com/isaacsim/latest/manual_replicator_composer.html#isaac-sim-app-manual-replicator-composer
    - Choice - return one from the list
    - Uniform, Normal
'''
def Uniform(low,high):
    return np.random.uniform(low,high)

def Normal(low,high):
    return np.random.normal(low,high)

def Choice(choices):
    selection = np.random.randint(0, len(choices))
    return choices[selection]
    # return np.random.choice(choices)


if __name__ == "__main__":
    # Create argument parser
    parser = define_arguments()
    args, _ = parser.parse_known_args()
    yamlFile = args.input
    numVariants = args.num

    # Hard code for testing
    # yamlFile = Path("./test.yaml")    
    # numVariants = 2

    with open(str(yamlFile), 'r') as f:
        yData = yaml.load(f, Loader=yaml.BaseLoader)        # BaseLoader disables automatic value conversion

    # Run it num times
    for i in range(numVariants):
        # next file...

        assert(yData['baseUSDFile'] is not None)
        usdFP = Path(yData['baseUSDFile'])
        print("usdFP: ", usdFP)

        if yData['outPrefix'] is not None:
            outPrefix = yData['outPrefix']
        else:
            outPrefix = "dither"

        ms = modifyStage(usdFP, fPrefix=outPrefix)

        operations = yData["Operations"]
        assert(operations is not None)

        for part,primOps in operations.items():     # loop through the parts
            primPath = primOps['path']
            ms.getPrim(primPath)

            for op, expr in primOps.items():       
                match op:
                    case 'path':
                        pass    # already captured
                    case 'translate':
                        print(op," : ", eval(str(expr))," from: ",expr) 
                        ms.setTranslate(eval(str(expr)))
                    case 'rotate':
                        print(op," : ", eval(str(expr))," from: ",expr) 
                        ms.setRotate(eval(str(expr)))
                    case 'scale':
                        print(op," : ", eval(str(expr))," from: ",expr) 
                        ms.setScale(eval(str(expr)))
                    case 'color':
                        print(op," : ", eval(str(expr))," from: ",expr) 
                        ms.setColor(eval(str(expr)))
                    case _:
                        print("Unknown prim dither Op: ", op)

            ms.endPrim()
        ms.close()
    print("done")


#%%


#%%