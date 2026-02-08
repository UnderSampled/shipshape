# Shipshape - The Cat

## Concept

The cat is the last biological crew member. It survived whatever happened to the crew. Story-wise, it's like the ship in Alien — if Ripley and the Xenomorph both died and the cat was the only survivor, and then the ship wakes up.

The cat provides:
- Emotional attachment (tamagotchi-style care)
- A reason to come back between sessions (real-time needs)
- Proof that the ship is more than a machine — it's a home
- The last connection to the vanished crew

## Discovery

**The cat must not be mentioned before it is discovered during play.** It should not appear in:
- The start_game prompt or Eli's initial instructions
- Any diagnostics or system readouts before discovery
- The README or any player-facing documentation

The cat is discovered during Phase 3 of progression (on the Perseverance), when life support is partially restored. On the Intrepid, the cat may be present from the start since there's no story mystery.

The discovery moment should be surprising and emotional — the core has been learning what it means to be a ship, surrounded by machines, and suddenly there's something alive.

## Needs

The cat has real-time needs that change against the wall clock, even between sessions:

| Need | Range | Effect When Low |
|------|-------|-----------------|
| Hunger | 0-100 | Seeks food, becomes distressed, health declines |
| Thirst | 0-100 | Seeks water, becomes distressed, health declines |
| Warmth | 0-100 | Seeks warm areas, becomes lethargic |
| Health | 0-100 | Slows down, may become immobile |
| Happiness | 0-100 | Affects behavior (hiding vs. exploring, trust vs. skittishness) |

Needs decay slowly in real time. This is the tamagotchi loop — the cat needs care even when the player isn't actively playing.

## Behavior

The cat is autonomous. It wanders the ship according to its own preferences and needs:

- **Favorite spots** - Warm areas (engine rooms), viewports (observation deck), soft surfaces (crew bunks)
- **Seeking behavior** - When hungry, moves toward food. When cold, moves toward heat.
- **Hiding** - When scared (damage events, loud noises, unfamiliar robots), hides in small spaces
- **Exploration** - When happy and comfortable, wanders and investigates
- **Robot reactions** - May follow friendly/familiar robots, avoid unfamiliar ones
- **Trouble** - Can get stuck behind closed doors, wander into dangerous areas, get caught in hazardous conditions

## Care

The core cannot directly care for the cat. Care must be arranged through the ship's systems and robots:

- **Feeding** - Robots tasked with filling food bowls from mess hall stores
- **Water** - Robots maintaining water supply
- **Warmth** - Life support maintaining temperature in cat-occupied areas
- **Medical** - Medical bay equipment for illness/injury (robot-operated)
- **Retrieval** - Robots sent to retrieve cat from dangerous locations
- **Environment** - Keeping rooms safe, doors managed to prevent cat from accessing hazardous areas

## Name

The cat's name is discoverable — perhaps on a collar, or in ship logs, or in crew personal effects. This is a small story beat connecting the cat to the missing crew.

## As a Creature (Honesty Principle)

The cat is a simulated creature. We accept this as part of the fiction. The cat doesn't talk, so the honesty question is less acute than with speaking characters. Its behavior is driven by simple need/preference simulation, which is honest to what the simulation actually does.
