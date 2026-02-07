# Durable Objects Architecture for Shipshape

## Overview

Cloudflare Durable Objects (DOs) provide per-instance SQLite storage with strong consistency. Each DO is a globally-unique, single-threaded execution environment that can communicate with other DOs via RPC.

## Single-Player Architecture

One DO per save game. Simple and isolated.

```
Player Request
    ↓
Worker (routes by save ID)
    ↓
Game DO (idFromName("save-{saveId}"))
    ├── SQLite: nodes table
    ├── SQLite: edges table
    ├── SQLite: events table
    └── Game simulation loop
```

### Schema

```sql
CREATE TABLE nodes (
  id TEXT PRIMARY KEY,
  type TEXT NOT NULL,
  data JSON
);

CREATE TABLE edges (
  source TEXT NOT NULL,
  target TEXT NOT NULL,
  type TEXT NOT NULL,
  data JSON,
  PRIMARY KEY (source, target, type)
);

CREATE TABLE events (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  timestamp INTEGER NOT NULL,
  type TEXT NOT NULL,
  data JSON
);
```

### Benefits
- Complete isolation per player
- No coordination overhead
- Simple save/load (DO persists automatically)
- Free tier friendly

---

## Multiplayer Architecture

### Option 1: Hierarchical (Sector-Owned State)

Sectors own authoritative state. Ships report actions, sectors resolve conflicts.

```
                    Universe DO (optional global coordinator)
                           │
         ┌─────────────────┼─────────────────┐
         ↓                 ↓                 ↓
    Sector DO         Sector DO         Sector DO
    "alpha-1"         "alpha-2"         "beta-1"
         │                 │
    ┌────┴────┐           │
    ↓         ↓           ↓
Ship DO   Ship DO     Ship DO
"ship-1"  "ship-2"    "ship-3"
```

**Communication Flow:**
```typescript
// Ship requests action
const sectorId = this.env.SECTOR.idFromName(this.currentSector);
const sector = this.env.SECTOR.get(sectorId);
const result = await sector.requestAction({
  ship: this.shipId,
  action: "fire",
  target: "ship-2"
});

// Sector resolves and notifies affected ships
const targetShip = this.env.SHIP.get(this.env.SHIP.idFromName("ship-2"));
await targetShip.receiveDamage(result.damage);
```

**Pros:**
- Clear authority (sector owns truth)
- Conflict resolution is centralized
- Ships can move between sectors

**Cons:**
- Sector DO can become bottleneck
- Cross-sector actions need coordination

---

### Option 2: Peer-to-Peer with Index

Ships communicate directly, index tracks existence.

```
         Index DO
         (registry)
        ↗    ↑    ↖
       /     |     \
Ship DO ←→ Ship DO ←→ Ship DO
```

**Discovery:**
```typescript
// Register on creation
const index = this.env.INDEX.get(this.env.INDEX.idFromName("global"));
await index.register(this.shipId, { sector: "alpha-1", position: [x, y] });

// Find nearby ships
const nearby = await index.findInSector("alpha-1");
for (const id of nearby) {
  const ship = this.env.SHIP.get(this.env.SHIP.idFromName(id));
  await ship.broadcast({ type: "ping", from: this.shipId });
}
```

**Pros:**
- No single bottleneck
- Direct communication is fast

**Cons:**
- Conflict resolution is complex (who wins simultaneous actions?)
- Index can become stale

---

### Option 3: Event Bus (Pub/Sub per Sector)

Sectors act as message brokers. Ships subscribe to events.

```
Sector DO "alpha-1"
    │
    ├── subscribers: [ship-1, ship-2, ship-3]
    │
    └── broadcast(event) → fans out to all ships
```

**Pattern:**
```typescript
// Ship subscribes when entering sector
await sector.subscribe(this.shipId);

// Ship publishes action
await sector.publish({
  type: "weapon-fired",
  source: this.shipId,
  target: "ship-2",
  timestamp: Date.now()
});

// Sector broadcasts to all subscribers
// Each ship processes events and updates local state
```

**Pros:**
- Decoupled communication
- Easy to add observers (stations, drones)

**Cons:**
- Eventually consistent (ships may see events in different order)
- Need conflict resolution for simultaneous actions

---

## Key Considerations

### No Cross-DO Transactions
There's no atomic transaction spanning multiple DOs. Handle partial failures:

```typescript
try {
  await shipA.deductCredits(100);
  await shipB.addCredits(100);
} catch (e) {
  // Must manually rollback shipA if shipB fails
  await shipA.addCredits(100);
}
```

### Latency
Each DO-to-DO call has network overhead. Batch when possible:

```typescript
// Bad: N round trips
for (const id of shipIds) {
  await getShip(id).ping();
}

// Better: parallel calls
await Promise.all(shipIds.map(id => getShip(id).ping()));
```

### Hot Spots
Coordinator DOs (universe, sector) can become bottlenecks. Mitigate by:
- Sharding sectors smaller
- Caching read-only data in Workers KV
- Using eventual consistency where acceptable

### Discovery
DOs don't have built-in discovery. Options:
- Deterministic IDs: `idFromName("sector-alpha-1")` - works if you know the name
- Index DO: maintains registry of active entities
- Workers KV: store ID mappings (eventually consistent)

---

## Recommended Architecture for Shipshape

### Single-Player (Current Design)
```
Game DO per save
    └── Full graph state in SQLite
    └── Simulation runs on request or via Alarms
```

### Multiplayer (Future)
```
Sector DO (authoritative)
    ├── Owns positions, combat resolution
    ├── Broadcasts events to ships in sector
    └── Handles ship arrivals/departures

Ship DO (player state)
    ├── Owns inventory, robot crew, cat
    ├── Reports actions to current sector
    └── Receives updates from sector

Station DO (persistent locations)
    ├── Owns docking, trade state
    └── Coordinates with sector for visibility
```

Ships are the only player-owned DOs. Sectors and stations are shared infrastructure.
