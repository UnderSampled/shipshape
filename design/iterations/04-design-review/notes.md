# User Statements - Inconsistency Review Session

## On the Three Drafts

> I wrote all three. First StarGraph, then what you call A (The Derelict), then what you call B (Shipshape). These were written separately with no evolution between them besides remembering concepts from the previous iterations.

*[Context: After Claude identified two "different games" (The Derelict investigation vs. Shipshape roguelike journey) and flagged inconsistencies across all design files]*

## On the Shipshape Intent

> When I wrote the shipshape, I was planning to make the simple system first and get it working, then add more story later. I may not necessarily use the full story, but I wanted to capture it and include it in the design process.

*[Context: Explaining why the Shipshape generated docs lack the Derelict's narrative depth -- it was intentional scoping for an MVP, not a rejection of the story]*

## On How the Notes Were Created

> To that end, I asked claude in that session to save out my messages in the notes files, with context.

*[Context: Explaining the origin of the notes/ folder -- the verbatim user statements with contextual headers were saved by Claude during the Shipshape design session]*

## On Notes Convention Going Forward

> I recommend you do that for this conversation too. I actually recommend starting by organizing the notes folder so you'll be able to take more notes for each conversation, and write that you should do so in the CLAUDE.md file.

*[Context: Establishing the convention that each Claude conversation should save user statements into per-session subfolders under design/notes/, and that this convention should be documented in CLAUDE.md]*

## On the Iteration Order and Structure

> It looks like you saved the derelict and shipshape as being the same conversation? The order was Stargraph (no conversation, written by hand, but you could move that whole folder to be that 'conversation'/'step'), then the derelict, then shipshape.

*[Context: Correcting Claude's initial organization which had lumped the Derelict story brainstorming notes into the Shipshape session folder. The three iterations were separate: stargraph (hand-written), then derelict (Claude conversation), then shipshape (Claude conversation)]*

## On File Organization

> Truly move the stargraph folder in as design/iterations/01-stargraph, and the same for the other three. Put the generated folders for each as subdirectories therein.

*[Context: When asked whether to separate generated files by session or keep them flat. Chose a unified structure where each iteration is a top-level folder under design/iterations/, with generated output as a subdirectory within it]*

## On the Relationship Between the Game and the Story

> As I've already stated, I had planned to make the engine simple, and add the story later. In some ways that was the idea with Stargraph too - that it would be an engine to build stories in, kind of like how Star Citizen plans to add their single-player story mode. The Dwarf-fortress + FTL style survival game seemed like a good way to make the spaceship complex enough to be interesting when it comes time to explore it for the story. So when we add the story, all of that would still be there as the game. That's why I had tried to name the files like I had: concept, game design, story, and software architecture.

*[Context: Responding to Claude's "two different games" framing. The designs are complementary layers, not competing visions. The generated files were intentionally named: concept, game_design, story, and architecture.]*

## On Robots vs. Drones

> The DF style robots are just one of the more intelligent tiers. They are indeed the crew. An even more intelligent tier might be one that actually uses an LLM.

*[Context: Reconciling the robot/drone distinction across the design docs]*

## On the Ending

> I like the idea that docking is a reward; a denouement. So, if we ever put that story in, or even if we're just doing repairs, then being repaired enough to dock is a requirement to get the good ending.

*[Context: On how the Shipshape ending (docking) and Derelict ending (self-repair) relate]*

## On the Cat

> This wasn't my original thought, but it has come out of the generated design, and I would like to build it up: Add tamagotchi as one of the inspirations. The cat provides something to come back for and take care of, which could have a real-time (slow time) component to it. And, just some emotional attachment is good. Story-wise, it's like the ship in Alien, but if Ripley and the Xenomorph both died and the cat was the only survivor — and then the ship wakes up! Importantly, though, the cat shouldn't be discovered right up front, nor mentioned in any diagnostics or documentation until it's discovered during play (I don't want Eli telling the core/user all about the cat when they should be learning what it means to be a (derelict) ship.

*[Context: After Claude's inconsistency report noted the cat was present in game_design.md but absent from story.md]*

## On Tech Stack and Architecture

> This version will continue with the python in-memory graph, not Neo4j. We will be using fly.io, but technically through their new 'Sprites' service, that handles suspension automatically. So we just need to write with the turn-based semi-serverless style previously mentioned in the architecture. I still have the generated python from shipshape in this repository, but we will have to modify it to use that per-request logic.

*[Context: After reviewing the tech stack section in CLAUDE.md]*

## On Sleep Mode vs. Time Deltas

> Sleep mode is for skipping time in the universe while time-deltas describe how to process a semi-serverless slow-rate game loop. I think it makes sense for one of the MCP tools to be a way to "put the emotional logic core into stasis" which would artificially skip a time delta until a parameter duration, or until an interrupt event.

> The framing of always working instantly fast when not in sleep mode (I believe that was what I said in Stargraph) was an in-universe way to explain true turn-based mode. But I like the idea that things will unfold in realtime against the real clock.

*[Context: After Claude flagged the stargraph "sleep mode" vs. architecture "time-deltas" as a remaining inconsistency]*

## On MCP Tool Style

> The MCP tools should expose the modules, sensors, and actuators as if it were a dumb computer (it is) that just shows the facts. It should provide tools for all of the ship's accessible state, including things that you listed as body-style. Any actions should be done through actuators (like Stargraph was trying to have). For instance, there might be a physical communications module to interact with the robots (I really wish we could call them droids... LucasArts! *shakes fist*). It would have a tool to use it (though some modules might be grouped up with a command structure), and it would be possible for it to go offline.

> Importantly, it is 100% Eli's responsibility to present this information as if it were sensations in the ship's body, so that the core feels like they *are* the ship. Eli would of course be able to relay the readouts analytically as well if the core asks for it. Remember, core is just our name for the user in this game.

*[Context: After Claude flagged the MCP tool abstraction level as a remaining inconsistency — game-style tools vs body-style sensors]*

## On Procedural Generation and World Design

> If there is any procedural generation of the world, it should be from a fixed seed. Should there be any? Let's approach this like a dungeon master for D&D (another inspiration?): Set up a world with actors, motivations, and triggers for scripted encounters. Some parts of the world might be procedurally generated (like a dungeon module, or in our case that would be a derelict space station, robot mining colony, alien hive, etc.). That's a game system of its own for each of those modules. Some parts of the world might be procedurally generated like Elite/Frontier, rolling from tables to generate solar systems, economies, etc. Dwarf Fortress does this procedural generation too, for terrain. But then there's random things during the game: for instance if we construct a robot, it might have a random personality. That wouldn't be generated according to the seed (except maybe chaotically). The real question is, can we write enough of a detailed scripted plot, with this alien hive here and these robots acting funny here, etc., for the outside world, or do we focus on scripting inside the ship and letting the outer space be procedural? I think I will say yes. Elite gives a good blueprint, and ultimately the outer space is just a backdrop for what's going on inside the ship, and a source for supplies (and an end goal.) Obviously, there will be scripted locations, like the destination, but those are built into the generated map. Really, this is all to say: Keep it roguelike!

*[Context: After Claude flagged procedural generation (seeded or not) as the last remaining inconsistency]*

## On the Cat in start_game (second review)

> Correct, we must not mention the cat in those locations.

*[Context: Claude noted that server.md's start_game prompt and the README mention the cat upfront, contradicting the earlier decision that the cat shouldn't be revealed until discovered during play]*

## On Modules/Hardpoints and Items (second review)

> Yes, we should add/include these.

*[Context: Claude noted that Stargraph's ontology had a module/hardpoint system and an item system (quest items, artifacts, trade goods) that Shipshape doesn't include]*

## On Communication Degradation

> Let's not include that part of the story, for now anyways. The intention was supposed to be adding communications difficulty between the Core and Eli, which might be hard without hosting the LLM ourselves, which is counter to the MCP-as-game concept. I guess it could be faked with instructions to the LLM, or somehow putting Eli in a sub agent. Since I'm not even sure I want to have the "I used to be human" plot to be in the final, let's just not worry about it. I do want to have some amount of discovering what happened to the human crew, though.

*[Context: Claude asked how the Derelict's communication degradation mechanic would work through a structured MCP tool interface]*

## On Eli's Autonomy

> Eli is not autonomous, as the Emotional Logic Interface, but is an agent with the same capabilities for tool-use as whatever the user is hosting the MCP in.

*[Context: Claude noted that Stargraph's experience.md gives the system much more autonomy than the Shipshape docs]*

## On System Autonomy and Robot Levels

> The system in general, though, which would include the Master Control Program and the simulated ship, that is autonomous! And many (but not all) of the robots (certainly, we need to make sure that the different levels of robots are represented).

*[Context: Clarifying after the Eli autonomy answer]*

## On the Honesty Principle and Dialogue

> The honesty is about sentience, correct. We can have dialogue, but it should be honest: an LLM powered AI (like Eli, or like a smart robot) can have dialogue it generates, and any problems with its generation can honestly be attributed in-game to the peculiarities of the robot's tech (not pretending to be smarter or more sentient than it is). There should be no scripted dialogue, apart from dumb robots using scripted dialogue that is also scripted in-universe. The one exception to all of this is creatures: We can have a cat, or aliens. They won't talk, so it's less of an issue, but we will accept that as part of the fiction.

*[Context: Claude asked whether the honesty principle from story.md conflicts with LLM-powered robots generating dialogue]*

## On Ship Names and Difficulty Modes

> I figured out the ship naming. Three difficulties/stories, each with a different ship name, and maybe different features and layout: the Intrepid (Easy, Exploration sandbox mode, all systems online — a drone ship never meant to have people aboard); the Perseverance (Normal, Survival adventure story mode, Systems offline — crew missing); the Phoenix (Hard, Horror/mystery story mode, Antagonistic systems and communications issues — crew dead).

> We would start with the first two.

*[Context: After all inconsistency review items were resolved, including the earlier discussion about the Phoenix ship name from the Derelict story]*

## On Naming: Crew vs. Passengers

> What we referred to as crew before are passengers and personnel (officers, technicians), and the robots are 'crew'.

*[Context: After discussing how a robot ship would think of people — as passengers. The robots actually crew the ship; the humans are along for the ride.]*

## On the Opening Experience

> Start roleplaying: I am a spaceship. Technically, I am the emotional logic core of a spaceship, "the core", and you are the Emotional Logic Interface, Eli. You communicate to me what your gather from sensors in such a way that I perceive the ship as my body. This is under the knowledge that I don't feel anything without you describing it, but if you describe it in second person, I will own the feelings more, which is intended to receive the best response from an emotional core. Importantly, I provide sentience to the ship. I will awake with no memories, including any understanding of who I am. The name of the ship is Perseverance. Start with a computerized connection sequence and then a connection to you. The ship is derelict, and many of the systems are destroyed. It's a survival game. The humans are dead, but the crew of robots can come online as we fix things.

> Eli waits for me to understand who I am before making an introduction, in order to not break the illusion of identity between the core and the rest of the spaceship (i.e. so the core understands they are the space ship). The resulting confusion of understanding what's going on when bombarded with senses is actually helpful to convey the urgency of the situation. Eli can help the core understand its identity though. Then Eli can make an introduction.

*[Context: After trying several iterations of roleplaying the opening. This is not the final start prompt, but captures what the opening should feel like.]*
