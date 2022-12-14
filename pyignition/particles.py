### EXESOFT PYIGNITION ###
# Copyright David Barker 2010
#
# Particle and ParticleSource objects


import keyframes, interpolate, random, math

DRAWTYPE_IMAGE = 1 #renpy only supports images for particles

class Particle:
    def __init__(self, parent, initpos, velocity, life, drawtype = 5, colour = (0, 0, 0), radius = 0.0, length = 0.0, image = None, keyframes = []):

        self.parent = parent
        self.pos = initpos
        self.velocity = velocity
        self.life = life
        self.colour = colour
        self.radius = radius
        self.length = length
        self.image = image
        self.drawtype = 5 # FORCING IMAGE TYPE (refactor)
        self.keyframes = []
        self.keyframes.extend(keyframes[:])
        self.curframe = 0
        self.alive = True
	
    def Update(self):

        self.pos = [self.pos[0] + self.velocity[0], self.pos[1] + self.velocity[1]]

        if self.curframe > self.life:
            self.alive = False
        else:
            # Not sure if renpy can handle color changes #
            self.colour = (self.parent.particlecache[self.curframe]['colour_r'], self.parent.particlecache[self.curframe]['colour_g'], self.parent.particlecache[self.curframe]['colour_b'])
            ####

            self.radius = self.parent.particlecache[self.curframe]['radius']
            self.length = self.parent.particlecache[self.curframe]['length']
            self.curframe = self.curframe + 1
	
    def Draw(self, display):
        if (self.pos[0] > 10000) or (self.pos[1] > 10000) or (self.pos[0] < -10000) or (self.pos[1] < -10000):
            return
		
        if self.drawtype == DRAWTYPE_IMAGE:  # Image (default)
            print("draw")

            # Convert this to renpy code? #
            size = self.image.get_size()
            display.blit(self.image, (self.pos[0] - size[1], self.pos[1] - size[1]))
            ####

    def CreateKeyframe(self, frame, colour = (None, None, None), radius = None, length = None):
        keyframes.CreateKeyframe(self.keyframes, frame, {'colour_r':colour[0], 'colour_g':colour[1], 'colour_b':colour[2], 'radius':radius, 'length':length})


class ParticleSource:
	def __init__(self, parenteffect, pos, initspeed, initdirection, initspeedrandrange, initdirectionrandrange, particlesperframe, particlelife, genspacing, drawtype = 0, colour = (0, 0, 0), radius = 0.0, length = 0.0, image = None):
		self.parenteffect = parenteffect
		self.pos = pos
		self.initspeed = initspeed
		self.initdirection = initdirection
		self.initspeedrandrange = initspeedrandrange
		self.initdirectionrandrange = initdirectionrandrange
		self.particlesperframe = particlesperframe
		self.particlelife = particlelife
		self.genspacing = genspacing
		self.colour = colour
		self.drawtype = drawtype
		self.radius = radius
		self.length = length
		self.image = image
		
		self.keyframes = []
		self.CreateKeyframe(0, self.pos, self.initspeed, self.initdirection, self.initspeedrandrange, self.initdirectionrandrange, self.particlesperframe, self.genspacing)
		self.particlekeyframes = []
		self.particlecache = []
		self.CreateParticleKeyframe(0, colour = self.colour, radius = self.radius, length = self.length)
		self.curframe = 0
	
	def Update(self):		
		newvars = interpolate.InterpolateKeyframes(self.curframe, {'pos_x':self.pos[0], 'pos_y':self.pos[1], 'initspeed':self.initspeed, 'initdirection':self.initdirection, 'initspeedrandrange':self.initspeedrandrange, 'initdirectionrandrange':self.initdirectionrandrange, 'particlesperframe':self.particlesperframe, 'genspacing':self.genspacing}, self.keyframes)
		self.pos = (newvars['pos_x'], newvars['pos_y'])
		self.initspeed = newvars['initspeed']
		self.initdirection = newvars['initdirection']
		self.initspeedrandrange = newvars['initspeedrandrange']
		self.initdirectionrandrange = newvars['initdirectionrandrange']
		self.particlesperframe = newvars['particlesperframe']
		self.genspacing = newvars['genspacing']
		
		particlesperframe = self.particlesperframe
		
		if (self.genspacing == 0) or ((self.curframe % self.genspacing) == 0):
			for i in range(0, particlesperframe):
				self.CreateParticle()
		
		self.curframe = self.curframe + 1
	
	def CreateParticle(self):
		if self.initspeedrandrange != 0.0:
			speed = self.initspeed + (float(random.randrange(int(-self.initspeedrandrange * 100.0), int(self.initspeedrandrange * 100.0))) / 100.0)
		else:
			speed = self.initspeed
		if self.initdirectionrandrange != 0.0:
			direction = self.initdirection + (float(random.randrange(int(-self.initdirectionrandrange * 100.0), int(self.initdirectionrandrange * 100.0))) / 100.0)
		else:
			direction = self.initdirection
		velocity = [speed * math.sin(direction), -speed * math.cos(direction)]
		newparticle = Particle(self, initpos = self.pos, velocity = velocity, life = self.particlelife, drawtype = self.drawtype, colour = self.colour, radius = self.radius, length = self.length, image = self.image, keyframes = self.particlekeyframes)
		self.parenteffect.AddParticle(newparticle)

	def CreateKeyframe(self, frame, pos = (None, None), initspeed = None, initdirection = None, initspeedrandrange = None, initdirectionrandrange = None, particlesperframe = None, genspacing = None, interpolationtype = "linear"):
		keyframes.CreateKeyframe(self.keyframes, frame, {'pos_x':pos[0], 'pos_y':pos[1], 'initspeed':initspeed, 'initdirection':initdirection, 'initspeedrandrange':initspeedrandrange, 'initdirectionrandrange':initdirectionrandrange, 'particlesperframe':particlesperframe, 'genspacing':genspacing, 'interpolationtype':interpolationtype})
	
	def CreateParticleKeyframe(self, frame, colour = (None, None, None), radius = None, length = None, interpolationtype = "linear"):
		keyframes.CreateKeyframe(self.particlekeyframes, frame, {'colour_r':colour[0], 'colour_g':colour[1], 'colour_b':colour[2], 'radius':radius, 'length':length, 'interpolationtype':interpolationtype})
		self.PreCalculateParticles()
	
	def PreCalculateParticles(self):
		self.particlecache = []  # Clear the cache
		
		# Interpolate the particle variables for each frame of its life
		for i in range(0, self.particlelife + 1):
			vars = interpolate.InterpolateKeyframes(i, {'colour_r':0, 'colour_g':0, 'colour_b':0, 'radius':0, 'length':0}, self.particlekeyframes)
			self.particlecache.append(vars)
	
	def ConsolidateKeyframes(self):
		keyframes.ConsolidateKeyframes(self.keyframes, self.curframe, {'pos_x':self.pos[0], 'pos_y':self.pos[1], 'initspeed':self.initspeed, 'initdirection':self.initdirection, 'initspeedrandrange':self.initspeedrandrange, 'initdirectionrandrange':self.initdirectionrandrange, 'particlesperframe':self.particlesperframe, 'genspacing':self.genspacing})
	
	def SetPos(self, newpos):
		self.CreateKeyframe(self.curframe, pos = newpos)
	
	def SetInitSpeed(self, newinitspeed):
		self.CreateKeyframe(self.curframe, initspeed = newinitspeed)
	
	def SetInitDirection(self, newinitdirection):
		self.CreateKeyframe(self.curframe, initdirection = newinitdirection)
	
	def SetInitSpeedRandRange(self, newinitspeedrandrange):
		self.CreateKeyframe(self.curframe, initspeedrangrange = newinitspeedrandrange)
	
	def SetInitDirectionRandRange(self, newinitdirectionrandrange):
		self.CreateKeyframe(self.curframe, initdirectionrandrange = newinitdirectionrandrange)
	
	def SetParticlesPerFrame(self, newparticlesperframe):
		self.CreateKeyframe(self.curframe, particlesperframe = newparticlesperframe)
	
	def SetGenSpacing(self, newgenspacing):
		self.CreateKeyframe(self.curframe, genspacing = newgenspacing)
