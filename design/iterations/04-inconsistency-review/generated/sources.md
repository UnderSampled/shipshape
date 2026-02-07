# Sources — How These Documents Were Assembled

Each design element traces back to the creator's own words across the notes files. This document maps design elements to their source statements.

Notation: `01/experience` = `iterations/01-stargraph/experience.md`, `02/notes` = `iterations/02-derelict/notes.md`, `03/concept` = `iterations/03-shipshape/notes_concept.md`, `03/arch` = `iterations/03-shipshape/notes_architecture.md`, `04/notes` = `iterations/04-inconsistency-review/notes.md`.

## experience.md

| Element | Source |
|---------|--------|
| ELC is the user/player, sentient part of ship | 01/experience, 03/concept |
| Core identifies as the ship | 02/notes "Naming the Interface" |
| Fresh boot, no memories | 02/notes "Naming the Interface" |
| Eli can play back memories | 02/notes "Naming the Interface" |
| Eli = Emotional Logic Interface | 02/notes "Naming the Interface", 03/concept |
| Eli has full LLM power | 02/notes "Eli's Characterization" |
| Eli is not autonomous | 04/notes "On Eli's Autonomy" |
| Eli same tool-use as host | 04/notes "On Eli's Autonomy" |
| Eli translates to embodied descriptions | 03/concept, 01/experience |
| Eli addresses core in second person | 01/experience |
| Ship provides computerized feel, not Eli | 02/notes "Eli's Characterization" |
| MCP = "Master Control Program" in-story | 03/concept |
| MCP is dumb computer, shows facts | 04/notes "On MCP Tool Style" |
| MCP tools expose modules/sensors/actuators | 04/notes "On MCP Tool Style" |
| Actions through actuators, can go offline | 04/notes "On MCP Tool Style" |
| Ship/MCP is autonomous | 04/notes "On System Autonomy" |
| Honesty is about sentience | 04/notes "On the Honesty Principle" |
| LLM dialogue attributed to robot's tech | 04/notes "On the Honesty Principle" |
| No scripted dialogue except dumb in-universe | 04/notes "On the Honesty Principle" |
| Creatures accepted as fiction | 04/notes "On the Honesty Principle" |
| Must consult sensors, not invent readings | 01/experience |
| No sentient beings | 03/concept |
| Real-time against real clock | 04/notes "On Sleep Mode vs. Time Deltas" |
| Stasis tool to skip time | 04/notes "On Sleep Mode vs. Time Deltas" |

## game.md

| Element | Source |
|---------|--------|
| Dwarf Fortress inspiration | 03/concept |
| FTL inspiration | 03/concept |
| MUD inspiration | 03/concept |
| Tamagotchi inspiration | 04/notes "On the Cat" |
| D&D inspiration | 04/notes "On Procedural Generation" |
| Elite/Frontier inspiration | 04/notes "On Procedural Generation" |
| Alien inspiration | 04/notes "On the Cat" |
| Rogue inspiration | 03/arch |
| Metroidvania inspiration | 02/notes "Game Structure" |
| Graph state with prepositional relationships | 03/concept, 01/state |
| Graph examples | 01/state |
| Ontology (environments through items) | 01/ontology |
| Modules/hardpoints confirmed | 04/notes "On Modules/Hardpoints" |
| Items confirmed | 04/notes "On Modules/Hardpoints" |
| Events/effects system | 01/state |
| Sensors as limited perception | 01/state |
| Robot intelligence tiers | 04/notes "On Robots vs. Drones", 02/notes "Repair Drones" |
| DF robots are the crew | 04/notes "On Robots vs. Drones" |
| LLM-powered robot tier | 04/notes "On Robots vs. Drones" |
| Full robot needs system | 03/concept |
| Communications module for robots | 04/notes "On MCP Tool Style" |
| Cat not discovered up front | 04/notes "On the Cat" |
| Cat as tamagotchi | 04/notes "On the Cat" |
| Systems offline at start, tutorial progression | 03/concept |
| Metroidvania progression | 02/notes "Game Structure" |
| Dormant human systems | 03/concept |
| D&D DM world approach | 04/notes "On Procedural Generation" |
| Procedural outer space, scripted ship | 04/notes "On Procedural Generation" |
| Fixed seed for procgen | 04/notes "On Procedural Generation" |
| Keep it roguelike | 04/notes "On Procedural Generation" |
| Three ship modes (Intrepid/Perseverance/Phoenix) | 04/notes "On Ship Names" |
| Start with first two | 04/notes "On Ship Names" |
| Docking as denouement | 04/notes "On the Ending" |

## story.md

| Element | Source |
|---------|--------|
| Thematic core quote | 02/notes "The Game's Thematic Core" |
| Design problem (no fake crew) | 02/notes "The Core Design Problem" |
| Three stories matching ship modes | 04/notes "On Ship Names" |
| Perseverance: reach repair facility | 03/concept |
| Phoenix: 3-act structure | 02/notes "Game Structure" |
| Midpoint twist (core went haywire) | 02/notes "The Central Twist" |
| Bio part dying (nutrients/oxygen) | 02/notes "Why the Original Core Failed" |
| Crew member upload/sacrifice | 02/notes "The Central Twist" |
| First boot after sacrifice | 02/notes "Timeline Clarification" |
| Eli distrusts after reveal | 02/notes "Eli's Distrust Mechanic" |
| Everyone already dead | 02/notes "The Deeper Reveal" |
| Ship's true mission (destroy colony) | 02/notes "The Ship's True Mission" |
| Crew stalled, disagreed | 02/notes "The Ship's True Mission" |
| Phoenix naming reveal | 02/notes "The Phoenix Name" |
| Cognitive failures as comm errors | 02/notes "Cognitive Failure Representation" |
| Comm degradation deferred | 04/notes "On Communication Degradation" |
| Some crew discovery in all modes | 04/notes "On Communication Degradation" |
| Single ending | 02/notes "Single Ending" |
| Docking as denouement | 04/notes "On the Ending" |
| Repair drones with AI tiers | 02/notes "Repair Drones" |
| Ship body systems (actuators/sensors) | 02/notes "Ship Body Systems" |

## software.md

| Element | Source |
|---------|--------|
| Python with type hints | 03/concept |
| NetworkX, not Neo4J | 04/notes "On Tech Stack" |
| FastMCP | 03/arch |
| Pydantic | 03/arch |
| Fly.io via Sprites | 04/notes "On Tech Stack" |
| Turn-based, per-request | 03/arch, 04/notes "On Tech Stack" |
| No background threads | 04/notes "On Tech Stack" |
| Real-time against real clock | 04/notes "On Sleep Mode vs. Time Deltas" |
| Time-delta processing | 03/arch |
| Must handle large time gaps | 03/arch |
| Memory as source of truth | 03/arch |
| Disk saves as backups | 03/arch |
| Server stays alive during session | 03/arch |
| Must not prevent idle/suspend | 03/arch |
| Multiplayer future concern | 03/arch |
| Cat not in start instructions | 04/notes "On the Cat", "On the Cat in start_game" |
| Stasis tool | 04/notes "On Sleep Mode vs. Time Deltas" |
