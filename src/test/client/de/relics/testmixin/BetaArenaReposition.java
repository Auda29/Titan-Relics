package de.relics.qa;

import java.lang.instrument.Instrumentation;
import com.sun.tools.attach.VirtualMachine;

/** Explicit operator reposition for an already running isolated named client. No rewards or code redefinition. */
public final class BetaArenaReposition {
    public static void main(String[] args)throws Exception{
        var vm=VirtualMachine.attach(args[0]);try{vm.loadAgent(args[1],args[2]);}finally{vm.detach();}
    }
    public static void agentmain(String command,Instrumentation instrumentation)throws Exception{
        for(Class<?> type:instrumentation.getAllLoadedClasses())if((type.getName().equals("net.minecraft.client.Minecraft")||type.getName().equals("net.minecraft.class_310"))){
            Object client=null;for(var method:type.getMethods())if(java.lang.reflect.Modifier.isStatic(method.getModifiers())&&method.getReturnType()==type&&method.getParameterCount()==0){client=method.invoke(null);break;}
            final Object game=client;
            if(command.equals("mute")){
                Runnable mute=()->{try{
                    Object options=null;for(var field:type.getFields())if(field.getType().getName().equals("net.minecraft.client.Options")||field.getType().getName().equals("net.minecraft.class_315")){options=field.get(game);break;}
                    for(var method:options.getClass().getMethods())if(method.getParameterCount()==1&&method.getParameterTypes()[0].isEnum()&&(method.getReturnType().getName().equals("net.minecraft.client.OptionInstance")||method.getReturnType().getName().equals("net.minecraft.class_7172"))){
                        Class<?> source=method.getParameterTypes()[0];if(!source.getName().equals("net.minecraft.sounds.SoundSource")&&!source.getName().equals("net.minecraft.class_3419"))continue;
                        Object option=method.invoke(options,source.getEnumConstants()[0]);for(var setter:option.getClass().getMethods())if(setter.getParameterCount()==1&&setter.getParameterTypes()[0]==Object.class&&setter.getReturnType()==void.class){setter.invoke(option,0.0);System.out.println("BETA_QA_MASTER_SOUND_ZERO "+System.currentTimeMillis());return;}
                    }
                    throw new IllegalStateException("Master sound option not found");
                }catch(Exception e){throw new IllegalStateException(e);}};
                type.getMethod("execute",Runnable.class).invoke(game,mute);return;
            }
            Object server=type.getMethod("getSingleplayerServer").invoke(client);
            if(server==null)throw new IllegalStateException("Only the isolated integrated host is supported");
            Runnable action=()->{try{
                Object source=server.getClass().getMethod("createCommandSourceStack").invoke(server);
                Object commands=server.getClass().getMethod("getCommands").invoke(server);
                commands.getClass().getMethod("performPrefixedCommand",source.getClass(),String.class).invoke(commands,source,command);
                System.out.println("BETA_QA_OPERATOR_REPOSITION "+System.currentTimeMillis()+" "+command);
            }catch(Exception e){throw new IllegalStateException(e);}};
            server.getClass().getMethod("execute",Runnable.class).invoke(server,action);return;
        }
        throw new IllegalStateException("Named Minecraft client class was not found");
    }
}
