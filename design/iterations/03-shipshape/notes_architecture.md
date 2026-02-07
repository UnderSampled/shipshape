# User Design Thoughts - Verbatim

## Platform Preference

> I like Fly.io.

*[Context: After comparing Cloudflare Workers, Fly.io, Railway, Supabase, and other platforms for hosting MCP servers with graph database needs]*

## On NetworkX and Idle Cost

> Would the NetworkX version run in fly.io, and not cost anything when idle?

*[Context: Exploring whether the original Python/NetworkX design could work on Fly.io with suspend/stop for cost savings]*

## On Persistent Memory and Saves

> Perhaps, since memory is persistent, it can just be a backup saved every once in a while, or queued up to save away from the game logic.

*[Context: After learning Fly.io suspend preserves memory state. Realizing that with memory persistence, disk saves become backups rather than the source of truth]*

## On Server Idle Behavior and Game Loop

> The key difference is that we'll still want to write the server to be asynchronous rather than continue processing the gamestate while idle. Basically, have the game loop not affect what the runner thinks of as idle just because it's processing idly itself, and any realtime functions must be able to process changes from hours instead of just fps milliseconds.

*[Context: Clarifying that the game shouldn't keep the machine awake with a continuous loop. The simulation must handle large time gaps efficiently]*

## On Hybrid Active/Idle Model

> The server can stay alive during a session (as in, able to process multiple requests in a short time, while updating the gamestate in the background). The key is it'd be a hybrid thing: It could be written per-request like you've just described, but it could also be written to call the loop with short updates to stay responsive for as long as it's awake.

*[Context: Clarifying that during active play, the server can stay running and tick. The constraint is about not preventing idle/suspend, not about never running a loop]*

## On Efficiency of Time-Based Updates

> All that said, since it would still need to be able to support the long-time updates, and just running the loop a bunch of times to catch up wouldn't be efficient, the per-request/per-input updates might still be the best idea.

*[Context: Recognizing that if large Δt must be handled efficiently anyway, turn-based/input-driven may be simpler than maintaining two update modes]*

## On Roguelike Comparison

> In some ways that makes it more rogue-like (Rogue would update the world only on input 'turns').

*[Context: Drawing parallel to classic roguelikes where the world only advances when the player acts]*

## On Turn-Based vs Multiplayer

> turn based is great, and probably what we'll do (it was this way in the stargraph design), but it doesn't work for multiplayer. That's where using time deltas comes in play.

*[Context: Acknowledging turn-based matches the original Stargraph design, but noting the limitation for multiplayer where world can't freeze for one player]*

## On Multiplayer Graph Challenges

> Of course it also makes things more challenging if we need to have multiple servers mutating the same graph.

*[Context: Identifying the distributed systems challenge - concurrent writes to shared game state across multiple server instances]*
