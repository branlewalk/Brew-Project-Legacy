from datetime import date, datetime, time, timedelta


class Recipe:

    def __init__(self):

        self.id = 1
        self.name = '808'
        self.completed = False

        self.hlt = 60
        self.mlt = 60
        self.bk = 60

        # Strike Temp aprox. 165
        self.strike_temp = 60
        # Mash Temp aprox. 152
        self.mash_temp = 60
        self.mash_temp_range = 2
        # Strike Temp aprox. 165
        self.mash_out_temp = 60
        # Boil Temp 212
        self.boil_temp = 60
        # Ferm Temp aprox. 60
        self.ferm_temp = 60

        # Boil time approx. 60 min
        self.boil_time = timedelta(seconds=10)
        # Mash time approx 60 min
        self.mash_time = timedelta(seconds=10)
        # Mash Out time approx 60 min
        self.mash_out_time = timedelta(seconds=10)
        # Hop Time varies 0-60 min
        self.hops_add_time = timedelta(seconds=10)

    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'completed': self.completed
        }


class BrewSession:

    def __init__(self):
        self.step = None
        self.transition_to(InitialBrewStep())
        self.recipe = Recipe()
        self.mash_timer_end = None
        self.mash_out_timer_end = None
        self.hops_timer_end = None
        self.boil_timer_end = None

    def transition_to(self, step):
        self.step = step
        self.step.session = self

    def prompt(self):
        return self.step.info()

    def toggle_step(self):
        self.step.toggle_step()

    def set_temp(self, temps):
        self.step.set_temps(temps)

    def start_mash_timer(self):
        self.mash_timer_end = datetime.now() + self.recipe.mash_time

    def start_mash_out_timer(self):
        self.mash_out_timer_end = datetime.now() + + self.recipe.mash_out_time

    def start_hops_timer(self):
        self.hops_timer_end = datetime.now() + self.recipe.hops_add_time

    def start_boil_timer(self):
        self.boil_timer_end = datetime.now() + self.recipe.boil_time

    def timer(self):
        self.step.timer(datetime.now())


class BrewStep:

    def __init__(self):
        self.session = None
        self.button = 'Next'
        self.message = None
        self.image = None

    def toggle_step(self):
        self.session.transition_to(self.next_step())

    def info(self):
        return {'button': self.button, 'prompt': self.message, 'image': self.image}

    def next_step(self):
        pass

    def set_temps(self, temps):
        pass

    def timer(self, current_time):
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
        self.button = 'Next'
        self.message = 'Filling HLT...'
        self.image = 'images/s2.png'

    def next_step(self):
        return HeatHLT()


# Toggle once HLT is at strike temp
class HeatHLT(BrewStep):

    def __init__(self):
        self.session = None
        self.button = ''
        self.message = 'Heating HLT...'
        self.image = 'images/s2.png'

    def set_temps(self, temps):
        self.message = 'Waiting for Strike Temp to reach {}'.format(self.session.recipe.strike_temp)
        if temps['hlt'] >= self.session.recipe.strike_temp:
            self.session.transition_to(FillMLT())


# Toggle once MLT is at capacity for mash thickness
class FillMLT(BrewStep):

    def __init__(self):
        self.session = None
        self.button = 'Next'
        self.message = 'Filling MLT...'
        self.image = 'images/s2.png'

    def next_step(self):
        return AddGrainToMLT()


# Toggle once Grain has been added to MLT
class AddGrainToMLT(BrewStep):

    def __init__(self):
        self.session = None
        self.button = 'Next'
        self.message = 'Adding Grain to Strike Water...'
        # TODO need better image for 'AddGrainTOMLT'
        self.image = 'images/s3.png'

    def next_step(self):
        return MashGrains(self.session)


# Toggle once mash is complete
class MashGrains(BrewStep):

    def __init__(self, session):
        self.session = session
        self.button = 'Next'
        self.message = 'Starting mash...'
        self.image = 'images/s3.png'
        self.session.start_mash_timer()

    def next_step(self):
        return FillHLT2()

    def set_temps(self, temps):
        mlt_temp = temps['mlt']
        plus_temp_range = self.session.recipe.mash_temp - self.session.recipe.mash_temp_range
        minus_temp_range = self.session.recipe.mash_temp + self.session.recipe.mash_temp_range
        if plus_temp_range < mlt_temp < minus_temp_range:
            self.session.transition_to(MashGrains(self.session))
        elif mlt_temp >= minus_temp_range:
            self.session.transition_to(AddColdWater())
        elif mlt_temp <= plus_temp_range:
            self.session.transition_to(AddMoreWaterFromHLT())

    def timer(self, current_time):
        if current_time >= self.session.mash_timer_end:
            self.session.transition_to(MashOut())


# Toggle if  MLT is over desired mash temp
class AddColdWater(BrewStep):

    def __init__(self):
        self.session = None
        self.button = ''
        self.message = 'Cooling Mash to desired temp...'
        self.image = 'images/s3.png'

    def set_temps(self, temps):
        self.message = 'Waiting for Mash Temp to reach {}'.format(self.session.recipe.mash_temp)
        if temps['mlt'] <= self.session.recipe.mash_temp:
            self.session.transition_to(MashGrains())

    def timer(self, current_time):
        if current_time >= self.session.mash_timer_end:
            self.session.transition_to(MashOut())


# Toggle if  MLT is over desired mash temp
class AddMoreWaterFromHLT(BrewStep):

    def __init__(self):
        self.session = None
        self.button = ''
        self.message = 'Heating Mash to desired temp...'
        self.image = 'images/s3.png'

    def set_temps(self, temps):
        self.message = 'Waiting for Mash Temp to reach {}'.format(self.session.recipe.mash_temp)
        if temps['mlt'] >= self.session.recipe.mash_temp:
            self.session.transition_to(MashGrains())

    def timer(self, current_time):
        if current_time >= self.session.mash_timer_end:
            self.session.transition_to(MashOut())


# Toggle once HLT is at capacity
class FillHLT2(BrewStep):

    def __init__(self):
        self.session = None
        self.button = 'Next'
        self.message = 'Filling HLT...'
        # TODO need better image for 'FillMLT2'
        self.image = 'images/s3.png'

    def next_step(self):
        return HeatHLT2()

    def timer(self, current_time):
        if current_time >= self.session.mash_timer_end:
            self.session.transition_to(MashOut())


# Toggle once HLT is at strike temp
class HeatHLT2(BrewStep):

    def __init__(self):
        self.session = None
        self.button = ''
        self.message = 'Heating HLT...'
        # TODO need better image for 'HeatHLT2'
        self.image = 'images/s3.png'

    def set_temps(self, temps):
        self.message = 'Waiting for Mash  Temp to reach {}'.format(self.session.recipe.mash_temp)
        if temps['hlt'] >= self.session.recipe.mash_temp:
            self.session.transition_to(CirculateMash())

    def timer(self, current_time):
        if current_time >= self.session.mash_timer_end:
            self.session.transition_to(MashOut())


# Toggle once Mash timer is completed
class MashAtRest(BrewStep):

    def __init__(self):
        self.session = None
        self.button = ''
        self.message = 'Mashing...'
        # TODO need better image for 'MashAtRest'
        self.image = 'images/s3.png'

    # TODO Show timer and how to handle multiple steps?
    def set_temps(self, temps):
        self.message = 'Waiting for Mash Temp to reach {}'.format(self.session.recipe.mash_temp)
        if temps['mlt'] <= self.session.recipe.mash_temp:
            self.session.transition_to(CirculateMash())

    def timer(self, current_time):
        self.message = 'Remaining time left on Mash {}'.format(str(self.session.mash_timer_end - current_time))
        if current_time >= self.session.mash_timer_end:
            self.session.transition_to(MashOut())


# Toggle once Mash timer is completed
class CirculateMash(BrewStep):

    def __init__(self):
        self.session = None
        self.button = ''
        self.message = 'Circulating Mash...'
        self.image = 'images/s3.png'

    # TODO Show timer and how to handle multiple steps?
    def set_temps(self, temps):
        self.message = 'Waiting for Mash Temp to reach {}'.format(self.session.recipe.mash_temp)
        if temps['mlt'] >= self.session.recipe.mash_temp:
            self.session.transition_to(MashAtRest())

    def timer(self, current_time):
        self.message = 'Remaining time left on Mash {}'.format(str(self.session.mash_timer_end - current_time))
        if current_time >= self.session.mash_timer_end:
            self.session.transition_to(MashOut())


# Toggle once Mash out timer is completed
class MashOut(BrewStep):

    def __init__(self):
        self.session = None
        self.button = ''
        self.message = 'Mashing out...'
        # TODO need better image for 'MashOut'
        self.image = 'images/s3.png'

    def set_temps(self, temps):
        self.message = 'Waiting for Mash Out Temp to reach {}'.format(self.session.recipe.mash_out_temp)
        if temps['mlt'] >= self.session.recipe.mash_out_temp:
            if self.session.mash_out_timer_end is None:
                self.session.start_mash_out_timer()

    def timer(self, current_time):
        if self.session.mash_out_timer_end is not None:
            self.message = 'Remaining time left on Mash Out {}'.format(str(self.session.mash_out_timer_end - current_time))
            if current_time >= self.session.mash_out_timer_end:
                self.session.transition_to(LauterGrains())


# Toggle once BK is at capacity
class LauterGrains(BrewStep):

    def __init__(self):
        self.session = None
        self.button = 'Next'
        self.message = 'Lautering...'
        self.image = 'images/s4.png'

    def next_step(self):
        return HeatBK(self.session)


# Toggle once BK is Boiling
class HeatBK(BrewStep):

    def __init__(self, session):
        self.session = session
        self.button = ''
        self.message = 'Heating BK...'
        self.image = 'images/s5.png'

    def set_temps(self, temps):
        self.message = 'Waiting for Boil Temp to reach {}'.format(self.session.recipe.boil_temp)
        if temps['bk'] >= self.session.recipe.boil_temp:
            self.session.transition_to(AddToBoil(self.session))


# Toggle once BK is Boiling
# TODO Add ability to repeat for multiple steps
class AddToBoil(BrewStep):

    def __init__(self, session):
        self.session = session
        self.button = 'Hops added to boil'
        self.message = 'Adding hops...'
        # TODO need better image for 'AddToBoil'
        self.image = 'images/s5.png'
        self.session.start_boil_timer()
        self.session.start_hops_timer()

    def timer(self, current_time):
        self.message = 'Remaining time left on Hops {}'.format(str(self.session.hops_timer_end - current_time))
        if current_time >= self.session.hops_timer_end:
            self.session.transition_to(CoolWort())


# Toggle once Wort is at temp
class CoolWort(BrewStep):

    def __init__(self):
        self.session = None
        self.button = ''
        self.message = 'Cooling Wort...'
        self.image = 'images/s6.png'

    # TODO Prompt should come from temp being reached
    def set_temps(self, temps):
        self.message = 'Waiting for Ferm temp to reach {}'.format(self.session.recipe.ferm_temp)
        if temps['bk'] >= self.session.recipe.ferm_temp:
            self.session.transition_to(TransferToFermenter())


# Toggle once Wort is at temp
class TransferToFermenter(BrewStep):

    def __init__(self):
        self.session = None
        self.button = 'Finished'
        self.message = 'Transferring Wort...'
        self.image = 'images/s7.png'

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

    def __init__(self, previous_step):
        self.session = None
        self.button = 'Start Session'
        self.message = 'Session has Paused!'
        self.image = 'images/s1.png'
        self.previous_step = previous_step

    # Return to previous step
    def next_step(self):
        return self.previous_step

