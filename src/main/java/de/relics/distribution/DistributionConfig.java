package de.relics.distribution;

import com.google.gson.*;
import java.nio.ByteBuffer;
import java.nio.channels.FileChannel;
import java.nio.charset.StandardCharsets;
import java.nio.file.*;
import java.util.Set;

/** Installation defaults only. Existing worlds read their saved settings, never this file. */
public final class DistributionConfig {
    private static final Gson JSON=new GsonBuilder().setPrettyPrinting().create();
    private static Path directory=Path.of("config");
    private DistributionConfig() { }
    public static void directory(Path path){directory=path;}
    public static Path file(){return directory.resolve("relics-distribution.json");}
    public static DistributionSettings load(){return read(file());}
    public static final String WORLD_FILE="data/relics_creation_settings.json";
    public static DistributionSettings forNewWorld(Path root){Path path=root.resolve(WORLD_FILE);return Files.exists(path)?read(path):load();}
    public static DistributionSettings read(Path path) {
        if(!Files.exists(path))return DistributionSettings.DISCOVERY;
        try {
            JsonObject root=JsonParser.parseString(Files.readString(path)).getAsJsonObject();
            if(!root.keySet().equals(Set.of("format","settings")) || integer(root.get("format"))!=1)
                throw new IllegalArgumentException("Unsupported settings file format");
            JsonObject value=root.getAsJsonObject("settings");
            var fields=new java.util.HashSet<>(value.keySet());fields.remove("biomes");fields.remove("colossusMinDistance");fields.remove("generationRevision");
            if(!fields.equals(Set.of("cellSize","minDistance","obeliskDistance","regionRadius","outside","inside")))
                throw new IllegalArgumentException("Unknown or missing settings");
            for(String field:java.util.List.of("cellSize","minDistance","obeliskDistance","regionRadius"))integer(value.get(field));
            if(value.has("colossusMinDistance"))integer(value.get("colossusMinDistance"));
            if(value.has("generationRevision"))integer(value.get("generationRevision"));
            for(String field:java.util.List.of("outside","inside"))for(JsonElement entry:value.getAsJsonArray(field))integer(entry);
            if(value.has("biomes")) {
                var biome=value.getAsJsonObject("biomes");if(!biome.keySet().equals(Set.of("families")))throw new IllegalArgumentException("Unknown biome settings");
                for(var entry:biome.getAsJsonObject("families").entrySet())if(!entry.getValue().getAsJsonObject().keySet().equals(Set.of("mode","selected")))throw new IllegalArgumentException("Unknown biome rule");
            }
            return JSON.fromJson(value,DistributionSettings.class);
        }catch(Exception error){throw new IllegalStateException("Cannot read relic distribution settings: "+path,error);}
    }
    private static int integer(JsonElement value) {
        if(!value.isJsonPrimitive() || !value.getAsJsonPrimitive().isNumber())throw new IllegalArgumentException("Expected integer");
        return value.getAsBigDecimal().intValueExact();
    }
    public static void save(DistributionSettings settings){write(file(),settings);}
    public static void write(Path path,DistributionSettings settings) {
        java.util.Objects.requireNonNull(settings);
        try {
            Files.createDirectories(path.toAbsolutePath().getParent());
            if(Files.exists(path))Files.copy(path,path.resolveSibling(path.getFileName()+".bak"),StandardCopyOption.REPLACE_EXISTING);
            JsonObject root=new JsonObject();root.addProperty("format",1);root.add("settings",JSON.toJsonTree(settings));
            Path temp=Files.createTempFile(path.toAbsolutePath().getParent(),"relics-settings-",".pending");
            try {
                try(var channel=FileChannel.open(temp,StandardOpenOption.WRITE)) {
                    var bytes=ByteBuffer.wrap((JSON.toJson(root)+"\n").getBytes(StandardCharsets.UTF_8));
                    while(bytes.hasRemaining())channel.write(bytes);channel.force(true);
                }
                Files.move(temp,path.toAbsolutePath(),StandardCopyOption.REPLACE_EXISTING,StandardCopyOption.ATOMIC_MOVE);
            }finally{Files.deleteIfExists(temp);}
        }catch(Exception error){throw new IllegalStateException("Cannot save relic distribution settings: "+path,error);}
    }
}
