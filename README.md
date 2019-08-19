# Biome Bundle Dynmap
The included file `BiomeBundle-texture.txt` is a premade color map for default biome IDs of Biome Bundle 6.1 (with Minecraft 1.12.2). If you have a compatible version, simply copy this premade file into Dynmap's `renderdata` directory and restart your server. If your map has already rendered, you will need to force a re-render (typically `/dynmap fullrender`) for displayed colors to be updated.

If your setup is incompatible with the premade file, or you would prefer to generate the config yourself, you can do so with the `generate.py` script as follows;
1. Place the generate.py script and VanillaBiomeIDs.txt in the same directory as your active Biome Bundle configuration, ie. in the same place as `WorldConfig.ini` and `WorldBiomes`. This will usually be in `/OpenTerrainGenerator/worlds/Biome Bundle` (in your mods or plugins location), though the world name may be different if you renamed it during installation. Alternatively, you can copy WorldConfig.ini and WorldBiomes into another temporary location with generate.py and VanillaBiomeIDs.txt.
2. Run generate.py with Python 3 (if you receive a syntax error you're using an older version). No external packages are required.
3. Copy the generated BiomeBundle-texture.txt to the Dynmap renderdata directory, restart your server and re-render if necessary (See above).

NOTE: This script should work for any up-to-date OpenTerrainGenerator world pack, however I have only tested it with Biome Bundle!

---
This repository is not associated with or officially supported by Biome Bundle, OpenTerrainGenerator or Dynmap. The project was originally created for a private server, but I decided to write a proper script and share it.
