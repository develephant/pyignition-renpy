### EXESOFT PYIGNITION ###
# Copyright David Barker 2010
#
# Particle effect manager

import particles, gravity

DRAWTYPE_IMAGE = particles.DRAWTYPE_IMAGE

class ParticleEffect:
	def __init__(self, display, pos, size):
		self.display = display
		self.pos = pos
		self.size = size
		
		self.left = pos[0]
		self.top = pos[1]
		self.right = pos[0] + size[0]
		self.bottom = pos[1] + size[1]
		
		self.particles = []
		self.sources = []
		self.gravities = []
	
	def Update(self):
		for source in self.sources:
			source.Update()
		
		for gravity in self.gravities:
			gravity.Update()

		for particle in self.particles:
			totalforce = [0.0, 0.0]
			
			for gravity in self.gravities:
				force = gravity.GetForce(particle.pos)
				totalforce[0] += force[0]
				totalforce[1] += force[1]
			
			particle.velocity = [particle.velocity[0] + totalforce[0], particle.velocity[1] + totalforce[1]]
			
			particle.Update()
		
		# Delete dead particles
		for particle in self.particles:
			if not particle.alive:
				self.particles.remove(particle)
	
	def Redraw(self):
		for particle in self.particles:
			particle.Draw(self.display)
	
	def CreateSource(self, pos = (0, 0), initspeed = 0.0, initdirection = 0.0, initspeedrandrange = 0.0, initdirectionrandrange = 0.0, particlesperframe = 0, particlelife = 0, genspacing = 0, drawtype = 0, colour = (0, 0, 0), radius = 0.0, length = 0.0, image = None):
		newsource = particles.ParticleSource(self, pos, initspeed, initdirection, initspeedrandrange, initdirectionrandrange, particlesperframe, particlelife, genspacing, drawtype, colour, radius, length, image)
		self.sources.append(newsource)
		return newsource  # Effectively a reference
	
	def CreatePointGravity(self, strength = 0.0, strengthrandrange = 0.0, pos = (0, 0)):
		newgrav = gravity.PointGravity(strength, strengthrandrange, pos)
		self.gravities.append(newgrav)
		return newgrav
	
	def CreateDirectedGravity(self, strength = 0.0, strengthrandrange = 0.0, direction = [0, 1]):
		newgrav = gravity.DirectedGravity(strength, strengthrandrange, direction)
		self.gravities.append(newgrav)
		return newgrav

	def AddParticle(self, particle):
		self.particles.append(particle)
