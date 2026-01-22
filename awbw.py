import math
import itertools

# Initialize variables
HPDefender = 100
HPA = [10, 10, 9]   # attacker HP for each attack
base_damage = [55, 55, 5]
A = [120, 120, 120]
terrainstar = 3
D = 110  # defense

# Store expected final HP for all 6 orders
results_expected_HPD = {}
results_distribution = {}

# Try all 6 permutations of 3 attacks
for order in itertools.permutations([0, 1, 2]):
    dictionary = {}
    
# Loop over all luck combinations
for L0 in range(10):
    for L1 in range(10):
        for L2 in range(10):
            total_damage = 0
            luck_values = [L0, L1, L2]

            # Apply attacks in the current order
            for pos, attack_index in enumerate(order):
                L = luck_values[attack_index] # choose an L out of L0, L1, L2
                base_damage = (base_damage[attack_index] * A[attack_index] / 100) + L
                hp_factor = HPA[attack_index] / 10
                defense_factor = (200 - (D + terrainstar * math.ceil(HPDefender / 10))) / 100

                damage_value = base_damage * hp_factor * defense_factor
                rounded_damage = int(math.ceil(damage_value / 0.05) * 0.05)
                total_damage += rounded_damage

            remainingHP = HPDefender - total_damage

            if remainingHP in dictionary:
                dictionary[remainingHP] += 1
            else:
                dictionary[remainingHP] = 1

# Calculate expected final HPD
total_outcomes = sum(dictionary.values())
expected_HPD = sum(k * v for k, v in dictionary.items()) / total_outcomes
results_expected_HPD[order] = expected_HPD
results_distribution[order] = dictionary

# Print expected HP for all 6 attack orders
print("Expected final HPD for all 6 attack orders:\n")
for order, ev in results_expected_HPD.items():
    print(f"Attack order {order}: Expected final HPD = {ev:.2f}")

# Pick the order with the **lowest expected HPD** (max damage)
best_order = min(results_expected_HPD, key=results_expected_HPD.get)
best_expected = results_expected_HPD[best_order]
best_distribution = results_distribution[best_order]

# Range of remaining HPD for best order
min_HPD = min(best_distribution.keys())
max_HPD = max(best_distribution.keys())

print(f"\nBest attack order: {best_order} (Expected final HPD = {best_expected:.2f})")
print(f"Range of remaining HPD for best order: {min_HPD} – {max_HPD}\n")

# Optional: print distribution for best order
print("Remaining HPD distribution for best order:")
for hp, count in sorted(best_distribution.items()):
    print(f"HPD {hp}: {count} occurrences")