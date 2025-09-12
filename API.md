# API Documentation

This document provides detailed information about the Language Evolution Simulator API.

## Core Classes

### Agent

Represents an individual language user in the simulation.

#### Constructor
```python
Agent(agent_id: int, initial_vocabulary: Set[str] = None)
```

**Parameters:**
- `agent_id` (int): Unique identifier for the agent
- `initial_vocabulary` (Set[str], optional): Starting vocabulary for the agent

#### Methods

##### `generate_message(message_type: MessageType, target_agent_id: int) -> Message`
Generates a message to send to another agent.

**Parameters:**
- `message_type` (MessageType): Type of message to generate
- `target_agent_id` (int): ID of the target agent

**Returns:**
- `Message`: Generated message object

##### `receive_message(message: Message, error_rate: float = 0.1) -> bool`
Receives and interprets a message from another agent.

**Parameters:**
- `message` (Message): Message to receive
- `error_rate` (float): Probability of misinterpretation (0.0-1.0)

**Returns:**
- `bool`: True if message was successfully interpreted

##### `evolve_language(mutation_rate: float = 0.1)`
Evolves the agent's language through mutations.

**Parameters:**
- `mutation_rate` (float): Rate of language mutations (0.0-1.0)

##### `get_communication_success_rate() -> float`
Gets the agent's communication success rate.

**Returns:**
- `float`: Success rate as a decimal (0.0-1.0)

##### `get_vocabulary_size() -> int`
Gets the size of the agent's vocabulary.

**Returns:**
- `int`: Number of words in vocabulary

##### `get_grammar_rules_count() -> int`
Gets the number of grammar rules the agent has.

**Returns:**
- `int`: Number of grammar rules

### LanguageEvolutionSimulator

Main simulator class that manages the language evolution process.

#### Constructor
```python
LanguageEvolutionSimulator(
    population_size: int = 50,
    mutation_rate: float = 0.1,
    communication_frequency: float = 0.5,
    error_rate: float = 0.1
)
```

**Parameters:**
- `population_size` (int): Number of agents in the simulation
- `mutation_rate` (float): Rate of language mutations per generation
- `communication_frequency` (float): Fraction of population that communicates each generation
- `error_rate` (float): Probability of message misinterpretation

#### Methods

##### `run_simulation(generations: int = 100, verbose: bool = True)`
Runs the language evolution simulation for specified generations.

**Parameters:**
- `generations` (int): Number of generations to simulate
- `verbose` (bool): Whether to print progress information

##### `visualize_language_evolution(save_path: str = None)`
Creates visualizations of language evolution over generations.

**Parameters:**
- `save_path` (str, optional): Path to save the visualization image

##### `get_agent_language_sample(agent_id: int, num_words: int = 10) -> Dict`
Gets a sample of an agent's language.

**Parameters:**
- `agent_id` (int): ID of the agent to sample
- `num_words` (int): Number of top words to return

**Returns:**
- `Dict`: Dictionary containing agent language information

##### `save_simulation_data(filename: str)`
Saves simulation data to a JSON file.

**Parameters:**
- `filename` (str): Path to save the data file

##### `load_simulation_data(filename: str)`
Loads simulation data from a JSON file.

**Parameters:**
- `filename` (str): Path to load the data file

**Returns:**
- `Dict`: Loaded simulation data

## Data Structures

### Message

Represents a message between agents.

```python
@dataclass
class Message:
    sender_id: int
    receiver_id: int
    content: str
    message_type: MessageType
    generation: int
    original_content: str = None
```

### GrammarRule

Represents a grammar rule in an agent's language.

```python
@dataclass
class GrammarRule:
    pattern: str
    replacement: str
    frequency: float
    generation_created: int
```

### Vocabulary

Represents an agent's vocabulary.

```python
@dataclass
class Vocabulary:
    words: Dict[str, float]  # word -> frequency
    meanings: Dict[str, Set[str]]  # word -> set of possible meanings
    generation_created: int
```

## Enums

### MessageType

Types of messages that can be communicated between agents.

```python
class MessageType(Enum):
    GREETING = "greeting"
    QUESTION = "question"
    STATEMENT = "statement"
    REQUEST = "request"
    RESPONSE = "response"
```

## Usage Examples

### Basic Usage

```python
from language_evolution_simulator import LanguageEvolutionSimulator

# Create simulator
simulator = LanguageEvolutionSimulator(
    population_size=30,
    mutation_rate=0.15,
    communication_frequency=0.6,
    error_rate=0.12
)

# Run simulation
simulator.run_simulation(generations=50, verbose=True)

# Generate visualization
simulator.visualize_language_evolution("results.png")

# Save data
simulator.save_simulation_data("simulation_data.json")
```

### Custom Agent Analysis

```python
# Get sample from specific agent
sample = simulator.get_agent_language_sample(agent_id=5, num_words=15)
print(f"Agent 5's top words: {sample['vocabulary_sample']}")
print(f"Grammar rules: {sample['grammar_rules_sample']}")
```

### Loading Previous Simulation

```python
# Load previous simulation data
data = simulator.load_simulation_data("previous_simulation.json")
print(f"Parameters: {data['simulation_parameters']}")
```

## Error Handling

The simulator includes comprehensive error handling:

- Invalid agent IDs return empty dictionaries
- Missing simulation data shows appropriate messages
- File I/O errors are handled gracefully
- Invalid parameters are validated

## Performance Considerations

- Large populations (>100 agents) may require more memory
- Many generations (>200) may take longer to complete
- Visualization generation can be memory-intensive
- Consider using `verbose=False` for batch processing
