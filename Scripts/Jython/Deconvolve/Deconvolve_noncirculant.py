# @StatusService status
# @DatasetService data
# @CommandService command
# @DisplayService display
# @IOService io

# this script extends and deconvolves an image using the model from the second deconvolution grand challenge
# described here: http://bigwww.epfl.ch/deconvolution/challenge/index.html?p=documentation/overview

import sys

jythonCurrentDir='/home/bnorthan/Brian2014/Projects/deconware/code/projects/Scripts/Jython/'
sys.path.insert(0, jythonCurrentDir+'/Psfs/')

import os
from net.imglib2.meta import Axes;

from PSF_NA14_DAPI_65_200_coverslip import PSF_NA14_DAPI_65_200_coverslip 

rootImageDir="/home/bnorthan/Brian2014/Images/General/Deconvolution/"

inputDir=rootImageDir+"/Phantoms/RandomSpheresZRatio/PSF_NA14_DAPI_65_200_coverslip/"
#inputDir=rootImageDir+"/BasicTests/Kurt_Thorn_Beads1_Cropped/"
psfDir=rootImageDir+"/Phantoms/RandomSpheresZRatio/PSF_NA14_DAPI_65_200_coverslip/"
outputDir=rootImageDir+"/Tests/RandomSpheresZRatio/PSF_NA14_DAPI_65_200_coverslip/noncirculant/"
#outputDir=rootImageDir+"/BasicTests/Kurt_Thorn_Beads1_Cropped/noncirculant_255_255_100/"

if not os.path.exists(outputDir):
    os.makedirs(outputDir)

inputName="phantom_.image.noisy.ome.tif"
#inputName="100xPSF_2k_2_MMStack.ome.tif"
generatePSF=False
#generatePSF=True


outputBase="phantom"

if generatePSF:
	psf=PSF_NA14_DAPI_65_200_coverslip(outputDir)
	psf=psf.CreatePsf(command, "com.truenorth.commands.psf.CreatePsfCommandCosmos", \
			255, 255, 100)
else:
	psfName="psf.ome.tif"
	# open and display the psf
	psf=data.open(psfDir+psfName)
	display.createDisplay(psf.getName(), psf);

# open and display the input image
inputData=data.open(inputDir+inputName)
display.createDisplay(inputData.getName(), inputData);	

# size of the measurement 
measurementSizeX=inputData.dimension(inputData.dimensionIndex(Axes.X));
measurementSizeY=inputData.dimension(inputData.dimensionIndex(Axes.Y));
#measurementSizeZ=inputData.dimension(inputData.dimensionIndex(Axes.Z));
measurementSizeZ=inputData.dimension(2);

# size of the psf
psfSizeX=psf.dimension(psf.dimensionIndex(Axes.X));
psfSizeY=psf.dimension(psf.dimensionIndex(Axes.Y));
#psfSizeZ=psf.dimension(psf.dimensionIndex(Axes.Z));
psfSizeZ=psf.dimension(2);

# size of the object space
objectSizeX=measurementSizeX+psfSizeX-1
objectSizeY=measurementSizeY+psfSizeY-1
objectSizeZ=measurementSizeZ+psfSizeZ-1

iterations=200
regularizationFactor=0.009
algorithm="rltv_tn_nc"

extendedName=outputDir+outputBase+".extended.ome.tif"
extendedPsfName=outputDir+"psf.extended.ome.tif"
deconvolvedName=outputDir+outputBase+str(algorithm)+"."+str(regularizationFactor)+"."+str(iterations)+".ome.tif"
finalName=outputDir+outputBase+str(algorithm)+"."+str(regularizationFactor)+"."+str(iterations)+".final.ome.tif"

# extend the image
extended=command.run("com.truenorth.commands.dim.ExtendCommandDimension", True, "input", inputData, "dimensionX", objectSizeX, \
		"dimensionY", objectSizeY, "dimensionZ", objectSizeZ, "boundaryType", "zero", "fftType", "speed").get().getOutputs().get("output");
io.save(extended, extendedName);

# extend the psf
psfExtended=command.run("com.truenorth.commands.dim.ExtendCommandDimension", True, "input", psf, "dimensionX", objectSizeX, \
		"dimensionY", objectSizeY, "dimensionZ", objectSizeZ, "boundaryType", "zero", "fftType", "speed").get().getOutputs().get("output");
io.save(psfExtended, extendedPsfName);

# call RL
deconvolved = command.run("com.truenorth.commands.fft.RichardsonLucyCommand", True, "input", extended, "psf", psfExtended, "truth", None,"firstGuess", None, "iterations", iterations, "firstGuessType", "constant", "convolutionStrategy", "noncirculant", "regularizationFactor", regularizationFactor, "imageWindowX", measurementSizeX, "imageWindowY", measurementSizeY, "imageWindowZ", measurementSizeZ, "psfWindowX", psfSizeX, "psfWindowY", psfSizeY, "psfWindowZ", psfSizeZ).get().getOutputs().get("output");
io.save(deconvolved, deconvolvedName);

# crop back down to image window size
final = command.run("com.truenorth.commands.dim.CropCommand", True, "input", deconvolved, "xSize", measurementSizeX, "ySize", measurementSizeY, "zSize", measurementSizeZ).get().getOutputs().get("output");
io.save(final, finalName);

