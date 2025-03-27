import baccarat  # Import the simulation module
import sys

def run_batch_simulation(num_simulations=100, starting_bankroll=30000):
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
    
    # Counters for relative increases.
    relative_markers = {
        "5% Increase": 0,
        "10% Increase": 0,
        "15% Increase": 0,
        "20% Increase": 0,
        "25% Increase": 0,
        "30% Increase": 0,
        "35% Increase": 0,
        "40% Increase": 0,
        "45% Increase": 0,
        "50% Increase": 0,
        "55% Increase": 0,
        "60% Increase": 0,
        "65% Increase": 0,
        "70% Increase": 0,
        "75% Increase": 0,
        "80% Increase": 0,
        "85% Increase": 0,
        "90% Increase": 0,
        "95% Increase": 0,
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
        
        # Tally relative markers.
        if max_balance >= starting_bankroll * 1.05:
            relative_markers["5% Increase"] += 1
        if max_balance >= starting_bankroll * 1.10:
            relative_markers["10% Increase"] += 1   
        if max_balance >= starting_bankroll * 1.15:
            relative_markers["15% Increase"] += 1
        if max_balance >= starting_bankroll * 1.20:
            relative_markers["20% Increase"] += 1
        if max_balance >= starting_bankroll * 1.25:
            relative_markers["25% Increase"] += 1
        if max_balance >= starting_bankroll * 1.30:  
            relative_markers["30% Increase"] += 1
        if max_balance >= starting_bankroll * 1.35:
            relative_markers["35% Increase"] += 1
        if max_balance >= starting_bankroll * 1.40:
            relative_markers["40% Increase"] += 1
        if max_balance >= starting_bankroll * 1.45:
            relative_markers["45% Increase"] += 1
        if max_balance >= starting_bankroll * 1.50:
            relative_markers["50% Increase"] += 1
        if max_balance >= starting_bankroll * 1.55:
            relative_markers["55% Increase"] += 1
        if max_balance >= starting_bankroll * 1.60:
            relative_markers["60% Increase"] += 1
        if max_balance >= starting_bankroll * 1.65:
            relative_markers["65% Increase"] += 1
        if max_balance >= starting_bankroll * 1.70:
            relative_markers["70% Increase"] += 1
        if max_balance >= starting_bankroll * 1.75:
            relative_markers["75% Increase"] += 1
        if max_balance >= starting_bankroll * 1.80:
            relative_markers["80% Increase"] += 1
        if max_balance >= starting_bankroll * 1.85:
            relative_markers["85% Increase"] += 1
        if max_balance >= starting_bankroll * 1.90:
            relative_markers["90% Increase"] += 1
        if max_balance >= starting_bankroll * 1.95:
            relative_markers["95% Increase"] += 1
        if max_balance >= starting_bankroll * 2.0:
            relative_markers["100% Increase"] += 1
        if max_balance >= starting_bankroll * 3.0:
            relative_markers["200% Increase"] += 1

        # Print progress every 10% of simulations.
        #if (i + 1) % max(1, (num_simulations // 10)) == 0:
        #    print(f"Progress: {i + 1}/{num_simulations} simulations completed...")
    
    # Calculate additional analysis.
    avg_max_balance = sum(all_max_balances) / len(all_max_balances)
    avg_final_balance = sum(all_final_balances) / len(all_final_balances)
    
    print("\nBatch Simulation Complete!")
    
    print("\nSummary of Relative Bankroll Increases:")
    for marker, count in relative_markers.items():
        pct = 100 * count / num_simulations
        print(f"  Simulations that reached {marker}: {count} ({pct:.2f}%)")
    
    print("\nAdditional Analysis:")
    print(f"  Average maximum balance reached: ${avg_max_balance:,.2f}")
    print(f"  Average final balance: ${avg_final_balance:,.2f}")
    
    return relative_markers

if __name__ == "__main__":
    # Default starting bankroll is $10,000 (minimum $1,000)
    starting_bankroll = 20000
    if len(sys.argv) > 2:
        try:
            starting_bankroll = float(sys.argv[2])
        except ValueError:
            print("Invalid starting bankroll. Using default: 10000")
    elif len(sys.argv) == 2:
        # if only one argument is provided, treat it as number of simulations
        starting_bankroll = 20000

    num_simulations = 100
    if len(sys.argv) > 1:
        try:
            num_simulations = int(sys.argv[1])
        except ValueError:
            print("Invalid number of simulations. Using default: 10")

    print(f"Running {num_simulations} Baccarat simulations with a starting bankroll of ${starting_bankroll:,.2f}...\n")
    run_batch_simulation(num_simulations, starting_bankroll)
