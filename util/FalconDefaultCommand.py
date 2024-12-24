# Python Imports
from typing import Hashable, Callable, Dict

# FRC Imports
from commands2 import cmd, SelectCommand, Command

class FalconDefaultCommand(SelectCommand):
    __prevState:Hashable = None

    def __init__(
        self,
        commands:Dict[Hashable, Command],
        selector:Callable[[],Hashable],
        defaultCommand:Command = None
    ):
        """
        Creates a new DefaultCommand.

        Additional Features:
        - Updates Command Name based on Selected Command
        - Added IsFinished Logic for State Change
        - Improved Default Command Configuration

        :param commands: the map of commands to choose from
        :param selector: the selector to determine which command to run
        """
        super().__init__(commands, selector)
        self._defaultCommand = cmd.none().withName( f"None" ) if defaultCommand is None else defaultCommand
        self.setName( f"{self.__class__.__name__}" )

    def initialize(self) -> None:
        super().initialize()
        self.__prevState = self.__getCurrentState()
        name = "None" if self._selectedCommand is None else self._selectedCommand.getName()
        self.setName( name )

    def execute(self) -> None:
        super().execute()

    def isFinished(self) -> bool:
        changedState = self.__hasStateChanged()
        isFinished = super().isFinished()
        return changedState or isFinished

    def end(self, interrupted:bool) -> None:
        self.setName( f"{self.__class__.__name__}" )
        changedState = self.__hasStateChanged()
        super().end( interrupted or changedState )

    def __hasStateChanged(self) -> bool:
        return self.__getPreviousState() != self.__getCurrentState()

    def __getPreviousState(self) -> Hashable:
        return self.__prevState
    
    def __getCurrentState(self) -> Hashable:
        return self._selector()