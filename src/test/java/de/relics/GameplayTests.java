package de.relics;

import com.google.gson.JsonParser;
import com.mojang.serialization.JsonOps;
import de.relics.gameplay.*;
import net.minecraft.SharedConstants;
import net.minecraft.core.RegistryAccess;
import net.minecraft.core.component.DataComponents;
import net.minecraft.core.registries.BuiltInRegistries;
import net.minecraft.resources.RegistryOps;
import net.minecraft.server.Bootstrap;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.item.Items;
import net.minecraft.world.item.crafting.CraftingInput;
import net.minecraft.world.item.crafting.CraftingRecipe;
import net.minecraft.world.item.crafting.Recipe;
import net.minecraft.network.chat.Component;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.*;
import static de.relics.gameplay.GameplayLedger.*;

/** No server/world: real 26.2 item/recipe codecs and the production ledger transitions. */
public final class GameplayTests {
    private static int assertions;
    private static void check(boolean valid, String message) {
        assertions++; if (!valid) throw new AssertionError(message);
    }
    private static void rejected(Runnable action, String message) {
        boolean failed = false; try { action.run(); } catch (RuntimeException expected) { failed = true; }
        check(failed, message);
    }
    private static ItemStack stack(net.minecraft.world.item.Item item) { return new ItemStack(item); }
    private static CraftingInput coreInput(ItemStack core, net.minecraft.world.item.Item fuel) {
        return CraftingInput.of(3, 3, List.of(ItemStack.EMPTY, stack(Items.AMETHYST_SHARD), ItemStack.EMPTY,
                stack(fuel), core, stack(fuel), ItemStack.EMPTY, ItemStack.EMPTY, ItemStack.EMPTY));
    }
    private static CraftingInput magnetInput(ItemStack magnet) {
        return CraftingInput.of(3, 3, List.of(ItemStack.EMPTY, stack(Items.AMETHYST_SHARD), ItemStack.EMPTY,
                stack(Items.IRON_INGOT), magnet, stack(Items.IRON_INGOT), stack(Items.IRON_INGOT), ItemStack.EMPTY, stack(Items.IRON_INGOT)));
    }
    private static void itemsAndRecipes(Path resources) throws Exception {
        // Simulate the pre-freeze registration window for these unit tests only.
        // This does NOT load Fabric/mixins, start MinecraftServer or claim runtime evidence.
        SharedConstants.tryDetectVersion();
        var bootstrapped = Bootstrap.class.getDeclaredField("isBootstrapped"); bootstrapped.setAccessible(true); bootstrapped.setBoolean(null, true);
        var create = BuiltInRegistries.class.getDeclaredMethod("createContents"); create.setAccessible(true); create.invoke(null);
        check(RelicItems.MACHINE_CORE != Items.COAL, "Original registered core item");
        MaintenanceRecipe.initialize();
        // Register the production map-origin component, without registering runtime callbacks.
        check(RelicItems.MAP_ORIGIN != null, "Persistent map-origin component registered");
        BuiltInRegistries.REGISTRY.freeze();
        for (var registry : BuiltInRegistries.REGISTRY) ((net.minecraft.core.MappedRegistry<?>)registry).bindAllTagsToEmpty();
        ((net.minecraft.core.MappedRegistry<net.minecraft.world.item.Item>)BuiltInRegistries.ITEM).bindTags(Map.of(
                net.minecraft.tags.ItemTags.TRIMMABLE_ARMOR, List.of(Items.LEATHER_HELMET.builtInRegistryHolder(), Items.LEATHER_CHESTPLATE.builtInRegistryHolder(),
                        Items.LEATHER_LEGGINGS.builtInRegistryHolder(), Items.LEATHER_BOOTS.builtInRegistryHolder()),
                net.minecraft.tags.ItemTags.TRIM_MATERIALS, List.of(Items.AMETHYST_SHARD.builtInRegistryHolder(), Items.IRON_INGOT.builtInRegistryHolder())));
        for (var registry : BuiltInRegistries.REGISTRY) registry.freeze();
        var trimMaterials = new net.minecraft.core.MappedRegistry<>(net.minecraft.core.registries.Registries.TRIM_MATERIAL,
                com.mojang.serialization.Lifecycle.stable());
        for (String name : List.of("amethyst", "iron", "diamond", "copper")) {
            try (var input = GameplayTests.class.getResourceAsStream("/data/minecraft/trim_material/" + name + ".json")) {
                var material = net.minecraft.world.item.equipment.trim.TrimMaterial.DIRECT_CODEC.parse(JsonOps.INSTANCE,
                        JsonParser.parseString(new String(input.readAllBytes(),java.nio.charset.StandardCharsets.UTF_8))).getOrThrow();
                net.minecraft.core.Registry.register(trimMaterials, net.minecraft.resources.Identifier.parse("minecraft:" + name), material);
            }
        }
        var registries = new ArrayList<net.minecraft.core.Registry<?>>();
        RegistryAccess.fromRegistryOfRegistries(BuiltInRegistries.REGISTRY).registries().forEach(entry -> registries.add(entry.value()));
        registries.add(trimMaterials.freeze());
        var patterns = new net.minecraft.core.MappedRegistry<>(net.minecraft.core.registries.Registries.TRIM_PATTERN,
                com.mojang.serialization.Lifecycle.stable());
        var monolith = net.minecraft.world.item.equipment.trim.TrimPattern.DIRECT_CODEC.parse(JsonOps.INSTANCE,
                JsonParser.parseString(Files.readString(resources.resolve("data/relics/trim_pattern/monolith.json")))).getOrThrow();
        net.minecraft.core.Registry.register(patterns,RelicItems.id("monolith"),monolith);
        registries.add(patterns.freeze());
        var access = new RegistryAccess.ImmutableRegistryAccess(registries).freeze();
        // Only these actual item initializers need no dynamic damage/enchantment tags.
        // This intentionally is not a full datapack load or a Fabric resource test.
        var selected = new net.minecraft.core.component.DataComponentInitializers();
        var entriesField = net.minecraft.core.component.DataComponentInitializers.class.getDeclaredField("initializers");
        entriesField.setAccessible(true);
        Set<String> needed = Set.of("minecraft:air", "minecraft:coal", "minecraft:charcoal", "minecraft:coal_block",
                "minecraft:amethyst_shard", "minecraft:iron_ingot", "minecraft:diamond", "minecraft:copper_block", "minecraft:stick", "minecraft:filled_map", "minecraft:map",
                "minecraft:leather_helmet", "minecraft:leather_chestplate", "minecraft:leather_leggings", "minecraft:leather_boots");
        for (Object entry : (List<?>)entriesField.get(BuiltInRegistries.DATA_COMPONENT_INITIALIZERS)) {
            var keyMethod = entry.getClass().getDeclaredMethod("key"); keyMethod.setAccessible(true);
            var initializerMethod = entry.getClass().getDeclaredMethod("initializer"); initializerMethod.setAccessible(true);
            var key = (net.minecraft.resources.ResourceKey<?>)keyMethod.invoke(entry);
            if (key.identifier().getNamespace().equals("relics") || needed.contains(key.identifier().toString()))
                addInitializer(selected, key, initializerMethod.invoke(entry));
        }
        selected.build(access)
                .forEach(net.minecraft.core.component.DataComponentInitializers.PendingComponents::apply);
        var ops = RegistryOps.create(JsonOps.INSTANCE, access);

        for (boolean core : List.of(true, false)) {
            int capacity = core ? RelicItems.CORE_CAPACITY : RelicItems.MAGNET_CAPACITY;
            ItemStack item = stack(core ? RelicItems.MACHINE_CORE : RelicItems.SALVAGE_MAGNET);
            check(item.getMaxStackSize() == 1, "Core/magnet unstackable");
            check(RelicItems.remaining(item, core) == capacity, "Starts full");
            check(!item.getItem().isBarVisible(item), "No inventory status bar");
            for (int left : List.of(capacity, capacity - 1, 1, 0)) {
                RelicItems.setRemaining(item, core, left);
                var encoded = ItemStack.CODEC.encodeStart(ops, item).getOrThrow();
                ItemStack roundtrip = ItemStack.CODEC.parse(ops, encoded).getOrThrow();
                check(RelicItems.remaining(roundtrip, core) == left, "Item charge survives actual stack codec");
                String base = core ? "machine_core" : "salvage_magnet";
                String suffix = left == capacity ? "" : left == 0 ? "_empty" : "_partial";
                check(roundtrip.get(DataComponents.ITEM_MODEL).equals(RelicItems.id(base + suffix)), "Exact icon threshold");
            }
            check(item.getCount() == 1, "Depleted item survives");
            rejected(() -> RelicItems.setRemaining(item, core, -1), "Negative budget rejected");
            rejected(() -> RelicItems.setRemaining(item, core, capacity + 1), "Overflow budget rejected");
            var codec = ItemBudget.codec(capacity);
            for (String bad : List.of("{\"version\":2,\"remaining\":0}", "{\"version\":1,\"remaining\":-1}",
                    "{\"version\":1,\"remaining\":" + (capacity+1) + "}", "{}"))
                check(codec.parse(JsonOps.INSTANCE, JsonParser.parseString(bad)).error().isPresent(), "Bad component fails closed");
        }
        ItemStack core = stack(RelicItems.MACHINE_CORE); RelicItems.setRemaining(core, true, 0);
        core.set(DataComponents.CUSTOM_NAME, Component.literal("Kept name"));
        var recharge = new MaintenanceRecipe(true);
        check(!recharge.isSpecial() && recharge.showNotification(),"Core recipe is visible in the crafting book");
        check(!recharge.placementInfo().isImpossibleToPlace() && recharge.placementInfo().slotsToIngredientIndex().size()==6,"Core book placement retains the normalized 3x2 shape");
        var coreDisplay=(net.minecraft.world.item.crafting.display.ShapedCraftingRecipeDisplay)recharge.display().getFirst();
        check(coreDisplay.width()==3 && coreDisplay.height()==2,"Core book sends shaped display");
        var depletedDisplay=(net.minecraft.world.item.crafting.display.SlotDisplay.ItemStackSlotDisplay)coreDisplay.ingredients().get(4);
        check(RelicItems.remaining(depletedDisplay.stack().create(),true)==0,"Book explicitly shows depleted core input");
        var encodedDisplay=net.minecraft.world.item.crafting.display.RecipeDisplay.CODEC.encodeStart(ops,coreDisplay).getOrThrow();
        check(net.minecraft.world.item.crafting.display.RecipeDisplay.CODEC.parse(ops,encodedDisplay).getOrThrow() instanceof net.minecraft.world.item.crafting.display.ShapedCraftingRecipeDisplay,"Book display round-trips native codec");
        check(recharge.matches(coreInput(core, Items.COAL_BLOCK), null), "Approved core shape matches normalized 3x3");
        ItemStack charged = recharge.assemble(coreInput(core, Items.COAL_BLOCK));
        check(charged.getCount() == 1 && RelicItems.remaining(charged, true) == 256, "Recharge one full existing core");
        check(charged.get(DataComponents.CUSTOM_NAME).equals(core.get(DataComponents.CUSTOM_NAME)), "Metadata preserved");
        check(RelicItems.remaining(core, true) == 0, "Preview never mutates source");
        check(recharge.getRemainingItems(coreInput(core, Items.COAL_BLOCK)).stream().allMatch(ItemStack::isEmpty), "No duplicate input remainder");
        check(!recharge.matches(coreInput(charged, Items.COAL_BLOCK), null), "Full core rejected");
        check(!recharge.matches(coreInput(core, Items.COAL), null) && !recharge.matches(coreInput(core, Items.CHARCOAL), null), "Alternate fuels rejected");
        ItemStack missing = core.copy(); missing.remove(RelicItems.CORE_CHARGE);
        check(!recharge.matches(coreInput(missing, Items.COAL_BLOCK), null), "Missing component does not mint charge");
        ItemStack stacked = core.copyWithCount(2);
        check(!recharge.matches(coreInput(stacked, Items.COAL_BLOCK), null), "Invalid stacked relic rejected");
        var extra = new ArrayList<>(List.of(ItemStack.EMPTY,stack(Items.AMETHYST_SHARD),ItemStack.EMPTY,
                stack(Items.COAL_BLOCK),core,stack(Items.COAL_BLOCK),ItemStack.EMPTY,stack(Items.STICK),ItemStack.EMPTY));
        check(!recharge.matches(CraftingInput.of(3,3,extra), null), "Extra occupied bottom cell rejected");
        check(!recharge.matches(CraftingInput.of(2,2,List.of(core,stack(Items.COAL_BLOCK),stack(Items.AMETHYST_SHARD),ItemStack.EMPTY)),null), "2x2 grid rejected");
        var repair = new MaintenanceRecipe(false); ItemStack magnet = stack(RelicItems.SALVAGE_MAGNET);
        check(!repair.isSpecial() && repair.display().size()==1 && repair.placementInfo().slotsToIngredientIndex().size()==9,"Magnet repair is also visible and placeable");
        check(!repair.matches(magnetInput(magnet), null), "Full magnet rejected");
        for (int left : List.of(999, 1, 0)) {
            RelicItems.setRemaining(magnet, false, left);
            check(repair.matches(magnetInput(magnet), null), "Damaged and broken magnets accepted");
            ItemStack repaired = repair.assemble(magnetInput(magnet));
            check(RelicItems.remaining(repaired, false) == 1000 && repaired.getCount() == 1, "One repaired existing magnet");
            check(repair.getRemainingItems(magnetInput(magnet)).stream().allMatch(ItemStack::isEmpty), "No magnet remainder");
        }
        for (String id : List.of("machine_core_recharge", "salvage_magnet_repair", "monolith_template_copy")) {
            Recipe<?> recipe = Recipe.CODEC.parse(ops, JsonParser.parseString(Files.readString(resources.resolve("data/relics/recipe/" + id + ".json")))).getOrThrow();
            check(recipe != null, "Actual 26.2 recipe resource decodes: " + id);
            if (id.equals("monolith_template_copy")) {
                var input = CraftingInput.of(3,3,List.of(stack(Items.DIAMOND),stack(RelicItems.MONOLITH_TEMPLATE),stack(Items.DIAMOND),
                        stack(Items.DIAMOND),stack(BuiltInRegistries.ITEM.getValue(net.minecraft.resources.Identifier.parse("minecraft:copper_block"))),
                        stack(Items.DIAMOND),stack(Items.DIAMOND),stack(Items.DIAMOND),stack(Items.DIAMOND)));
                var copy = (CraftingRecipe)recipe;
                check(copy.matches(input,null) && copy.assemble(input).getCount() == 2, "Monolith copy uses seven diamonds/copper, outputs two");
                check(copy.getRemainingItems(input).stream().allMatch(ItemStack::isEmpty), "No third template via remainder");
            }
        }
        for (String id : List.of("trial_key", "vault_core")) {
            var table = net.minecraft.world.level.storage.loot.LootTable.DIRECT_CODEC.parse(ops,
                    JsonParser.parseString(Files.readString(resources.resolve("data/relics/loot_table/gameplay/" + id + ".json")))).getOrThrow();
            check(table != null, "Fixed reward table decodes with actual 26.2 loot codec");
        }
        ItemStack pending = stack(Items.FILLED_MAP); pending.set(RelicItems.MAP_ORIGIN, "origin-test");
        check(!pending.has(DataComponents.MAP_ID), "Pending map invents no coordinates/map ID");
        CraftingRecipe cloning;
        try (var input = GameplayTests.class.getResourceAsStream("/data/minecraft/recipe/map_cloning.json")) {
            cloning = (CraftingRecipe)Recipe.CODEC.parse(ops, JsonParser.parseString(new String(input.readAllBytes(),java.nio.charset.StandardCharsets.UTF_8))).getOrThrow();
        }
        var mapInput = CraftingInput.of(3,1,List.of(pending,stack(Items.MAP),stack(Items.MAP)));
        check(cloning.matches(mapInput,null), "Native 26.2 map-cloning recipe accepts pending map");
        ItemStack copied = cloning.assemble(mapInput);
        check("origin-test".equals(copied.get(RelicItems.MAP_ORIGIN)) && copied.getCount() == 3, "26.2 transmute map copying preserves origin");
        check(!copied.has(DataComponents.MAP_ID), "Pending copies invent no target");
        for (int coordinate : List.of(-2000000,-577,-576,-65,-64,-1,0,511,512,2000000,30000000)) {
            var target = new Point("minecraft:overworld",coordinate,70,-coordinate);
            var nativeMap = net.minecraft.world.level.saveddata.maps.MapItemSavedData.createFresh(coordinate,-coordinate,(byte)2,true,true,net.minecraft.world.level.Level.OVERWORLD);
            check(ExpeditionMaps.matches(nativeMap,target), "Stored map-center check agrees with actual 26.2 at signed boundaries");
            check(!ExpeditionMaps.matches(nativeMap,new Point("minecraft:the_nether",coordinate,70,-coordinate)), "Wrong-dimension saved map cannot hijack origin");
        }
        pending.set(DataComponents.MAP_ID,new net.minecraft.world.level.saveddata.maps.MapId(42));
        copied = cloning.assemble(mapInput);
        check(copied.get(DataComponents.MAP_ID).id()==42 && "origin-test".equals(copied.get(RelicItems.MAP_ORIGIN)), "Resolved copies share map ID and origin");
        var smithing = (net.minecraft.world.item.crafting.SmithingTrimRecipe)Recipe.CODEC.parse(ops,
                JsonParser.parseString(Files.readString(resources.resolve("data/relics/recipe/monolith_armor_trim.json")))).getOrThrow();
        for (var armor : List.of(Items.LEATHER_HELMET,Items.LEATHER_CHESTPLATE,Items.LEATHER_LEGGINGS,Items.LEATHER_BOOTS)) {
            ItemStack base = stack(armor); base.set(DataComponents.CUSTOM_NAME,Component.literal("Kept armor"));
            var smithingInput = new net.minecraft.world.item.crafting.SmithingRecipeInput(stack(RelicItems.MONOLITH_TEMPLATE),base,stack(Items.AMETHYST_SHARD));
            check(smithing.matches(smithingInput,null), "Actual Monolith smithing recipe accepts fixture-tagged armor");
            ItemStack trimmed = smithing.assemble(smithingInput);
            check(trimmed.get(DataComponents.TRIM).pattern().value().assetId().equals(RelicItems.id("monolith")), "Original trim pattern applied");
            trimmed.remove(DataComponents.TRIM);
            check(ItemStack.isSameItemSameComponents(base,trimmed), "Cosmetic only: armor attributes/components/metadata unchanged");
        }
        UUID a = new UUID(0,1), b = new UUID(0,2);
        check(SalvageMagnet.nearer(4,a,9,b) && !SalvageMagnet.nearer(9,a,4,b), "Nearest magnet wins");
        check(SalvageMagnet.nearer(4,a,4,b) && !SalvageMagnet.nearer(4,b,4,a), "Stable UUID tie break");
    }
    private static Site site(GameplayLedger journal, String id) {
        Site site = new Site(); site.id = id; site.fixture = true;
        site.spawner = new Point("minecraft:overworld",0,0,0); site.golemSpawn = new Point("minecraft:overworld",0,1,0);
        site.vault = new Point("minecraft:overworld",0,2,0); journal.state.sites.put(id, site); return site;
    }
    @SuppressWarnings({"unchecked", "rawtypes"})
    private static void addInitializer(net.minecraft.core.component.DataComponentInitializers selected,
            net.minecraft.resources.ResourceKey key, Object initializer) {
        selected.add(key, (net.minecraft.core.component.DataComponentInitializers.Initializer)initializer);
    }
    private static void ledgerTests(Path temporary) throws Exception {
        Path file = temporary.resolve("ledger.json"); GameplayLedger journal = new GameplayLedger(file);
        Site site = site(journal, "fixture:one"); String player = UUID.randomUUID().toString();
        Delivery delivery = journal.reserveVault(site, player);
        check(delivery.reward == Reward.CORE && delivery.phase == DeliveryPhase.QUEUED, "Vault reserves guaranteed core");
        check(journal.reserveVault(site, player) == null, "Repeat/concurrent claim rejected before delivery");
        for (int i=0;i<512;i++) check(journal.reserveVault(site,UUID.randomUUID().toString()) != null, "Vault UUID claims exceed native history limit");
        journal.flush(); journal = new GameplayLedger(file);
        check(journal.state.vaultClaims.size() == 513, "All lifetime claims survive atomic reload");
        check(journal.reserveVault(journal.state.sites.get(site.id), player) == null, "Oldest claim not evicted on reload");
        delivery = journal.state.deliveries.get(delivery.id);
        check(!journal.reconcile(delivery,Set.of()) && delivery.phase == DeliveryPhase.QUEUED, "Offline/full inventory queue survives");
        delivery.phase = DeliveryPhase.IN_FLIGHT; journal.flush(); journal = new GameplayLedger(file); delivery = journal.state.deliveries.get(delivery.id);
        check(journal.reconcile(delivery,Set.of()) && delivery.phase == DeliveryPhase.AMBIGUOUS, "Crash before player receipt: hold, never duplicate");
        check(journal.reconcile(delivery,Set.of(delivery.id)) && delivery.phase == DeliveryPhase.DELIVERED, "Crash after receipt: acknowledge existing grant");
        check(!journal.reconcile(delivery,Set.of(delivery.id)), "Repeated receipt reconciliation is idempotent");
        check(journal.reconcile(delivery,Set.of()) && delivery.phase == DeliveryPhase.AMBIGUOUS, "Acknowledged journal with rolled-back/missing player receipt also holds");

        site = journal.state.sites.get(site.id); site.golem = UUID.randomUUID().toString(); site.encounter = UUID.randomUUID().toString();
        site.phase = TrialPhase.ENTITY_UNKNOWN; site.participants.add(player); String second = UUID.randomUUID().toString(); site.participants.add(second);
        check(!journal.completeEncounter(site,UUID.randomUUID().toString(),site.encounter,true,100), "Unrelated golem cannot complete trial");
        check(journal.completeEncounter(site,site.golem,site.encounter,true,100), "Confirmed tracked death resolves unknown encounter");
        check(site.rewardAnimationUntil==180,"Trial reward keeps a saved shutter animation window");
        check(journal.state.deliveries.values().stream().filter(d->d.reward==GameplayLedger.Reward.KEY).allMatch(d->d.notBefore==160),"Keys wait for spawner reward presentation");
        check(site.phase == TrialPhase.COOLDOWN && site.cooldown == 36100, "Saved-time 36000-tick cooldown");
        check(journal.state.terminalGolems.contains(site.golem), "Confirmed terminal UUID tombstone prevents stale saved resurrection");
        check(journal.state.deliveries.containsKey("trial:"+site.encounter+":"+player) && journal.state.deliveries.containsKey("trial:"+site.encounter+":"+second), "One key each including late participant");
        int count = journal.state.deliveries.size();
        check(!journal.completeEncounter(site,site.golem,site.encounter,true,101) && journal.state.deliveries.size() == count, "Duplicate death callback grants nothing");
        site.golem = UUID.randomUUID().toString(); site.encounter = UUID.randomUUID().toString(); site.phase = TrialPhase.ACTIVE; site.participants.add(player);
        check(journal.completeEncounter(site,site.golem,site.encounter,false,500) && journal.state.deliveries.size()==count, "Confirmed nondefeat abort has no keys");

        Origin origin = new Origin(); origin.id = "original"; journal.state.origins.put(origin.id,origin);
        check(!journal.resolveOrigin(origin) && origin.target == null, "Pending has no candidate coordinates");
        journal.state.targetUnavailable = true;
        Delivery compensation = journal.reserveCompensation(origin,player);
        check(compensation.reward == Reward.EMERALDS && origin.phase == OriginPhase.COMPENSATED, "One original compensation reservation");
        check(journal.reserveCompensation(origin,second) == null, "Copies cannot reserve extra compensation");
        journal.state.targetUnavailable = false; journal.state.committedTarget = new Point("minecraft:overworld",2000000,70,-2000000);
        check(!journal.resolveOrigin(origin), "Re-enabling never revives compensated copies");
        Origin resolved = new Origin(); resolved.id = "other"; journal.state.origins.put(resolved.id,resolved);
        check(journal.resolveOrigin(resolved) && resolved.target.equals(journal.state.committedTarget), "Distant committed target remains valid");
        journal.state.targetUnavailable = true;
        check(journal.reserveCompensation(resolved,player) == null && resolved.phase == OriginPhase.MAP_RESOLVED, "Deactivation cannot compensate an already resolved map");
        journal.state.trees.put("fixture:tree",new Point("minecraft:overworld",-33,70,-33)); journal.flush(); journal = new GameplayLedger(file);
        check(journal.state.trees.size()==1 && journal.state.origins.size()==2, "Tree anchors/map origins survive reload independent of blocks");
        check(journal.state.sites.get(site.id).rewardAnimationUntil==180 && journal.state.deliveries.values().stream()
                .filter(d->d.reward==Reward.KEY).allMatch(d->d.notBefore==160),"Reward timeline survives ledger reload");
        Point anchor = journal.state.trees.get("fixture:tree");
        check(TreeAura.contains(anchor,-32.5,70.5,-32.5), "Block-center anchor and negative coordinates");
        check(TreeAura.contains(anchor,-8.5,70.5,-32.5) && !TreeAura.contains(anchor,-8.499,70.5,-32.5), "Inclusive 24-block sphere boundary");
        check(!TreeAura.contains(anchor,-9,94,-32.5), "Sphere is not an infinite cylinder or box");
        rejected(() -> new Point("bad dimension",0,0,0), "Invalid dimension fails anchor decoding");
        rejected(() -> new Point("minecraft:overworld",Integer.MIN_VALUE,0,0), "Out-of-world signed-coordinate overflow rejected");
        Delivery drop=journal.queue("physical-test",player,Reward.KEY,site.id);
        drop.phase=DeliveryPhase.DROP_RESERVED;drop.dropUuid=UUID.randomUUID().toString();drop.dropPoint=site.spawner;
        check(!journal.reconcile(drop,Set.of()),"Uncertain dispatch is not silently reissued");
        drop.phase=DeliveryPhase.DROPPED;journal.flush();journal=new GameplayLedger(file);
        drop=journal.state.deliveries.get("physical-test");
        check(drop.dropUuid!=null && drop.dropPoint!=null && drop.phase==DeliveryPhase.DROPPED,"Uncollected physical reward survives ledger reload");
        check(!journal.reconcile(drop,Set.of()) && drop.phase==DeliveryPhase.DROPPED,"Uncollected world entity is not mistaken for missing inventory receipt");
        check(journal.reconcile(drop,Set.of(drop.id)) && drop.phase==DeliveryPhase.DELIVERED,"Saved pickup receipt completes physical reward");
        Delivery paid=journal.queue("paid-before-ejection",player,Reward.CORE,site.id);paid.keyPaid=true;journal.flush();
        journal=new GameplayLedger(file);paid=journal.state.deliveries.get("paid-before-ejection");
        check(paid.keyPaid && paid.phase==DeliveryPhase.QUEUED,"Consumed key remains paid while the core is still queued");
        check(!journal.reconcile(paid,Set.of()) && paid.phase==DeliveryPhase.QUEUED,"A paid key does not falsely complete core pickup");
        Files.writeString(file,Files.readString(file).replace("fixture:tree","fixture:corruption"));
        rejected(() -> new GameplayLedger(file), "Tampered ledger fails closed rather than refilling rewards");
    }
    public static void main(String[] args) throws Exception {
        itemsAndRecipes(Path.of(args[0])); ledgerTests(Path.of(args[1]));
        GameplayMixinTargets.verify(Path.of(args[0]));
        System.out.println("PASS: " + assertions + " headless gameplay assertions (no Fabric/mixin/server runtime)");
    }
}
