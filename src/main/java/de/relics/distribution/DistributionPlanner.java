package de.relics.distribution;

import java.util.*;
import java.util.function.Supplier;

/** Pure, versioned planner. No chunks, clocks, entities, loot rolls or global random state. */
public final class DistributionPlanner {
    public static final int CELL = 5000, MARGIN = 256, SEPARATION = 2000, REGION = 6000,
            OBELISK_SEPARATION = 15000, UNIQUE_MIN = 30000;
    public static final String LEGACY_POLICY = "relics-distribution-v1";
    public static final String POLICY = "relics-distribution-v2-local64-r3072";
    public enum Family {
        COLOSSUS("colossus"), OBELISK("obelisk"), SKULL("titan_skull"), SKULL_2("titan_skull_2"),
        TOWER("ruined_tower"), SMALL("small_colossus"), TREE("world_tree"), EMPTY("");
        public final String id;
        Family(String id) { this.id = id; }
    }
    public record Cell(int x, int z) { }
    public record Candidate(Cell cell, int x, int z, int ticket, long priority, int rotation, boolean unique) {
        public int chunkX() { return Math.floorDiv(x, 16); }
        public int chunkZ() { return Math.floorDiv(z, 16); }
    }
    /** Doubled centers preserve half-block parity. Origins are the actual transformed template origin. */
    public record Site(Candidate candidate, String asset, int x2, int z2, int surface,
                       int originX, int originY, int originZ, int minX, int minZ, int maxX, int maxZ) {
        public int x() { return Math.floorDiv(x2, 2); }
        public int z() { return Math.floorDiv(z2, 2); }
    }
    @FunctionalInterface public interface Validator { Site validate(Candidate candidate, Family family); }
    public static final class Pending extends RuntimeException {
        public Pending() { super("Unique relic destination is still pending", null, false, false); }
    }
    private record Key(Cell cell, Family family) { }
    private final long seed;
    private final Set<Family> enabled;
    private final Validator validator;
    private final Supplier<Site> unique;
    private final Supplier<Boolean> unavailable;
    private final int bootstrapX, bootstrapZ, bootstrapUncertainty;
    private final String policy;
    private final DistributionSettings settings;
    private final Map<Cell,List<Candidate>> locations = bounded(2048);
    private final Map<Cell,Optional<Site>> choices = bounded(2048);
    private final Map<Key, Optional<Site>> terrain = bounded(4096);
    private final Map<Cell, Optional<Site>> obelisks = bounded(2048);
    public volatile long opportunities, terrainChecks, terrainRejected, spacingRejected, acceptedQueries;
    public volatile long locationAttempts;

    public DistributionPlanner(long seed, Set<Family> enabled, Validator validator, Supplier<Site> unique,
            Supplier<Boolean> unavailable, int bootstrapX, int bootstrapZ, int bootstrapUncertainty) {
        this(LEGACY_POLICY,seed,enabled,validator,unique,unavailable,bootstrapX,bootstrapZ,bootstrapUncertainty);
    }
    public DistributionPlanner(String policy,long seed, Set<Family> enabled, Validator validator, Supplier<Site> unique,
            Supplier<Boolean> unavailable, int bootstrapX, int bootstrapZ, int bootstrapUncertainty) {
        this(policy,DistributionSettings.EXPEDITION,seed,enabled,validator,unique,unavailable,bootstrapX,bootstrapZ,bootstrapUncertainty);
    }
    public DistributionPlanner(String policy,DistributionSettings settings,long seed,Set<Family> enabled,Validator validator,
            Supplier<Site> unique,Supplier<Boolean> unavailable,int bootstrapX,int bootstrapZ,int bootstrapUncertainty) {
        if(!Set.of(POLICY,LEGACY_POLICY,DistributionSettings.POLICY).contains(policy))throw new IllegalArgumentException("Unsupported distribution policy: "+policy);
        this.settings=Objects.requireNonNull(settings);
        if(!policy.equals(DistributionSettings.POLICY) && !settings.equals(DistributionSettings.EXPEDITION))
            throw new IllegalArgumentException("Historical policies require historical settings");
        this.policy=policy;
        this.seed = seed; this.enabled = Set.copyOf(enabled); this.validator = validator;
        this.unique = unique; this.unavailable = unavailable;
        this.bootstrapX = bootstrapX; this.bootstrapZ = bootstrapZ; this.bootstrapUncertainty = bootstrapUncertainty;
    }
    public List<Candidate> candidateLocations(Cell cell) {
        return locations.computeIfAbsent(cell,key->{var anchor=ordinaryCandidate(key);
            return policy.equals(LEGACY_POLICY)?List.of(anchor):LocationSearch.positions(seed,anchor,settings.cellSize());});
    }
    public int cellSize(){return settings.cellSize();}
    public Candidate ordinaryCandidate(Cell cell){return candidate(seed,cell,false,settings.cellSize());}
    public boolean mayMatch(int ticket,Set<Family> requested){return settings.mayMatch(ticket,requested);}
    private boolean isObelisk(Candidate c){return settings.ticket(c.ticket,false)==Family.OBELISK;}
    private boolean alwaysEmpty(Candidate c){return settings.ticket(c.ticket,false)==Family.EMPTY && settings.ticket(c.ticket,true)==Family.EMPTY;}
    private Family selected(int ticket,boolean inside){return settings.ticket(ticket,inside);}
    private static <K,V> Map<K,V> bounded(int limit) {
        return new LinkedHashMap<>(64, .75f, true) {
            @Override protected boolean removeEldestEntry(Map.Entry<K,V> entry) { return size() > limit; }
        };
    }
    /** SplitMix64 finalizer; signed cell coordinates are packed as two two's-complement int32s. */
    public static long mix(long value) {
        value = (value ^ (value >>> 30)) * 0xbf58476d1ce4e5b9L;
        value = (value ^ (value >>> 27)) * 0x94d049bb133111ebL;
        return value ^ (value >>> 31);
    }
    public static long stream(long seed, Cell cell, long domain) {
        return mix(seed ^ mix(((long)cell.x << 32) ^ Integer.toUnsignedLong(cell.z)) ^ domain);
    }
    public static Candidate candidate(long seed, Cell cell, boolean unique) {
        return candidate(seed,cell,unique,CELL);
    }
    public static Candidate candidate(long seed,Cell cell,boolean unique,int cellSize) {
        long domain = unique ? 0x51f2c45ae730b91dL : 0xa7b096e354d12c8fL;
        int x = position(seed,cell,domain,cell.x,cellSize), z = position(seed,cell,domain ^ 1,cell.z,cellSize);
        return new Candidate(cell, x, z, (int)Long.remainderUnsigned(stream(seed, cell, domain ^ 2), 10000),
                stream(seed, cell, domain ^ 3), (int)(stream(seed, cell, domain ^ 4) & 3), unique);
    }
    private static int position(long seed,Cell cell,long domain,int axis,int cellSize) {
        long origin=(long)axis*cellSize;
        long first=-Math.floorDiv(-(origin+MARGIN-8),16), last=Math.floorDiv(origin+cellSize-MARGIN-8,16);
        return Math.toIntExact((first+Long.remainderUnsigned(stream(seed,cell,domain),last-first+1))*16+8);
    }
    public static Family ticket(int u, boolean inside) {
        if (u < 0 || u >= 10000) throw new IllegalArgumentException("Ticket outside 0..9999");
        if (u < 3000) return Family.OBELISK;
        if (inside) {
            if (u < 4500) return Family.SKULL;
            if (u < 6000) return Family.SKULL_2;
        } else {
            if (u < 3250) return Family.SKULL;
            if (u < 3500) return Family.SKULL_2;
            if (u < 6000) return Family.EMPTY;
        }
        if (u < 6200) return Family.TOWER;
        if (u < 6400) return Family.SMALL;
        if (u < 6600) return Family.TREE;
        return Family.EMPTY;
    }
    public static int priority(Candidate a, Candidate b) {
        int c = Long.compareUnsigned(a.priority, b.priority);
        if (c == 0) c = Integer.compare(a.cell.x, b.cell.x);
        return c == 0 ? Integer.compare(a.cell.z, b.cell.z) : c;
    }
    public static boolean within(Site a, Site b, int distance, boolean inclusive) {
        long x = (long)a.x2 - b.x2, z = (long)a.z2 - b.z2, limit = 4L * distance * distance;
        return inclusive ? x*x + z*z <= limit : x*x + z*z < limit;
    }
    private boolean clearLarge(Site site) {
        Site large = unique.get();
        if (large != null) return !within(site, large, settings.minDistance(), false);
        if (unavailable.get()) return true;
        // During vanilla's spawn search, every possible final spawn is within the
        // captured uncertainty. A site strictly inside this disk cannot conflict
        // with ANY future large destination. Everything else stays pending.
        long dx = (long)site.x2 - 2L * bootstrapX, dz = (long)site.z2 - 2L * bootstrapZ;
        long safe = 2L * (settings.colossusMinDistance() - settings.minDistance() - bootstrapUncertainty);
        if (dx*dx + dz*dz < safe*safe) return true;
        throw new Pending();
    }
    private Site rawTerrain(Candidate c, Family family) {
        if (!enabled.contains(family) || family == Family.EMPTY) return null;
        Key key = new Key(c.cell, family);
        Optional<Site> cached = terrain.get(key);
        if (cached == null) {
            terrainChecks++;
            Site site = null;
            for(Candidate location:candidateLocations(c.cell)) {
                locationAttempts++;
                site=validator.validate(location,family);
                if(site!=null)break;
            }
            if (site == null) terrainRejected++;
            cached = Optional.ofNullable(site); terrain.put(key, cached);
        }
        return cached.orElse(null);
    }
    private Site raw(Candidate c,Family family) {
        Site site=rawTerrain(c,family);
        return site != null && clearLarge(site) ? site : null;
    }
    private List<Candidate> neighbors(Site center, int radius) {
        List<Candidate> result = new ArrayList<>();
        int padding = radius + 2 + (policy.equals(LEGACY_POLICY)?0:LocationSearch.RADIUS);
        for (int x = Math.floorDiv(center.x() - padding, settings.cellSize()); x <= Math.floorDiv(center.x() + padding, settings.cellSize()); x++)
            for (int z = Math.floorDiv(center.z() - padding, settings.cellSize()); z <= Math.floorDiv(center.z() + padding, settings.cellSize()); z++) {
                Candidate c = ordinaryCandidate(new Cell(x,z));
                long dx = (long)c.x - center.x(), dz = (long)c.z - center.z();
                if (dx*dx + dz*dz <= (long)padding*padding) result.add(c);
            }
        return result;
    }
    private Site obelisk(Candidate c) {
        if (!isObelisk(c)) return null;
        Optional<Site> cached = obelisks.get(c.cell);
        if (cached != null) return cached.orElse(null);
        Site site = raw(c, Family.OBELISK);
        if (site != null) for (Candidate neighbor : neighbors(site, settings.obeliskDistance())) {
            if (!isObelisk(neighbor) || priority(neighbor,c) >= 0) continue;
            Site other = policy.equals(LEGACY_POLICY)?raw(neighbor,Family.OBELISK):rawTerrain(neighbor,Family.OBELISK);
            if (other != null && within(site,other,settings.obeliskDistance(),false)
                    && (policy.equals(LEGACY_POLICY) || clearLarge(other))) {
                spacingRejected++; site = null; break;
            }
        }
        // Never cache a pending decision: raw() throws before reaching this point.
        obelisks.put(c.cell, Optional.ofNullable(site));
        return site;
    }
    private Site eligible(Candidate c) {
        if (isObelisk(c) || alwaysEmpty(c)) return null;
        if(!policy.equals(LEGACY_POLICY))return eligibleLocal(c);
        // A nominal zero-size site is used only to enumerate the complete halo.
        Site nominal = new Site(c,"",2*c.x,2*c.z,0,0,0,0,0,0,0,0);
        boolean inside = false;
        List<Site> anchors = new ArrayList<>();
        for (Candidate neighbor : neighbors(nominal, settings.regionRadius() + 2 + (policy.equals(LEGACY_POLICY)?0:LocationSearch.RADIUS))) {
            Site anchor = obelisk(neighbor);
            if (anchor != null) { anchors.add(anchor); if (within(nominal,anchor,settings.regionRadius()+2,true)) inside = true; }
        }
        // Terrain and palette can change the center by half a block. Classify on
        // the exact transformed center, revalidating the selected family once.
        Family family = selected(c.ticket, inside);
        Site site = raw(c, family);
        if (site == null) return null;
        boolean exactInside = false;
        for (Site anchor : anchors) {
            if (within(site,anchor,settings.minDistance(),false)) return null;
            if (within(site,anchor,settings.regionRadius(),true)) exactInside = true;
        }
        if (selected(c.ticket,exactInside) != family) {
            if(!policy.equals(LEGACY_POLICY))return null; // A moved site cannot obtain a different family ticket.
            site = raw(c,selected(c.ticket,exactInside));
        }
        return site;
    }
    private List<Site> anchorsAt(Site center,int radius) {
        List<Site> result=new ArrayList<>();
        for(Candidate neighbor:neighbors(center,radius)) {
            if(!isObelisk(neighbor))continue;
            Site terrain=rawTerrain(neighbor,Family.OBELISK);
            // Only relevant, physically nearby candidates may require the
            // unique-site decision. Irrelevant halo cells never block spawn.
            if(terrain==null || !within(center,terrain,radius,true))continue;
            Site anchor=obelisk(neighbor);if(anchor!=null)result.add(anchor);
        }
        return result;
    }
    /** First terrain fit for the original fixed family, before final spacing.
     * The chunk gate uses this to avoid planning an unrelated distant site
     * while vanilla is still selecting the initial spawn. */
    public Site candidateChoice(Cell cell) {
        if(policy.equals(LEGACY_POLICY))throw new IllegalStateException("Legacy policy has no location search");
        Optional<Site> cached=choices.get(cell);if(cached!=null)return cached.orElse(null);
        Candidate c=ordinaryCandidate(cell);Family family;
        if(isObelisk(c))family=Family.OBELISK;
        else if(alwaysEmpty(c))family=Family.EMPTY;
        else {
            Site nominal=new Site(c,"",2*c.x,2*c.z,0,0,0,0,0,0,0,0);
            family=selected(c.ticket,!anchorsAt(nominal,settings.regionRadius()).isEmpty());
        }
        Site chosen=rawTerrain(c,family);choices.put(cell,Optional.ofNullable(chosen));return chosen;
    }
    private static Family familyOf(Site site) {
        String id=site.asset;
        if(id.startsWith("titan_skull_") && !id.equals("titan_skull_2"))return Family.SKULL;
        return Arrays.stream(Family.values()).filter(f->f.id.equals(id)).findFirst().orElseThrow();
    }
    private Site eligibleLocal(Candidate c) {
        Site site=candidateChoice(c.cell);if(site==null || !clearLarge(site))return null;
        boolean inside=false;
        for(Site anchor:anchorsAt(site,settings.regionRadius())) {
            if(within(site,anchor,settings.minDistance(),false))return null;
            inside=true;
        }
        // Keep the original family even if relocation crosses a region edge.
        // Such an opportunity stays empty rather than obtaining another ticket.
        return selected(c.ticket,inside)==familyOf(site)?site:null;
    }
    public Site plan(Cell cell) {
        opportunities++;
        Candidate c = ordinaryCandidate(cell);
        Site site = isObelisk(c) ? obelisk(c) : eligible(c);
        if (site == null) return null;
        if (!isObelisk(c)) for (Candidate neighbor : neighbors(site, settings.minDistance())) {
            if (priority(neighbor,c) >= 0) continue;
            if(!policy.equals(LEGACY_POLICY)) {
                if(isObelisk(neighbor) || alwaysEmpty(neighbor))continue;
                Site possible=candidateChoice(neighbor.cell);
                if(possible==null || !within(site,possible,settings.minDistance(),false))continue;
            }
            Site other = eligible(neighbor);
            if (other != null && within(site,other,settings.minDistance(),false)) { spacingRejected++; return null; }
        }
        acceptedQueries++; return site;
    }
    public static double distance(Candidate c, int x, int z) { return Math.hypot((double)c.x-x,(double)c.z-z); }
    /** Enumerate only annulus-intersecting rows, never the entire interior square. */
    public static List<Candidate> annulus(long seed, int spawnX, int spawnZ, int lower, int upper,
            int minX, int minZ, int maxX, int maxZ) {
        List<Candidate> result = new ArrayList<>();
        int firstX = Math.floorDiv(Math.max(minX, spawnX-upper), CELL), lastX = Math.floorDiv(Math.min(maxX,spawnX+upper), CELL);
        for (int x = firstX; x <= lastX; x++) {
            long left = (long)x*CELL-spawnX, right = left+CELL;
            double nearX = left <= 0 && right >= 0 ? 0 : Math.min(Math.abs(left),Math.abs(right));
            if (nearX >= upper) continue;
            int outerZ = (int)Math.ceil(Math.sqrt((double)upper*upper-nearX*nearX));
            double farX = Math.max(Math.abs(left),Math.abs(right));
            int innerZ = farX >= lower ? 0 : (int)Math.floor(Math.sqrt((double)lower*lower-farX*farX));
            int firstZ = Math.floorDiv(Math.max(minZ,spawnZ-outerZ),CELL), lastZ = Math.floorDiv(Math.min(maxZ,spawnZ+outerZ),CELL);
            for (int z=firstZ; z<=lastZ; z++) {
                if ((long)z*CELL-spawnZ > -innerZ && (long)(z+1)*CELL-spawnZ < innerZ) continue;
                Candidate c = candidate(seed,new Cell(x,z),true);
                double d=distance(c,spawnX,spawnZ);
                if (d>=lower && d<upper && c.x>=minX && c.x<=maxX && c.z>=minZ && c.z<=maxZ) result.add(c);
            }
        }
        result.sort(DistributionPlanner::priority); return List.copyOf(result);
    }
}
