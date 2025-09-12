import random
import numpy as np
import matplotlib.pyplot as plt
import networkx as nx
from collections import defaultdict, Counter
from typing import Dict, List, Set, Tuple, Optional
import json
import time
from dataclasses import dataclass, asdict
from enum import Enum


class MessageType(Enum):
    GREETING = "greeting"
    QUESTION = "question"
    STATEMENT = "statement"
    REQUEST = "request"
    RESPONSE = "response"


@dataclass
class Message:
    sender_id: int
    receiver_id: int
    content: str
    message_type: MessageType
    generation: int
    original_content: str = None


@dataclass
class GrammarRule:
    pattern: str
    replacement: str
    frequency: float
    generation_created: int


@dataclass
class Vocabulary:
    words: Dict[str, float]
    meanings: Dict[str, Set[str]]
    generation_created: int


class Agent:
    
    def __init__(self, agent_id: int, initial_vocabulary: Set[str] = None):
        self.agent_id = agent_id
        self.generation = 0
        
        if initial_vocabulary is None:
            initial_vocabulary = {
                "hello", "goodbye", "yes", "no", "please", "thank", "you", "me", "I",
                "the", "a", "and", "or", "but", "is", "are", "was", "were", "have", "has"
            }
        
        self.vocabulary = Vocabulary(
            words={word: 1.0 for word in initial_vocabulary},
            meanings={word: {word} for word in initial_vocabulary},
            generation_created=0
        )
        
        self.grammar_rules = self._initialize_basic_grammar()
        
        self.message_history = []
        self.successful_communications = 0
        self.total_communications = 0
        
        self.language_complexity = self._calculate_language_complexity()
        self.unique_words_created = 0
        self.grammar_rules_created = 0
    
    def _initialize_basic_grammar(self) -> List[GrammarRule]:
        basic_rules = [
            GrammarRule("greeting", "hello", 1.0, 0),
            GrammarRule("farewell", "goodbye", 1.0, 0),
            GrammarRule("agreement", "yes", 1.0, 0),
            GrammarRule("disagreement", "no", 1.0, 0),
            GrammarRule("question_marker", "?", 0.8, 0),
            GrammarRule("statement_marker", ".", 0.9, 0),
        ]
        return basic_rules
    
    def _calculate_language_complexity(self) -> float:
        vocab_complexity = len(self.vocabulary.words) * 0.1
        grammar_complexity = len(self.grammar_rules) * 0.2
        meaning_complexity = sum(len(meanings) for meanings in self.vocabulary.meanings.values()) * 0.05
        
        return vocab_complexity + grammar_complexity + meaning_complexity
    
    def generate_message(self, message_type: MessageType, target_agent_id: int) -> Message:
        content = self._construct_message_content(message_type)
        original_content = content
        
        content = self._apply_grammar_rules(content)
        
        message = Message(
            sender_id=self.agent_id,
            receiver_id=target_agent_id,
            content=content,
            message_type=message_type,
            generation=self.generation,
            original_content=original_content
        )
        
        return message
    
    def _construct_message_content(self, message_type: MessageType) -> str:
        if message_type == MessageType.GREETING:
            return random.choice(["hello", "hi", "hey"])
        elif message_type == MessageType.QUESTION:
            return random.choice(["what", "how", "why", "when", "where"]) + " " + random.choice(list(self.vocabulary.words.keys())[:5])
        elif message_type == MessageType.STATEMENT:
            return random.choice(list(self.vocabulary.words.keys())[:3]) + " " + random.choice(list(self.vocabulary.words.keys())[3:6])
        elif message_type == MessageType.REQUEST:
            return "please " + random.choice(list(self.vocabulary.words.keys())[:4])
        else:
            return random.choice(list(self.vocabulary.words.keys())[:2])
    
    def _apply_grammar_rules(self, content: str) -> str:
        modified_content = content
        
        for rule in self.grammar_rules:
            if random.random() < rule.frequency:
                if rule.pattern in modified_content:
                    modified_content = modified_content.replace(rule.pattern, rule.replacement)
        
        return modified_content
    
    def receive_message(self, message: Message, error_rate: float = 0.1) -> bool:
        self.total_communications += 1
        
        if random.random() < error_rate:
            interpreted_content = self._mutate_message_content(message.content)
            success = False
        else:
            interpreted_content = message.content
            success = True
        
        self._learn_from_message(interpreted_content, message.message_type)
        
        self.message_history.append({
            'message': message,
            'interpreted_content': interpreted_content,
            'success': success,
            'timestamp': time.time()
        })
        
        if success:
            self.successful_communications += 1
        
        return success
    
    def _mutate_message_content(self, content: str) -> str:
        words = content.split()
        mutated_words = []
        
        for word in words:
            if random.random() < 0.3:
                mutated_word = self._mutate_word(word)
                mutated_words.append(mutated_word)
            else:
                mutated_words.append(word)
        
        return " ".join(mutated_words)
    
    def _mutate_word(self, word: str) -> str:
        if len(word) <= 1:
            return word
        
        mutation_type = random.choice(['substitute', 'insert', 'delete', 'transpose'])
        
        if mutation_type == 'substitute' and len(word) > 1:
            pos = random.randint(0, len(word) - 1)
            new_char = random.choice('abcdefghijklmnopqrstuvwxyz')
            return word[:pos] + new_char + word[pos+1:]
        
        elif mutation_type == 'insert':
            pos = random.randint(0, len(word))
            new_char = random.choice('abcdefghijklmnopqrstuvwxyz')
            return word[:pos] + new_char + word[pos:]
        
        elif mutation_type == 'delete' and len(word) > 1:
            pos = random.randint(0, len(word) - 1)
            return word[:pos] + word[pos+1:]
        
        elif mutation_type == 'transpose' and len(word) > 1:
            pos = random.randint(0, len(word) - 2)
            chars = list(word)
            chars[pos], chars[pos+1] = chars[pos+1], chars[pos]
            return ''.join(chars)
        
        return word
    
    def _learn_from_message(self, content: str, message_type: MessageType):
        words = content.split()
        
        for word in words:
            if word not in self.vocabulary.words:
                self.vocabulary.words[word] = 0.1
                self.vocabulary.meanings[word] = {word}
                self.unique_words_created += 1
            else:
                self.vocabulary.words[word] = min(1.0, self.vocabulary.words[word] + 0.05)
    
    def evolve_language(self, mutation_rate: float = 0.1):
        self._mutate_vocabulary(mutation_rate)
        self._mutate_grammar_rules(mutation_rate)
        self.language_complexity = self._calculate_language_complexity()
        self.generation += 1
    
    def _mutate_vocabulary(self, mutation_rate: float):
        words_to_remove = []
        words_to_add = {}
        meanings_to_add = {}
        
        for word, frequency in list(self.vocabulary.words.items()):
            if random.random() < mutation_rate:
                if frequency < 0.1:
                    words_to_remove.append(word)
                else:
                    mutated_word = self._mutate_word(word)
                    if mutated_word != word:
                        words_to_add[mutated_word] = frequency
                        meanings_to_add[mutated_word] = self.vocabulary.meanings[word].copy()
                        words_to_remove.append(word)
        
        for word, frequency in words_to_add.items():
            self.vocabulary.words[word] = frequency
        for word, meanings in meanings_to_add.items():
            self.vocabulary.meanings[word] = meanings
        
        for word in words_to_remove:
            if word in self.vocabulary.words:
                del self.vocabulary.words[word]
            if word in self.vocabulary.meanings:
                del self.vocabulary.meanings[word]
    
    def _mutate_grammar_rules(self, mutation_rate: float):
        rules_to_remove = []
        
        for rule in self.grammar_rules:
            if random.random() < mutation_rate:
                if rule.frequency < 0.1:
                    rules_to_remove.append(rule)
                else:
                    rule.pattern = self._mutate_word(rule.pattern)
                    rule.replacement = self._mutate_word(rule.replacement)
                    rule.frequency = max(0.1, rule.frequency + random.uniform(-0.1, 0.1))
        
        for rule in rules_to_remove:
            if rule in self.grammar_rules:
                self.grammar_rules.remove(rule)
        
        if random.random() < mutation_rate * 2:
            new_rule = self._create_random_grammar_rule()
            self.grammar_rules.append(new_rule)
            self.grammar_rules_created += 1
    
    def _create_random_grammar_rule(self) -> GrammarRule:
        patterns = ["the", "a", "and", "or", "but", "is", "are", "was", "were"]
        replacements = ["da", "an", "und", "oder", "aber", "ist", "sind", "war", "waren"]
        
        pattern = random.choice(patterns)
        replacement = random.choice(replacements)
        frequency = random.uniform(0.1, 0.8)
        
        return GrammarRule(pattern, replacement, frequency, self.generation)
    
    def get_communication_success_rate(self) -> float:
        if self.total_communications == 0:
            return 0.0
        return self.successful_communications / self.total_communications
    
    def get_vocabulary_size(self) -> int:
        return len(self.vocabulary.words)
    
    def get_grammar_rules_count(self) -> int:
        return len(self.grammar_rules)
    
    def to_dict(self) -> Dict:
        return {
            'agent_id': self.agent_id,
            'generation': self.generation,
            'vocabulary_size': self.get_vocabulary_size(),
            'grammar_rules_count': self.get_grammar_rules_count(),
            'language_complexity': self.language_complexity,
            'communication_success_rate': self.get_communication_success_rate(),
            'unique_words_created': self.unique_words_created,
            'grammar_rules_created': self.grammar_rules_created
        }


class LanguageEvolutionSimulator:
    
    def __init__(self, population_size: int = 50, mutation_rate: float = 0.1, 
                 communication_frequency: float = 0.5, error_rate: float = 0.1):
        self.population_size = population_size
        self.mutation_rate = mutation_rate
        self.communication_frequency = communication_frequency
        self.error_rate = error_rate
        
        self.current_generation = 0
        self.simulation_data = []
        self.communication_network = nx.Graph()
        
        self.agents = []
        self._initialize_agents()
        
        self.generation_stats = []
    
    def _initialize_agents(self):
        initial_vocabulary = {
            "hello", "goodbye", "yes", "no", "please", "thank", "you", "me", "I",
            "the", "a", "and", "or", "but", "is", "are", "was", "were", "have", "has",
            "water", "food", "house", "tree", "sun", "moon", "day", "night", "big", "small"
        }
        
        for i in range(self.population_size):
            agent_vocab = initial_vocabulary.copy()
            if i % 3 == 0:
                agent_vocab.add("greetings")
                agent_vocab.add("farewell")
            
            agent = Agent(i, agent_vocab)
            self.agents.append(agent)
            self.communication_network.add_node(i)
    
    def run_simulation(self, generations: int = 100, verbose: bool = True):
        if verbose:
            print(f"Running language evolution simulation...")
            print(f"Agents: {self.population_size}, Time periods: {generations}")
            print(f"Change rate: {self.mutation_rate}, Misunderstanding rate: {self.error_rate}")
            print("-" * 60)
        
        for generation in range(generations):
            self._simulate_generation()
            self._collect_generation_statistics()
            
            if verbose and (generation % 10 == 0 or generation == generations - 1):
                self._print_generation_summary(generation)
        
        if verbose:
            print("\nDone! Here's what happened:")
            self._print_final_statistics()
    
    def _simulate_generation(self):
        self._simulate_communication()
        
        for agent in self.agents:
            agent.evolve_language(self.mutation_rate)
        
        self.current_generation += 1
    
    def _simulate_communication(self):
        num_communications = int(self.population_size * self.communication_frequency)
        
        for _ in range(num_communications):
            sender = random.choice(self.agents)
            receiver = random.choice([a for a in self.agents if a.agent_id != sender.agent_id])
            
            message_type = random.choice(list(MessageType))
            
            message = sender.generate_message(message_type, receiver.agent_id)
            success = receiver.receive_message(message, self.error_rate)
            
            if success:
                self.communication_network.add_edge(sender.agent_id, receiver.agent_id)
    
    def _collect_generation_statistics(self):
        stats = {
            'generation': self.current_generation,
            'avg_vocabulary_size': np.mean([agent.get_vocabulary_size() for agent in self.agents]),
            'avg_grammar_rules': np.mean([agent.get_grammar_rules_count() for agent in self.agents]),
            'avg_language_complexity': np.mean([agent.language_complexity for agent in self.agents]),
            'avg_communication_success': np.mean([agent.get_communication_success_rate() for agent in self.agents]),
            'total_unique_words': len(set().union(*[agent.vocabulary.words.keys() for agent in self.agents])),
            'network_density': nx.density(self.communication_network)
        }
        
        self.generation_stats.append(stats)
        self.simulation_data.append([agent.to_dict() for agent in self.agents])
    
    def _print_generation_summary(self, generation: int):
        stats = self.generation_stats[-1]
        print(f"Period {generation:3d}: "
              f"Words: {stats['avg_vocabulary_size']:5.1f}, "
              f"Rules: {stats['avg_grammar_rules']:4.1f}, "
              f"Complexity: {stats['avg_language_complexity']:5.2f}, "
              f"Success: {stats['avg_communication_success']:5.3f}, "
              f"Unique: {stats['total_unique_words']:3d}")
    
    def _print_final_statistics(self):
        if not self.generation_stats:
            return
        
        initial_stats = self.generation_stats[0]
        final_stats = self.generation_stats[-1]
        
        print("\n" + "="*60)
        print("FINAL RESULTS")
        print("="*60)
        print(f"Words per agent - Started: {initial_stats['avg_vocabulary_size']:.1f}, Ended: {final_stats['avg_vocabulary_size']:.1f}")
        print(f"Vocabulary growth: {final_stats['avg_vocabulary_size'] - initial_stats['avg_vocabulary_size']:+.1f} words")
        print()
        print(f"Grammar rules - Started: {initial_stats['avg_grammar_rules']:.1f}, Ended: {final_stats['avg_grammar_rules']:.1f}")
        print(f"Grammar growth: {final_stats['avg_grammar_rules'] - initial_stats['avg_grammar_rules']:+.1f} rules")
        print()
        print(f"Language complexity - Started: {initial_stats['avg_language_complexity']:.2f}, Ended: {final_stats['avg_language_complexity']:.2f}")
        print(f"Complexity change: {final_stats['avg_language_complexity'] - initial_stats['avg_language_complexity']:+.2f}")
        print()
        print(f"Communication success: {final_stats['avg_communication_success']:.1%}")
        print(f"Total unique words: {final_stats['total_unique_words']}")
        print(f"Network connections: {final_stats['network_density']:.1%}")
    
    def visualize_language_evolution(self, save_path: str = None):
        if not self.generation_stats:
            print("No data to visualize yet. Run a simulation first.")
            return
        
        generations = [stats['generation'] for stats in self.generation_stats]
        vocab_sizes = [stats['avg_vocabulary_size'] for stats in self.generation_stats]
        grammar_rules = [stats['avg_grammar_rules'] for stats in self.generation_stats]
        complexity = [stats['avg_language_complexity'] for stats in self.generation_stats]
        success_rates = [stats['avg_communication_success'] for stats in self.generation_stats]
        unique_words = [stats['total_unique_words'] for stats in self.generation_stats]
        
        fig, axes = plt.subplots(2, 3, figsize=(18, 12))
        fig.suptitle('Language Evolution Simulation Results', fontsize=16, fontweight='bold')
        
        axes[0, 0].plot(generations, vocab_sizes, 'b-', linewidth=2, marker='o', markersize=4)
        axes[0, 0].set_title('Average Vocabulary Size Over Generations')
        axes[0, 0].set_xlabel('Generation')
        axes[0, 0].set_ylabel('Vocabulary Size')
        axes[0, 0].grid(True, alpha=0.3)
        
        axes[0, 1].plot(generations, grammar_rules, 'g-', linewidth=2, marker='s', markersize=4)
        axes[0, 1].set_title('Average Grammar Rules Over Generations')
        axes[0, 1].set_xlabel('Generation')
        axes[0, 1].set_ylabel('Grammar Rules Count')
        axes[0, 1].grid(True, alpha=0.3)
        
        axes[0, 2].plot(generations, complexity, 'r-', linewidth=2, marker='^', markersize=4)
        axes[0, 2].set_title('Language Complexity Over Generations')
        axes[0, 2].set_xlabel('Generation')
        axes[0, 2].set_ylabel('Complexity Score')
        axes[0, 2].grid(True, alpha=0.3)
        
        axes[1, 0].plot(generations, success_rates, 'm-', linewidth=2, marker='d', markersize=4)
        axes[1, 0].set_title('Communication Success Rate Over Generations')
        axes[1, 0].set_xlabel('Generation')
        axes[1, 0].set_ylabel('Success Rate')
        axes[1, 0].grid(True, alpha=0.3)
        
        axes[1, 1].plot(generations, unique_words, 'c-', linewidth=2, marker='v', markersize=4)
        axes[1, 1].set_title('Total Unique Words in Population')
        axes[1, 1].set_xlabel('Generation')
        axes[1, 1].set_ylabel('Unique Words Count')
        axes[1, 1].grid(True, alpha=0.3)
        
        if self.communication_network.number_of_nodes() > 0:
            pos = nx.spring_layout(self.communication_network, k=1, iterations=50)
            nx.draw(self.communication_network, pos, ax=axes[1, 2], 
                   node_color='lightblue', node_size=100, 
                   edge_color='gray', alpha=0.7, with_labels=True)
            axes[1, 2].set_title('Communication Network (Final Generation)')
        else:
            axes[1, 2].text(0.5, 0.5, 'No communication network data', 
                           ha='center', va='center', transform=axes[1, 2].transAxes)
            axes[1, 2].set_title('Communication Network')
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            print(f"Visualization saved to: {save_path}")
        else:
            plt.savefig("language_evolution_results.png", dpi=300, bbox_inches='tight')
            print("Visualization saved to: language_evolution_results.png")
        
        plt.close()
    
    def get_agent_language_sample(self, agent_id: int, num_words: int = 10) -> Dict:
        if agent_id >= len(self.agents):
            return {}
        
        agent = self.agents[agent_id]
        
        sorted_words = sorted(agent.vocabulary.words.items(), key=lambda x: x[1], reverse=True)
        top_words = [word for word, freq in sorted_words[:num_words]]
        
        sample_rules = agent.grammar_rules[:5]
        
        return {
            'agent_id': agent_id,
            'generation': agent.generation,
            'vocabulary_sample': top_words,
            'grammar_rules_sample': [(rule.pattern, rule.replacement, rule.frequency) for rule in sample_rules],
            'total_vocabulary_size': len(agent.vocabulary.words),
            'total_grammar_rules': len(agent.grammar_rules),
            'language_complexity': agent.language_complexity
        }
    
    def save_simulation_data(self, filename: str):
        data = {
            'simulation_parameters': {
                'population_size': self.population_size,
                'mutation_rate': self.mutation_rate,
                'communication_frequency': self.communication_frequency,
                'error_rate': self.error_rate,
                'generations': len(self.generation_stats)
            },
            'generation_statistics': self.generation_stats,
            'final_agent_data': [agent.to_dict() for agent in self.agents]
        }
        
        with open(filename, 'w') as f:
            json.dump(data, f, indent=2)
        
        print(f"Data saved to: {filename}")
    
    def load_simulation_data(self, filename: str):
        with open(filename, 'r') as f:
            data = json.load(f)
        
        print(f"Data loaded from: {filename}")
        print(f"Settings: {data['simulation_parameters']}")
        return data


def main():
    print("Language Evolution Simulator")
    print("=" * 40)
    
    simulator = LanguageEvolutionSimulator(
        population_size=30,
        mutation_rate=0.15,
        communication_frequency=0.6,
        error_rate=0.12
    )
    
    simulator.run_simulation(generations=50, verbose=True)
    
    simulator.visualize_language_evolution(save_path="language_evolution_results.png")
    
    simulator.save_simulation_data("simulation_data.json")
    
    print("\n" + "="*60)
    print("SAMPLE AGENT LANGUAGES")
    print("="*60)
    
    for agent_id in [0, 5, 10, 15, 20]:
        sample = simulator.get_agent_language_sample(agent_id)
        if sample:
            print(f"\nAgent {agent_id}:")
            print(f"  Generation: {sample['generation']}")
            print(f"  Vocabulary Size: {sample['total_vocabulary_size']}")
            print(f"  Grammar Rules: {sample['total_grammar_rules']}")
            print(f"  Language Complexity: {sample['language_complexity']:.2f}")
            print(f"  Top Words: {sample['vocabulary_sample'][:5]}")
            print(f"  Sample Grammar: {sample['grammar_rules_sample'][:3]}")


if __name__ == "__main__":
    main()