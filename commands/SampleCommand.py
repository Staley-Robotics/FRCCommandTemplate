import typing

from commands2 import Command, Subsystem
from subsystems.SampleSubsystem import SampleSubsystem

class SampleCommand(Command):
    # Variable Declaration
    m_subsystem:SampleSubsystem = None
    m_getValue:typing.Callable[[],float] = lambda: 0.0
    
    # Initialization
    def __init__( self,
                  mySubsystem:Subsystem,
                  myValue: typing.Callable[[], float] = lambda: 0.0
                ) -> None:
        # Command Attributes
        self.m_subsystem:SampleSubsystem = mySubsystem
        self.m_getValue = myValue
        self.setName( "SampleCommand" )
        self.addRequirements( mySubsystem )

    # On Start
    def initialize(self) -> None:
        pass

    # Periodic
    def execute(self) -> None:
        self.m_subsystem.setSetpoint( self.m_getValue() )

    # On End
    def end(self, interrupted:bool) -> None:
        pass

    # Is Finished
    def isFinished(self) -> bool:
        return False

    # Run When Disabled
    def runsWhenDisabled(self) -> bool:
        return False