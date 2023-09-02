A (simple) Tool for Creating Better Synthetic Images for ML Training
====================================================================

This is the code to support the Medium article of the same title.

Try it out
----------

Install the code and components:
- Clone this to your local machine. 

- Choose to install using either Conda or pip
  - conda env create -f environment.yml
  - pip install -r requirements.txt

- Test - run
  - python dither.py --input test.yaml --num 3

This has only been tested on Ubuntu 22.

Use for your needs
------------------

The first thing you'll want to do is look into your usd (or usda) file to identify the components that you want to 'dither'.
A good tool for this is NVidia Isaac Sim.   (To install this, install NVidia Omniverse and follow their instructions.)    

With the object open, you can map from the components you're interested in to the 'prim' path - shown in the right hand window.   You'll need this for the next step.

##YAML file

Look at the test.yaml file.   There are two sections:
- header - here you identify the base USD file that you will dither from.    You can also specify the base name of the dithered files you create.
- per prim modification.   You can specify as many prims as you'd like to modify.    Elements include:
  - path (required) - the prim path to that element - you identified this using Isaac Sim.
  - dithering elements - all optional
    - Translate - with arguments (X,Y,Z)
    - Rotate - with arguments to rotate around (X,Y,Z)
    - Scale -  with arguments to scale along (X,Y,Z)
    - Color - with arguments (R,G,B)
    
There are also three functions (currently) you can use within your arguments for dithering:
- Uniform - provides a uniform distribution, arguments (low, high)
- Normal - provides a normal distribution, arguments (low, high)
- Choice - returns one out of a list of options, arguments a list of options

Example (from test.yaml)
```
  front-top:
    path: /Root/GMA_Pallet/part2
    translate: (0,Uniform(-0.2,0.2),Uniform(-0.2,0.2))
    rotate: Choice([(0,0,0), (0,0,Uniform(-5,5))])
    scale: (1,Uniform(0.95,1.05),Uniform(0.95,1.05))
    color: (0.85, 0.35, 0.35)
```

Hints:
- You'll probably need to experiment to get the effects you desire.
- Setting the color to be obvious, can help in this.    This is what is done in the test.yaml example.


Integrate into your synthetic data creation pipeline
----------------------------------------------------

The dithered files you create can be directly used from NVidia composer.   The use of that is beyond this article, but here is an example of how it might be included, i.e., using the Choice operation.

See the full example in composerExample/simple.yaml

```
# header - set the basics, e.g., wall, floor

object_pallet_0001:
  obj_model: Choice(["built/GMApallet.usda", "built/xtest_1.usda", "built/xtest_2.usda", "built/xtest_3.usda" ])
  obj_count: 1
  obj_coord_camera_relative: False    # Use exact coordinates
  obj_coord: (Uniform(2.6, 3.0), Uniform(-0.2,0.2), 0)
  obj_rot: (0, 0, Uniform(90, 120))  # isd pallet, w/o payload
  obj_texture: Choice(["*/assets/materials/pallet_textures.txt"])
  obj_texture_scale: (Uniform(0.1, 10.0), Uniform(0.1,10.0))
  obj_class_id: 91

# rest - lighting, camera, output desired
```


# Good luck!


Feedback/Contributing
---------------------

Feedback and Contributions are encouraged!
