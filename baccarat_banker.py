import random
import math
import matplotlib.pyplot as plt

def simulate_baccarat_banker(starting_bankroll = float(input("What is your starting bankroll? ")), display_plot = True):
    ruin_rate = float(input("What is your ruin rate? (0.01 = 1%) "))
    
    bankroll = starting_bankroll
    theoretical_bankroll = starting_bankroll  # Independent theoretical model
    bet_size = (-2 * starting_bankroll * 0.0136) / (math.log(ruin_rate))
    theoretical_bet_size = bet_size  # Theoretical bet size follows the same formula initially
    
    balance_history = [bankroll]
    theoretical_balance_history = [theoretical_bankroll]
    
    num_hands = 0
    shoe_number = 1
    hands_per_shoe = 80
    shoe_start_balance = bankroll
    expected_win_rate = 0.0124  # Expected return per hand

    while bankroll > 0:
        num_hands += 1
        bet = min(bet_size, bankroll)
        theoretical_bet = min(theoretical_bet_size, theoretical_bankroll)

        # Simulate real outcome
        outcome = random.choices(["banker", "player", "tie"], weights=[45.86, 44.62, 9.52], k=1)[0]

        if outcome == "banker":
            bankroll += bet
        elif outcome == "player":
            bankroll -= bet

        # Theoretical bankroll grows at the expected rate
        theoretical_bankroll += theoretical_bet * expected_win_rate

        balance_history.append(bankroll)
        theoretical_balance_history.append(theoretical_bankroll)

        if num_hands % hands_per_shoe == 0:
            shoe_profit = bankroll - shoe_start_balance
            print(f"Shoe {shoe_number}: Profit = {shoe_profit:+.2f}, Balance = {bankroll:.2f}")
            shoe_number += 1
            shoe_start_balance = bankroll

            # Recalculate bet size every 20 shoes (1600 hands)
            if shoe_number % 20 == 0:  
                bet_size = (-2 * bankroll * 0.0136) / (math.log(ruin_rate))
                theoretical_bet_size = (-2 * theoretical_bankroll * 0.0136) / (math.log(ruin_rate))

                print(f"Bet size recalculated: Actual = {bet_size:.2f}, Theoretical = {theoretical_bet_size:.2f}")

        if bankroll > 1_000_000:
            break

    if display_plot:
        plt.figure(figsize=(10, 6))
        plt.plot(balance_history, lw=2, label="Actual Balance", color="blue")
        plt.plot(theoretical_balance_history, lw=2, linestyle="dashed", color="red", label="Theoretical Expected Balance")
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
