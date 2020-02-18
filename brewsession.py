class BrewSession:

    def __init__(self):
        self.step = None
        self.transition_to(InitialBrewStep())

    def transition_to(self, step):
        self.step = step
        self.step.session = self

    def prompt(self):
        return self.step.info()

    def toggle_step(self):
        self.step.toggle_step()


class BrewStep:

    def __init__(self):
        self.session = None
        self.button = None
        self.message = None
        self.image = None

    def toggle_step(self):
        self.session.transition_to(self.next_step())

    def info(self):
        return {'button': self.button, 'prompt': self.message, 'image': self.image}

    def next_step(self):
        pass


class InitialBrewStep(BrewStep):

    def __init__(self):
        self.session = None
        self.button = 'Start Session'
        self.message = 'Session Starting'
        self.image = 'images/s1.png'

    def next_step(self):
        return FillHLT()


# Toggle once HLT is at capacity
class FillHLT(BrewStep):

    def __init__(self):
        self.session = None
        self.button = 'HLT Full'
        self.message = 'Filling HLT...'
        self.image = 'images/s2.png'

    def next_step(self):
        return HeatHLT()


# Toggle once HLT is at strike temp
class HeatHLT(BrewStep):

    def __init__(self):
        self.session = None
        self.button = 'HLT at temperature'
        self.message = 'Heating HLT...'
        self.image = 'images/s2.png'

    # TODO Prompt should come from temp being reached
    def next_step(self):
        return FillMLT()


# Toggle once MLT is at capacity for mash thickness
class FillMLT(BrewStep):

    def __init__(self):
        self.session = None
        self.button = 'MLT at capacity'
        self.message = 'Filling MLT...'
        self.image = 'images/s2.png'

    def next_step(self):
        return AddGrainToMLT()


# Toggle once Grain has been added to MLT
class AddGrainToMLT(BrewStep):

    def __init__(self):
        self.session = None
        self.button = 'Grain Infused'
        self.message = 'Infuse Grain with Strike Water...'
        # TODO need better image for 'AddGrainTOMLT'
        self.image = 'images/s3.png'

    def next_step(self):
        return MashGrains()


# Currently no way to handle this step
# Toggle if  MLT is over desired mash temp
class AddColdWater(BrewStep):

    def __init__(self):
        self.session = None
        self.button = 'Mash temp reached'
        self.message = 'Cooling Mash to desired temp...'
        self.image = 'images/s3.png'

    # TODO Prompt should come from temp being reached
    def next_step(self):
        return MashGrains()


# Currently no way to handle this step
# Toggle if  MLT is over desired mash temp
class AddMoreWaterFromHLT(BrewStep):

    def __init__(self):
        self.session = None
        self.button = 'Mash temp reached'
        self.message = 'Heating Mash to desired temp...'
        self.image = 'images/s3.png'

    # TODO Prompt should come from temp being reached
    def next_step(self):
        return MashGrains()


# Toggle once mash is complete
class MashGrains(BrewStep):

    def __init__(self):
        self.session = None
        self.button = 'Mash started'
        self.message = 'Starting mash...'
        self.image = 'images/s3.png'

    def next_step(self):
        return FillHLT2()


# Toggle once HLT is at capacity
class FillHLT2(BrewStep):

    def __init__(self):
        self.session = None
        self.button = 'HLT Full'
        self.message = 'Filling HLT...'
        # TODO need better image for 'FillMLT2'
        self.image = 'images/s3.png'

    def next_step(self):
        return HeatHLT2()


# Toggle once HLT is at strike temp
# TODO Find a way to reuse 'HeatHLT'
class HeatHLT2(BrewStep):

    def __init__(self):
        self.session = None
        self.button = 'HLT at temperature'
        self.message = 'Heating HLT...'
        # TODO need better image for 'HeatHLT2'
        self.image = 'images/s3.png'

    # TODO Prompt should come from temp being reached
    def next_step(self):
        return MashAtRest()


# Toggle once Mash timer is completed
class MashAtRest(BrewStep):

    def __init__(self):
        self.session = None
        self.button = 'Mash Complete'
        self.message = 'Mashing...'
        # TODO need better image for 'MashAtRest'
        self.image = 'images/s3.png'

    # Show timer and how to handle multiple steps?
    # TODO Prompt should come from timer being reached
    def next_step(self):
        return MashOut()


# Currently no way to handle this step
# Toggle once Mash timer is completed
class CirculateMash(BrewStep):

    def __init__(self):
        self.session = None
        self.button = 'Mash temp reached'
        self.message = 'Circulating Mash...'
        self.image = 'images/s3.png'

    # Show timer and how to handle multiple steps?
    # TODO Prompt should come from timer being reached
    def next_step(self):
        return MashOut()


# Toggle once Mash out timer is completed
# Mash out should not start timer until mash temp has been achieved
class MashOut(BrewStep):

    def __init__(self):
        self.session = None
        self.button = 'Mash Out Complete'
        self.message = 'Mashing out...'
        # TODO need better image for 'MashOut'
        self.image = 'images/s3.png'

    # TODO Prompt should come from timer AND temp being reached
    def next_step(self):
        return LauterGrains()


# Toggle once BK is at capacity
class LauterGrains(BrewStep):

    def __init__(self):
        self.session = None
        self.button = 'Lautering Complete'
        self.message = 'Lautering...'
        self.image = 'images/s4.png'

    def next_step(self):
        return HeatBK()


# Toggle once BK is Boiling
class HeatBK(BrewStep):

    def __init__(self):
        self.session = None
        self.button = 'BK at a boil'
        self.message = 'Heating BK...'
        self.image = 'images/s5.png'

    # TODO Prompt should come from temp being reached
    def next_step(self):
        return AddToBoil()


# Toggle once BK is Boiling
# TODO Add ability to repeat for multiple steps
class AddToBoil(BrewStep):

    def __init__(self):
        self.session = None
        self.button = 'Hops added to boil'
        self.message = 'Adding hops...'
        # TODO need better image for 'AddToBoil'
        self.image = 'images/s5.png'

    def next_step(self):
        return CoolWort()


# Toggle once Wort is at temp
class CoolWort(BrewStep):

    def __init__(self):
        self.session = None
        self.button = 'Wort at temp'
        self.message = 'Cooling Wort...'
        self.image = 'images/s6.png'

    # TODO Prompt should come from temp being reached
    def next_step(self):
        return TransferToFermenter()


# Toggle once Wort is at temp
class TransferToFermenter(BrewStep):

    def __init__(self):
        self.session = None
        self.button = 'Wort has Transferred'
        self.message = 'Transferring Wort...'
        self.image = 'images/s7.png'

    # TODO Prompt should come from temp being reached
    def next_step(self):
        return BrewSessionComplete()


class BrewSessionComplete(BrewStep):

    def __init__(self):
        self.session = None
        self.button = 'Start New Session?'
        self.message = 'Session has Completed!'
        self.image = 'images/s7.png'

    def next_step(self):
        return InitialBrewStep()


# Currently no way to handle this step
class PauseBrewSession(BrewStep):

    def __init__(self):
        self.session = None
        self.button = 'Start Session'
        self.message = 'Session has Paused!'
        self.image = 'images/s1.png'

    # Return to previous step
    def next_step(self):
        return InitialBrewStep()

