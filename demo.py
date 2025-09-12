#!/usr/bin/env python3

from language_evolution_simulator import LanguageEvolutionSimulator
import time

def run_demo():
    print("🚀 Language Evolution Simulator - Demo")
    print("=" * 50)
    print()
    
    print("This demo will show you how languages evolve through agent communication.")
    print("Watch as agents develop unique vocabularies and grammar rules over time!")
    print()
    
    input("Press Enter to start the demo...")
    print()
    
    print("Creating 20 agents with different starting vocabularies...")
    simulator = LanguageEvolutionSimulator(
        population_size=20,
        mutation_rate=0.12,
        communication_frequency=0.7,
        error_rate=0.15
    )
    
    print("Starting 30-generation simulation...")
    print("(This will take about 10-15 seconds)")
    print()
    
    start_time = time.time()
    simulator.run_simulation(generations=30, verbose=True)
    end_time = time.time()
    
    print(f"\nSimulation completed in {end_time - start_time:.1f} seconds!")
    print()
    
    print("Generating visualization...")
    simulator.visualize_language_evolution("demo_results.png")
    print("Visualization saved as 'demo_results.png'")
    print()
    
    print("Saving simulation data...")
    simulator.save_simulation_data("demo_data.json")
    print("Data saved as 'demo_data.json'")
    print()
    
    print("🎉 Demo completed!")
    print()
    print("What you can do next:")
    print("1. Open 'demo_results.png' to see the evolution charts")
    print("2. Run 'python example_scenarios.py' to try different scenarios")
    print("3. Modify the parameters in this demo script")
    print("4. Check out the README.md for more information")
    print()
    print("Thanks for trying the Language Evolution Simulator! 🎯")

if __name__ == "__main__":
    run_demo()
