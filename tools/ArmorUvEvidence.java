import com.google.gson.*;
import net.minecraft.client.model.HumanoidModel;
import net.minecraft.client.model.geom.ModelPart;
import net.minecraft.client.model.geom.builders.*;
import net.minecraft.world.entity.EquipmentSlot;
import org.joml.*;
import java.nio.file.*;
import java.util.*;

/** Extract baked native 26.2 armor polygons and UVs without starting a client. */
public final class ArmorUvEvidence {
    private static final JsonArray faces=new JsonArray();
    @SuppressWarnings("unchecked") private static void collect(ModelPart part,Matrix4f parent,String slot,String path) throws Exception {
        Matrix4f pose=new Matrix4f(parent).translate(part.x,part.y,part.z).rotateZYX(part.zRot,part.yRot,part.xRot).scale(part.xScale,part.yScale,part.zScale);
        var cubeField=ModelPart.class.getDeclaredField("cubes");cubeField.setAccessible(true);
        if(part.visible && !part.skipDraw)for(var cube:(List<ModelPart.Cube>)cubeField.get(part))for(var polygon:cube.polygons) {
            JsonObject face=new JsonObject();face.addProperty("slot",slot);face.addProperty("part",path);
            JsonArray vertices=new JsonArray();
            for(var vertex:polygon.vertices()) {
                Vector3f p=pose.transformPosition(new Vector3f(vertex.x(),vertex.y(),vertex.z()));
                JsonArray v=new JsonArray();for(float n:new float[]{p.x,p.y,p.z,vertex.u(),vertex.v()})v.add(n);vertices.add(v);
            }
            face.add("vertices",vertices);faces.add(face);
            Vector3f normal=pose.normal(new Matrix3f()).transform(new Vector3f(polygon.normal()));
            JsonArray ns=new JsonArray();for(float n:new float[]{normal.x,normal.y,normal.z})ns.add(n);face.add("normal",ns);
        }
        var childField=ModelPart.class.getDeclaredField("children");childField.setAccessible(true);
        for(var child:((Map<String,ModelPart>)childField.get(part)).entrySet())collect(child.getValue(),pose,slot,path+"/"+child.getKey());
    }
    public static void main(String[] args) throws Exception {
        var set=HumanoidModel.createArmorMeshSet(new CubeDeformation(.5f),new CubeDeformation(1f));
        for(var slot:List.of(EquipmentSlot.HEAD,EquipmentSlot.CHEST,EquipmentSlot.LEGS,EquipmentSlot.FEET))
            collect(LayerDefinition.create(set.get(slot),64,32).bakeRoot(),new Matrix4f(),slot.getName(),"root");
        JsonObject result=new JsonObject();result.addProperty("minecraft","26.2");result.addProperty("texture_width",64);result.addProperty("texture_height",32);
        result.addProperty("inner_deformation",.5f);result.addProperty("outer_deformation",1f);result.add("faces",faces);
        Files.writeString(Path.of(args[0]),new GsonBuilder().setPrettyPrinting().create().toJson(result)+"\n");
        System.out.println("NATIVE_ARMOR_UV_EXPORTED "+faces.size());
    }
}
