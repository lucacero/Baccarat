import baccarat  # Import the simulation module
import sys

def run_batch_simulation(num_simulations=1000, starting_bankroll=10000):
    """
    Runs multiple Baccarat simulations without displaying plots.
    In addition to previous thresholds ($12k, $15k, $20k), this version tracks
    the number of simulations that reach:
      - 20% initial bankroll increase (i.e. balance >= 120% of starting bankroll)
      - 50% initial bankroll increase (>=150% of starting bankroll)
      - 100% initial bankroll increase (>=200% of starting bankroll)
      - 200% initial bankroll increase (>=300% of starting bankroll)
    Also prints an analysis summary of all sessions.
    """
    # Counters for existing absolute thresholds.
    threshold_counts = {12000: 0, 15000: 0, 20000: 0}
    
    # Counters for relative increases.
    relative_markers = {
        "20% Increase": 0,
        "50% Increase": 0,
        "100% Increase": 0,
        "200% Increase": 0
    }
    
    # Lists to store max and final balances from each simulation.
    all_max_balances = []
    all_final_balances = []
    
    for i in range(num_simulations):
        # Run simulation without plotting/printing.
        sim_data = baccarat.simulate_baccarat(display_plot=False, starting_bankroll=starting_bankroll)
        max_balance = sim_data["max_balance"]
        final_balance = sim_data["final_balance"]
        
        all_max_balances.append(max_balance)
        all_final_balances.append(final_balance)
        
        # Tally each absolute threshold.
        if max_balance >= 12000:
            threshold_counts[12000] += 1
        if max_balance >= 15000:
            threshold_counts[15000] += 1
        if max_balance >= 20000:
            threshold_counts[20000] += 1
        
        # Tally relative markers.
        if max_balance >= starting_bankroll * 1.2:
            relative_markers["20% Increase"] += 1
        if max_balance >= starting_bankroll * 1.5:
            relative_markers["50% Increase"] += 1
        if max_balance >= starting_bankroll * 2.0:
            relative_markers["100% Increase"] += 1
        if max_balance >= starting_bankroll * 3.0:
            relative_markers["200% Increase"] += 1

        # Print progress every 10% of simulations.
        #if (i + 1) % max(1, (num_simulations // 10)) == 0:
        #    print(f"Progress: {i + 1}/{num_simulations} simulations completed...")

    # Calculate percentages for absolute thresholds.
    pct_12k = 100 * threshold_counts[12000] / num_simulations
    pct_15k = 100 * threshold_counts[15000] / num_simulations
    pct_20k = 100 * threshold_counts[20000] / num_simulations
    
    # Calculate additional analysis.
    avg_max_balance = sum(all_max_balances) / len(all_max_balances)
    avg_final_balance = sum(all_final_balances) / len(all_final_balances)
    
    print("\nBatch Simulation Complete!")
    print("Summary of Absolute Thresholds:")
    print(f"  Simulations that reached at least $12,000: {threshold_counts[12000]} ({pct_12k:.2f}%)")
    print(f"  Simulations that reached at least $15,000: {threshold_counts[15000]} ({pct_15k:.2f}%)")
    print(f"  Simulations that reached at least $20,000: {threshold_counts[20000]} ({pct_20k:.2f}%)")
    
    print("\nSummary of Relative Bankroll Increases:")
    for marker, count in relative_markers.items():
        pct = 100 * count / num_simulations
        print(f"  Simulations that reached {marker}: {count} ({pct:.2f}%)")
    
    print("\nAdditional Analysis:")
    print(f"  Average maximum balance reached: ${avg_max_balance:,.2f}")
    print(f"  Average final balance: ${avg_final_balance:,.2f}")
    
    return threshold_counts, relative_markers

if __name__ == "__main__":
    # Default starting bankroll is $10,000 (minimum $1,000)
    starting_bankroll = 10000
    if len(sys.argv) > 2:
        try:
            starting_bankroll = float(sys.argv[2])
        except ValueError:
            print("Invalid starting bankroll. Using default: 10000")
    elif len(sys.argv) == 2:
        # if only one argument is provided, treat it as number of simulations
        starting_bankroll = 10000

    num_simulations = 1000
    if len(sys.argv) > 1:
        try:
            num_simulations = int(sys.argv[1])
        except ValueError:
            print("Invalid number of simulations. Using default: 10")

    print(f"Running {num_simulations} Baccarat simulations with a starting bankroll of ${starting_bankroll:,.2f}...\n")
    run_batch_simulation(num_simulations, starting_bankroll)
