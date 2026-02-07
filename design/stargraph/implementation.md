# Stargraph Implementation Details:
- The Graph is defined in @state.md
    - State is stored in Neo4J.
    - Logic is implemented in Python with type-hints
    - Actions and Sensors are exposed through an MCP server
- The Graph is populated with memoized, procedurally generated objects (which are mutable after discovery), determined according to a seed with a deterministic pseudorandom RNG, the types for which are described in @ontology.md
- The MCP server has a 'start' tool, which provides instructions to the AI model to begin the interactive experience defined in @experience.md