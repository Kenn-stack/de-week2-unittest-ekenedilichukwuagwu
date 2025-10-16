class ArtificialPancreasSystem:
    """A simplified model for data-driven glucose regulation."""
        
    GLUCOSE_PER_CARB: float = 0.5      # fixed increase per carb unit
    GLUCOSE_BURN_PER_MIN: float = 0.3  # fixed decrease per minute of exercise


    def __init__(self, glucose_level: float):
        """
        glucose_level: The current glucose reading of the person.
        insulin_sensitivity: How strongly insulin affects the glucose drop. Higher = more sensitive.
        target_glucose: The “ideal” glucose level the system is trying to maintain.
        tolerance: The small range above or below the target where we can still consider the glucose level stable.
        """
        self.glucose_level: float = glucose_level
        self.insulin_sensitivity: float = 1.0
        self.target_glucose: int = 100
        self.tolerance: int = 10
        

    def meal(self, carbs: float):
        """Simulate a meal event (input feature: carbs)."""
        self.glucose_level += carbs * ArtificialPancreasSystem.GLUCOSE_PER_CARB

    def exercise(self, duration: float):
        """Simulate physical activity (input feature: duration)."""
        if self.glucose_level - (duration * ArtificialPancreasSystem.GLUCOSE_BURN_PER_MIN) < 50:
            self.glucose_level = 50
        else:
            self.glucose_level -= duration * ArtificialPancreasSystem.GLUCOSE_BURN_PER_MIN

    def predict_action(self):
        """
        Predict and apply an appropriate system action.
        Acts like a decision function in a model.
        """
        if self.glucose_level > (self.target_glucose + self.tolerance):
            return self.deliver_insulin()
        elif self.glucose_level < (self.target_glucose - self.tolerance):
            return self.warn_low_glucose()
        else:
            return self.maintain()
        
        
    def deliver_insulin(self):
        dose = self.glucose_level - self.target_glucose
        self.glucose_level -= dose
        return ('deliver_insulin', self.glucose_level)
        
    def warn_low_glucose(self):
        glucose_needed = self.target_glucose - self.glucose_level
        carbs_needed = glucose_needed / 0.5
        self.meal(carbs_needed)
        return ('warn_low_glucose', self.glucose_level)
        
    def maintain(self):
        return ('maintain', self.glucose_level)