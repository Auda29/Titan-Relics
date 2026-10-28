# Shared native Alpha 5 adapters

These sources implement native mod-bus registration, NeoForge persistent
attachments and server events. Generated targets contain no Fabric API types.
The Java algorithms for distribution, rewards, cores, magnets, interiors and
Trees stay shared with the primary release.

Test adapters live in a separate validation package and JAR. They provide
packet-sink players, an embedded network channel, controlled access to the
native player list and a cancellable native spawn probe. They are excluded
from player artifacts.
