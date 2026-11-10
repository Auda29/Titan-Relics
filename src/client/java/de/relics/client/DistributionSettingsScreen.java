package de.relics.client;

import de.relics.distribution.*;
import net.minecraft.client.gui.GuiGraphicsExtractor;
import net.minecraft.client.gui.components.Button;
import net.minecraft.client.gui.components.EditBox;
import net.minecraft.client.gui.components.Tooltip;
import net.minecraft.client.gui.screens.Screen;
import net.minecraft.network.chat.Component;
import java.math.BigDecimal;
import java.util.*;

/** Edits defaults for future worlds only; never sends changes to a running server. */
public final class DistributionSettingsScreen extends Screen {
    private final Screen parent;
    private final java.util.function.Consumer<DistributionSettings> saveAction;
    private final ClientBiomeCatalog catalog;
    private final String scope;
    private final Map<String,Long> diagnostics;
    private BiomeRules biomes;
    private int generationRevision;
    private final String[] geometry=new String[5],outside=new String[6],inside=new String[6];
    private static final String[] FIELDS={"cell","distance","obelisks","region","colossus"};
    private static final String[] TYPES={"obelisk","skull","skull2","tower","small","tree"};
    private int page;
    private Button save;
    private Component error;
    private String invalid;
    public DistributionSettingsScreen(Screen parent) {
        this(parent,DistributionConfig.load(),DistributionConfig::save,null,"scope.defaults",Map.of());
    }
    public DistributionSettingsScreen(Screen parent,DistributionSettings initial,java.util.function.Consumer<DistributionSettings> saveAction,ClientBiomeCatalog catalog,String scope,Map<String,Long> diagnostics) {
        super(text("title"));this.parent=parent;this.saveAction=saveAction;this.catalog=catalog;this.scope=scope;this.diagnostics=Map.copyOf(diagnostics);
        biomes=initial.biomes();select(initial);
    }
    public void loadError(){error=text("load_error");}
    private static Component text(String key){return Component.translatable("relics.settings."+key);}
    private void select(DistributionSettings value) {
        biomes=value.biomes();generationRevision=value.generationRevision();
        int[] dimensions={value.cellSize(),value.minDistance(),value.obeliskDistance(),value.regionRadius(),value.colossusMinDistance()};
        for(int i=0;i<geometry.length;i++)geometry[i]=Integer.toString(dimensions[i]);
        for(int i=0;i<6;i++){outside[i]=percent(value.outside().get(i));inside[i]=percent(value.inside().get(i));}
        error=null;
    }
    private static String percent(int value){return BigDecimal.valueOf(value,2).stripTrailingZeros().toPlainString();}
    private static int share(String value){return new BigDecimal(value.trim().replace(',','.')).movePointRight(2).intValueExact();}
    private DistributionSettings draft() {
        try {
            List<Integer> a=Arrays.stream(outside).map(DistributionSettingsScreen::share).toList();
            List<Integer> b=Arrays.stream(inside).map(DistributionSettingsScreen::share).toList();
            return new DistributionSettings(Integer.parseInt(geometry[0]),Integer.parseInt(geometry[1]),
                    Integer.parseInt(geometry[2]),Integer.parseInt(geometry[3]),a,b,biomes,Integer.parseInt(geometry[4]),generationRevision);
        }catch(NumberFormatException|ArithmeticException failure){throw new IllegalArgumentException("relics.settings.error.number");}
    }
    private void validateDraft(){try{draft();invalid=null;}catch(IllegalArgumentException failure){invalid=failure.getMessage();}if(save!=null)save.active=invalid==null && saveAction!=null;}
    private Button button(Component label,int x,int y,int w,Runnable action) {
        return addRenderableWidget(Button.builder(label,b->action.run()).bounds(x,y,w,20).build());
    }
    private int left(){return Math.max(8,(width-Math.min(560,width-16))/2);}
    private int span(){return Math.min(560,width-16);}
    private int geometryStep(){return height<280?16:20;}
    @Override protected void init() {
        int x=left(),w=span(),third=(w-8)/3;
        if(page==0 && saveAction!=null){
        button(text("preset.expedition"),x,36,third,()->{select(DistributionSettings.EXPEDITION);rebuildWidgets();});
        button(text("preset.balanced"),x+third+4,36,third,()->{select(DistributionSettings.BALANCED);rebuildWidgets();});
        button(text("preset.discovery"),x+2*(third+4),36,third,()->{select(DistributionSettings.DISCOVERY);rebuildWidgets();});
        }
        int count=page==0?geometry.length:page<5?3:0;
        int offset=page==0?0:((page-1)%2)*3;
        for(int i=0;i<count;i++) {
            final int row=i+offset;String[] values=page==0?geometry:page<=2?outside:inside;
            int step=page==0?geometryStep():20;
            int y=82+i*step;EditBox field=new EditBox(font,x+w-86,y,82,step,text(page==0?FIELDS[row]:"type."+TYPES[row]));
            field.setMaxLength(8);field.setValue(values[row]);
            field.setResponder(value->{values[row]=value;if(page==1 && row==0)inside[0]=value;validateDraft();});
            field.setEditable(saveAction!=null && !(page==3 && row==0));
            field.setTooltip(Tooltip.create(text(page==0?FIELDS[row]+".help":row==0 && page==3?"anchor.help":"chance.help")));
            addRenderableWidget(field);
        }
        if(page==5)button(text("biomes"),x,84,w,()->minecraft.gui.setScreen(new BiomeSettingsScreen(this,catalog,biomes,value->biomes=value,saveAction==null)));
        button(text("previous"),x,height-54,34,()->{page=(page+6)%7;rebuildWidgets();});
        button(text("next"),x+w-34,height-54,34,()->{page=(page+1)%7;rebuildWidgets();});
        save=button(text(scope.equals("scope.world")?"apply":"save"),x,height-28,(w-4)/2,()->{
            try{saveAction.accept(draft());onClose();}
            catch(RuntimeException failure){error=text("save_error");}
        });
        button(Component.translatable(saveAction==null?"gui.done":"gui.cancel"),x+(w+4)/2,height-28,(w-4)/2,this::onClose);
        validateDraft();
    }
    @Override public void tick(){validateDraft();}
    @Override public void onClose(){minecraft.gui.setScreen(parent);}
    @Override public void extractRenderState(GuiGraphicsExtractor graphics,int mouseX,int mouseY,float delta) {
        super.extractRenderState(graphics,mouseX,mouseY,delta);
        int x=left(),w=span();
        graphics.centeredText(font,title,width/2,8,0xffffffff);
        graphics.centeredText(font,text(scope),width/2,23,0xffcccccc);
        graphics.centeredText(font,text("page."+page),width/2,65,0xffffffff);
        for(int i=0;i<(page==0?geometry.length:page<5?3:0);i++){
            int row=i+(page==0?0:((page-1)%2)*3),step=page==0?geometryStep():20;
            graphics.text(font,text(page==0?FIELDS[row]:"type."+TYPES[row]),x+3,82+(step-9)/2+i*step,0xffffffff);
        }
        graphics.centeredText(font,text("page_count").copy().append(" "+(page+1)+" / 7"),width/2,height-48,0xffcccccc);
        if(page>0 && page<5) {
            try{int empty=10000-Arrays.stream(page<=2?outside:inside).mapToInt(DistributionSettingsScreen::share).sum();
                graphics.text(font,text("empty").copy().append(" "+percent(empty)+" %"),x,height-90,0xffcccccc);
            }catch(RuntimeException ignored){ }
        }
        if(page==5)graphics.textWithWordWrap(font,text("biomes.help"),x,116,w,0xffcccccc);
        if(page==6) {
            int row=0;for(String key:List.of("biome","terrain","bounds","distance"))graphics.text(font,text("diag."+key).copy().append(": "+(diagnostics.containsKey(key)?diagnostics.get(key):"—")),x,84+20*row++,0xffffffff);
        }
        Component message=invalid!=null?Component.translatable(invalid):error!=null?error:text(page==0?"unique":"footer");
        graphics.textWithWordWrap(font,message,x,height-76,w,invalid!=null || error!=null?0xffff7777:0xffcccccc);
    }
}
