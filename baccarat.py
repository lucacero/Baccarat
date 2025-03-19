import random
import matplotlib.pyplot as plt

def simulate_baccarat(starting_bankroll, display_plot = True):
    if starting_bankroll < 1000:
        raise ValueError("Starting bankroll must be at least $1,000.")
    
    initial_bankroll = starting_bankroll
    balance = starting_bankroll
    hand_count = 0
    balance_history = [balance]
    
    # Bet sizing: start with 5% of the starting bankroll.
    bet_size = 0.05 * initial_bankroll
    
    # For the first hand, default to betting on banker.
    last_win = "banker"
    
    # Variables for tracking shoe statistics (assume 80 hands per shoe)
    current_shoe_number = 1
    current_shoe_hand_count = 0  # count hands within current shoe
    shoe_start_balance = balance  # record starting balance for current shoe
    
    # Variables for tracking streaks in the current shoe.
    current_streak_side = None  # current streak outcome ("banker" or "player")
    current_streak_length = 0   # current consecutive non-tie outcomes count
    current_streak_profit = 0.0  # net profit of the current streak
    current_shoe_max_streak = 0   # longest streak observed in current shoe
    current_shoe_max_side = None  # which side produced that longest streak
    current_shoe_max_profit = 0.0 # net profit for the longest streak in this shoe
    
    # List to record per shoe data:
    # Each entry: (shoe number, max streak, streak side, streak profit, shoe profit)
    shoe_streaks = []
    
    # Variable to record the hand at which the bet size first decreases.
    stop_point = None
    
    # Run simulation until the balance reaches $0.
    while balance > 0:
        # --- Adjust bet tier based on current balance relative to starting bankroll ---
        if balance > 1000000:
            break # Stop if balance exceeds $1,000,000 due to runtime issues.

        old_bet_size = bet_size
        if balance >= initial_bankroll * 3.0:
            bet_size = 0.20 * initial_bankroll
        elif balance >= initial_bankroll * 2.0:
            bet_size = 0.15 * initial_bankroll
        elif balance >= initial_bankroll * 1.5:
            bet_size = 0.10 * initial_bankroll
        elif balance <= initial_bankroll * 0.5:
            bet_size = 0.025 * initial_bankroll
        else:
            bet_size = 0.05 * initial_bankroll
        
        if bet_size < old_bet_size and stop_point is None:
            stop_point = hand_count
            if display_plot:
                print("(you should stop play here)")
        
        # Ensure the bet does not exceed the current balance.
        current_bet = min(bet_size, balance)
        
        # --- Simulate one baccarat hand ---
        outcome = random.choices(
            population=["banker", "player", "tie"],
            weights=[45.86, 44.62, 9.52],
            k=1
        )[0]
        
        # Place the bet on the side that won the previous (non-tie) hand.
        bet_side = last_win
        
        if outcome == "tie":
            result = 0
        else:
            if outcome == bet_side:
                result = current_bet
            else:
                result = -current_bet
        
        balance += result
        hand_count += 1
        current_shoe_hand_count += 1
        balance_history.append(balance)
        
        # --- Update streak tracking for the current shoe ---
        if outcome != "tie":
            if current_streak_side is None:
                current_streak_side = outcome
                current_streak_length = 1
                current_streak_profit = result
            elif current_streak_side == outcome:
                current_streak_length += 1
                current_streak_profit += result
            else:
                if current_streak_length > current_shoe_max_streak:
                    current_shoe_max_streak = current_streak_length
                    current_shoe_max_side = current_streak_side
                    current_shoe_max_profit = current_streak_profit
                current_streak_side = outcome
                current_streak_length = 1
                current_streak_profit = result
        else:
            if current_streak_side is not None:
                if current_streak_length > current_shoe_max_streak:
                    current_shoe_max_streak = current_streak_length
                    current_shoe_max_side = current_streak_side
                    current_shoe_max_profit = current_streak_profit
                current_streak_side = None
                current_streak_length = 0
                current_streak_profit = 0
        
        if outcome != "tie":
            last_win = outcome
        
        # --- Check if the current shoe (80 hands) is complete ---
        if current_shoe_hand_count == 80:
            if current_streak_side is not None and current_streak_length > current_shoe_max_streak:
                current_shoe_max_streak = current_streak_length
                current_shoe_max_side = current_streak_side
                current_shoe_max_profit = current_streak_profit
            
            shoe_profit = balance - shoe_start_balance
            shoe_streaks.append((current_shoe_number, current_shoe_max_streak, current_shoe_max_side, current_shoe_max_profit, shoe_profit))
            
            current_shoe_number += 1
            current_shoe_hand_count = 0
            shoe_start_balance = balance
            current_streak_side = None
            current_streak_length = 0
            current_streak_profit = 0
            current_shoe_max_streak = 0
            current_shoe_max_side = None
            current_shoe_max_profit = 0
    
    # Record data for an incomplete shoe if needed.
    if current_shoe_hand_count > 0:
        if current_streak_side is not None and current_streak_length > current_shoe_max_streak:
            current_shoe_max_streak = current_streak_length
            current_shoe_max_side = current_streak_side
            current_shoe_max_profit = current_streak_profit
        shoe_profit = balance - shoe_start_balance
        shoe_streaks.append((current_shoe_number, current_shoe_max_streak, current_streak_side, current_streak_profit, shoe_profit))
    
    shoes_used = hand_count / 80.0
    max_balance = max(balance_history)
    
    # If running interactively, show the simulation details and graph.
    if display_plot:
        print("Reached $0 after", hand_count, "hands.")
        print("That is approximately", round(shoes_used, 2), "shoes (assuming 8 decks per shoe).")
        print("\nPer-Shoe Data:")
        for shoe, streak, side, streak_profit, shoe_profit in shoe_streaks:
            if side is not None:
                print(f"  Shoe {shoe}: Longest streak = {streak} consecutive {side} outcomes, "
                      f"streak profit = {streak_profit:+.2f}, shoe profit = {shoe_profit:+.2f}")
            else:
                print(f"  Shoe {shoe}: No non-tie outcomes, shoe profit = {shoe_profit:+.2f}")
        
        plt.figure(figsize=(10, 6))
        plt.plot(balance_history, lw=2, label="Balance")
        plt.title("Baccarat Simulation: Earnings Over Hands")
        plt.xlabel("Hands Played")
        plt.ylabel("Balance ($)")
        plt.grid(True)
        if stop_point is not None:
            plt.axvline(x=stop_point, color='red', linestyle='--', lw=2, label="Stop play here")
            plt.legend()
        plt.show()
    
    # Return key simulation results (including max balance reached).
    return {"final_balance": balance, "max_balance": max_balance, "hand_count": hand_count, "shoe_streaks": shoe_streaks}

if __name__ == "__main__":
    try:
        starting_bankroll = float(input("Enter your starting bankroll (minimum $1,000): "))
    except ValueError:
        print("Invalid input. Please enter a valid number.")
        exit(1)
    simulate_baccarat(starting_bankroll, display_plot = True)  # Corrected line
