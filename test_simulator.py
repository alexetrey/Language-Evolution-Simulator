from language_evolution_simulator import LanguageEvolutionSimulator


def test_basic_functionality():
    print("Testing the simulator...")
    
    simulator = LanguageEvolutionSimulator(
        population_size=10,
        mutation_rate=0.1,
        communication_frequency=0.5,
        error_rate=0.1
    )
    
    print("Running a quick test...")
    simulator.run_simulation(generations=10, verbose=True)
    
    stats = simulator.generation_stats[-1]
    print(f"\nResults:")
    print(f"  Words per agent: {stats['avg_vocabulary_size']:.1f}")
    print(f"  Grammar rules: {stats['avg_grammar_rules']:.1f}")
    print(f"  Language complexity: {stats['avg_language_complexity']:.2f}")
    print(f"  Communication success: {stats['avg_communication_success']:.1%}")
    
    sample = simulator.get_agent_language_sample(0, 5)
    print(f"\nAgent 0 example:")
    print(f"  Top words: {sample['vocabulary_sample']}")
    print(f"  Grammar rules: {sample['grammar_rules_sample'][:2]}")
    
    print("\nTest completed!")


if __name__ == "__main__":
    test_basic_functionality()