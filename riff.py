import genki_signals.functions as f
import numpy as np

class Riff(f.SignalFunction):
    def __init__(self, input_signal: f.SignalName, name: str, threshold: float):
        super().__init__(input_signal, name=name, params={"threshold": threshold})
        self.threshold = threshold
        self.aerostar = False

    def __call__(self, x):
        exceeds = x > self.threshold
        squeeze = np.array([any(x) for x in exceeds.T])

    
        if any(x < self.threshold) and not self.aerostar:
            self.aerostar = True
        elif any(x < self.threshold) and self.aerostar:
            self.aerostar = False
        return x

