#!/usr/bin/env python3
"""
Complete BF2 Deployment Pipeline for Slovenia Golovec (4km x 4km)
Installs cleanly into /media/ator/Tera/Bf2/Battlefield 2/mods/bf2/Levels/slovenia_golovec
"""

import os
import shutil
import zipfile
import subprocess
import numpy as np
from PIL import Image

SRC_DIR = "/home/ator/BF2/levels/slovenia_golovec"
ROOT_DIR = "/home/ator/BF2"
TARGET_DIR = "/media/ator/Tera/Bf2/Battlefield 2/mods/bf2/Levels/slovenia_golovec"
BF2_MODS = "/media/ator/Tera/Bf2/Battlefield 2/mods/bf2"

print(f"Deploying BF2 map to {TARGET_DIR}...")
os.makedirs(TARGET_DIR, exist_ok=True)
os.makedirs(os.path.join(TARGET_DIR, "Info"), exist_ok=True)
os.makedirs(os.path.join(TARGET_DIR, "Overgrowth"), exist_ok=True)
for size in [16, 32, 64]:
    os.makedirs(os.path.join(TARGET_DIR, f"GameModes/gpm_cq/{size}"), exist_ok=True)

# 1. Base .con scripts
for f in ["Heightdata.con", "Sky.con", "Water.con", "StaticObjects.con", "GameplayObjects.con", "Heightmap.raw", "ColorMap.dds"]:
    shutil.copy2(os.path.join(SRC_DIR, f), os.path.join(TARGET_DIR, f))
shutil.copy2(os.path.join(SRC_DIR, "Heightmap.raw"), os.path.join(TARGET_DIR, "HeightmapPrimary.raw"))

# 2. Terrain.con configured for compiled runtime
terrain_con = """if v_arg1 == BF2Editor
terrain.create TerrainEditable
else
terrain.create Terrain
terrain.load Levels/slovenia_golovec/terraindata.raw
endIf
"""
with open(os.path.join(TARGET_DIR, "Terrain.con"), "w") as f:
    f.write(terrain_con)

# 3. Init.con with engine conductors and LevelSettings
init_con = """rem *** Master Conductor for Slovenia Golovec (4km x 4km) ***
run Heightdata.con
run Terrain.con
run Sky.con
run Water.con
run StaticObjects.con
run GameplayObjects.con
run Overgrowth/Overgrowth.con

rem ------------------------------- LevelSettings -------------------------------
rem -----------------------------------------------------------------------------

gameLogic.setTeamName 1 "EU"
gameLogic.setTeamName 2 "MEC"

gameLogic.setTeamLanguage 1 "EU"
gameLogic.setTeamLanguage 2 "MEC"

gameLogic.setTeamFlag 0 "flag_neutral"
gameLogic.setTeamFlag 1 "flag_EU"
gameLogic.setTeamFlag 2 "flag_MEC"

gameLogic.setKit 1 0 "EU_Specops" "EU_soldier"
gameLogic.setKit 2 0 "MEC_Specops" "mec_light_soldier"

gameLogic.setKit 1 1 "EU_Sniper" "EU_soldier"
gameLogic.setKit 2 1 "MEC_Sniper" "mec_light_soldier"

gameLogic.setKit 1 2 "EU_Assault" "EU_heavy_soldier"
gameLogic.setKit 2 2 "MEC_Assault" "mec_heavy_soldier"

gameLogic.setKit 1 3 "EU_Support" "EU_heavy_soldier"
gameLogic.setKit 2 3 "MEC_Support" "mec_heavy_soldier"

gameLogic.setKit 1 4 "EU_Engineer" "EU_soldier"
gameLogic.setKit 2 4 "MEC_Engineer" "mec_light_soldier"

gameLogic.setKit 1 5 "EU_Medic" "EU_soldier"
gameLogic.setKit 2 5 "MEC_Medic" "mec_light_soldier"

gameLogic.setKit 1 6 "EU_AT" "EU_heavy_soldier"
gameLogic.setKit 2 6 "MEC_AT" "mec_heavy_soldier"

rem -----------------------------------------------------------------------------

gameLogic.setBeforeSpawnCamera 0/320/1200 0/-15/0

GameLogic.MaximumLevelViewDistance 1200

gameLogic.setDefaultNumberOfTicketsEx 16 1 200
gameLogic.setDefaultNumberOfTicketsEx 16 2 200
gameLogic.setDefaultNumberOfTicketsEx 32 1 250
gameLogic.setDefaultNumberOfTicketsEx 32 2 250
gameLogic.setDefaultNumberOfTicketsEx 64 1 300
gameLogic.setDefaultNumberOfTicketsEx 64 2 300
gameLogic.setDefaultNumberOfTicketsEx 128 1 200
gameLogic.setDefaultNumberOfTicketsEx 128 2 200
gameLogic.setDefaultTimeToNextAIWave 8
gameLogic.setTicketLossAtEndPerMin 1000
gameLogic.setTicketLossPerMin 1 10
gameLogic.setTicketLossPerMin 2 10

renderer.globalStaticMeshLodDistanceScale 1
renderer.globalBundleMeshLodDistanceScale 1
renderer.globalSkinnedMeshLodDistanceScale 1

gameLogic.setTeamDropVehicle 1 "xpak2_faav"
gameLogic.setTeamDropVehicle 2 "jep_mec_paratrooper"
"""
with open(os.path.join(TARGET_DIR, "Init.con"), "w") as f:
    f.write(init_con)
with open(os.path.join(TARGET_DIR, "init.con"), "w") as f:
    f.write(init_con)

# 4. Overgrowth.raw with material indices [0, 1]
raw_og = np.fromfile(os.path.join(SRC_DIR, "Overgrowth/Overgrowth.raw"), dtype=np.uint8)
binary_og = np.where(raw_og > 30, 1, 0).astype(np.uint8)
binary_og.tofile(os.path.join(TARGET_DIR, "Overgrowth/Overgrowth.raw"))

# 5. Extract terrain texture patches from base package if not present
if not os.path.exists(os.path.join(TARGET_DIR, "terraindata.raw")):
    ref_zf = zipfile.ZipFile(f"{BF2_MODS}/Levels/Dragon_Valley/client.zip")
    tdata = ref_zf.read("terraindata.raw")
    tdata_patched = tdata.replace(b"Dragon_Valley", b"slovenia_golovec")
    with open(os.path.join(TARGET_DIR, "terraindata.raw"), "wb") as f:
        f.write(tdata_patched)
    for prefix in ["Colormaps/", "Detailmaps/", "LowDetailmaps/", "Lightmaps/"]:
        for name in ref_zf.namelist():
            if name.startswith(prefix):
                ref_zf.extract(name, TARGET_DIR)

# 6. GameplayObjects in GameModes
for size in [16, 32, 64]:
    shutil.copy2(os.path.join(SRC_DIR, "GameplayObjects.con"), os.path.join(TARGET_DIR, f"GameModes/gpm_cq/{size}/GamePlayObjects.con"))
    shutil.copy2(os.path.join(SRC_DIR, "GameplayObjects.con"), os.path.join(TARGET_DIR, f"GameModes/gpm_cq/{size}/GameplayObjects.con"))

# 7. Menu UI in Info/
desc_content = """<map>
	<name> Slovenia Golovec (4km) </name>
	<briefing> Golovec ridge real-world 4km x 4km battlefield in SE Ljubljana, Slovenia. Real cyclic LiDAR topography and OpenStreetMap structures. </briefing>
	<music> common/sound/menu/music/load_MEC_music.ogg </music>
	<modes>
		<mode type="gpm_cq">
			<maptype players="16" type="headon">Head-On Conquest across Golovec ridge</maptype>
			<maptype players="32" type="headon">Head-On Conquest across Golovec ridge</maptype>
			<maptype players="64" type="headon">Head-On Conquest across Golovec ridge</maptype>
		</mode>
	</modes>
</map>
"""
with open(os.path.join(TARGET_DIR, "Info/slovenia_golovec.desc"), "w") as f:
    f.write(desc_content)

preview_png = os.path.join(ROOT_DIR, "ColorMap_preview.png")
if os.path.exists(preview_png):
    img = Image.open(preview_png)
    img_1024 = img.resize((1024, 1024), Image.Resampling.LANCZOS)
    for name in ["gpm_cq_16_menuMap.png", "gpm_cq_32_menuMap.png", "gpm_cq_64_menuMap.png"]:
        img_1024.save(os.path.join(TARGET_DIR, "Info", name), format="DDS", pixel_format="DXT1")
    img_512 = img.resize((512, 512), Image.Resampling.LANCZOS)
    img_512.save(os.path.join(TARGET_DIR, "Info/loadmap.png"), format="DDS", pixel_format="DXT1")
    img_256 = img.resize((256, 256), Image.Resampling.LANCZOS)
    img_256.save(os.path.join(TARGET_DIR, "Info/favoriteMap.png"), format="DDS", pixel_format="DXT1")

# 8. Rebuild clean client.zip and server.zip
print("Packaging archives...")
cmd_sz = ["zip", "-u", "-r", "server.zip", "Init.con", "init.con", "Heightdata.con", "Terrain.con", "Sky.con", "Water.con", "StaticObjects.con", "GameplayObjects.con", "GameModes", "Overgrowth"]
subprocess.run(cmd_sz, cwd=TARGET_DIR, check=True, stdout=subprocess.DEVNULL)

cmd_cz = ["zip", "-u", "-r", "client.zip", "Init.con", "init.con", "Heightdata.con", "Terrain.con", "Sky.con", "Water.con", "StaticObjects.con", "GameplayObjects.con", "Heightmap.raw", "HeightmapPrimary.raw", "ColorMap.dds", "terraindata.raw", "Colormaps", "Detailmaps", "LowDetailmaps", "Lightmaps", "GameModes", "Overgrowth"]
subprocess.run(cmd_cz, cwd=TARGET_DIR, check=True, stdout=subprocess.DEVNULL)

print("Level deployment verified and complete!")
