import random
import matplotlib.pyplot as plt

def simulate_baccarat():
    # Initial parameters
    balance = 10000
    hand_count = 0
    balance_history = [balance]
    
    # Bet sizing variables: start with $500 bets.
    bet_size = 500  
    
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
        # --- Adjust bet tier based on current balance ---
        # Save the current bet size so we can detect a downgrade.
        old_bet_size = bet_size
        
        # Upgrade/downgrade between $500 and $1,000.
        if bet_size == 500 and balance >= 15000:
            bet_size = 1000
        elif bet_size == 1000 and balance < 11000:
            bet_size = 500
        
        # Upgrade/downgrade between $1,000 and $2,000.
        if bet_size < 2000 and balance >= 30000:
            bet_size = 2000
        elif bet_size == 2000 and balance < 20000:
            bet_size = 1000 if balance >= 11000 else 500
        
        # New Tier: Upgrade to $3,000 if balance reaches $50,000,
        # and downgrade back to $2,000 if balance goes to $40,000 or less.
        if bet_size < 3000 and balance >= 50000:
            bet_size = 3000
        elif bet_size == 3000 and balance <= 40000:
            bet_size = 2000
        
        # If the bet size decreased from the previous hand, record stop_point (if not already set)
        if bet_size < old_bet_size and stop_point is None:
            stop_point = hand_count
            print("(you should stop play here)")
        
        # Ensure the bet does not exceed the current balance.
        current_bet = min(bet_size, balance)
        
        # --- Simulate one baccarat hand ---
        # Outcomes: "banker" win, "player" win, or "tie" (push).
        outcome = random.choices(
            population=["banker", "player", "tie"],
            weights=[45.86, 44.62, 9.52],
            k=1
        )[0]
        
        # Place the bet on the side that won the previous (non-tie) hand.
        bet_side = last_win
        
        # Determine hand result:
        # A tie is a push (no change in balance) and breaks any ongoing streak.
        if outcome == "tie":
            result = 0
        else:
            if outcome == bet_side:
                # Win: In this simulation, wins pay 1:1 for both sides.
                result = current_bet
            else:
                # Loss.
                result = -current_bet
        
        # Update balance and hand counts.
        balance += result
        hand_count += 1
        current_shoe_hand_count += 1
        balance_history.append(balance)
        
        # --- Update streak tracking for the current shoe ---
        if outcome != "tie":
            # If starting a new streak.
            if current_streak_side is None:
                current_streak_side = outcome
                current_streak_length = 1
                current_streak_profit = result
            elif current_streak_side == outcome:
                # Continue current streak.
                current_streak_length += 1
                current_streak_profit += result
            else:
                # Outcome changed, so check if the previous streak was the longest.
                if current_streak_length > current_shoe_max_streak:
                    current_shoe_max_streak = current_streak_length
                    current_shoe_max_side = current_streak_side
                    current_shoe_max_profit = current_streak_profit
                # Start a new streak.
                current_streak_side = outcome
                current_streak_length = 1
                current_streak_profit = result
        else:
            # A tie: break the current streak.
            if current_streak_side is not None:
                if current_streak_length > current_shoe_max_streak:
                    current_shoe_max_streak = current_streak_length
                    current_shoe_max_side = current_streak_side
                    current_shoe_max_profit = current_streak_profit
                current_streak_side = None
                current_streak_length = 0
                current_streak_profit = 0
        
        # Update the betting side for next hand (if not a tie).
        if outcome != "tie":
            last_win = outcome
        
        # --- Check if the current shoe (80 hands) is complete ---
        if current_shoe_hand_count == 80:
            # Before closing the shoe, check the active streak.
            if current_streak_side is not None and current_streak_length > current_shoe_max_streak:
                current_shoe_max_streak = current_streak_length
                current_shoe_max_side = current_streak_side
                current_shoe_max_profit = current_streak_profit
            
            # Calculate shoe profit.
            shoe_profit = balance - shoe_start_balance
            
            # Record the shoe's streak and profit data.
            shoe_streaks.append((current_shoe_number, current_shoe_max_streak, current_shoe_max_side, current_shoe_max_profit, shoe_profit))
            
            # Reset variables for the next shoe.
            current_shoe_number += 1
            current_shoe_hand_count = 0
            shoe_start_balance = balance
            current_streak_side = None
            current_streak_length = 0
            current_streak_profit = 0
            current_shoe_max_streak = 0
            current_shoe_max_side = None
            current_shoe_max_profit = 0

    # If the simulation ends with an incomplete shoe, record its data.
    if current_shoe_hand_count > 0:
        if current_streak_side is not None and current_streak_length > current_shoe_max_streak:
            current_shoe_max_streak = current_streak_length
            current_shoe_max_side = current_streak_side
            current_shoe_max_profit = current_streak_profit
        shoe_profit = balance - shoe_start_balance
        shoe_streaks.append((current_shoe_number, current_shoe_max_streak, current_shoe_max_side, current_shoe_max_profit, shoe_profit))
    
    # Estimate the number of shoes played (assuming 80 hands per shoe).
    shoes_used = hand_count / 80.0

    # Print the simulation results.
    print("Reached $0 after", hand_count, "hands.")
    print("That is approximately", round(shoes_used, 2), "shoes (assuming 8 decks per shoe).")
    print("\nPer-Shoe Data:")
    for shoe, streak, side, streak_profit, shoe_profit in shoe_streaks:
        if side is not None:
            print(f"  Shoe {shoe}: Longest streak = {streak} consecutive {side} outcomes, "
                  f"streak profit = {streak_profit:+.2f}, shoe profit = {shoe_profit:+.2f}")
        else:
            print(f"  Shoe {shoe}: No non-tie outcomes, shoe profit = {shoe_profit:+.2f}")
    
    # Plot a graph of your balance over the session.
    plt.figure(figsize=(10, 6))
    plt.plot(balance_history, lw=2, label="Balance")
    plt.title("Baccarat Simulation: Earnings Over Hands")
    plt.xlabel("Hands Played")
    plt.ylabel("Balance ($)")
    plt.grid(True)
    
    # If a stop point was recorded, add a vertical line to indicate it.
    if stop_point is not None:
        plt.axvline(x=stop_point, color='red', linestyle='--', lw=2, label="Stop play here")
        plt.legend()
    
    plt.show()

if __name__ == "__main__":
    simulate_baccarat()
