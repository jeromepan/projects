# this script deconvolves the challenge images using a simple reflection model

echo running deconvolve challenge images

export MAVEN_OPTS="-Xmx4096m"

# set the directories

# set the directories
scriptDir=~/Brian2014/Projects/deconware/code/bin/Generated/
projectsDir=~/Brian2014/Projects/deconware/code/projects/truenorthJ/ImageJ2Plugins/
rootImageDir=~/Brian2014/Projects/deconware/Images/Tests/

# the directory where we expect to find the images that have been extended 

inputDir=$rootImageDir/ShellTest2/
psfDir=$rootImageDir/ShellTest2/
outputDir=$rootImageDir/ShellTest2/Deconvolve2/

inputName=shell.image.noisy.ome.tif
psfName=psf.ome.tif
extendedName=extended.ome.tif
psfExtendedName=psf.extended.ome.tif

iterations=200
regularizationFactor=0.0002
algorithm=rltv
convolution=conv
deconvolvedName=$inputName.$algorithm.$iterations.ome.tif
croppedName=$inputName.$algorithm.$iterations.cropped.ome.tif

# size of the measurement 
measurementSizeX=192
measurementSizeY=192
measurementSizeZ=64

# size of the psf
psfSizeX=129
psfSizeY=129
psfSizeZ=127

# extension size
extensionSizeX=20
extensionSizeY=20
extensionSizeZ=40

# size of the object
extendedSizeX=$(($measurementSizeX+2*$extensionSizeX))
extendedSizeY=$(($measurementSizeY+2*$extensionSizeY))
extendedSizeZ=$(($measurementSizeZ+2*$extensionSizeZ))

cd $projectsDir/
mvn

cd $projectsDir/DeconvolutionTest

scriptName=$scriptDir/DeconvolveChallengeImages.hackscript

# extend the phantom using reflection
echo "com.truenorth.commands.dim.ExtendCommandDimension silent input=$inputDir$inputName output=$outputDir$extendedName dimensionX=$extendedSizeX dimensionY=$extendedSizeY dimensionZ=$extendedSizeZ boundaryType=mirror fftType=speed" > $scriptName

# extend the psf using zeros
echo "com.truenorth.commands.dim.ExtendCommandDimension silent input=$inputDir$psfName output=$outputDir$psfExtendedName dimensionX=$extendedSizeX dimensionY=$extendedSizeY dimensionZ=$extendedSizeZ boundaryType=boundaryZero fftType=speed" >> $scriptName

#mvn exec:java -Dexec.mainClass=com.truenorth.DeconvolutionTest -Dexec.args="com.truenorth.commands.fft.ConvolutionCommand silent input=$inputDir$inputName psf=$psfDir$psfName output=$outputDir$convolvedName"

#echo "com.truenorth.commands.fft.RichardsonLucyCommand silent input=$outputDir$extendedName psf=$outputDir$psfExtendedName output=$outputDir$deconvolvedName iterations=$iterations" >> $scriptName

echo "com.truenorth.commands.fft.TotalVariationRLCommand silent input=$outputDir$extendedName psf=$outputDir$psfExtendedName output=$outputDir$deconvolvedName firstGuessType=constant iterations=$iterations regularizationFactor=$regularizationFactor" >> $scriptName

echo "com.truenorth.commands.dim.CropCommand silent input=$outputDir$deconvolvedName output=$outputDir$croppedName xSize=$measurementSizeX ySize=$measurementSizeY zSize=$measurementSizeZ" >> $scriptName

mvn exec:java -Dexec.mainClass=com.truenorth.DeconvolutionTest -Dexec.args="$scriptName"


