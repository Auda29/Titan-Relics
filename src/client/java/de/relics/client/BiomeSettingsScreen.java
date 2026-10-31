package de.relics.client;

import de.relics.distribution.*;
import static de.relics.distribution.DistributionPlanner.Family;
import net.minecraft.client.gui.GuiGraphicsExtractor;
import net.minecraft.client.gui.components.*;
import net.minecraft.client.gui.screens.Screen;
import net.minecraft.network.chat.Component;
import java.util.*;
import java.util.function.Consumer;

/** Searchable registry-backed selection; all changes remain a cancellable draft. */
public final class BiomeSettingsScreen extends Screen {
    private final Screen parent;private final ClientBiomeCatalog catalog;private final Consumer<BiomeRules> accept;private final boolean readOnly;
    private BiomeRules rules;private int family,page;private String query="";
    private static final Family[] FAMILIES=Arrays.stream(Family.values()).filter(f->f!=Family.EMPTY).toArray(Family[]::new);
    public BiomeSettingsScreen(Screen parent,ClientBiomeCatalog catalog,BiomeRules rules,Consumer<BiomeRules> accept,boolean readOnly){
        super(text("biomes"));this.parent=parent;this.catalog=catalog;this.rules=rules;this.accept=accept;this.readOnly=readOnly;
    }
    private static Component text(String key){return Component.translatable("relics.settings."+key);}
    private Family current(){return FAMILIES[family];}
    private List<ClientBiomeCatalog.Entry> filtered(){return catalog==null?List.of():catalog.entries().stream().filter(e->e.id().contains(query.toLowerCase(Locale.ROOT)) || ClientModNames.name(e.id().split(":")[0]).toLowerCase(Locale.ROOT).contains(query.toLowerCase(Locale.ROOT))).toList();}
    private Button button(Component label,int x,int y,int w,Runnable action){return addRenderableWidget(Button.builder(label,b->action.run()).bounds(x,y,w,20).build());}
    @Override protected void init(){
        int w=Math.min(560,width-16),x=(width-w)/2;
        button(Component.literal("<"),x,32,30,()->{family=(family+6)%7;page=0;rebuildWidgets();});
        button(text("family."+current().id),x+34,32,w-68,()->{}).active=false;
        button(Component.literal(">"),x+w-30,32,30,()->{family=(family+1)%7;page=0;rebuildWidgets();});
        int third=(w-8)/3;
        for(var mode:BiomeRules.Mode.values()) {
            Button b=button(text("mode."+mode.name().toLowerCase(Locale.ROOT)),x+mode.ordinal()*(third+4),58,third,()->{
                Set<String> selected=rules.rule(current()).selected();
                if(mode==BiomeRules.Mode.CUSTOM && rules.rule(current()).mode()!=mode && catalog!=null) {
                    selected=new TreeSet<>();for(var entry:catalog.entries())if(entry.allowed(rules,current()))selected.add(entry.id());
                }
                rules=rules.with(current(),new BiomeRules.Rule(mode,selected));rebuildWidgets();
            });b.active=!readOnly && mode!=rules.rule(current()).mode();
        }
        EditBox search=new EditBox(font,x,84,w,20,text("biome.search"));search.setMaxLength(200);search.setValue(query);
        search.setResponder(value->{query=value;page=0;refreshEntries();});addRenderableWidget(search);
        addEntries();
        button(Component.literal("<"),x,height-54,30,()->{page=Math.max(0,page-1);rebuildWidgets();});
        button(Component.literal(">"),x+w-30,height-54,30,()->{if((page+1)*3<filtered().size())page++;rebuildWidgets();});
        button(Component.translatable(readOnly?"gui.done":"relics.settings.apply"),x,height-28,(w-4)/2,()->{if(!readOnly)accept.accept(rules);onClose();});
        button(Component.translatable("gui.cancel"),x+(w+4)/2,height-28,(w-4)/2,this::onClose);
    }
    private final List<Button> entries=new ArrayList<>();
    private void refreshEntries(){for(Button b:entries)removeWidget(b);entries.clear();addEntries();}
    private void addEntries(){
        entries.clear();int w=Math.min(560,width-16),x=(width-w)/2;List<ClientBiomeCatalog.Entry> list=filtered();
        for(int i=page*3;i<Math.min(page*3+3,list.size());i++) {
            var entry=list.get(i);boolean allowed=entry.allowed(rules,current());
            Button b=button(Component.literal((allowed?"[x] ":"[ ] ")+entry.id()),x,110+(i-page*3)*20,w,()->{
                var selected=new TreeSet<>(rules.rule(current()).selected());if(!selected.remove(entry.id()))selected.add(entry.id());
                rules=rules.with(current(),new BiomeRules.Rule(BiomeRules.Mode.CUSTOM,selected));rebuildWidgets();
            });b.active=!readOnly && rules.rule(current()).mode()==BiomeRules.Mode.CUSTOM;
            String groups=BiomeRules.groups(entry.id(),entry.tags()).stream().sorted().map(g->text("group."+g).getString()).collect(java.util.stream.Collectors.joining(", "));
            b.setTooltip(Tooltip.create(Component.literal(ClientModNames.name(entry.id().split(":")[0])+"\n"+entry.id()).append("\n").append(groups.isEmpty()?text("biome.unassigned"):Component.literal(groups))));entries.add(b);
        }
    }
    @Override public void onClose(){minecraft.gui.setScreen(parent);}
    @Override public void extractRenderState(GuiGraphicsExtractor graphics,int mouseX,int mouseY,float delta){
        super.extractRenderState(graphics,mouseX,mouseY,delta);int w=Math.min(560,width-16),x=(width-w)/2;
        graphics.centeredText(font,title,width/2,10,0xffffffff);
        long count=catalog==null?0:catalog.entries().stream().filter(e->e.allowed(rules,current())).count();
        graphics.text(font,text("biome.allowed").copy().append(" "+count+" / "+(catalog==null?0:catalog.entries().size())),x,height-70,0xffcccccc);
        long missing=catalog==null?0:rules.rule(current()).selected().stream().filter(id->catalog.entries().stream().noneMatch(e->e.id().equals(id))).count();
        graphics.centeredText(font,missing>0?text("biome.missing").copy().append(" "+missing):Component.literal((page+1)+" / "+Math.max(1,(filtered().size()+2)/3)),width/2,height-48,missing>0?0xffff7777:0xffcccccc);
    }
}
