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
    private int page=-1;
    private static final String[] PRESETS={"expedition","balanced","discovery"};
    private static final DistributionSettings[] PRESET_VALUES={DistributionSettings.EXPEDITION,DistributionSettings.BALANCED,DistributionSettings.DISCOVERY};
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
    private String chosenPreset() {
        try {var value=draft();for(int i=0;i<PRESETS.length;i++)if(value.equals(PRESET_VALUES[i]))return PRESETS[i];}
        catch(IllegalArgumentException ignored) { }
        return "custom";
    }
    private void openPage(int value){page=value;rebuildWidgets();}
    @Override protected void init() {
        int x=left(),w=span(),third=(w-8)/3;
        if(page==-1) {
            if(saveAction!=null)for(int i=0;i<PRESETS.length;i++) {
                final int choice=i;
                Button preset=button(text("preset."+PRESETS[i]),x+i*(third+4),42,third,()->{select(PRESET_VALUES[choice]);rebuildWidgets();});
                preset.active=!PRESETS[i].equals(chosenPreset());
                preset.setTooltip(Tooltip.create(text("experience."+PRESETS[i])));
            }
            button(text("advanced"),x,height-54,w,()->openPage(0));
        }else {
            String[] tabs={"distances","relics","biomes","diagnostics"};int[] pages={0,1,5,6};
            int tab=(w-12)/4;
            for(int i=0;i<tabs.length;i++) {
                final int target=pages[i];
                Button b=button(text("tab."+tabs[i]),x+i*(tab+4),42,tab,()->openPage(target));
                b.active=!(i==0 && page==0 || i==1 && page>=1 && page<=4 || i==2 && page==5 || i==3 && page==6);
            }
            button(text("simple"),x+38,height-54,w-76,()->openPage(-1));
            button(text("previous"),x,height-54,34,()->openPage((page+6)%7));
            button(text("next"),x+w-34,height-54,34,()->openPage((page+1)%7));
        }
        int count=page==0?geometry.length:page>=1 && page<5?3:0;
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
        save=null;
        if(saveAction==null){button(Component.translatable("gui.done"),x,height-28,w,this::onClose);validateDraft();return;}
        save=button(text(scope.equals("scope.world")?"apply":"save"),x,height-28,(w-4)/2,()->{
            try{saveAction.accept(draft());onClose();}
            catch(RuntimeException failure){error=text("save_error");}
        });
        button(Component.translatable(saveAction==null?"gui.done":"gui.cancel"),x+(w+4)/2,height-28,(w-4)/2,this::onClose);
        validateDraft();
    }
    @Override public void tick(){validateDraft();}
    @Override public Component getNarrationMessage() {
        return title.copy().append(". ").append(text(scope)).append(". ")
                .append(text(page==-1?"preset."+chosenPreset():"page."+page))
                .append(". ").append(text(page==-1?"experience."+chosenPreset():"footer"));
    }
    @Override public void onClose(){minecraft.gui.setScreen(parent);}
    @Override public void extractRenderState(GuiGraphicsExtractor graphics,int mouseX,int mouseY,float delta) {
        super.extractRenderState(graphics,mouseX,mouseY,delta);
        int x=left(),w=span();
        graphics.centeredText(font,title,width/2,8,0xffffffff);
        graphics.centeredText(font,text(scope),width/2,23,0xffcccccc);
        if(page==-1)renderOverview(graphics,x,w);
        else graphics.centeredText(font,text("page."+page),width/2,65,0xffffffff);
        for(int i=0;i<(page==0?geometry.length:page>=1 && page<5?3:0);i++){
            int row=i+(page==0?0:((page-1)%2)*3),step=page==0?geometryStep():20;
            graphics.text(font,text(page==0?FIELDS[row]:"type."+TYPES[row]),x+3,82+(step-9)/2+i*step,0xffffffff);
        }
        if(page>0 && page<5) {
            try{int empty=10000-Arrays.stream(page<=2?outside:inside).mapToInt(DistributionSettingsScreen::share).sum();
                graphics.text(font,text("empty").copy().append(" "+percent(empty)+" %"),x,height-90,0xffcccccc);
            }catch(RuntimeException ignored){ }
        }
        if(page==5)graphics.textWithWordWrap(font,text("biomes.help"),x,116,w,0xffcccccc);
        if(page==6) {
            int row=0;for(String key:List.of("biome","terrain","bounds","distance"))graphics.text(font,text("diag."+key).copy().append(": "+(diagnostics.containsKey(key)?diagnostics.get(key):"—")),x,84+20*row++,0xffffffff);
        }
        Component message=invalid!=null?Component.translatable(invalid):error!=null?error:text(page==-1?saveAction==null?"overview.saved":"overview.note":page==0?"unique":"footer");
        graphics.textWithWordWrap(font,message,x,height-76,w,invalid!=null || error!=null?0xffff7777:0xffcccccc);
    }
    /** An illustrative pacing diagram only. Never invokes the generator or reads a seed. */
    private void renderOverview(GuiGraphicsExtractor graphics,int x,int w) {
        String selected=chosenPreset();
        if(saveAction!=null)for(int i=0;i<PRESETS.length;i++)if(PRESETS[i].equals(selected)) {
            int third=(w-8)/3,cardX=x+i*(third+4);
            graphics.fill(cardX,63,cardX+third,65,0xffe8bd67);
        }
        if(saveAction==null)graphics.centeredText(font,text("preset."+selected),width/2,47,0xffffd080);
        if(height>=320 && saveAction!=null) {
            int third=(w-8)/3;
            for(int i=0;i<PRESETS.length;i++) {
                int cardX=x+i*(third+4);boolean active=PRESETS[i].equals(selected);
                graphics.fill(cardX,65,cardX+third,105,active?0x994b5838:0x66202020);
                graphics.fill(cardX,65,cardX+third,67,active?0xffe8bd67:0xff606060);
                graphics.textWithWordWrap(font,text("experience."+PRESETS[i]),cardX+5,72,third-10,0xffeeeeee);
            }
        }else graphics.textWithWordWrap(font,text("experience."+selected),x+4,70,w-8,0xffeeeeee);
        int top=height>=320?122:104,bottom=height-108;
        graphics.fill(x,top,x+w,bottom,0xc0182724);
        int mapHeight=bottom-top;
        // Use a fixed pattern so changing a style is easy to compare. Symbols
        // represent opportunities, not guaranteed structures or real positions.
        int opportunities=5;
        try {
            var settings=draft();
            opportunities=settings.outside().stream().mapToInt(Integer::intValue).sum()==0
                    && settings.inside().stream().mapToInt(Integer::intValue).sum()==0
                    ?0:Math.max(4,Math.min(16,26000/settings.cellSize()));
        }catch(IllegalArgumentException ignored) { }
        for(int i=0;i<opportunities;i++) {
            int px=x+12+(int)((long)(i*73+31)%(Math.max(1,w-24)));
            int py=top+5+(int)((long)(i*37+13)%Math.max(1,mapHeight-16));
            // A few simple ruin silhouettes avoid spoiling the actual models.
            graphics.fill(px,py+3,px+7,py+8,0xffc8b68a);
            graphics.fill(px+1,py,px+3,py+6,0xffe8d7ae);
            graphics.fill(px+5,py+1,px+7,py+6,0xffe8d7ae);
        }
        int homeX=x+w/2,homeY=top+mapHeight/2;
        graphics.fill(homeX-5,homeY-5,homeX+6,homeY+6,0xff182724);
        graphics.fill(homeX-3,homeY-3,homeX+4,homeY+4,0xff78d4e6);
        if(mapHeight>=70)graphics.centeredText(font,text("preview.start"),homeX,homeY+9,0xff9ee7f4);
        else {
            graphics.fill(homeX+9,homeY-5,homeX+13+font.width(text("preview.start")),homeY+7,0xff182724);
            graphics.text(font,text("preview.start"),homeX+11,homeY-3,0xff9ee7f4);
        }
        graphics.text(font,text("preview.caption"),x+3,bottom+5,0xffc7d2c9);
        if(selected.equals("custom") && height>=320 && saveAction!=null)
            graphics.centeredText(font,text("preset.custom"),width/2,107,0xffffd080);
    }
}
