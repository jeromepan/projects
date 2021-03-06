from Experiment import Experiment
import Phantoms

class Spheres2(Experiment):
	
	def __init__(self, measurementSizeX, measurementSizeY, measurementSizeZ, psfSizeX, psfSizeY, psfSizeZ, homeDirectory):	
		Experiment.__init__(self,measurementSizeX, measurementSizeY, measurementSizeZ, psfSizeX, psfSizeY, psfSizeZ, homeDirectory)
	
		# parameters of the top sphere
		self.spherePositionX=self.objectSizeX / 2
		self.spherePositionY=self.objectSizeY / 2
		self.spherePositionZ=self.objectSizeZ / 2 - 27
		self.sphereRadius=6
		self.zRadius=2
		self.sphereIntensity=100

		# parameters of the bottom sphere
		self.spherePosition2X=self.objectSizeX / 2
		self.spherePosition2Y=self.objectSizeY / 2
		self.spherePosition2Z=self.objectSizeZ / 2 
		self.sphereRadius2=6
		self.szRadium=2
		self.sphereIntensity2=100

		self.background=0.000001

		self.directory=homeDirectory+"/Tester2/"

	def CreatePhantom(self, command):
		module=command.run("com.truenorth.commands.phantom.CreatePhantomCommand", True, "xSize", self.objectSizeX, "ySize", self.objectSizeY, "zSize", self.objectSizeZ, "background", self.background).get();

		Phantoms.AddSphere(command, self.spherePositionX, self.spherePositionY, self.spherePositionZ, self.sphereRadius, self.sphereIntensity);
		
		module=Phantoms.AddSphere(command, self.spherePosition2X, self.spherePosition2Y, self.spherePosition2Z, self.sphereRadius, self.sphereIntensity);
		
		return module.getOutputs().get("output")
