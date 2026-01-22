# imports
import math
import itertools

# Initialize variables
BASE_DAMAGE_VALUES = [55.0, 55.0, 5.0]
A_VALUES = [120.0, 120.0, 120.0]
HPA_VALUES = [10.0, 10.0, 9.0]
DTR = 3.0
DV = 110.0  
# wait to initialize Hpd inside the calculation loop

ALL_L_VALUES = [float(x) for x in range(10)]

### CALCULATE DAMAGES ##################################################################
damages = []
num_perms = len(BASE_DAMAGE_VALUES)

# iterate over all attack permutations
for attack_indices in itertools.permutations(range(num_perms)):
    sub_damages = []

    # iterate over all permutations of L's
    for L_VALUES in itertools.product(ALL_L_VALUES, repeat=num_perms):
        # initialize variables
        damage = 0
        HPd = 100.0

        # simulate attacks
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

### KILL PROBABILITIES ############################################################
kill_probs = {}

# calculate
for d in damages:
    perm = list(d.keys())[0]
    ds = list(d.values())[0]
    kp = sum(i >= 100 for i in ds) / 10.0 # /1000*100

    kill_probs[perm] = kp

# print
print("Kill Probabilites (%):")
for k,v in kill_probs.items():
    print(k, ': ', v, '%')
