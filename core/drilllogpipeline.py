import pandas as pd
import numpy as np
from pathlib import Path
np.random.seed(42)



class DrillLogPipeline:
    """Ingests, validates, and formats drill-log data for PyMC models."""

    def __init__(self, filepath: Path ) -> None:
        self.filepath = filepath
        self.raw_data = None
        self.clean_data = None


    def load(self) -> pd.DataFrame:
        """load the raw csv"""
        self.raw_data = pd.read_csv(self.filepath)
        print(f"Loaded {len(self.raw_data)} rows from {self.filepath}")
        return self.raw_data

    def check_null(self):
        """High-signal Forensic Audit: only reports on Data Voids (NaNs)."""
        null_counts = self.raw_data.isnull().sum() #type: ignore
        self.data_voids = null_counts[null_counts > 0]

        if self.data_voids.empty:
            print("Forensic Audit: No data voids detected.")
        else:
            print("Forensic Alert: Data voids found in high-priority parameters:")
            for param, count in self.data_voids.items():
                print(f"  - {param}: {count} null values")
        return self.data_voids

    def check_range(self, column_targets: list | dict, min_val: float = 0, max_val: float = 100, clipto_bounds: bool = False):
        """
        Checks columns against physical ranges.
        Provide a list to use default min/max bounds, or a dict mapping targets to (min, max) tuples.
        """
        results = {}


        if isinstance(column_targets, list):
            column_targets = {col: (min_val, max_val) for col in column_targets}

        for target, (target_min, target_max) in column_targets.items():
            col_name = self.raw_data.columns[target] if isinstance(target, int) else target  #type: ignore

            out_of_range = np.sum((self.raw_data[col_name] < target_min) | (self.raw_data[col_name] > target_max)).item()  #type: ignore
            results[col_name] = out_of_range

            if out_of_range > 0:
                print(f"Forensic Alert: [{col_name}] has {out_of_range} values outside [{target_min}, {target_max}]")

            if clipto_bounds:

                self.raw_data[col_name] = self.raw_data[col_name].clip(lower=target_min, upper=target_max) #type: ignore
                if out_of_range > 0:
                    print(f"  -> Action Taken: Clipped out-of-bounds values for [{col_name}] to [{target_min}, {target_max}].")

        return results


    def clean(self, drop_na: bool = False, reset_index: bool = True) -> pd.DataFrame:
        """Clean the data for modeling."""
        df = self.raw_data.copy() #type: ignore

        if drop_na:
            print("\n[!] FORENSIC ALERT: Prime Directive Violation. Dropping data voids instead of interrogating them.")
            na_cols = df.columns[df.isnull().any()].tolist()
            if na_cols:
                df = df.dropna(subset=na_cols)
                print(f"Dropped rows with missing values in {na_cols}. Remaining: {len(df)}")

        if reset_index:
            df = df.reset_index(drop=True)

        self.clean_data = df
        return df


    def to_pymc(self, column: str) -> np.ndarray:
        """Extract a clean NumPy array ready for PyMC observed= parameter."""
        if self.clean_data is None:
            raise ValueError("Run .clean() first!")
        return self.clean_data[column].values #type: ignore


    def get_summary(self) -> pd.DataFrame:
        """High-signal statistical readout for pre-MCMC variance checks."""
        if self.clean_data is None:
            raise ValueError("Run .clean() first!")

        print("\n--- Operational Data Summary ---")
        summary = self.clean_data.describe().T[['count', 'mean', 'std', 'min', 'max']]
        return summary.round(1)

    def suggest_priors(self, column: str) -> dict:
        """
        Suggest weakly informative priors based on the empirical data range.
        Calculates and formats both Normal and Uniform distributions so you can choose based on physics.
        """

        data = self.to_pymc(column)

        emp_mean = np.mean(data)
        emp_std = np.std(data)
        emp_min = np.min(data)
        emp_max = np.max(data)

        n_mu = round(float(emp_mean), 2)
        n_sig = round(float(emp_std * 2.0), 2) # Double std dev for Normal
        u_low = round(float(emp_min * 0.8), 2) # -20% buffer for Uniform
        u_high = round(float(emp_max * 1.2), 2) # +20% buffer for Uniform

        print(f"\n[+] Prior Orchestration for '{column}':")
        print(f"  -> Empirical Data : mean={emp_mean:.1f} | std={emp_std:.1f} | range=[{emp_min:.1f}, {emp_max:.1f}]")
        print("  [Option A] Normal prior (Use if physics allow symmetric variance without hitting 0):")
        print(f"      pm.Normal('{column}_prior', mu={n_mu}, sigma={n_sig})")
        print("  [Option B] Uniform prior (Use if you have hard structural min/max boundaries):")
        print(f"      pm.Uniform('{column}_prior', lower={u_low}, upper={u_high})")

        return {"normal": (n_mu, n_sig), "uniform": (u_low, u_high)}

    def encode_rock_class(self) -> np.ndarray:
        """Convert rock class strings to ordered integers for PyMC."""
        mapping = {"I": 0, "II": 1, "III": 2, "IV": 3, "V": 4}
        return self.clean_data["rock_class"].map(mapping).values #type: ignore

    def __repr__(self):
        n = len(self.raw_data) if self.raw_data is not None else 0
        return f"<DrillLogPipeline('{self.filepath}', n={n})>"
