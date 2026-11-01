package de.relics.distribution;

import java.util.*;
import static de.relics.distribution.DistributionPlanner.Family;

/** Pure biome routing. No names/temperature guesses and no family or palette rerolls. */
public record BiomeRules(Map<String,Rule> families) {
    public enum Mode { STANDARD, LANDSCAPES, CUSTOM }
    public record Rule(Mode mode,Set<String> selected) {
        public Rule {
            Objects.requireNonNull(mode);selected=Collections.unmodifiableSet(new TreeSet<>(selected));
            if(selected.size()>10000 || selected.stream().anyMatch(s->!s.matches("[a-z0-9_.-]+:[a-z0-9_./-]+")))throw new IllegalArgumentException("Invalid biome ID");
        }
    }
    public static final BiomeRules STANDARD=new BiomeRules(Map.of());
    public BiomeRules {
        var copy=new TreeMap<String,Rule>();families.forEach((key,value)->{
            if(Arrays.stream(Family.values()).noneMatch(f->f!=Family.EMPTY && f.id.equals(key)))throw new IllegalArgumentException("Unknown biome family");
            copy.put(key,Objects.requireNonNull(value));
        });families=Collections.unmodifiableMap(copy);
    }
    public Rule rule(Family family){return families.getOrDefault(family.id,new Rule(Mode.STANDARD,Set.of()));}
    public BiomeRules with(Family family,Rule rule){var values=new TreeMap<>(families);values.put(family.id,rule);return new BiomeRules(values);}
    public static Set<String> groups(String id,Set<String> tags) {
        var groups=new HashSet<String>();
        for(String group:List.of("desert","forest","open","dry","rocky")) {
            List<String> names=switch(group){
                case "desert"->List.of("desert","badlands");case "open"->List.of("plains","meadow");
                case "dry"->List.of("savanna","dry");case "rocky"->List.of("mountain","stony_shores");default->List.of("forest");};
            for(String name:names)if(tags.contains("minecraft:is_"+name) || tags.contains("c:is_"+name) || tags.contains("forge:is_"+name))groups.add(group);
        }
        if(Set.of("minecraft:desert","minecraft:badlands","minecraft:wooded_badlands","minecraft:eroded_badlands","terralith:desert_spires","terralith:desert_canyon","terralith:gravel_desert","biomesoplenty:wasteland").contains(id))groups.add("desert");
        if(Set.of("minecraft:plains","minecraft:sunflower_plains","minecraft:meadow","terralith:blooming_valley","terralith:blooming_plateau","biomesoplenty:prairie").contains(id))groups.add("open");
        if(Set.of("minecraft:savanna","minecraft:savanna_plateau","terralith:steppe","biomesoplenty:scrubland","biomesoplenty:dryland").contains(id))groups.add("dry");
        if(Set.of("minecraft:stony_shore","minecraft:stony_peaks","minecraft:windswept_hills","minecraft:windswept_gravelly_hills","terralith:rocky_mountains").contains(id))groups.add("rocky");
        return Set.copyOf(groups);
    }
    public String profile(Family family,String biome,Set<String> tags,List<String> standard) {
        Rule rule=rule(family);Set<String> groups=groups(biome,tags);
        if(rule.mode==Mode.STANDARD)return standardProfile(standard);
        if(rule.mode==Mode.CUSTOM && !rule.selected.contains(biome))return null;
        if(rule.mode==Mode.LANDSCAPES && standard.isEmpty()) {
            Set<String> allowed=switch(family){case OBELISK->Set.of("desert");case COLOSSUS,SKULL_2->Set.of("open","dry");
                case SKULL->Set.of("open","dry","desert","rocky");case TREE->Set.of("open","forest");
                case SMALL,TOWER->Set.of("open","forest","dry");default->Set.of();};
            if(Collections.disjoint(allowed,groups))return null;
        }
        String preferred=standardProfile(standard);if(preferred!=null)return preferred;
        if(family==Family.SKULL)return groups.contains("desert")?"titan_skull_sand":groups.contains("dry")?"titan_skull_dry":groups.contains("rocky")?"titan_skull_rock":"titan_skull";
        return family.id;
    }
    private static String standardProfile(List<String> profiles) {
        if(profiles.size()>1)throw new IllegalStateException("Ambiguous relic palette biome tags");
        return profiles.isEmpty()?null:profiles.getFirst();
    }
}
