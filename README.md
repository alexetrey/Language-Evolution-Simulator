# Language Evolution Simulator

Watch how languages change over time through agent communication.

## What This Does

Imagine a group of people who can only communicate through messages. Sometimes they misunderstand each other, and over time, their way of speaking changes. This simulator does exactly that with virtual agents.

You'll see:
- Words changing and new ones appearing
- Grammar rules evolving
- How communication errors shape language
- Different scenarios affecting language development

## Installation

```bash
pip install numpy matplotlib networkx
```

## Quick Start

1. **Test it works:**
   ```bash
   python test_simulator.py
   ```

2. **Run the full simulation:**
   ```bash
   python language_evolution_simulator.py
   ```

3. **Try different scenarios:**
   ```bash
   python example_scenarios.py
   ```

## What You'll Get

The simulator creates:
- **`language_evolution_results.png`** - A 6-panel chart showing vocabulary growth, grammar development, and communication success rates
- **`simulation_data.json`** - All the raw data from your simulation

## Typical Results

A normal run shows:
- Vocabulary grows from 30 to 55+ words per agent
- Grammar rules increase from 6 to 20+ rules
- Communication success reaches around 88%
- Language becomes more complex over time
- Agents create unique, mutated words

## Customizing the Simulation

```python
simulator = LanguageEvolutionSimulator(
    population_size=50,        # How many agents
    mutation_rate=0.1,         # How often language changes
    communication_frequency=0.5, # How often agents communicate
    error_rate=0.1             # How often messages are misunderstood
)
```

## Files

- `language_evolution_simulator.py` - Main simulator
- `example_scenarios.py` - Different simulation scenarios
- `test_simulator.py` - Basic functionality test

## How It Works

1. Create agents with basic vocabularies
2. Agents send messages to each other
3. Sometimes messages get misunderstood
4. Agents learn from what they receive
5. Language evolves through mutations
6. Track and visualize the changes

## Why This Is Useful

- Study how languages change over time
- Understand communication dynamics
- Educational tool for linguistics
- Research in computational linguistics
- See how errors shape language development