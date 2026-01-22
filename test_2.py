# imports
import math
import itertools

# Initialize constants and damage list
BASE_DAMAGE_VALUES = [55.0, 55.0, 5.0]
A_VALUES = [120.0, 120.0, 120.0]
HPA_VALUES = [10.0, 10.0, 9.0]
DTR = 3.0
DV = 110.0  
# don't initialize HPd yet

ALL_L_VALUES = [float(x) for x in range(10)]

damages = []

# calculate damages
for attack_indices in itertools.permutations(range(3)):
    sub_damages = []

    # loop over permutations of L's
    for L_VALUES in itertools.product(ALL_L_VALUES, repeat=3):
        # initialize variables
        damage = 0
        HPd = 100.0

        # simulate 3 attacks
        for attack_index, L in zip(attack_indices, L_VALUES):
            # pre-calculate
            BD = BASE_DAMAGE_VALUES[attack_index]
            A = A_VALUES[attack_index]
            HPA = HPA_VALUES[attack_index]
            HPd_visible = math.ceil(HPd/10.0)
            
            # calculate
            damage_float = (BD*A/100.0+L) * HPA/10.0 * (200.0-(DV+DTR*HPd_visible))/100.0

            # round down if the decimal is between 0 and 0.95
            # round up if the decimal is between 0.95 and 1
            damage_part = math.ceil(damage_float - 0.95)

            # iterate
            HPd -= damage_part
            damage += damage_part

        # append damage
        sub_damages.append(damage)

    # append damages of one attack permutation
    damages.append({attack_indices: sub_damages})

# print kill probabilities
print("Kill Probabilities:")
for damage_index in range(6):
    perm = list(damages[damage_index].keys())[0]
    ds = list(damages[damage_index].values())[0]
    kill_prob = sum(i >= 100 for i in ds) / 1000
    
    print(perm, ": ", kill_prob)
