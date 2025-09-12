from language_evolution_simulator import LanguageEvolutionSimulator
import matplotlib.pyplot as plt


def run_high_mutation_scenario():
    print("=" * 60)
    print("RAPID LANGUAGE CHANGE SCENARIO")
    print("=" * 60)
    
    simulator = LanguageEvolutionSimulator(
        population_size=40,
        mutation_rate=0.25,
        communication_frequency=0.6,
        error_rate=0.15
    )
    
    simulator.run_simulation(generations=75, verbose=True)
    simulator.visualize_language_evolution(save_path="high_mutation_results.png")
    
    return simulator


def run_stable_communication_scenario():
    print("\n" + "=" * 60)
    print("STABLE LANGUAGE SCENARIO")
    print("=" * 60)
    
    simulator = LanguageEvolutionSimulator(
        population_size=40,
        mutation_rate=0.08,
        communication_frequency=0.7,
        error_rate=0.03
    )
    
    simulator.run_simulation(generations=75, verbose=True)
    simulator.visualize_language_evolution(save_path="stable_communication_results.png")
    
    return simulator


def run_chaotic_scenario():
    print("\n" + "=" * 60)
    print("CHAOTIC LANGUAGE SCENARIO")
    print("=" * 60)
    
    simulator = LanguageEvolutionSimulator(
        population_size=40,
        mutation_rate=0.2,
        communication_frequency=0.8,
        error_rate=0.3
    )
    
    simulator.run_simulation(generations=75, verbose=True)
    simulator.visualize_language_evolution(save_path="chaotic_communication_results.png")
    
    return simulator


def run_small_population_scenario():
    print("\n" + "=" * 60)
    print("SMALL GROUP SCENARIO")
    print("=" * 60)
    
    simulator = LanguageEvolutionSimulator(
        population_size=15,
        mutation_rate=0.12,
        communication_frequency=0.9,
        error_rate=0.1
    )
    
    simulator.run_simulation(generations=50, verbose=True)
    simulator.visualize_language_evolution(save_path="small_population_results.png")
    
    return simulator


def compare_scenarios():
    print("\n" + "=" * 60)
    print("COMPARING DIFFERENT SCENARIOS")
    print("=" * 60)
    
    scenarios = {
        "High Mutation": LanguageEvolutionSimulator(40, 0.25, 0.6, 0.15),
        "Stable": LanguageEvolutionSimulator(40, 0.08, 0.7, 0.03),
        "Chaotic": LanguageEvolutionSimulator(40, 0.2, 0.8, 0.3),
        "Small Population": LanguageEvolutionSimulator(15, 0.12, 0.9, 0.1)
    }
    
    results = {}
    
    for name, simulator in scenarios.items():
        print(f"\nRunning {name} scenario...")
        simulator.run_simulation(generations=50, verbose=False)
        results[name] = simulator.generation_stats[-1]
    
    print("\n" + "=" * 80)
    print("SCENARIO COMPARISON")
    print("=" * 80)
    print(f"{'Scenario':<15} {'Words':<10} {'Rules':<8} {'Complexity':<10} {'Success':<12}")
    print("-" * 80)
    
    for name, stats in results.items():
        print(f"{name:<15} {stats['avg_vocabulary_size']:<10.1f} "
              f"{stats['avg_grammar_rules']:<8.1f} {stats['avg_language_complexity']:<10.2f} "
              f"{stats['avg_communication_success']:<12.3f}")


def analyze_agent_diversity(simulator):
    print("\n" + "=" * 60)
    print("AGENT LANGUAGE DIVERSITY")
    print("=" * 60)
    
    vocab_sizes = [agent.get_vocabulary_size() for agent in simulator.agents]
    grammar_counts = [agent.get_grammar_rules_count() for agent in simulator.agents]
    complexities = [agent.language_complexity for agent in simulator.agents]
    
    print(f"Vocabulary Size - Min: {min(vocab_sizes):.1f}, Max: {max(vocab_sizes):.1f}, "
          f"Std: {sum((x - sum(vocab_sizes)/len(vocab_sizes))**2 for x in vocab_sizes)**0.5/len(vocab_sizes):.1f}")
    
    print(f"Grammar Rules - Min: {min(grammar_counts):.1f}, Max: {max(grammar_counts):.1f}, "
          f"Std: {sum((x - sum(grammar_counts)/len(grammar_counts))**2 for x in grammar_counts)**0.5/len(grammar_counts):.1f}")
    
    print(f"Language Complexity - Min: {min(complexities):.2f}, Max: {max(complexities):.2f}, "
          f"Std: {sum((x - sum(complexities)/len(complexities))**2 for x in complexities)**0.5/len(complexities):.2f}")
    
    print("\nMost unique agents:")
    agent_vocab = [(i, agent.get_vocabulary_size()) for i, agent in enumerate(simulator.agents)]
    agent_vocab.sort(key=lambda x: x[1], reverse=True)
    
    for i, (agent_id, vocab_size) in enumerate(agent_vocab[:5]):
        sample = simulator.get_agent_language_sample(agent_id, 8)
        print(f"  Agent {agent_id}: {vocab_size} words, top words: {sample['vocabulary_sample'][:4]}")


def main():
    print("Language Evolution Simulator - Different Scenarios")
    print("=" * 60)
    
    high_mutation_sim = run_high_mutation_scenario()
    stable_sim = run_stable_communication_scenario()
    chaotic_sim = run_chaotic_scenario()
    small_pop_sim = run_small_population_scenario()
    
    compare_scenarios()
    
    analyze_agent_diversity(high_mutation_sim)
    
    print("\n" + "=" * 60)
    print("All scenarios done! Check the PNG files for results.")
    print("=" * 60)


if __name__ == "__main__":
    main()