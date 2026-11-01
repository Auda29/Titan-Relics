package de.relics.client;

import de.relics.distribution.*;
import net.minecraft.core.RegistryAccess;
import net.minecraft.core.registries.Registries;
import java.util.*;
import static de.relics.distribution.DistributionPlanner.Family;

/** Snapshot of the selected datapacks' real registry, never a guessed list. */
public record ClientBiomeCatalog(List<Entry> entries) {
    public record Entry(String id,Set<String> tags,Map<String,List<String>> standard) {
        public boolean allowed(BiomeRules rules,Family family){return rules.profile(family,id,tags,standard.getOrDefault(family.id,List.of()))!=null;}
    }
    public static ClientBiomeCatalog from(RegistryAccess access) {
        var biomes=access.lookupOrThrow(Registries.BIOME);
        var entries=new ArrayList<Entry>();
        biomes.listElements().forEach(b->{
            String id=b.unwrapKey().orElseThrow().identifier().toString();Set<String> tags=new TreeSet<>();b.tags().forEach(t->tags.add(t.location().toString()));
            Map<String,List<String>> standard=new TreeMap<>();
            tags.stream().filter(t->t.startsWith("relics:has_structure/")).forEach(t->{
                String profile=t.substring("relics:has_structure/".length());String family=profile.startsWith("titan_skull_") && !profile.equals("titan_skull_2")?"titan_skull":profile;
                standard.computeIfAbsent(family,k->new ArrayList<>()).add(profile);
            });entries.add(new Entry(id,Set.copyOf(tags),standard));
        });entries.sort(Comparator.comparing(Entry::id));return new ClientBiomeCatalog(List.copyOf(entries));
    }
}
