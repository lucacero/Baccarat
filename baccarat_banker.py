import random
import matplotlib.pyplot as plt

def simulate_baccarat_banker(starting_bankroll = float(input("What is your starting bankroll?")), display_plot = True):
    ruin_rate = float(input("What is your ruin rate? (0.01 = 1%)"))
    bankroll = starting_bankroll
    bet_size = (-2 * starting_bankroll * 0.0136) / (Math.log(ruin_rate))
    balance_history = [bankroll]
    num_hands = 0
    shoe_number = 1
    hands_per_shoe = 80
    shoe_start_balance = bankroll
    
    while bankroll > 0:
        num_hands += 1
        bet = min(bet_size, bankroll)
        outcome = random.choices(
            population=["banker", "player", "tie"],
            weights=[45.86, 44.62, 9.52],
            k=1
        )[0]
        
        if outcome == "banker":
            bankroll += bet  # No commission taken
        elif outcome == "player":
            bankroll -= bet
        # Tie results in no gain or loss
        
        balance_history.append(bankroll)
        
        if num_hands % hands_per_shoe == 0:
            shoe_profit = bankroll - shoe_start_balance
            print(f"Shoe {shoe_number}: Profit = {shoe_profit:.2f}, Balance = {bankroll:.2f}")
            shoe_number += 1
            shoe_start_balance = bankroll
        
        if bankroll > 1000000:
            break
    
    if display_plot:
        plt.figure(figsize=(10, 6))
        plt.plot(balance_history, lw=2, label="Balance")
        plt.title("Baccarat Simulation: Bankroll Over Time")
        plt.xlabel("Number of Hands")
        plt.ylabel("Bankroll ($)")
        plt.grid(True)
        plt.legend()
        plt.show()
    
    return {
        "final_bankroll": bankroll,
        "num_hands": num_hands,
    }

if __name__ == "__main__":
    simulate_baccarat_banker()
