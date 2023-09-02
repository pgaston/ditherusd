#%%
'''
Interface to the USD stage
- Create a copy
- Modify prims
- Export to file

How to call:
    - open the file - modifyStage

    - cycle through prims
        - getPrim
        - one of:
            - setTranslate
            - setRotate
            - setVisibility
            - setScale
            - setColor 
        - endPrim

    - close the file - close

'''

import os
from pathlib import Path
from pxr import Usd, UsdGeom, Vt, Gf, Sdf


## #%%

class modifyStage:
    iNum = 0

    def __init__(self, stageFP: Path, fPrefix="xfrm", bDebug = False):
        self.stageFP = stageFP
        self.fPrefix = fPrefix
        self.bDebug = bDebug
        self.stage = None
        self.dstFP = None

        self.partPrim = None
        self.xform = None
        self.primModified = False

        assert(stageFP.exists())
        assert(stageFP.is_file())
        self.stage = Usd.Stage.Open(str(stageFP))
        assert(self.stage is not None)

        # create a unique destination FP
        modifyStage.iNum += 1
        self.dstFP = stageFP.parent / (self.fPrefix + "_" + str(modifyStage.iNum)+'.usda')

    def close(self):
        assert(self.stage is not None)
        self.stage.Export(str(self.dstFP))
        self.stage = None

    def getPrim(self, primPath: str):
        assert(self.partPrim is None)
        assert(self.xform is None)
        assert(self.stage is not None)
        self.primPath = primPath

        self.partPrim = self.stage.GetPrimAtPath(primPath)
        assert(self.partPrim is not None)

        self.xform = UsdGeom.Xformable(self.partPrim)
        assert(self.xform is not None)

        # test
        # gfMatOrig: Gf.Matrix4d = self.xform.GetLocalTransformation()
        # assert(gfMatOrig is not None)
        # print("gfMatOrig: ", gfMatOrig)
        # print("all:",self.partPrim.GetPropertyNames())


    def endPrim(self):
        assert(self.partPrim is not None)
        assert(self.xform is not None)

        # may or may not work...
        if self.primModified:
            self.partPrim.GetPrim().SetMetadata("comment", "prim modified/transformed")

        self.partPrim = None
        self.xform = None
        self.primModified = False


    def setTranslate(self, tXYZ: tuple):
        assert(self.xform is not None)
        self.xform.AddTranslateOp().Set(value=tXYZ)
        self.primModified = True

    def setRotate(self, tXYZ: tuple):
        assert(self.xform is not None)
        self.xform.AddRotateXYZOp().Set(value=tXYZ)
        self.primModified = True

    def setScale(self, tXYZ: tuple):
        assert(self.xform is not None)
        self.xform.AddScaleOp().Set(value=tXYZ)
        self.primModified = True

    # Color - after some research, one way to do this is to add a primvar
    '''
    SetColor - after some research, one way to do this is to remove the "Looks" component
    and add 'color3f primvars:displayColor = (1., 0., 0.0)'

    Needless to say, removing "Looks" will remove any current material/texture/??? assignments.
    '''
    def setColor(self, tRGB: tuple, scopeName="Looks"):
        assert(self.xform is not None)

        # remove the Looks component
        self.stage.RemovePrim(self.primPath+"/"+scopeName)

        vector_attr: Usd.Attribute = self.partPrim.CreateAttribute(
            "primvars:displayColor", Sdf.ValueTypeNames.Color3f             # Color3f
        )
        vector_value = Gf.Vec3f(tRGB)
        vector_value_array = Vt.Vec3fArray([vector_value])
        vector_attr.Set(vector_value)

        self.primModified = True

    '''
    t.b.d.
    '''
    def setMaterial(self, mtlPath: str):
        assert(self.partPrim is not None)

    '''
    t.b.d.
    '''
    def setTexture(self, txtPath: str):
        assert(self.partPrim is not None)

    def setVisibility(self, bVis: bool):
        assert(self.partPrim is not None)

        imageable = UsdGeom.Imageable(self.partPrim)
        # print("imageable: ", imageable)
        if bVis:
            imageable.MakeVisible()
        else:
            imageable.MakeInvisible()
        self.primModified = True


## Testing
if False:
    tstIt = modifyStage(Path('built/GMApallet.usda'))               # /home/pg/Documents/synthUSD/

    tstIt.getPrim("/Root/GMA_Pallet/part3_02")

    tstIt.setTranslate((0,0,10))
    tstIt.setRotate((0,0,45))
    tstIt.setVisibility(True)

    tstIt.setColor((1.,1.,0.))

    tstIt.setScale((1,1,1.5))

    tstIt.endPrim()

    tstIt.close()

    print("done ")


#%%



#%%

