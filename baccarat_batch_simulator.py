import baccarat  # Import the simulation module
import sys

def run_batch_simulation(num_simulations=10):
    """
    Runs multiple Baccarat simulations without displaying plots,
    and counts how many simulations reached at least $12,000, $15,000, and $20,000.
    Also, prints an analysis summary of all sessions.
    """
    # Counters for reaching specific thresholds.
    threshold_counts = {12000: 0, 15000: 0, 20000: 0}
    
    # Lists to store max and final balances from each simulation.
    all_max_balances = []
    all_final_balances = []
    
    for i in range(num_simulations):
        # Run simulation without plotting/printing.
        sim_data = baccarat.simulate_baccarat(display_plot=False)
        max_balance = sim_data["max_balance"]
        final_balance = sim_data["final_balance"]
        
        all_max_balances.append(max_balance)
        all_final_balances.append(final_balance)
        
        # Tally each threshold.
        if max_balance >= 12000:
            threshold_counts[12000] += 1
        if max_balance >= 15000:
            threshold_counts[15000] += 1
        if max_balance >= 20000:
            threshold_counts[20000] += 1

        # Print progress every 10% of simulations.
        if (i + 1) % max(1, (num_simulations // 10)) == 0:
            print(f"Progress: {i + 1}/{num_simulations} simulations completed...")

    # Calculate percentages.
    pct_12k = 100 * threshold_counts[12000] / num_simulations
    pct_15k = 100 * threshold_counts[15000] / num_simulations
    pct_20k = 100 * threshold_counts[20000] / num_simulations
    
    # Calculate additional analysis.
    avg_max_balance = sum(all_max_balances) / len(all_max_balances)
    avg_final_balance = sum(all_final_balances) / len(all_final_balances)
    
    print("\nBatch Simulation Complete!")
    print("Summary of Results:")
    print(f"  Simulations that reached at least $12,000: {threshold_counts[12000]} ({pct_12k:.2f}%)")
    print(f"  Simulations that reached at least $15,000: {threshold_counts[15000]} ({pct_15k:.2f}%)")
    print(f"  Simulations that reached at least $20,000: {threshold_counts[20000]} ({pct_20k:.2f}%)")
    
    print("\nAdditional Analysis:")
    print(f"  Average maximum balance reached: ${avg_max_balance:,.2f}")
    print(f"  Average final balance: ${avg_final_balance:,.2f}")
    
    return threshold_counts

if __name__ == "__main__":
    # Default to 100 simulations, or use a command-line argument if provided.
    num_simulations = 10
    if len(sys.argv) > 1:
        try:
            num_simulations = int(sys.argv[1])
        except ValueError:
            print("Invalid number of simulations. Using default: 100")

    print(f"Running {num_simulations} Baccarat simulations...\n")
    run_batch_simulation(num_simulations)
