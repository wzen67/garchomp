import numpy as np
import matplotlib.pyplot as plt

def B_terms(atk, crit, defense):
    B1 = int(int(1.2 * crit * atk)*600/(defense+600))
    B2 = int(int(1.2 * atk)*600/(defense+600))
    return(B1, B2)

# Precompute probabilities instead of generating them in the simulation loop
def compute_outcomes(probability, n_autos, n_runs):
    rng = np.random.default_rng()
    outcomes = rng.binomial(n=1, p=probability, size=(n_autos,2,n_runs))

    return(outcomes)

def simulation(Bk_1, Bk_2, crit, hp, defense, outs, n_autos, n_runs):
    sim_values = []

    for j in range(n_runs):
        # Initialize sum
        S_k = 0
        # Compute A_k iteratively
        for k in range(n_autos):
            remaining_hp = hp - S_k

            # Choose probabilistically
            if outs[k,0,j]:
                B_k = Bk_1
            else:
                B_k = Bk_2

            if outs[k,1,j]:
                term = int(int(0.1 * crit * remaining_hp)*600/(defense+600))
            else:
                term = int(int(0.1 * remaining_hp)*600/(defense+600))

            # Update sum
            S_k += B_k + term

        sim_values.append(S_k)

    return(sim_values)

if __name__ == "__main__":
    # constants
    # level 9, scarf, scope
    atk = 312
    crit = 2.12
    pre_nerf_probability = 0.26
    current_probability = 0.16
    hp = 4900
    d = 275
    autos = 3
    runs = 10000

    # compute terms
    Bk_1, Bk_2 = B_terms(atk=atk, crit=crit, defense=d)

    outcomes = compute_outcomes(probability=pre_nerf_probability, n_autos=autos, n_runs=runs)
    pre_nerf_values = simulation(Bk_1, Bk_2, crit=crit, hp=hp, defense=d, outs=outcomes, n_autos=autos, n_runs=runs)

    outcomes = compute_outcomes(probability=current_probability, n_autos=autos, n_runs=runs)
    current_values = simulation(Bk_1, Bk_2, crit=crit, hp=hp, defense=d, outs=outcomes, n_autos=autos, n_runs=runs)

    # plot
    fig, (ax1, ax2) = plt.subplots(1, 2, sharey=True)
    ax1.hist(pre_nerf_values, weights=np.ones_like(pre_nerf_values) / len(pre_nerf_values))
    ax2.hist(current_values, weights=np.ones_like(current_values) / len(current_values))
    ax1.set_xlabel('Damage')
    ax2.set_xlabel('Damage')
    ax1.set_ylabel('Frequency')
    ax1.set_title('Pre-Nerf')
    ax2.set_title('Post-Nerf')
    title = 'Garchomp: Level 9, Scarf, Scope; 3 Boosted Autos\nEnemy: 7500 HP, 500 Def\n10,000 Simulations'
    fig.suptitle(title)
    plt.show()
