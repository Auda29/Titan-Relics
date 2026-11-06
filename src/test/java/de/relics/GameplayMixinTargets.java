package de.relics;

import com.google.gson.JsonParser;
import org.objectweb.asm.ClassReader;
import org.objectweb.asm.Type;
import org.objectweb.asm.tree.*;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.ArrayList;
import java.util.List;

/** Static bytecode contract check only. Does not apply or execute any mixin. */
public final class GameplayMixinTargets {
    private static ClassNode read(String name) throws Exception {
        try (var input = GameplayMixinTargets.class.getResourceAsStream("/" + name + ".class")) {
            if (input == null) throw new AssertionError("Missing class " + name);
            ClassNode node = new ClassNode(); new ClassReader(input).accept(node,0); return node;
        }
    }
    private static Object value(AnnotationNode annotation, String key) {
        if (annotation.values != null) for (int i=0;i<annotation.values.size();i+=2)
            if (key.equals(annotation.values.get(i))) return annotation.values.get(i+1);
        return null;
    }
    private static List<AnnotationNode> annotations(List<AnnotationNode> visible, List<AnnotationNode> invisible) {
        var all = new ArrayList<AnnotationNode>(); if (visible != null) all.addAll(visible); if (invisible != null) all.addAll(invisible); return all;
    }
    private static List<MethodNode> targets(ClassNode target, String selector) {
        return target.methods.stream().filter(method -> selector.equals(method.name) || selector.equals(method.name+method.desc)).toList();
    }
    @SuppressWarnings("unchecked")
    public static void verify(Path resources) throws Exception {
        int checked = 0;
        var config = JsonParser.parseString(Files.readString(resources.resolve("relics.mixins.json"))).getAsJsonObject();
        for (var element : config.getAsJsonArray("mixins")) {
            String name = element.getAsString();
            if (List.of("StructureTemplateMixin", "WorldGenRegionMixin", "OreFeatureMixin").contains(name)) continue;
            ClassNode mixin = read(config.get("package").getAsString().replace('.','/')+"/"+name);
            AnnotationNode marker = annotations(mixin.visibleAnnotations,mixin.invisibleAnnotations).stream()
                    .filter(a -> a.desc.equals("Lorg/spongepowered/asm/mixin/Mixin;")).findFirst().orElseThrow();
            var classTargets = (List<Type>)value(marker,"value");
            var namedTargets = (List<String>)value(marker,"targets");
            int targetCount = (classTargets == null ? 0 : classTargets.size())
                    + (namedTargets == null ? 0 : namedTargets.size());
            if (targetCount != 1) throw new AssertionError(name+": expected exactly one explicit mixin target");
            ClassNode target = read(classTargets != null && !classTargets.isEmpty()
                    ? classTargets.getFirst().getInternalName()
                    : namedTargets.getFirst().replace('.','/'));
            for (FieldNode field : mixin.fields) for (var annotation : annotations(field.visibleAnnotations,field.invisibleAnnotations)) {
                if (!annotation.desc.equals("Lorg/spongepowered/asm/mixin/Shadow;")) continue;
                if (target.fields.stream().noneMatch(f -> f.name.equals(field.name) && f.desc.equals(field.desc)))
                    throw new AssertionError(name+": missing shadow field "+field.name+field.desc);
                checked++;
            }
            for (MethodNode method : mixin.methods) for (var annotation : annotations(method.visibleAnnotations,method.invisibleAnnotations)) {
                if (annotation.desc.equals("Lorg/spongepowered/asm/mixin/Shadow;")) {
                    if (target.methods.stream().noneMatch(m -> m.name.equals(method.name) && m.desc.equals(method.desc)))
                        throw new AssertionError(name+": missing shadow method "+method.name+method.desc);
                    checked++;
                } else if (annotation.desc.equals("Lorg/spongepowered/asm/mixin/gen/Invoker;")) {
                    String selector = (String)value(annotation,"value");
                    if (targets(target,selector).stream().noneMatch(m -> m.desc.equals(method.desc)))
                        throw new AssertionError(name+": missing invoker "+selector+method.desc);
                    checked++;
                } else if (annotation.desc.equals("Lorg/spongepowered/asm/mixin/gen/Accessor;")) {
                    String selector = (String)value(annotation,"value");
                    String descriptor = Type.getReturnType(method.desc).getDescriptor();
                    if(descriptor.equals("V")) {
                        var arguments=Type.getArgumentTypes(method.desc);
                        if(arguments.length!=1)throw new AssertionError(name+": accessor setter must have one field value");
                        descriptor=arguments[0].getDescriptor();
                    } else if(Type.getArgumentTypes(method.desc).length!=0)throw new AssertionError(name+": accessor getter has arguments");
                    final String fieldDescriptor=descriptor;
                    if (target.fields.stream().noneMatch(f -> f.name.equals(selector) && f.desc.equals(fieldDescriptor)))
                        throw new AssertionError(name+": missing accessor "+selector);
                    checked++;
                } else if (annotation.desc.equals("Lorg/spongepowered/asm/mixin/injection/Inject;")
                        || annotation.desc.equals("Lcom/llamalad7/mixinextras/injector/wrapoperation/WrapOperation;")) {
                    for (String selector : (List<String>)value(annotation,"method")) {
                        var methods = targets(target,selector);
                        if (methods.isEmpty()) throw new AssertionError(name+": missing injection target "+selector);
                        checked++;
                        if (annotation.desc.contains("WrapOperation")) {
                            Object location = value(annotation,"at");
                            var at = (AnnotationNode)(location instanceof List<?> list ? list.getFirst() : location);
                            String invocation = (String)value(at,"target");
                            boolean present = false;
                            for (MethodNode selected : methods) for (var instruction : selected.instructions)
                                if (instruction instanceof MethodInsnNode call && invocation.equals("L"+call.owner+";"+call.name+call.desc)) present = true;
                            if (!present) throw new AssertionError(name+": missing wrapped invocation "+invocation);
                            checked++;
                        }
                    }
                }
            }
        }
        System.out.println("PASS: " + checked + " static 26.2 mixin target contracts (not mixin runtime)");
    }
}
