# imports
import math
import itertools

# initialize variables
B_VALUES = [55.0, 55.0, 5.0]
A_VALUES = [120.0, 120.0, 120.0]
HPA_VALUES = [10.0, 10.0, 9.0]
DTR = 3.0
DV = 110.0  
# wait to initialize Hpd inside the calculation loop

# constant
ALL_L_VALUES = [float(x) for x in range(10)]

### CALCULATE DAMAGES ##################################################################
damages = []
num_attacks = len(B_VALUES)

# iterate over all attack permutations
for attack_indices in itertools.permutations(range(num_attacks)):
    sub_damages = []

    # iterate over all permutations of L's
    for L_VALUES in itertools.product(ALL_L_VALUES, repeat=num_attacks):
        # initialize variables
        damage = 0
        HPd = 100.0

        # simulate attacks
        for ai, L in zip(attack_indices, L_VALUES):
            # pre-calculate
            B = B_VALUES[ai]
            A = A_VALUES[ai]
            HPA = HPA_VALUES[ai]
            HPd_visible = math.ceil(HPd/10.0)
            
            # calculate
            damage_float = (B*A/100.0+L) * HPA/10.0 * (200.0-(DV+DTR*HPd_visible))/100.0

            # round down if the decimal is between 0 and 0.95
            # round down if the decimal is 0.95
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
    kp = sum(i >= 100 for i in ds) / 1000.0 

    kill_probs[perm] = kp

# print (descending)
sorted_kp = sorted(kill_probs.items(), key=lambda item: item[1], reverse=True)

print("Kill Probability Per Permutation:")
for k,v in sorted_kp:
    print(k,': ', v)
