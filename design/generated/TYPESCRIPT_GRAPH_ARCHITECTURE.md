# TypeScript Graph Architecture for Shipshape

## Overview

This document outlines how to manage the game state graph in TypeScript on Cloudflare Workers with Durable Objects SQLite storage.

## Approach Options

### Option A: In-Memory Library + SQLite Persistence

Use a library like [Graphology](https://graphology.github.io/) for graph operations, sync to SQLite for durability.

**Pros:**
- Rich query API (traversal, algorithms)
- Fast in-memory operations
- Battle-tested library

**Cons:**
- Must sync in-memory state ↔ SQLite
- Memory overhead (full graph in RAM)
- Potential consistency issues

### Option B: SQLite-Native with Recursive CTEs

Store nodes/edges directly in SQLite, use recursive CTEs for traversal.

**Pros:**
- Single source of truth
- No sync complexity
- Works with large graphs
- Durable by default

**Cons:**
- Less expressive than Cypher/Gremlin
- Complex traversals need careful SQL
- More boilerplate

### Option C: Hybrid (Recommended)

SQLite as source of truth, thin TypeScript abstraction layer for common operations, load subgraphs into memory only when needed.

**Pros:**
- Best of both worlds
- Type-safe API
- Efficient for game-sized graphs
- No external dependencies

---

## Recommended Architecture (Option C)

### SQLite Schema

```sql
-- Core tables
CREATE TABLE nodes (
  id TEXT PRIMARY KEY,
  type TEXT NOT NULL,
  data TEXT NOT NULL DEFAULT '{}'  -- JSON
);

CREATE TABLE edges (
  id TEXT PRIMARY KEY,  -- generated: source:type:target
  source TEXT NOT NULL,
  target TEXT NOT NULL,
  type TEXT NOT NULL,
  data TEXT NOT NULL DEFAULT '{}',  -- JSON
  UNIQUE(source, type, target),
  FOREIGN KEY (source) REFERENCES nodes(id) ON DELETE CASCADE,
  FOREIGN KEY (target) REFERENCES nodes(id) ON DELETE CASCADE
);

-- Indexes for traversal
CREATE INDEX idx_edges_source ON edges(source);
CREATE INDEX idx_edges_target ON edges(target);
CREATE INDEX idx_edges_type ON edges(type);
CREATE INDEX idx_nodes_type ON nodes(type);

-- Event log for game events
CREATE TABLE events (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  timestamp INTEGER NOT NULL,
  type TEXT NOT NULL,
  data TEXT NOT NULL DEFAULT '{}'
);

CREATE INDEX idx_events_timestamp ON events(timestamp);
CREATE INDEX idx_events_type ON events(type);
```

### TypeScript Types

```typescript
// Node types matching Shipshape ontology
type NodeType =
  | 'ship' | 'room' | 'system' | 'robot' | 'cat'
  | 'item' | 'module' | 'sector' | 'station' | 'hazard';

// Edge types (relationships)
type EdgeType =
  | 'contains'      // room contains robot
  | 'connects'      // room connects to room
  | 'powers'        // reactor powers system
  | 'assigned_to'   // robot assigned to task
  | 'located_in'    // cat located in room
  | 'docked_at'     // ship docked at station
  | 'in_sector'     // ship in sector
  | 'targets'       // weapon targets hazard
  | 'requires'      // system requires power
  | 'owns';         // ship owns item

// Base node interface
interface BaseNode<T extends NodeType, D = Record<string, unknown>> {
  id: string;
  type: T;
  data: D;
}

// Specific node types with typed data
interface RoomNode extends BaseNode<'room', {
  name: string;
  atmosphere: number;      // 0-100
  temperature: number;     // kelvin
  powered: boolean;
  damaged: boolean;
}> {}

interface RobotNode extends BaseNode<'robot', {
  designation: string;     // "ENG-1", "MNT-4"
  role: 'ENG' | 'PWR' | 'NAV' | 'SEC' | 'MNT' | 'MED';
  power: number;           // 0-100 battery
  thermal: number;         // operating temp
  maintenance: number;     // wear level
  memory: number;          // data integrity
  traits: {
    diligent: number;
    cautious: number;
    social: number;
    curious: number;
  };
  task?: string;
  status: 'idle' | 'working' | 'charging' | 'malfunctioning' | 'offline';
}> {}

interface CatNode extends BaseNode<'cat', {
  name: string;
  hunger: number;
  thirst: number;
  warmth: number;
  health: number;
  happiness: number;
  status: 'exploring' | 'sleeping' | 'eating' | 'hiding' | 'following';
}> {}

interface SystemNode extends BaseNode<'system', {
  name: string;
  type: 'reactor' | 'life_support' | 'sensors' | 'engines' | 'shields' | 'weapons' | 'doors' | 'comms';
  powered: boolean;
  powerDraw: number;
  health: number;
  online: boolean;
}> {}

// Union type for all nodes
type GameNode = RoomNode | RobotNode | CatNode | SystemNode; // ... extend as needed

// Edge interface
interface Edge<T extends EdgeType = EdgeType> {
  id: string;
  source: string;
  target: string;
  type: T;
  data: Record<string, unknown>;
}
```

### Graph Service Class

```typescript
import { SqlStorage } from 'cloudflare:workers';

export class GraphService {
  constructor(private sql: SqlStorage) {}

  // ─────────────────────────────────────────────────────────────
  // Node Operations
  // ─────────────────────────────────────────────────────────────

  addNode<T extends GameNode>(node: T): void {
    this.sql.exec(
      `INSERT INTO nodes (id, type, data) VALUES (?, ?, ?)`,
      node.id,
      node.type,
      JSON.stringify(node.data)
    );
  }

  getNode<T extends GameNode>(id: string): T | null {
    const row = this.sql.exec(
      `SELECT id, type, data FROM nodes WHERE id = ?`,
      id
    ).one();
    if (!row) return null;
    return {
      id: row.id as string,
      type: row.type as T['type'],
      data: JSON.parse(row.data as string)
    } as T;
  }

  getNodesByType<T extends GameNode>(type: T['type']): T[] {
    const rows = this.sql.exec(
      `SELECT id, type, data FROM nodes WHERE type = ?`,
      type
    ).toArray();
    return rows.map(row => ({
      id: row.id as string,
      type: row.type as T['type'],
      data: JSON.parse(row.data as string)
    })) as T[];
  }

  updateNode<T extends GameNode>(id: string, data: Partial<T['data']>): void {
    const existing = this.getNode(id);
    if (!existing) throw new Error(`Node ${id} not found`);

    this.sql.exec(
      `UPDATE nodes SET data = ? WHERE id = ?`,
      JSON.stringify({ ...existing.data, ...data }),
      id
    );
  }

  deleteNode(id: string): void {
    // Edges deleted via CASCADE
    this.sql.exec(`DELETE FROM nodes WHERE id = ?`, id);
  }

  // ─────────────────────────────────────────────────────────────
  // Edge Operations
  // ─────────────────────────────────────────────────────────────

  addEdge(source: string, target: string, type: EdgeType, data: Record<string, unknown> = {}): void {
    const id = `${source}:${type}:${target}`;
    this.sql.exec(
      `INSERT INTO edges (id, source, target, type, data) VALUES (?, ?, ?, ?, ?)`,
      id, source, target, type, JSON.stringify(data)
    );
  }

  removeEdge(source: string, target: string, type: EdgeType): void {
    this.sql.exec(
      `DELETE FROM edges WHERE source = ? AND target = ? AND type = ?`,
      source, target, type
    );
  }

  getEdgesFrom(source: string, type?: EdgeType): Edge[] {
    const query = type
      ? `SELECT * FROM edges WHERE source = ? AND type = ?`
      : `SELECT * FROM edges WHERE source = ?`;
    const rows = type
      ? this.sql.exec(query, source, type).toArray()
      : this.sql.exec(query, source).toArray();
    return this.parseEdges(rows);
  }

  getEdgesTo(target: string, type?: EdgeType): Edge[] {
    const query = type
      ? `SELECT * FROM edges WHERE target = ? AND type = ?`
      : `SELECT * FROM edges WHERE target = ?`;
    const rows = type
      ? this.sql.exec(query, target, type).toArray()
      : this.sql.exec(query, target).toArray();
    return this.parseEdges(rows);
  }

  private parseEdges(rows: Record<string, unknown>[]): Edge[] {
    return rows.map(row => ({
      id: row.id as string,
      source: row.source as string,
      target: row.target as string,
      type: row.type as EdgeType,
      data: JSON.parse(row.data as string)
    }));
  }

  // ─────────────────────────────────────────────────────────────
  // Traversal Operations
  // ─────────────────────────────────────────────────────────────

  // Get all nodes connected from source via edge type
  getConnected(source: string, edgeType: EdgeType): GameNode[] {
    const rows = this.sql.exec(`
      SELECT n.id, n.type, n.data
      FROM nodes n
      JOIN edges e ON n.id = e.target
      WHERE e.source = ? AND e.type = ?
    `, source, edgeType).toArray();
    return this.parseNodes(rows);
  }

  // Get container (what contains this node)
  getContainer(nodeId: string): GameNode | null {
    const row = this.sql.exec(`
      SELECT n.id, n.type, n.data
      FROM nodes n
      JOIN edges e ON n.id = e.source
      WHERE e.target = ? AND e.type = 'contains'
      LIMIT 1
    `, nodeId).one();
    if (!row) return null;
    return this.parseNode(row);
  }

  // Get contents (what this node contains)
  getContents(nodeId: string): GameNode[] {
    return this.getConnected(nodeId, 'contains');
  }

  // Find path between nodes (BFS via recursive CTE)
  findPath(from: string, to: string, maxDepth = 10): string[] | null {
    const rows = this.sql.exec(`
      WITH RECURSIVE path(node, route, depth) AS (
        SELECT ?, ?, 0
        UNION ALL
        SELECT
          e.target,
          path.route || ',' || e.target,
          path.depth + 1
        FROM path
        JOIN edges e ON e.source = path.node
        WHERE path.depth < ?
          AND path.route NOT LIKE '%' || e.target || '%'
      )
      SELECT route FROM path WHERE node = ? LIMIT 1
    `, from, from, maxDepth, to).one();

    if (!rows) return null;
    return (rows.route as string).split(',');
  }

  // Get all nodes reachable from source within depth
  getReachable(source: string, maxDepth = 5): GameNode[] {
    const rows = this.sql.exec(`
      WITH RECURSIVE reachable(id, depth) AS (
        SELECT ?, 0
        UNION
        SELECT e.target, r.depth + 1
        FROM reachable r
        JOIN edges e ON e.source = r.id
        WHERE r.depth < ?
      )
      SELECT DISTINCT n.id, n.type, n.data
      FROM reachable r
      JOIN nodes n ON n.id = r.id
    `, source, maxDepth).toArray();
    return this.parseNodes(rows);
  }

  private parseNodes(rows: Record<string, unknown>[]): GameNode[] {
    return rows.map(row => this.parseNode(row));
  }

  private parseNode(row: Record<string, unknown>): GameNode {
    return {
      id: row.id as string,
      type: row.type as NodeType,
      data: JSON.parse(row.data as string)
    } as GameNode;
  }

  // ─────────────────────────────────────────────────────────────
  // Game-Specific Queries
  // ─────────────────────────────────────────────────────────────

  getRobotsInRoom(roomId: string): RobotNode[] {
    return this.getContents(roomId).filter(n => n.type === 'robot') as RobotNode[];
  }

  getCatLocation(): { cat: CatNode; room: RoomNode } | null {
    const cats = this.getNodesByType<CatNode>('cat');
    if (cats.length === 0) return null;
    const cat = cats[0];
    const room = this.getContainer(cat.id) as RoomNode;
    return { cat, room };
  }

  getSystemsByPowerState(powered: boolean): SystemNode[] {
    const systems = this.getNodesByType<SystemNode>('system');
    return systems.filter(s => s.data.powered === powered);
  }

  moveEntity(entityId: string, toRoomId: string): void {
    // Remove from current container
    this.sql.exec(
      `DELETE FROM edges WHERE target = ? AND type = 'contains'`,
      entityId
    );
    // Add to new container
    this.addEdge(toRoomId, entityId, 'contains');
  }
}
```

### Integration with MCP Server

```typescript
import { McpAgent } from "agents/mcp";
import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { z } from "zod";
import { GraphService } from "./graph";

export class ShipshapeMCP extends McpAgent {
  server = new McpServer({ name: "Shipshape", version: "1.0.0" });
  graph!: GraphService;

  async init() {
    // Initialize graph service with DO's SQLite
    this.graph = new GraphService(this.ctx.storage.sql);

    // Sensor tools
    this.server.tool("scan_ship", {}, async () => {
      const systems = this.graph.getNodesByType('system');
      const robots = this.graph.getNodesByType('robot');
      const cat = this.graph.getCatLocation();
      return {
        content: [{
          type: "text",
          text: JSON.stringify({ systems, robots, cat }, null, 2)
        }]
      };
    });

    this.server.tool("scan_room", { roomId: z.string() }, async ({ roomId }) => {
      const room = this.graph.getNode(roomId);
      const contents = this.graph.getContents(roomId);
      const connections = this.graph.getConnected(roomId, 'connects');
      return {
        content: [{
          type: "text",
          text: JSON.stringify({ room, contents, connections }, null, 2)
        }]
      };
    });

    this.server.tool("scan_robot", { robotId: z.string() }, async ({ robotId }) => {
      const robot = this.graph.getNode<RobotNode>(robotId);
      const location = this.graph.getContainer(robotId);
      return {
        content: [{
          type: "text",
          text: JSON.stringify({ robot, location }, null, 2)
        }]
      };
    });

    // Actuator tools
    this.server.tool("order_robot", {
      robotId: z.string(),
      task: z.string(),
      targetId: z.string().optional()
    }, async ({ robotId, task, targetId }) => {
      this.graph.updateNode<RobotNode>(robotId, {
        task,
        status: 'working'
      });
      if (targetId) {
        this.graph.addEdge(robotId, targetId, 'assigned_to', { task });
      }
      return {
        content: [{ type: "text", text: `Robot ${robotId} assigned to ${task}` }]
      };
    });

    this.server.tool("move_robot", {
      robotId: z.string(),
      roomId: z.string()
    }, async ({ robotId, roomId }) => {
      this.graph.moveEntity(robotId, roomId);
      return {
        content: [{ type: "text", text: `Robot ${robotId} moved to ${roomId}` }]
      };
    });
  }
}
```

---

## Alternative: Using Graphology

If you want richer in-memory graph operations, you can use [Graphology](https://graphology.github.io/) as a cache layer:

```typescript
import Graph from 'graphology';

export class GraphologyCache {
  private graph = new Graph();

  constructor(private sql: SqlStorage) {}

  // Load full graph from SQLite into memory
  async load(): Promise<void> {
    const nodes = this.sql.exec('SELECT * FROM nodes').toArray();
    const edges = this.sql.exec('SELECT * FROM edges').toArray();

    for (const node of nodes) {
      this.graph.addNode(node.id as string, {
        type: node.type,
        ...JSON.parse(node.data as string)
      });
    }

    for (const edge of edges) {
      this.graph.addEdge(edge.source as string, edge.target as string, {
        type: edge.type,
        ...JSON.parse(edge.data as string)
      });
    }
  }

  // Sync changes back to SQLite
  async persist(): Promise<void> {
    // Use transactions for atomicity
    this.sql.exec('BEGIN TRANSACTION');
    try {
      this.sql.exec('DELETE FROM edges');
      this.sql.exec('DELETE FROM nodes');

      this.graph.forEachNode((id, attrs) => {
        const { type, ...data } = attrs;
        this.sql.exec(
          'INSERT INTO nodes (id, type, data) VALUES (?, ?, ?)',
          id, type, JSON.stringify(data)
        );
      });

      this.graph.forEachEdge((id, attrs, source, target) => {
        const { type, ...data } = attrs;
        this.sql.exec(
          'INSERT INTO edges (id, source, target, type, data) VALUES (?, ?, ?, ?, ?)',
          id, source, target, type, JSON.stringify(data)
        );
      });

      this.sql.exec('COMMIT');
    } catch (e) {
      this.sql.exec('ROLLBACK');
      throw e;
    }
  }

  // Use Graphology's rich API
  findNeighbors(nodeId: string): string[] {
    return this.graph.neighbors(nodeId);
  }

  // ... more Graphology operations
}
```

**Trade-off:** More expressive queries vs. sync complexity. For Shipshape's graph size (hundreds of nodes), the SQLite-native approach is simpler and sufficient.

---

## Simulation Loop

The game simulation runs via Durable Object Alarms:

```typescript
export class ShipshapeDO extends DurableObject {
  graph!: GraphService;

  async alarm() {
    const now = Date.now();

    // Tick all robots
    const robots = this.graph.getNodesByType<RobotNode>('robot');
    for (const robot of robots) {
      this.tickRobot(robot, now);
    }

    // Tick cat
    const catInfo = this.graph.getCatLocation();
    if (catInfo) {
      this.tickCat(catInfo.cat, catInfo.room, now);
    }

    // Tick systems
    const systems = this.graph.getNodesByType<SystemNode>('system');
    for (const system of systems) {
      this.tickSystem(system, now);
    }

    // Schedule next tick (e.g., every 5 seconds game time)
    this.ctx.storage.setAlarm(now + 5000);
  }

  private tickRobot(robot: RobotNode, now: number) {
    // Drain power, check needs, execute task, etc.
    const newPower = Math.max(0, robot.data.power - 0.1);
    this.graph.updateNode(robot.id, { power: newPower });

    if (newPower < 10 && robot.data.status !== 'charging') {
      // Robot needs to find charging station
      this.graph.updateNode(robot.id, { status: 'charging', task: undefined });
    }
  }

  private tickCat(cat: CatNode, room: RoomNode, now: number) {
    // Update hunger, warmth based on room conditions
    const newHunger = Math.max(0, cat.data.hunger - 0.05);
    const warmthDelta = room.data.temperature > 290 ? 0.01 : -0.02;
    this.graph.updateNode(cat.id, {
      hunger: newHunger,
      warmth: Math.max(0, Math.min(100, cat.data.warmth + warmthDelta))
    });
  }

  private tickSystem(system: SystemNode, now: number) {
    // Check power requirements, degrade health, etc.
  }
}
```

---

## Summary

| Aspect | Recommendation |
|--------|----------------|
| **Storage** | SQLite in Durable Objects |
| **Query Layer** | Custom TypeScript `GraphService` class |
| **Traversal** | Recursive CTEs for paths, simple JOINs for neighbors |
| **Types** | Discriminated unions for node types |
| **Simulation** | DO Alarms for game ticks |
| **MCP Integration** | Tools call `GraphService` methods |

This gives you type safety, persistence, and enough graph functionality for a game without external dependencies.
