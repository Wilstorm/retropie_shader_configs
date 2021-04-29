# creates cfg files for retropie using crt-pi or zfast
# params are:
# * core (eg mame2003 or fbneo)
# * shader (eg crtpi or zfast)
# * screen width (eg 1920) OR curvature
# * screen height (eg 1080)
# example usage:
# python crt_pi_configs.py mame2003 crtpi 1920 1080
# python crt_pi_configs.py fbneo zfast 1920 1080
# python crt_pi_configs.py consoles crtpi 1920 1080
# python crt_pi_configs.py 2003plus zfast curvature
# python -c "import pi_shader_configs; pi_shader_configs.createZip('crtpi',False,1920,1080)"
# python -c "import pi_shader_configs; pi_shader_configs.createZip('zfast',True)"


from __future__ import division
import sys
import os
import shutil


def generateConfigs(arg1, arg2, arg3, arg4):

    console = False
    if "mame2000" in arg1:
        fileName = "resolution_db/mame2000.txt"
        coreName = "MAME 2000"
    if "mame2003" in arg1:
        fileName = "resolution_db/mame2003.txt"
        coreName = "MAME 2003 (0.78)"
    elif "2003plus" in arg1:
        fileName = "resolution_db/mame2003-plus.txt"
        coreName = "MAME 2003-Plus"
    elif "mame2010" in arg1:
        fileName = "resolution_db/mame2010.txt"
        coreName = "MAME 2010"
    elif "mame2015" in arg1:
        fileName = "resolution_db/mame2015.txt"
        coreName = "MAME 2015"
    elif "mame2016" in arg1:
        fileName = "resolution_db/mame2016.txt"
        coreName = "MAME 2016"
    elif "fba2012" in arg1:
        fileName = "resolution_db/fba2012.txt"
        coreName = "FB Alpha"
    elif "fbneo" in arg1:
        fileName = "resolution_db/fbneo.txt"
        coreName = "FinalBurn Neo"
    elif "consoles" in arg1:
        fileName = "resolution_db/consoles.txt"
        # Initialize coreName for consoles to allow log file creation
        coreName = "Consoles"
        console = True

    if "crtpi" in arg2:
        shaderName = "crtpi"
    elif "zfast" in arg2:
        shaderName = "zfast"

    if "curvature" in arg3:
        curvature = True
        scaleFactor = "N/A"
    else:
        curvature = False
        screenWidth = int(arg3)
        screenHeight = int(arg4)

        # Tolerance for "scale to fit" in either axis - the unit is the percentage of the game size in that direction. Default is 25 (i.e. 25%)
        tolerance = 25

        # Create output log file with detail info
        resolution = str(screenWidth) + "x" + str(screenHeight)
        outputLogFile = open(coreName + "_" + resolution + "_" + shaderName + ".csv", "w")
        outputLogFile.write("Tolerance : ,{}\n".format(tolerance))
        outputLogFile.write("ROM Name,X,Y,Orientation,Aspect1,Aspect2,ViewportWidth,ViewportHeight,HorizontalOffset,VerticalOffset,ScaleFactor\n")

    resolutionDbFile = open(fileName, "r" )
    print("Opened database file {}".format(fileName))
    if not curvature:
        print("created log file ./{}".format(outputLogFile.name))

    # Progress indicator
    print("Creating system-specific config files.\n")
    sys.stdout.write('[')
    sys.stdout.flush()
    gameCount = 0

    for gameInfo in resolutionDbFile:

        # Progress indicator
        gameCount = gameCount+1

        # Strip line breaks
        gameInfo = gameInfo.rstrip()

        # Parse DB info
        gameInfo = gameInfo.split(",")
        gameName = gameInfo[0]
        gameWidth = int(gameInfo[1])
        gameHeight = int(gameInfo[2])
        gameType = gameInfo[3]
        gameOrientation = gameInfo[4]
        aspectRatio = int(gameInfo[5]) / int(gameInfo[6])

        if console:
            coreName = gameName

        cfgFileName = gameName + ".cfg"

        # Create directory for cfgs, if it doesn't already exist
        if curvature:
            path = "curvature" + "/" + coreName + "/" + shaderName
        else:
            path = resolution + "/" + coreName + "/" + shaderName
        if not os.path.isdir(path):
            os.makedirs (path)

        # Progress indicator
        if (gameCount%100 == 0):
            sys.stdout.write('.')
            sys.stdout.flush()

        # Determine shader to use for non-vector games
        if not "vector" in gameType:
            if "vertical" in gameOrientation:
                if "crtpi" in shaderName:
                    if curvature:
                        shader = "crt-pi-curvature-vertical.glslp"
                    else:
                        shader = "crt-pi-vertical.glslp"
                elif "zfast" in shaderName:
                    if curvature:
                        shader = "zfast_crt_curve_vertical.glslp"
                    else:
                        shader = "zfast_crt_standard_vertical.glslp"
                
                # Calculate pixel 'squareness' and adjust gameHeight figure to keep the same aspect ratio, but with square pixels (keeping width as-was to avoid scaling artifacts)
                pixelSquareness = ((gameWidth/gameHeight)/aspectRatio)
                gameHeight = int(gameHeight * pixelSquareness)

            elif "horizontal" in gameOrientation:
                if "crtpi" in shaderName:
                    if curvature:
                        shader = "crt-pi-curvature.glslp"
                    else:
                        shader = "crt-pi.glslp"
                elif "zfast" in shaderName:
                    if curvature:
                        shader = "zfast_crt_curve.glslp"
                    else:
                        shader = "zfast_crt_standard.glslp"
                
                # Calculate pixel 'squareness' and adjust gameWidth figure to keep the same aspect ratio, but with square pixels (keeping height as-was)
                pixelSquareness = ((gameWidth/gameHeight)/aspectRatio)
                gameWidth = int(gameWidth / pixelSquareness)

            if not curvature:
                # Check scale factor in horizontal and vertical directions
                vScaling = screenHeight/gameHeight
                hScaling = screenWidth/gameWidth

                # Keep whichever scaling factor is smaller
                if vScaling < hScaling:
                    scaleFactor = vScaling
                else:
                    scaleFactor = hScaling

                # For vertical format games, width multiplies by an integer scale factor, height can multiply by the actual scale factor
                if "vertical" in gameOrientation:
                    # Pick whichever integer scale factor is nearest to the actual scale factor for the width without going outside the screen area
                    if (scaleFactor - int(scaleFactor) > 0.5 and gameWidth * int(scaleFactor + 1) < screenWidth):
                        viewportWidth = gameWidth * int(scaleFactor + 1)
                    else:
                        viewportWidth = gameWidth * int(scaleFactor)
                    viewportHeight = int(gameHeight * scaleFactor)
                    # If, somehow, the viewport height is less than the screen height, but it's within tolerance of the game height, scale to fill the screen vertically 
                    if screenHeight - viewportHeight < (gameHeight * (tolerance / 100)):
                        viewportHeight = screenHeight

                # For horizontal games, scale both axes by the scaling factor. If the resulting viewport size is within our tolerance for the game height or width, expand it to fill in that direction
                else:
                    viewportWidth = int(gameWidth * scaleFactor)
                    if screenWidth - viewportWidth < (gameWidth * (tolerance / 100)):
                        viewportWidth = screenWidth
                    viewportHeight = int(gameHeight * scaleFactor)
                    if screenHeight - viewportHeight < (gameHeight * (tolerance / 100)):
                        viewportHeight = screenHeight
                    # Add 'overscan' area for Nestopia consoles, as per original script (more or less)
                    if ("console" and "Nestopia" in coreName):
                        viewportHeight = viewportHeight + 8 * int(scaleFactor)

                # Center screen within target resolution
                viewportX = int((screenWidth - viewportWidth) / 2)
                viewportY = int((screenHeight - viewportHeight) / 2)

                outputLogFile.write("{},{},{},{},{},{},{},{},{},{},{}\n".format(gameInfo[0], gameInfo[1], gameInfo[2], gameInfo[4], gameInfo[5], gameInfo[6], viewportWidth, viewportHeight, viewportX, viewportY, scaleFactor))

        # Create cfg file
        newCfgFile = open(path + "/" + cfgFileName, "w")

        # Vector games shouldn't use shaders; disable them
        if "vector" in gameType:
            newCfgFile.write("# Auto-generated vector .cfg\n")
            newCfgFile.write("# Place in /opt/retropie/configs/all/retroarch/config/{}/\n".format(coreName))
            newCfgFile.write("video_shader_enable = \"false\"\n")

        # Write shader cfgs for non-vector games
        else:
            newCfgFile.write("# Auto-generated {} .cfg\n".format(shader))
            newCfgFile.write("# Game Title : {} , Width : {}, Height : {}, Aspect : {}:{}, Scale Factor : {}\n".format(gameName, gameWidth, gameHeight, int(gameInfo[5]), int(gameInfo[6]), scaleFactor))
            if not curvature:
                newCfgFile.write("# Screen Width : {}, Screen Height : {}\n".format(screenWidth, screenHeight))
            newCfgFile.write("# Place in /opt/retropie/configs/all/retroarch/config/{}/\n".format(coreName))
            newCfgFile.write("video_shader_enable = \"true\"\n")
            newCfgFile.write("video_shader = \"/opt/retropie/configs/all/retroarch/shaders/{}\"\n".format(shader))

            # Disable shader if the scale factor is less than 3
            if not curvature:
                if scaleFactor >= 3:
                    newCfgFile.write("aspect_ratio_index = \"23\"\n")
                    newCfgFile.write("custom_viewport_width = \"{}\"\n".format(viewportWidth))
                    newCfgFile.write("custom_viewport_height = \"{}\"\n".format(viewportHeight))
                    newCfgFile.write("custom_viewport_x = \"{}\"\n".format(viewportX))
                    newCfgFile.write("custom_viewport_y = \"{}\"\n".format(viewportY))
                else:
                    newCfgFile.write("# Insufficient resolution for good quality shader\n")
                    newCfgFile.write("video_shader_enable = \"false\"\n")

        newCfgFile.close()
    resolutionDbFile.close()

    # Progress indicator
    print("]\n")
    print("Done!\n")

    # Close output log file
    if not curvature:
        outputLogFile.close()
        print("Log written to ./{}  <--Delete if not needed".format(outputLogFile.name))
    print("Files written to ./{}/\nPlease transfer files to /opt/retropie/configs/all/retroarch/config/{}/\n".format(path, coreName))


def createZip(shaderName="crtpi", curvature=False, screenWidth=0, screenHeight=0):
    if "crtpi" in shaderName:
        if curvature:
            outputFileName = "crt-pi_configs_curvature"
            path = "curvature"
        else:
            resolution = str(screenWidth) + "x" + str(screenHeight)
            outputFileName = "crt-pi_configs_" + resolution
            path = resolution
    elif "zfast" in shaderName:
        if curvature:
            outputFileName = "zfast_configs_curvature"
            path = "curvature"
        else:
            resolution = str(screenWidth) + "x" + str(screenHeight)
            outputFileName = "zfast_configs_" + resolution
            path = resolution        
    outputFileName = outputFileName.replace(" ", "")
    outputFileName = outputFileName.lower()

    print("Creating zipfile {}".format(outputFileName))
    shutil.make_archive(outputFileName, "zip", path)

    # Delete config dirs
    print("Deleting temp directory: {}".format(path))
    shutil.rmtree(path)


if __name__ == "__main__":
    if "curvature" in sys.argv[3]:
        generateConfigs(sys.argv[1], sys.argv[2], sys.argv[3], 0)
    else:
        generateConfigs(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])
