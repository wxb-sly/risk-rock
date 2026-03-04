import numpy as np
from core.geology import Hrock

class TunnelSupport:
    def __init__(self, cost_per_m: float, **kwargs):
        shotcrete_thickness = kwargs.get('shotcrete_thickness')
        self.shotcrete_thickness = shotcrete_thickness
        bolt_length = kwargs.get('bolt_length')
        self.bolt_length = bolt_length
        self.cost_per_m = cost_per_m

    def __repr__(self):
        active = [f"{k.lstrip('_')}={v!r}" for k, v in vars(self).items() if v is not None]
        return f"{self.__class__.__name__}({', '.join(active)})"

    def __str__(self):
        report = [
            f"{k.lstrip('_').replace('_', ' ').title()}: {v}"
            for k, v in vars(self).items()
            if v is not None and k != 'name'
        ]
        return f"SUPPORT | {' | '.join(report)}"

class TunnelSection:
    def __init__(self, section_id: str, geology: Hrock, support: TunnelSupport, fos):
        self.section_id = section_id
        self.geology = geology
        self.support = support
        self.fos = fos

    def calculate_risk_factor(self):
        strength = self.geology.estimated_strength(confinement=0, stress_dir=90)
        return np.where(strength < 50, "Low Risk", "High Risk")

    def total_cost(self, length):
        return self.support.cost_per_m * length

    def __repr__(self):
        active = [f"{k.lstrip('_')}={v!r}" for k, v in vars(self).items() if v is not None]
        return f"{self.__class__.__name__}({', '.join(active)})"

    def __str__(self):
        return (
            f"--- SECTION REPORT: {self.section_id} ---\n"
            f"  GEOLOGY: {self.geology}\n"
            f"  SUPPORT: {self.support}\n"
            f"  STATUS:  {self.calculate_risk_factor()}"
        )

    def implement_fos(self):
        return pow(2, self.fos)

    def __call__(self, length):
        return self.total_cost(length)

    def __add__(self, other):
        return self.implement_fos() + other.implement_fos()
