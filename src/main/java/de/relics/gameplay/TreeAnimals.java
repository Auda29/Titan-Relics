package de.relics.gameplay;

import de.relics.mixin.*;
import net.minecraft.core.BlockPos;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.world.entity.*;
import net.minecraft.world.level.NaturalSpawner;
import net.minecraft.world.level.chunk.ChunkAccess;

/** One extra ordinary candidate after a successful selected natural creature spawn. */
public final class TreeAnimals {
    public static final int RADIUS=64,HEIGHT=8;
    private record Context(NaturalSpawner.SpawnState state,NaturalSpawner.SpawnPredicate predicate,NaturalSpawner.AfterSpawnCallback after) { }
    private static final ThreadLocal<Context> CONTEXT=new ThreadLocal<>();
    private TreeAnimals() { }
    public static boolean selected(EntityType<?> type) {
        return type==EntityTypes.PIG || type==EntityTypes.CHICKEN || type==EntityTypes.SHEEP || type==EntityTypes.COW;
    }
    public static boolean contains(GameplayLedger.Point anchor,double x,double y,double z) {
        double dx=x-anchor.x()-.5,dz=z-anchor.z()-.5;
        return dx*dx+dz*dz<=RADIUS*RADIUS && Math.abs(y-anchor.y()-.5)<=HEIGHT;
    }
    public static void withContext(NaturalSpawner.SpawnState state,NaturalSpawner.SpawnPredicate predicate,
            NaturalSpawner.AfterSpawnCallback after,Runnable ordinary) {
        var previous=CONTEXT.get();CONTEXT.set(new Context(state,predicate,after));
        try{ordinary.run();}finally{if(previous==null)CONTEXT.remove();else CONTEXT.set(previous);}
    }
    public static boolean afterNaturalSpawn(ServerLevel level,Mob source,ChunkAccess chunk) {
        var context=CONTEXT.get();
        if(context==null || !selected(source.getType()) || !RelicGameplay.treeHabitat(level,source.blockPosition()))return false;
        var caps=(TreeAnimalCapAccess)(Object)context.state();
        if(!caps.relics$global(MobCategory.CREATURE) || !caps.relics$local(MobCategory.CREATURE,chunk.getPos()))return false;
        var random=level.getRandom();var pos=source.blockPosition().mutable();
        pos.move(random.nextInt(6)-random.nextInt(6),0,random.nextInt(6)-random.nextInt(6));
        // Never load a neighbour or let a pack walk outside the registered habitat.
        if((pos.getX()>>4)!=chunk.getPos().x() || (pos.getZ()>>4)!=chunk.getPos().z()
                || level.getChunkSource().getChunkNow(pos.getX()>>4,pos.getZ()>>4)!=chunk
                || !RelicGameplay.treeHabitat(level,pos))return false;
        var player=level.getNearestPlayer(pos.getX()+.5,pos.getY(),pos.getZ()+.5,-1,false);
        if(player==null)return false;
        double distance=player.distanceToSqr(pos.getX()+.5,pos.getY(),pos.getZ()+.5);
        if(!TreeAnimalSpawnerAccess.relics$distance(level,chunk,pos,distance))return false;
        var structures=level.structureManager();var generator=level.getChunkSource().getGenerator();
        var choice=TreeAnimalSpawnerAccess.relics$selection(level,structures,generator,MobCategory.CREATURE,random,pos);
        if(choice.isEmpty() || !selected(choice.get().type()))return false;
        var data=choice.get();
        if(!TreeAnimalSpawnerAccess.relics$type(level,MobCategory.CREATURE,structures,generator,data,pos,distance)
                || !context.predicate().test(data.type(),pos,chunk))return false;
        Mob mob=TreeAnimalSpawnerAccess.relics$mob(level,data.type());if(mob==null)return false;
        mob.snapTo(pos.getX()+.5,pos.getY(),pos.getZ()+.5,random.nextFloat()*360,0);
        if(!TreeAnimalSpawnerAccess.relics$position(level,mob,distance))return false;
        mob.finalizeSpawn(level,level.getCurrentDifficultyAt(pos),EntitySpawnReason.NATURAL,null);
        level.addFreshEntityWithPassengers(mob);
        if(level.getEntity(mob.getUUID())!=mob)return false;
        context.after().run(mob,chunk);return true; // Same population and biome-energy bookkeeping.
    }
}
