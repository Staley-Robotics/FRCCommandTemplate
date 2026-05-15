import typing

from commands2 import Command, Subsystem
from subsystems.ExampleSubsystem import ExampleSubsystem

'''
If you're new to commands/programming, try hovering over the functions used here to see what they do
'''

class ExampleCommand(Command):
    def __init__( self,
                  mySubsystem:ExampleSubsystem,
                  myValue: typing.Callable[[], float] = lambda: 0.0
                ) -> None:
        '''
        Called once when the command is *created*, so is called only once
        the 'initialize' function overrided below, is called every time the command is run (e.g. every time its attached trigger, like a controller button, activates)
        '''
        # Command Attributes
        self.subsystem:ExampleSubsystem = mySubsystem
        self.getValue = myValue

        ## Command setup
        # setName assigns how this command will be labeled, primarily in NetworkTables
        self.setName( f"{self.__class__.__name__}" ) # "self.__class__.__name__" will automatically get the name of the class, in this case "ExampleCommand"
        self.addRequirements( mySubsystem ) # <- take note of the description of addRequirements

    ## Overriding functions inherited from Command
    def initialize(self) -> None:
        ... # Run what happens immediately when the command is called

    def execute(self) -> None:
        self.subsystem.setSetpoint( self.getValue() )

    def end(self, interrupted:bool) -> None:
        ... # Run what happens when the command ends

    def isFinished(self) -> bool:
        return False

    def runsWhenDisabled(self) -> bool:
        return False