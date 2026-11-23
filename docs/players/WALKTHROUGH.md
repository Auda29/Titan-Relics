# Titan Relics Gameplay Walkthrough & Item Reference

> **Spoiler notice:** This guide explains every gameplay mechanic, structure reward, crafting recipe, and exclusive item in Titan Relics (`1.0.0-beta.5`, V6 interiors). For a spoiler-light introduction, read the [short player guide](PLAYER_GUIDE.md).
>
> **Website edition:** [English Guide](https://auda29.github.io/Titan-Relics/guide-en.html) · [Deutscher Guide](https://auda29.github.io/Titan-Relics/guide.html)

---

## Testing in Creative mode: Survival is required

If you are testing Titan Relics in a Creative test world, switch to **Survival** (`/gamemode survival`) or **Adventure** before interacting with gameplay mechanics. The following systems **intentionally ignore Creative and Spectator players**:

- **Great Colossus Trial Spawner:** will not detect you or spawn the guardian Iron Golem (`NO_CREATIVE_PLAYERS`).
- **Great Colossus Vault:** stays inactive, hides its preview item, and will not accept a Colossus Key.
- **Personal reward drops** (Colossus Key & Machine Core): can only be picked up by their eligible owner in Survival/Adventure.
- **Salvage Magnet:** will not attract dropped items while in Creative or Spectator.
- **World Tree Aura:** does not grant Regeneration II or Resistance II in Creative or Spectator.
- **Expedition Map compensation:** right-clicking an unavailable map to redeem emeralds requires Survival/Adventure.

Brushing Suspicious Sand and opening ordinary chests work normally, which can make the rest of the mod appear unresponsive in Creative if you are not aware of this rule.

---

## Progression at a glance

1. **Find an Obelisk** in the Overworld and bring a **Brush**.
2. **Brush the 8 Suspicious Sand blocks** around its ruins to recover an **Expedition Map** and a **Monolith Armor Trim Smithing Template**.
3. **Follow the Expedition Map** to your world's unique **Great Colossus**.
4. **Loot the arm chest** for a guaranteed full **Salvage Magnet** (or find a broken one with a 10% chance in a **Small Colossus**).
5. **Climb into the upper hatch** of the Great Colossus in **Survival**, trigger the **Trial Spawner**, and defeat the **guardian Iron Golem** to earn a personal **Colossus Key**.
6. **Unlock the Vault** beside the spawner in **Survival** with your **Colossus Key** to claim a **Machine Core**.

---

## Suspicious blocks & archaeology

Suspicious blocks in Titan Relics generate **exclusively around Obelisks**.

- Every Obelisk contains **8 Suspicious Sand blocks** placed in the surrounding archaeological remains (all 8 are `minecraft:suspicious_sand`).
- **Use a Brush** — breaking a Suspicious Sand block destroys its find permanently.
- Finds are **shared and finite** per Obelisk: once brushed or broken, they never refill on reload or for later players.

### Guaranteed & ordinary finds per Obelisk

| Slot | Count per Obelisk | Reward |
| --- | --- | --- |
| Expedition Map | **1 guaranteed** | **Expedition Map — Colossus** pointing to the world's unique Great Colossus (or **3 Emeralds** directly if the planner confirmed no valid Colossus site exists in the world) |
| Armor Trim | **1 guaranteed** | **Monolith Armor Trim Smithing Template** |
| Ordinary finds | **6 blocks** | Rolled per block: **25%** Pottery Sherd (equal chance of Angler, Archer, Arms Up, or Blade), **20%** Clay Ball, **15%** Brick, **10%** Bone, **10%** String, **10%** Wheat Seeds, **5%** Iron Nugget, **5%** Copper Ingot |

---

## How the Great Colossus Trial & Vault work

Each supported Overworld has **one unique Great Colossus**. Every Expedition Map in that world points to the same site.

### Entering the chamber
- The Great Colossus's encounter room is located high inside the upper structure, entered through the **upper hatch** (bring blocks, ladders, scaffolding, or water to climb up).
- Inside are the **Trial Spawner** and the **Vault**.

### Step 1: The Trial Spawner → Colossus Key
- **Mode requirement:** Survival or Adventure (Creative/Spectator players are ignored).
- **Ominous mode:** disabled — Bad Omen / Trial Omen will not convert this spawner into an Ominous Trial.
- **Activation:** walk within **14 blocks** with line of sight to the Trial Spawner. After a **2-second (40-tick) wind-up**, it spawns **1 persistent guardian Iron Golem**.
- **Multiplayer participation:** any eligible Survival/Adventure player within 14 blocks when the encounter starts — or who enters within 14 blocks while the Golem is alive — is recorded as a participant.
- **Reward:** when the guardian Iron Golem is defeated, **every recorded participant** receives **1 personal Colossus Key** dropped from the spawner (invulnerable, never despawns, owner-only Survival pickup).
- **Cooldown & abort:** after defeat (or if the Golem is destroyed by non-combat removal), the spawner enters a **30-minute (36,000-tick) cooldown**. Non-combat removal grants no keys.

### Step 2: The Vault → Machine Core
- **Mode requirement:** Survival or Adventure.
- **Key requirement:** right-click the Vault holding a **Colossus Key** (vanilla Trial Keys do not work). Colossus Keys are transferable between players.
- **Limit:** **once per player** per Great Colossus, permanently tracked in the world ledger.
- **Reward:** right-clicking immediately consumes 1 Colossus Key, plays a ~2.7-second unlock animation, and ejects **1 full Machine Core (`256 / 256`)** as a personal drop.

---

## Every exclusive item

### 1. Expedition Map — Colossus
- **How to obtain:** 1 guaranteed in Suspicious Sand around every **Obelisk**.
- **How it works:** A scale-2 exploration map marked with an `X` pointing to the world's unique Great Colossus. Can be copied and shared using standard Minecraft map duplication.
- **Map states:**
  - *Resolved:* points directly to the Great Colossus.
  - *Unconfirmed (Pending):* the background site search is still running; the map updates automatically once a destination is confirmed.
  - *Destination Unavailable:* if the world's biomes/border have no valid Colossus site, right-click the map in **Survival/Adventure** with free inventory space to redeem **3 Emeralds** once for that map origin.

### 2. Monolith Armor Trim Smithing Template
- **How to obtain:** 1 guaranteed in Suspicious Sand around every **Obelisk**.
- **Use:** Apply the **Monolith Armor Trim** pattern to any trimmable armor piece at a **Smithing Table** with any standard trim material.
- **Duplication recipe (Crafting Table → yields 2 Templates):**

```text
[ Diamond ] [ Monolith Template ] [ Diamond ]
[ Diamond ] [   Copper Block    ] [ Diamond ]
[ Diamond ] [      Diamond      ] [ Diamond ]
```

### 3. Colossus Key
- **How to obtain:** Trigger the **Great Colossus Trial Spawner** in **Survival/Adventure** and defeat the guardian Iron Golem.
- **Use:** Right-click the **Vault** inside the Great Colossus in **Survival/Adventure** to claim a **Machine Core**. Keys can be traded or given to other players.

### 4. Machine Core
- **How to obtain:** Unlock the **Great Colossus Vault** with a **Colossus Key** in **Survival/Adventure** (once per player).
- **Use:** Place in the **fuel slot** of a **Furnace**, **Blast Furnace**, or **Smoker**.
  - Keeps the appliance's normal smelting speed.
  - Holds **256 completed operations** (1 charge spent per smelted item; idle time never drains charge).
  - If ordinary fuel is already burning, it finishes first before the Core takes over.
  - Automation friendly: hoppers can insert charged Cores (`> 0`) and extract depleted Cores (`0 / 256`) from below.
  - Never disappears when empty — it stays intact as a depleted item (`0 / 256`).
- **Recharge recipe (Crafting Table — requires a *fully depleted* Core at `0 / 256`):**
  Unlocks in the Recipe Book automatically once you hold a Machine Core.

```text
[    (empty)    ] [ Amethyst Shard ] [    (empty)    ]
[  Coal Block   ] [  Empty Core    ] [  Coal Block   ]
[    (empty)    ] [    (empty)     ] [    (empty)    ]
```

*(Uses 1 Amethyst Shard + 2 Coal Blocks → returns a fully charged `256 / 256` Machine Core.)*

### 5. Salvage Magnet
- **How to obtain:**
  - **Guaranteed (full, `1,000 / 1,000`):** in the chest inside the detached arm of the **Great Colossus** (`colossus_arm_magnet_chest`).
  - **10% chance (broken, `0 / 1,000` — needs repair):** in the chest of a **Small Colossus**.
- **Use:** Hold a working magnet (`> 0`) in your **selected main hand or offhand** while in **Survival/Adventure** (it stays inactive in regular inventory slots).
  - Pulls dropped items within **8 blocks** when there is a clear line of sight (solid blocks, glass, and closed doors/trapdoors block attraction) and space in your inventory.
  - Respects item pickup ownership.
  - **1,000-item budget:** counts individual items collected, not stacks. Stays intact as a broken item at `0 / 1,000`.
- **Repair recipe (Crafting Table — works on any worn or broken Magnet from `0` to `999 / 1,000`):**
  Unlocks in the Recipe Book automatically once you hold a Salvage Magnet.

```text
[   (empty)   ] [ Amethyst Shard ] [   (empty)   ]
[ Iron Ingot  ] [ Salvage Magnet ] [ Iron Ingot  ]
[ Iron Ingot  ] [    (empty)     ] [ Iron Ingot  ]
```

*(Uses 1 Amethyst Shard + 4 Iron Ingots → restores full `1,000 / 1,000` budget.)*

---

## All landmarks & rewards

| Landmark | Gameplay & Loot |
| --- | --- |
| **Obelisk** | **8 Suspicious Sand blocks**: 1× Expedition Map (guaranteed), 1× Monolith Armor Trim Template (guaranteed), 6× ordinary archaeology finds. |
| **Great Colossus** *(unique per world)* | **Arm chest:** 24–40 Copper Ingots, 8–16 Iron Ingots, 0–4 Redstone Dust, 0–2 Amethyst Shards, **1× full Salvage Magnet (guaranteed)**.<br>**Upper chamber:** Trial Spawner (guardian Iron Golem → personal **Colossus Key**) & Vault (Colossus Key → personal **Machine Core**). |
| **Small Colossus** | **1 chest:** 12–20 Copper Ingots, 4–8 Iron Ingots, 0–2 Redstone Dust, 0–1 Amethyst Shard, and a **10% chance** for a **broken Salvage Magnet** (`0 / 1,000`). |
| **Ruined Tower** | **5 one-time Endermen** (skipped on Peaceful).<br>**Lower chest:** 95% chance of 4–6 Ender Pearls, 5% chance of 1 Eye of Ender.<br>**Upper platform chest (Beta 4 / V6 worlds):** 1× **Feather Falling IV** Enchanted Book, 3–6 Diamonds, 8–16 Iron Ingots. |
| **World Tree** | **Sanctuary aura (Survival/Adventure):** grants **Regeneration II** and **Resistance II** within an **80-block radius** (through walls) with a **5-minute linger** after leaving.<br>**Wildlife:** within 64 blocks horizontally (±8 vertically), natural Pig/Chicken/Sheep/Cow spawns can receive up to 1 extra normal spawn attempt under vanilla habitat and mob caps.<br>Contains a decorative amethyst core; no chests. |
| **Titan Skull (Crowned)** & **Sword Skull** | Atmospheric Overworld landmarks with **no chests, archaeology, or scripted encounters**. |

---

## Generation presets, existing worlds & 1.21.1 notes

- **World creation presets** (**Create World → World → Relic generation**):
  - **Discoveries** *(default)*: 2,000-block search spacing, 800-block min relic distance, 4,000-block min Great Colossus distance.
  - **Balanced**: 3,000-block spacing, 1,200-block min relic distance, 8,000-block min Great Colossus distance.
  - **Expedition**: 5,000-block spacing, 2,000-block min relic distance, 15,000-block min Great Colossus distance.
  - All presets use *Matching landscapes* (including classified modpack biomes). Distances are lower bounds; terrain and biome checks can push valid sites farther away.
- **Existing worlds:** each world freezes its generation settings and interior revision when created (even for unexplored chunks). Updating does not retrogen structures, add the Beta 4 upper tower chest to older worlds, or refill shared chests/archaeology.
- **Minecraft 1.21.1 builds:** use ordinary Chests in place of Waxed Copper Chests and Ferns where newer 26.2+ blocks are unavailable. All gameplay mechanics, drops, and recipes are otherwise identical.
- **Need setup help or hit a bug?** See the [installation & reporting guide](INSTALLATION.md).
