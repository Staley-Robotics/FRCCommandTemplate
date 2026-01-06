import typing

from commands2 import Command, Subsystem
from subsystems.ExampleSubsystem import ExampleSubsystem

class ExampleCommand(Command):
    # Variable Declaration
    subsystem:ExampleSubsystem = None
    getValue:typing.Callable[[],float] = lambda: 0.0
    
    # Initialization
    def __init__( self,
                  mySubsystem:Subsystem,
                  myValue: typing.Callable[[], float] = lambda: 0.0
                ) -> None:
        # Command Attributes
        self.subsystem:ExampleSubsystem = mySubsystem
        self.getValue = myValue
        self.setName( "ExampleCommand" )
        self.addRequirements( mySubsystem )

    def initialize(self) -> None:
        pass

    def execute(self) -> None:
        self.subsystem.setSetpoint( self.getValue() )

    def end(self, interrupted:bool) -> None:
        pass

    def isFinished(self) -> bool:
        return False

    def runsWhenDisabled(self) -> bool:
        return False