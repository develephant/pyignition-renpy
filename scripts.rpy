### THIS IS ONLY A SCRIPTING ATTEMPT. ADD TO A RENPY PROJECT TO HACK. ###

# The game starts here.
init python:
    renpy.add_python_directory("pyignition")

init 1 python:

    ## ALL OF THE CODE IN THIS BLOCK APPEARS TO BE VALID. NO ERRORS THROWN. ##

    import PyIgnition, math
    
    effect = PyIgnition.ParticleEffect(renpy.display, (0, 0), (1280, 720))
    effect.CreateDirectedGravity(strength = 0.2, direction = [0, 1])

    particle = renpy.image("particle", "images/particle.png")

    particlesource = effect.CreateSource((10, 10), initspeed = 8.0, initdirection = 0.0, initspeedrandrange = 2.0, initdirectionrandrange = math.pi, particlesperframe = 0, particlelife = 150, drawtype = PyIgnition.DRAWTYPE_IMAGE, image = particle)

    particlesource.SetPos((200, 200))

label start:

    ## HERE WE HAVE A CHALLEGE. HOW TO "PUMP" THE EVENT LOOP. ##

    # Locks the thread. Sigh...

    # label .effect_pump:
    #     $ print("pump")
    #     $ effect.Update()
    #     $ effect.Redraw()
    #     pause(1)
    #     jump .effect_pump

    "Can we do this? Who knows!"

    return
