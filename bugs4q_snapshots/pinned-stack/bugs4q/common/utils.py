import math
from scipy.stats import norm, chisquare

ALPHA = 0.05


def lower_confidence_bound(probability, shots):
    z = norm.ppf(1 - ALPHA)
    sigma = math.sqrt(probability * (1 - probability) / shots)
    lower_bound = probability - z * sigma

    return lower_bound


def compute_component_delta(expected_value, total_shots):
    if total_shots <= 0:
        raise ValueError("total_shots must be positive")
    if not (-1.0 <= expected_value <= 1.0):
        raise ValueError("expected_value must satisfy -1 <= expected_value <= 1")

    z = norm.ppf(1 - ALPHA / 2)
    return z * math.sqrt((1.0 - expected_value ** 2) / total_shots)


def chi_square_pvalue(expected_dict, observed_dict):
    expected_keys = set(expected_dict.keys())
    observed_keys = set(observed_dict.keys())

    if expected_keys != observed_keys:
        return None, ALPHA

    keys = sorted(expected_keys)

    f_exp = []
    f_obs = []

    for key in keys:
        exp = expected_dict[key]
        obs = observed_dict[key]

        if exp < 0 or obs < 0:
            raise ValueError("counts must be non-negative")

        if exp == 0 and obs == 0:
            continue

        if exp == 0 and obs > 0:
            return 0.0, ALPHA

        f_exp.append(exp)
        f_obs.append(obs)

    if not f_exp:
        raise ValueError("no valid bins to compare")

    if sum(f_exp) != sum(f_obs):
        raise ValueError("total counts differ")

    return float(chisquare(f_obs=f_obs, f_exp=f_exp).pvalue), ALPHA