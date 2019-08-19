import os
import re

def main():
    biomes = []
    vanillaIDsPath = "VanillaBiomeIDs.txt"
    if not os.path.isfile(vanillaIDsPath):
        print("ERROR: Missing file "+vanillaIDsPath)
        return
    with open(vanillaIDsPath) as vanillaIDs:
        for line in vanillaIDs.readlines():
            # Ignore comments and blank lines
            if line.startswith("#") or len(line.strip()) == 0:
                continue
            biomeInfo = getBiomeInfo(line)
            if biomeInfo != None:
                 biomes.append(biomeInfo)
            else:
                # Error message sent by getBiomeInfo already
                return
            
    customBiomesKey = "CustomBiomes:"
    worldConfigPath = "WorldConfig.ini"
    if not os.path.isfile(worldConfigPath):
        print("ERROR: Missing file "+worldConfigPath)
        return
    with open(worldConfigPath) as worldConfig:
        for line in worldConfig.readlines():
            if line.startswith(customBiomesKey):
                biomeList = line[len(customBiomesKey):].strip().split(",")
                for biomeDef in biomeList:
                    biomeInfo = getBiomeInfo(biomeDef)
                    if biomeInfo != None:
                        biomes.append(biomeInfo)
                    else:
                        # Error message sent by getBiomeInfo already
                        return
    
    outPath = "BiomeBundle-texture.txt"
    outFile = open(outPath, "w")
    
    print("Generating file, please wait...")
    outFile.write("# File created using https://github.com/KasaneKona/BiomeBundleDynmap\n")
    outFile.write("\n")
    outFile.write("# Biome Bundle\n")
    outFile.write("modname:biomebundle\n")
    outFile.write("\n")
    biomes.sort(key = lambda b: b[1])
    # Get color info and output biome IDs as variables if color info not empty
    outFile.write("# Biome IDs\n")
    for biomeInfo in biomes:
        path = "./WorldBiomes/" + biomeInfo[1] + ".bc"
        if not os.path.isfile(path):
            print("ERROR: Missing file "+path)
            return
        with open(path) as biomeDefFile:
            # Note: color data will already start with a comma!
            biomeInfo[3] = findColorData(biomeDefFile.readlines())
        if (biomeInfo[3] != None) and (len(biomeInfo[3]) > 0):
            outFile.write("var:biome_ids/" + biomeInfo[2] + "=" + str(biomeInfo[0]) + "\n")
    outFile.write("\n")
    outFile.write("# Biome color definitions\n")
    # Output biome definitions where color info not empty
    for biomeInfo in biomes:
        if (biomeInfo[3] != None) and (len(biomeInfo[3]) > 0):
            outFile.write("biome:id=biome_ids/" + biomeInfo[2] + biomeInfo[3] + "\n")
    outFile.close()
    print("Written to "+outPath+"!")

nameRemoveFilter = re.compile("[()[\]]")
nameUnderscoreFilter = re.compile("[^\w]") # Excludes characters removed by previous filter
safeNameCounters = {}

def getBiomeInfo(biomeDef):
    parts = biomeDef.strip().split(":")
    if len(parts) != 2:
        print("ERROR: Incorrect number of terms in \""+biomeDef+"\"")
        return None

    # Trimmed name
    name = parts[0].strip()
    # Name with "+" replaced with "Plus", spaces and brackets removed, and other non-alphanumeric
    # characters replaced with underscores
    safeName = nameUnderscoreFilter.sub("_",nameRemoveFilter.sub("",name.replace("+","Plus")))
    safeNameInitial = safeName
    safeNameNum = 0
    # If name is already used, make it unique
    if safeName in safeNameCounters:
        safeNameCounters[safeName] += 1
        # Name should not contain spaces at this point, so it's a safe separator
        safeName = safeName + " " + safeNameCounters[safeName]
    # Otherwise add to set of used names
    else:
        safeNameCounters[safeName] = 0
    
    idNum = parts[1].strip()
    if not idNum.isnumeric():
        print("ERROR: ID for "+name+" is non-numeric!")
        return None
    return [int(idNum), name, safeName, None]

def findColorData(lines):
    grassMixKey = 'GrassColorIsMultiplier:'
    foliageMixKey = 'FoliageColorIsMultiplier:'
    grassColKey = 'GrassColor:'
    foliageColKey = 'FoliageColor:'
    waterColKey = 'WaterColor:'
    tempKey = 'BiomeTemperature:'
    rainKey = 'BiomeWetness:'

    grassMix = True
    foliageMix = True
    grassCol = "000000"
    foliageCol = "000000"
    waterCol = "FFFFFF"
    temp = 0.5
    rain = 0.5

    for line in lines:
        # Grass mix
        if line.startswith(grassMixKey):
            grassMix = (line[len(grassMixKey):].strip().lower() == 'true')
        # Foliage mix
        elif line.startswith(foliageMixKey):
            foliageMix = (line[len(foliageMixKey):].strip().lower() == 'true')
        # Grass color
        elif line.startswith(grassColKey):
            grassCol = line[len(grassColKey):].strip()[1:]
        # Foliage color
        elif line.startswith(foliageColKey):
            foliageCol = line[len(foliageColKey):].strip()[1:]
        # Water color
        elif line.startswith(waterColKey):
            waterCol = line[len(waterColKey):].strip()[1:]
        # Temperature
        elif line.startswith(tempKey):
            temp = float(line[len(tempKey):].strip())
        # Rainfall
        elif line.startswith(rainKey):
            rain = float(line[len(rainKey):].strip())

    # Check and mix grass
    if len(grassCol) == 6:
        if not grassMix:
            grassCol = "1" + grassCol
    else:
        print("ERROR: Definition for grass color is invalid: "+grassCol)
        return None

    # Check and mix foliage
    if len(foliageCol) == 6:
        if not foliageMix:
            foliageCol = "1" + foliageCol
    else:
        print("ERROR: Definition for foliage color is invalid: "+foliageCol)
        return None

    # Check water
    if len(waterCol) != 6:
        print("ERROR: Definition for water color is invalid: "+waterCol)
        return None

    # Fix temp/rain ranges
    temp = min(max(0.0,temp),2.0)
    rain = min(max(0.0,rain),1.0)

    assembledString = ""
    # If grass/foliage not BB defaults, fix Dynmap defaults and add to output
    if grassCol != "FFFFFF":
        if grassCol == "000000":
            grassCol = "000100"
        assembledString += f',grassColorMult={grassCol}'
    if foliageCol != "FFFFFF":
        if foliageCol == "000000":
            foliageCol = "000100"
        assembledString += f',foliageColorMult={foliageCol}'
    # No point adding water if it's the default
    if waterCol != "FFFFFF":
        assembledString += f',waterColorMult={waterCol}'
    # No point adding temp/rain if defaults or unused
    if grassMix or foliageMix:
        if temp != 0.5:
            assembledString += f',temp={temp}'
        if rain != 0.5:
            assembledString += f',rain={rain}'

    # Return data
    return assembledString

main()
