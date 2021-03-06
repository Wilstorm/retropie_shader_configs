# creates cfg files for retropie using crt-pi or zfast
# params are:
# * core (eg mame2003, mame2003-plus, fbneo, etc.)
# * shader (eg crtpi or zfast)
# * curvature (eg true or false)
# * screen width (eg 1920)
# * screen height (eg 1080)
# * orientation (eg horizontal, vertical or all)
# example usage:
# python retropie_shader_configs.py mame2003 -s crtpi -c false -x 1920 -y 1080 -o all
# python retropie_shader_configs.py fbneo -s zfast -c true -o horizontal
# python retropie_shader_configs.py mame2016 -s zfast -c false -x 1280 -y 720 -o vertical
# python retropie_shader_configs.py 2003plus -s crtpi -c true -o all
# python -c "import retropie_shader_configs; retropie_shader_configs.createZip('mame2003')"


from __future__ import division
import argparse
import sys
import os
import shutil


def main():

    parser = argparse.ArgumentParser(prog='retropie_shader_configs.py',usage='python %(prog)s core [options]',description='Create shaders for RetroPie Libretro cores', epilog='Example: python retropie_shader_configs.py mame2003 -s crtpi -c false -x 1920 -y 1080 -o all')
    parser.add_argument('core', metavar='core', action='store', choices=['mame2000','mame2003','2003plus','mame2010','mame2015','mame2016','fba2012','fbneo','consoles'], help='core name (mame2000|mame2003|2003plus|mame2010|mame2015|mame2016|fba2012|fbneo|consoles)')
    parser.add_argument('-s', metavar='shader', action='store', default='crtpi', choices=['crtpi','zfast'], help='select shader (crtpi|zfast) default: crtpi')
    parser.add_argument('-c', metavar='curvature', action='store', default='false', choices=['true','false'], help='use curvature with shader (true|false) default: false')
    parser.add_argument('-x', metavar='screen width', action='store', default=1920, type=int, help='any screen width (unneeded/ignored if curvature is true) default: 1920')
    parser.add_argument('-y', metavar='screen height', action='store', default=1080, type=int, help='any screen height (unneeded/ignored if curvature is true) default: 1080')
    parser.add_argument('-o', metavar='orientation', action='store', default='all', choices=['horizontal','vertical','all'], help='select game orientation--i.e., horizontal games only, vertical games only or all (horizontal|vertical|all) default: all')

    #args = parser.parse_args(args=None if sys.argv[1:] else ['--help'])
    args = parser.parse_args()

    console = False
    if "mame2000" in args.core:
        fileName = "resolution_db/mame2000.txt"
        coreName = "MAME 2000"
    elif "mame2003" in args.core:
        fileName = "resolution_db/mame2003.txt"
        coreName = "MAME 2003 (0.78)"
    elif "2003plus" in args.core:
        fileName = "resolution_db/mame2003-plus.txt"
        coreName = "MAME 2003-Plus"
    elif "mame2010" in args.core:
        fileName = "resolution_db/mame2010.txt"
        coreName = "MAME 2010"
    elif "mame2015" in args.core:
        fileName = "resolution_db/mame2015.txt"
        coreName = "MAME 2015"
    elif "mame2016" in args.core:
        fileName = "resolution_db/mame2016.txt"
        coreName = "MAME 2016"
    elif "fba2012" in args.core:
        fileName = "resolution_db/fba2012.txt"
        coreName = "FB Alpha"
    elif "fbneo" in args.core:
        fileName = "resolution_db/fbneo.txt"
        coreName = "FinalBurn Neo"
    elif "consoles" in args.core:
        fileName = "resolution_db/consoles.txt"
        # Initialize coreName for consoles to allow log file creation
        coreName = "Consoles"
        console = True

    coreDir = args.core
    shaderName = args.s
    orientation = args.o

    # Initialize flags for selected game orientation
    hFlag = True
    vFlag = True
    if "horizontal" in orientation:
        vFlag = False
    elif "vertical" in orientation:
        hFlag = False

    if "true" in args.c:
        curvature = True
        scaleFactor = "N/A"
        resolution = "curvature"
    else:
        curvature = False
        screenWidth = args.x
        screenHeight = args.y
        resolution = str(screenWidth) + "x" + str(screenHeight)

        # Tolerance for "scale to fit" in either axis - the unit is the percentage of the game size in that direction. Default is 25 (i.e., 25%)
        tolerance = 25

        # Create output log file in csv format with per game detail info
        outputLogFile = open(coreDir + "_" + resolution + "_" + shaderName + "_" + orientation + ".csv", "w")
        outputLogFile.write("Tolerance : ,{}\n".format(tolerance))
        outputLogFile.write("ROM Name,X,Y,Orientation,Aspect1,Aspect2,ViewportWidth,ViewportHeight,HorizontalOffset,VerticalOffset,ScaleFactor\n")

    # Create directory for cfgs, if it doesn't already exist
    path = coreDir + "/" + resolution + "/" + shaderName + "/" + orientation
    if not os.path.isdir(path):
        os.makedirs (path)

    resolutionDbFile = open(fileName, "r" )
    print("Opened database file {}".format(fileName))
    if not curvature:
        print("created log file ./{}".format(outputLogFile.name))
    print("Creating system-specific config files.\n")

    # Progress indicator
    sys.stdout.write('[')
    sys.stdout.flush()
    gameCount = 0

    for gameInfo in resolutionDbFile:

        # Progress indicator
        gameCount += 1
        if (gameCount%100 == 0):
            sys.stdout.write('.')
            sys.stdout.flush()

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

        # Generate cfgs for selected game orientation only
        if "horizontal" in gameOrientation and hFlag or "vertical" in gameOrientation and vFlag:

            # Determine shader type for all non-vector games
            if not "vector" in gameType:
                shaderType = shader(curvature, shaderName, gameOrientation)

                # Perform calculations for non-curvature games only
                if not curvature:
                    if "horizontal" in gameOrientation:
                        # Calculate pixel 'squareness' and adjust gameWidth figure to keep the same aspect ratio, but with square pixels (keeping height as-was)        
                        gameWidth = pixel_squareness(gameWidth, gameHeight, aspectRatio, gameOrientation)

                    elif "vertical" in gameOrientation:
                        # Calculate pixel 'squareness' and adjust gameHeight figure to keep the same aspect ratio, but with square pixels (keeping width as-was to avoid scaling artifacts)
                        gameHeight = pixel_squareness(gameWidth, gameHeight, aspectRatio, gameOrientation)

                    # Check scale factor in horizontal and vertical directions; keep whichever scaling factor is smaller
                    scaleFactor = scale_factor(gameWidth, screenWidth, gameHeight, screenHeight)

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

                    # Round to hundredths before writing shader cfgs below (or conflicts with curvature "N/A")
                    scaleFactor = round(scaleFactor, 2)

            # Create cfg file
            newCfgFile = open(path + "/" + cfgFileName, "w")

            # Vector games shouldn't use shaders; disable them
            if "vector" in gameType:
                newCfgFile.write("# Auto-generated vector .cfg\n")
                newCfgFile.write("# Place in /opt/retropie/configs/all/retroarch/config/{}/\n".format(coreName))
                newCfgFile.write("video_shader_enable = \"false\"\n")

            # Write shader cfgs for all non-vector games
            else:
                newCfgFile.write("# Auto-generated {} shader configuration file\n".format(shaderName))
                newCfgFile.write("# Game Title : {}, Width : {}, Height : {}, Aspect : {}:{}, Scale Factor : {}\n".format(gameName, gameWidth, gameHeight, int(gameInfo[5]), int(gameInfo[6]), scaleFactor))
                if not curvature:
                    newCfgFile.write("# Screen Width : {}, Screen Height : {}\n".format(screenWidth, screenHeight))
                newCfgFile.write("# Place in /opt/retropie/configs/all/retroarch/config/{}/\n".format(coreName))
                newCfgFile.write("video_shader_enable = \"true\"\n")
                newCfgFile.write("video_shader = \"/opt/retropie/configs/all/retroarch/shaders/{}\"\n".format(shaderType))

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


def shader(curvature, shaderName, gameOrientation):
    if "vertical" in gameOrientation:
        if "crtpi" in shaderName:
            if curvature:
                shaderType = "crt-pi-curvature-vertical.glslp"
            else:
                shaderType = "crt-pi-vertical.glslp"
        elif "zfast" in shaderName:
            if curvature:
                shaderType = "zfast_crt_curve_vertical.glslp"
            else:
                shaderType = "zfast_crt_standard_vertical.glslp"
    elif "horizontal" in gameOrientation:
        if "crtpi" in shaderName:
            if curvature:
                shaderType = "crt-pi-curvature.glslp"
            else:
                shaderType = "crt-pi.glslp"
        elif "zfast" in shaderName:
            if curvature:
                shaderType = "zfast_crt_curve.glslp"
            else:
                shaderType = "zfast_crt_standard.glslp"
    return shaderType


def pixel_squareness(gameWidth, gameHeight, aspectRatio, gameOrientation):
    pixelSquareness = ((gameWidth / gameHeight) / aspectRatio)
    if "horizontal" in gameOrientation:
        psTemp = int(gameWidth / pixelSquareness)
    else:
        psTemp = int(gameHeight * pixelSquareness)
    return psTemp


def scale_factor(gameWidth, screenWidth, gameHeight, screenHeight):
    hScaling = screenWidth / gameWidth
    vScaling = screenHeight / gameHeight
    if hScaling < vScaling:
        scaleFactor = hScaling
    else:
        scaleFactor = vScaling
    return scaleFactor


def createZip(coreName="mame2003"):
    path = coreName
    outputFileName = coreName + "_retropie_shader_configs"
    #outputFileName = outputFileName.replace(" ", "_")
    #outputFileName = outputFileName.lower()

    print("Creating zipfile {}".format(outputFileName))
    shutil.make_archive(outputFileName, "zip", path)

    # Delete config dirs
    print("Deleting temp directory: {}".format(path))
    shutil.rmtree(path)


if __name__ == "__main__":
    main()
