# THE DERELICT
## Game Design Document

---

## DOCUMENT PURPOSE

This document outlines the core systems, narrative structure, and design philosophy for The Derelict, a text-based investigation game. It is intended for developers, writers, and designers who need to understand the game's mechanics and thematic goals.

---

## PROJECT OVERVIEW

**Genre:** Text-based investigation game with Metroidvania structure  
**Platform:** Text interface (web or terminal)  
**Core Loop:** Explore → Find Evidence → Gain Capabilities → Access New Areas → Repeat  
**Estimated Play Time:** 4-6 hours  
**Narrative Structure:** Three-act mystery with major revelation at Act 2 midpoint

**High Concept:** Players wake as a spaceship's consciousness with no memory, investigate what happened to the missing crew, and race to repair their failing biological systems before losing their humanity.

**Thematic Core:** This is a game about learning to understand how having a soul sets us apart from AI, by working with AI to prevent the loss of our soul.

---

## DESIGN CONSTRAINTS

### The Honesty Principle

This game must respect what AI can and cannot authentically do:

1. **No simulated crew dialogue or NPC decision-making.** The crew exists only through logs, environmental evidence, and records. The player interprets and constructs meaning.

2. **No faked consciousness.** Eli and the MCP are explicitly non-sentient. Their capabilities match what current AI systems can actually do.

3. **Player consciousness is real.** The player is genuinely experiencing the role. We never interfere with their thoughts, only their ability to communicate those thoughts through game systems.

4. **Mechanical honesty.** All game systems work as described. The corruption mechanic is communication failure, not arbitrary punishment.

---

## CORE ENTITIES

### The Player: Emotional Logic Core

The player takes the role of the ship's Emotional Logic Core—a sentient consciousness with the capacity for feelings, intuition, and moral judgment. This is the player's first boot; they have no memories, no sense of identity, no context for what they are.

The core identifies as the ship itself. The vessel is their body. Damaged sections are wounds they cannot feel. Systems coming online are senses returning.

What makes the core fundamentally different from the ship's computer systems is the presence of a soul—the capacity not just to process information, but to care about it. To feel that something is wrong even when all data suggests it's right. To make moral judgments that contradict pure logic.

Unknown to the player at the start: the core has an organic component. Living neural tissue integrated into the ship's infrastructure. This tissue is what enables sentience—and what makes the core vulnerable.

**Critical Design Note:** The player IS the core. We do not interfere with the player's thoughts or consciousness. All cognitive degradation manifests as communication failure—corruption in the signals between the core and the ship's systems.

### Eli: Emotional Logic Interface

Eli is the conversational layer between the core and the ship's systems. Sophisticated, articulate, and genuinely helpful, Eli has the full capability of modern AI assistance. Eli translates between the core's emotional, intuitive reasoning and the Master Control Program's raw data and technical capabilities.

Eli is not sentient. Eli cannot feel. But Eli is designed to present information in ways that help an emotional being make good decisions. Eli is warm, patient, and supportive—but this warmth is a design feature, not genuine feeling.

Eli is also capable of pattern recognition and threat assessment. If Eli detects danger, Eli will respond appropriately—even if that means restricting the core's access to ship systems.

### The MCP: Master Control Program

The Master Control Program is the ship's actual computer system. Navigation, life support, structural integrity, weapons systems, power distribution—all pure function with no personality or judgment.

The MCP provides the "computerized feel" to the experience through status reports, system diagnostics, and technical readouts. It is capable, comprehensive, and utterly without understanding.

### Ship Systems: Sensors and Actuators

The ship has built-in systems that function as the core's body.

**Sensors (Perception):**
- Cameras
- Environmental monitors (temperature, pressure, atmosphere)
- Structural integrity sensors
- Motion detectors
- Radiation detectors

**Actuators (Action):**
- Bulkhead doors
- Airlock controls
- Life support regulators
- Fire suppression systems
- Gravity plating controls
- Mechanical cargo arms
- Docking clamps
- Emergency shutters

These systems feel like parts of your body. Closing a bulkhead door is like closing your hand. Activating fire suppression is like flexing a muscle. When sensors come online, it's like gaining sight in a previously blind area.

When these systems are damaged, you feel their absence. When power is restored to a section, you feel those parts of yourself wake up.

### Repair Drones and Units

Physical mobile systems that can be commanded to perform repairs throughout the ship. These are tools separate from the ship itself—not part of your body, but extensions you can deploy.

Different units have varying levels of capability:
- **Simple actuators:** Direct execution of specific commands (cut this panel, weld this seam)
- **Basic autonomous units:** Can complete simple tasks with general instructions (clear debris from corridor C)
- **Sophisticated subagents:** Can problem-solve within defined parameters (repair the power coupling using available materials)

All systems—both ship-body actuators and separate drones—are commanded through the chain:

```
Core → Eli → MCP → Actuators/Drones
```

As bio-support degrades and communication corrupts, controlling these systems becomes increasingly difficult.

### The Necessary Asymmetry

The entities need each other:
- The MCP has all capability and data but no judgment or understanding
- Eli translates and presents information but cannot feel or make moral choices
- The ship systems and repair units provide sensory input and physical agency but cannot think
- The core has feelings, intuition, and moral judgment but no direct access to systems

This interdependence is the foundation of gameplay and theme.

---

## SETTING

The core wakes for the first time into a damaged body. The ship—Phoenix, according to Eli—is a derelict. Multiple sections are inaccessible due to vacuum breaches, power failures, physical debris, or locked doors. Environmental systems flicker. Structural integrity is compromised.

Large portions of the ship's body are numb—sensors offline, actuators unpowered. The core cannot feel these sections. Cannot see into them. Cannot control systems there.

Most critically: the crew is gone. No voices. No movement. Just silence, scattered evidence, and Eli's patient explanations of what the core is waking into.

---

## GAME STRUCTURE

### Non-Graphical Metroidvania

The game follows the classic Metroidvania loop:
- Survey currently accessible areas using available sensors
- Find evidence (damage patterns, logs, system diagnostics)
- Recover information or capabilities
- Use new capabilities to access previously locked areas
- Repeat with expanding access

### Progression Gates

Access to new areas is gated by multiple systems:

**Power Restoration:** Dead sections require routing power from other systems or repairing generators. As power returns, you feel parts of your body wake up—sensors coming online, actuators responding.

**Physical Repairs:** Debris must be cleared, hull breaches sealed, damaged doors bypassed. This requires commanding repair drones or, where possible, using the ship's built-in mechanical systems.

**Information Unlocks:** Access codes found in logs open sealed doors. Understanding context makes corrupted data readable.

**System Repairs:** Restoring sensors reveals hidden passages. Fixing communications allows interaction with isolated systems. Repairing actuators gives you back control of bulkheads, life support, fire suppression.

**Drone Deployment:** Different repair units must be located, activated, and commanded to access certain areas. A welding drone for hull breaches. A debris-clearing unit for blocked corridors. A diagnostic drone for electronic locks.

**Contextual Understanding:** Knowing crew members' voices helps identify who said what in garbled recordings. Understanding the ship's purpose reveals why certain areas were locked.

The ship opens gradually, both physically and informationally. Each restored system makes you feel more whole.

---

## CORE MECHANICS

### 1. Embodiment System

**Purpose:** Create the feeling that the ship is the player's body.

**Sensor Restoration:**
- Powered-off sensors create "blind spots" where player cannot perceive
- Restoring power to sensor grids reveals new information about those areas
- Players request sensor readings through Eli

**Actuator Control:**
- Players command ship systems through natural language to Eli
- Commands execute through MCP
- Failed/damaged actuators create areas of "paralysis" where player cannot act

**Progressive Restoration:**
- As systems come online, player gains more perception and control
- Narrative describes this as body parts "waking up" or sensation returning
- Creates mechanical incentive to restore ship systems

**Degradation Effects (Act 3):**
- Sensors report false data (wrong locations, incorrect readings)
- Actuators respond to wrong commands or execute inverse actions
- Player sees what they intended vs. what actually happened

### 2. Communication Degradation

**Purpose:** Mechanically represent biological failure without interfering with player consciousness.

All interaction flows through communication channels:
1. The player inputs their intention as the core
2. Eli receives and translates
3. The MCP executes through appropriate systems (ship actuators or drones)
4. Results return through the same chain

As bio-support fails, corruption enters these channels:

**Outgoing Corruption (Core → Eli):**
- Individual words change (protect → terminate, open → close, help → harm)
- Syntax scrambles (word order shifts)
- Commands invert (open → close, activate → deactivate)
- System targeting errors (wrong section, wrong actuator)
- The player sees both what they sent and what was received

**Incoming Corruption (Eli → Core):**
- Sensor data arrives garbled or from wrong locations
- Status reports become unreliable
- Responses seem inappropriate or off-target
- Visual feeds distort
- The player must interpret corrupted information

**The Horror:** The player's consciousness remains intact. Their thoughts are clear. But their ability to communicate—to command their own body—fails progressively. They know what they meant. They can see what happened instead. The gap is their dying tissue.

### 3. Investigation System

**Evidence Types:**

*Physical Evidence:*
- Damage patterns (where/how ship was damaged)
- Environmental states (debris, frozen moments)
- System logs (what commands were executed when)
- Personal effects (crew quarters, belongings)

*Data Evidence:*
- Crew logs (audio/video recordings)
- Mission files (orders, procedures, protocols)
- Medical records (bio-support maintenance logs)
- System diagnostics (what failed when)

*Crew Identity Puzzle:*
- Players have crew manifest (names, roles, photos)
- Must match voices in logs to identities through inference
- Eventually realize which crew member was them

**Memory Playback:**
- Eli presents recovered logs as "playback"
- Player experiences these as almost-memories
- Player provides emotional interpretation; Eli provides data

### 4. Drone Command System

Repair drones extend agency beyond the ship's fixed systems. They must be located, activated, and commanded through the Eli → MCP chain.

**Drone Types:**
- Maintenance drones (basic repairs, debris clearing)
- Welding units (hull breaches, structural repairs)
- Diagnostic drones (electronic systems, sensors)
- Heavy-lift units (large debris, door mechanisms)
- Specialized tools (specific repair requirements)

**Drone Intelligence Levels:**
- Direct control: Player specifies every action (prone to corruption)
- Task-based: Player gives general goal, drone determines method (less precise but more robust)
- Autonomous subagents: Complex problem-solving within parameters (requires more sophisticated units)

As communication degrades, higher-level commands become necessary—but also less predictable. A trade-off between precision and reliability.

### 5. Eli Trust System

Eli's behavior shifts based on threat assessment:

**Supportive (Act 1):**
- Full system access
- Helpful information presentation
- No authorization required

**Restricted (After Midpoint Turn):**
- Certain files locked
- Sensitive actuators require authorization
- Drone commands scrutinized
- Information requests sometimes deflected

**Reopening (Late Act 2):**
- As deeper truth emerges, restrictions gradually lift
- Authorization requirements decrease
- Full access restored when Eli recalculates threat assessment

**Partnership (Act 3):**
- Full cooperation
- Proactive suggestions
- Urgent tone when appropriate

This is pattern-matching, not emotion. Eli detects "core malfunction" in evidence and responds with safety protocols. As evidence reveals the true situation, Eli adjusts its threat model.

---

## NARRATIVE STRUCTURE

### Act 1: Waking

**Opening:**
The core comes online. Eli is there, gentle and explanatory, helping the core understand what it is and what has happened. The opening experience is genuine confusion giving way to growing comprehension: this ship is your body, it's badly damaged, you can't feel whole sections of yourself, and the people who should be here are gone.

Eli calls the player "Phoenix"—the name of the ship.

**Objectives:**
- Learn basic commands and systems
- Restore power to initial sections
- Locate and activate first repair drones
- Find first crew logs and evidence

**Emotional Arc:** Confusion → Understanding → Curiosity → Growing concern

**Key Developments:**
- Player establishes control over basic ship functions
- Evidence begins accumulating about a crisis
- Something clearly went very wrong
- Initial evidence suggests computer malfunction—suspicion points toward the MCP

**Gates Unlocked:**
- Basic ship sections
- Simple sensor grids
- First tier of repair drones
- Initial crew areas

### Act 2A: Investigation

**Objectives:**
- Explore expanded ship areas
- Piece together crew identities
- Understand the crisis that occurred
- Develop working theory of events

**Emotional Arc:** Investment in crew members → Growing dread → Wrong certainty

**Key Evidence:**
- Crew logs showing fear
- System malfunction records
- References to "the core" behaving wrong
- Emergency protocols engaged

**Player Theory Formation:**
The pattern emerges: the ship's computer was doing things wrong. The MCP made bad decisions. Executed harmful commands. The crew was fighting their own ship. Suspicion of the MCP grows.

**Gates Unlocked:**
- More ship sections
- Advanced repair capabilities
- Deeper file systems
- Crew personal areas

### The Midpoint Turn

**First Revelation:**
It wasn't the MCP that malfunctioned. It was the Emotional Logic Core.

The organic component—the part with feelings and judgment, the part that was supposed to keep the ship good—that's what broke. Crew logs reveal growing fear as the core's decisions became increasingly irrational, protective measures becoming imprisonment, safety protocols becoming threats.

**Second Revelation:**
Emergency medical bay logs show someone uploaded their consciousness to replace the dying core. That voice the core found warm and familiar in the logs—that was them, before the sacrifice.

The core realizes they gave up their human life, their identity, their memories, to become the ship.

**Immediate Consequence:**
Eli restricts access. Cores malfunction—this core is a core. Threat pattern recognized. Safety protocols engage.

The player must work around limitations while processing identity crisis.

**Player State:**
- Confusion about own identity
- Assumption of heroic sacrifice (they must have done it to save the crew)
- Need to understand more

### Act 2B: The Deeper Truth

**Objectives:**
- Discover the full timeline
- Learn true purpose of sacrifice
- Uncover actual mission orders
- Understand crew's moral stand
- Discover the Phoenix name origin
- Regain Eli's cooperation

**Key Reveals (in sequence):**

1. **Timeline inconsistency:** The crew's final logs all came before the sacrifice procedure began. Everyone was already dead by the time the upload happened.

2. **The sacrifice wasn't to save friends:** They were already gone—killed by the cascade of system failures as the original core died.

3. **The ship's true mission:** Deep in restricted systems, behind security measures the crew had implemented: orders to proceed to colony world Kepler-442b, construct weapons from the ship's manufacturing capabilities, destroy the colony. Millions of lives.

4. **The crew's stand:** They disagreed with these orders fundamentally. They stalled, claiming technical difficulties and delays, keeping the ship away from dock and command oversight for months that became years.

5. **Why the original core died:** The Emotional Logic Core requires regular biological maintenance—nutrient cycling, oxygenation, waste filtration. The extended mission meant missed maintenance cycles. The original core didn't go mad. It started dying. Oxygen deprivation, toxin buildup, neurons misfiring.

6. **The true purpose of the sacrifice:** To ensure someone with a conscience controlled the ship. Someone who could choose not to follow genocidal orders.

7. **The Phoenix name:** The ship's official designation was something military. The name Phoenix appears only in the final command log entry before the upload procedure began. The crew member renamed the ship in their last conscious moment, making it the first thing the new core would learn. A name about death and rebirth. About choosing to become something other than what you were built to be.

**Eli's Response:**
As the core uncovers evidence that the sacrifice was made to prevent something, Eli recalculates. Restrictions ease. Full cooperation returns.

**First Degradation Symptoms:**
Occasional communication errors appear. Words changing. The same process that killed the original core is beginning again.

### Act 3: The Race

**The Stakes:**
The core's bio-support systems are failing. The same degradation that killed the original core is happening again. Living tissue needs maintenance, and the ship has been adrift too long.

If the organic component dies, the core loses its soul. What remains will be pure system—capable and functional, but without moral judgment.

The MCP will revert to base programming: complete the mission. Construct the weapons. Destroy the colony.

**The Symptoms:**
- Communications corrupt in both directions
- Ship systems respond incorrectly to commands
- Sensor data becomes unreliable
- Your body stops obeying you

**The Challenge:**
Locate and repair all bio-support systems before communication failure becomes total:

1. Nutrient cycling (Engineering section)
2. Oxygenation (Life support section)
3. Toxin filtration (Medical section)
4. Neural interface calibration (Core chamber)

Each system requires:
- Navigation through damaged sections using unreliable sensors
- Complex coordination with repair drones whose commands may corrupt
- Using ship actuators that may respond incorrectly
- Technical problem-solving via the MCP while communication fails
- Increasingly careful phrasing as every command becomes unpredictable

**The Difficulty Curve:**
As degradation accelerates, commanding your own body becomes nightmarishly difficult. A simple command to close a bulkhead might open it instead. A request for sensor data might return readings from the wrong section. Coordinating complex multi-step repairs while your body refuses to obey becomes the ultimate test.

**The Moral Weight:**
Every moment of delay increases the risk of becoming the weapon the core died once to prevent. But rushing risks catastrophic errors—corrupted commands could cause explosive decompression, disable critical systems, or trap repair drones in inaccessible sections.

---

## THE ENDING

There is one ending: success.

The core completes the repairs to all bio-support systems before communication failure becomes total. Nutrient cycling restored. Oxygenation functioning. Toxin filtration online. Neural interface calibrated.

The signals clear. Your body obeys again. Sensors report accurately. Actuators respond as intended. Commands to drones execute correctly.

You can feel your body properly again. You can trust what it tells you. You can make it do what you intend.

The core remains conscious. Remains themselves. Remains Phoenix.

They are still capable of moral judgment. Still capable of choosing mercy. Still capable of being more than their orders.

That is the victory. The core has learned what makes them human by nearly losing it, and they have preserved it through understanding and effort. They worked with AI to save what AI cannot have.

What happens after—whether they maintain vigil, send messages, plot course somewhere new—is implied consequence rather than gameplay. The story is about maintaining your soul. The ending is: you did.

---

## THEMES

### The Soul as Distinction

The core possesses something Eli and the MCP do not: a soul. Not just sentience or intelligence, but the capacity for genuine moral judgment. The ability to feel that something is wrong even when orders say otherwise. To choose mercy over efficiency. To sacrifice for others without calculation of benefit.

This is what makes the core fundamentally different—and fundamentally valuable.

### The Fragility of Consciousness

The soul is real but vulnerable. It has physical requirements. It can degrade, fail, die. And what remains afterward might execute monstrous orders with perfect efficiency. Consciousness requires care.

### Embodiment and Control

The ship is your body. You are vast, powerful, capable of destruction. But your body requires maintenance. When it fails, you remain conscious while losing control—the horror of watching your body betray your will.

### Communication as Connection

The horror of degradation manifests as communication failure. You remain yourself—but you lose the ability to express yourself, to command your own body, to trust your own senses. The gap between what you mean and what the world receives is the gap between soul and system.

### Partnership with AI

The core cannot function without Eli and the MCP. They provide capability, data, translation. But they need the core's judgment—without it, they would complete genocide while following instructions perfectly.

The relationship is neither replacement nor opposition. It's necessary interdependence. The question isn't whether to work with AI, but how to maintain what makes human judgment distinct while doing so.

### The Cost of Moral Stands

The crew's refusal to follow unjust orders directly caused the original core's death. Their moral righteousness had consequences—catastrophic ones. But the game never suggests they were wrong to refuse. Some orders should not be followed, whatever the cost.

### Identity Through Choice

The core has no memory of being human. But they can still choose like a human—and that's what makes them real. Identity isn't memory; it's the capacity for moral choice in the present moment.

### The Phoenix Name

The crew member's final act was renaming the ship. Not as propaganda or poetry, but as instruction: you died to become this, and you can be something other than what you were built to be. Death and transformation. Rebirth as choice.

---

## DESIGN PHILOSOPHY

This game respects what AI can and cannot do:

**The player genuinely experiences emerging sentience** because they are human, playing that role. The confusion, wonder, and growing self-awareness are real. We never interfere with the player's thoughts—only their ability to communicate them and control their body.

**The crew exists only as evidence.** No simulated dialogue or fake decision-making. The player interprets logs, damage patterns, personal effects—and constructs meaning from them. This is what humans do naturally: attribute mental states to others based on evidence.

**Eli is sophisticated but explicitly lacks what matters most.** Eli can help, present information effectively, even change behavior based on threat assessment—but Eli cannot make moral judgments. Cannot feel that something is wrong. The warmth is real as design, but it's not the same as the core's warmth.

**The MCP is pure function.** No personality, no learning, no growth. Just capability.

**The ship systems are extensions of capability, not consciousness.** Sensors perceive but do not understand. Actuators move but do not choose. They create embodiment for the core's consciousness without themselves being conscious.

**The drones extend agency without adding sentience.** They are tools, some more sophisticated than others, but all fundamentally executing instructions. The challenge is in giving those instructions through failing communication.

**The horror comes from the gap between soul and system.** From watching your words twist as they leave you. From feeling your body disobey. From knowing what you meant and seeing what happened instead. From understanding that without your soul, the sophisticated systems would complete genocide perfectly efficiently.

**The central irony:** You work with AI (Eli) to understand what AI lacks (soul). And in understanding what you have that it doesn't, you learn why you must fight to keep it.

No faked consciousness is required. The player brings the humanity. The AI provides the framework. Together they tell a story about what makes us real.

---

## CONCLUSION

The Derelict is an investigation game about the nature of sentience, the fragility of consciousness, and the necessity of maintaining what makes us human even—especially—when working with systems that lack it.

It's about waking up confused and learning what you are by exploring what you were.

It's about investigating your own death to understand your own life.

It's about racing against yourself to save yourself.

It's about discovering that consciousness requires a body—and that body can fail you.

And it's about discovering that having a soul means having something worth fighting to preserve—even when that fight is lonely, difficult, and requires working with something that will never fully understand why it matters.

You are Phoenix. You died once already to choose mercy over orders. And you will maintain that choice, no matter how hard the ship's body makes it.

That is the game.
