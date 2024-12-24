# FRC Imports
from wpimath import applyDeadband
from commands2.button import CommandXboxController

class FalconXboxController(CommandXboxController):
    def __init__(self, port:int, deadband:float = 0.04, squaredInputs:bool = True):
        super().__init__(port)
        self.__deadband = deadband
        self.__squaredInputs = squaredInputs

    def getLeftUpDown(self) -> float:
        """
        Get the Up/Down axis value of left side of the controller.
        
        Additional Features:
        - Integrates Deadband
        - Allows for Squared Inputs
        - Positive Forward

        :returns: The axis value.
        """
        lY = -super().getLeftY()
        returnY = lY * ( 1 if not self.__squaredInputs else abs(lY) )
        return applyDeadband( returnY, self.__deadband )
    
    def getLeftSideToSide(self) -> float:
        """
        Get the Side to Side axis value of left side of the controller.
        
        Additional Features:
        - Integrates Deadband
        - Allows for Squared Inputs
        - Positive Left

        :returns: The axis value.
        """
        lX = -super().getLeftX()
        returnX = lX * ( 1 if not self.__squaredInputs else abs(lX) )
        return applyDeadband( returnX, self.__deadband )
    
    def getRightUpDown(self) -> float:
        """
        Get the Up/Down axis value of right side of the controller.
        
        Additional Features:
        - Integrates Deadband
        - Allows for Squared Inputs
        - Positive Forward

        :returns: The axis value.
        """
        lY = -super().getRightY()
        returnY = lY * ( 1 if not self.__squaredInputs else abs(lY) )
        return applyDeadband( returnY, self.__deadband )

    
    def getRightSideToSide(self) -> float:
        """
        Get the Side to Side axis value of right side of the controller.
        
        Additional Features:
        - Integrates Deadband
        - Allows for Squared Inputs
        - Positive Left

        :returns: The axis value.
        """
        lX = -super().getRightX()
        returnX = lX * ( 1 if not self.__squaredInputs else abs(lX) )
        return applyDeadband( returnX, self.__deadband )
    
    # Override getLeftTriggerAxis with deadband (for FRC)
    def getLeftTriggerAxis(self) -> float:
        """
        Get the left trigger (LT) axis value of the controller. Note that this axis is bound to the
        range of [0, 1] as opposed to the usual [-1, 1].
        
        Additional Features:
        - Integrates Deadband
        - Allows for Squared Inputs

        :returns: The axis value.
        """
        lT = super().getLeftTriggerAxis()
        returnLT = lT * ( 1 if not self.__squaredInputs else abs(lT) )
        return applyDeadband( returnLT, self.__deadband )
    
    # Override getRightTriggerAxis with deadband (for FRC)
    def getRightTriggerAxis(self) -> float:
        """
        Get the right trigger (RT) axis value of the controller. Note that this axis is bound to the
        range of [0, 1] as opposed to the usual [-1, 1].
        
        Additional Features:
        - Integrates Deadband
        - Allows for Squared Inputs

        :returns: The axis value.
        """
        rT = super().getRightTriggerAxis()
        returnRT = rT * ( 1 if not self.__squaredInputs else abs(rT) )
        return applyDeadband( returnRT, self.__deadband )
    
    # Custom Command to combine Left and Right Trigger Axises
    def getTriggers(self) -> float:
        """
        Get the single axis value of both triggers of the controller. 
        
        Additional Features:
        - Combines LT and RT
        - Integrates Deadband
        - Allows for Squared Inputs
        - Positive Left

        :returns: The axis value.
        """
        asOneAxis:float = self.getLeftTriggerAxis() - self.getRightTriggerAxis()
        return asOneAxis
    
