import numpy as np
from abc import ABC, abstractmethod

class Rockmass(ABC):
    def __init__(self, ucs, fa, name=None):
        self.ucs = ucs
        self.fa = fa
        self.name = name or self.__class__.__name__

    @property
    @abstractmethod
    def fa(self) -> float:
        pass

    @fa.setter
    @abstractmethod
    def fa(self, value):
        value_array = np.asarray(value)
        if np.any((value_array < 0) | (value_array > 90)):
            raise ValueError("Physics Breach: Friction angle must be between 0 and 90.")

    @abstractmethod
    def estimated_strength(self, confinement, **kwargs):
        k = (1 + np.sin(np.radians(self.fa))) / (1 - np.sin(np.radians(self.fa)))
        return self.ucs + (k * confinement)

    def __str__(self):
        return f"{self.name} | UCS: {self.ucs} MPa | FA: {self.fa}°"

    def __repr__(self):
        active = [f"{k.lstrip('_')}={v!r}" for k, v in vars(self).items() if v is not None]
        return f"{self.__class__.__name__}({', '.join(active)})"

class Hrock(Rockmass):
    def __init__(self, ucs, fa, fd, name=None):
        self._fa = None
        super().__init__(ucs, fa, name=name)
        self.fd = fd

    @property
    def fa(self) -> float:
        return self._fa # type: ignore

    @fa.setter
    def fa(self, value):
        Rockmass.fa.fset(self, value) # type: ignore
        self._fa = value

    def estimated_strength(self, confinement, **kwargs):
        base_str = super().estimated_strength(confinement=confinement, **kwargs)
        stress_dir = kwargs.get('stress_dir')

        if stress_dir is not None:
            condition = np.abs(stress_dir - self.fd) <= 10
            return np.where(condition, base_str * 0.68, base_str)

        return base_str

    def __repr__(self):
        active = [f"{k.lstrip('_')}={v!r}" for k, v in vars(self).items() if v is not None]
        return f"{self.__class__.__name__}({', '.join(active)})"

    def __str__(self):
        return f"{super().__str__()} | Foliation: {self.fd}°"
