# RetroPie Shader Config Files

This script creates cfg files for optimum shader appearence for use with RetroPie. Works with the following cores:

mame2000-libretro (MAME 0.37b5)
mame2003-libretro (MAME 0.78)
mame2003-plus-libretro (MAME 0.78 + plus additions)
mame2010-libretro (MAME 0.139)
mame2015-libretro (MAME 0.160)
mame2016-libretro (MAME 0.174)
consoles (currently only Nestopia/NES)

### Usage:

python pi_shader_configs.py \<*core*\> \<*shader*\> \<*screen width*\> \<*screen height*\>

## Parameters:

  * core (*mame2000*, *mame2003*, *2003plus*, etc.)
  * shader (*crtpi* or *zfast*)
  * screen width (i.e. *1920* or *curvature*)
  * screen height (i.e. *1080* or *leave blank*)

**Core:**
  * mame2000-libretro = *mame2000*
  * mame2003-libretro = *mame2003*
  * mame2003-plus-libretro = *2003plus*
  * mame2010-libretro = *mame2010*
  * mame2015-libretro = *mame2015*
  * Nestopia/NES = *consoles*

**Shader:**
  * *crtpi*
  * *zfast*

**Screen Width:**
  * any width or *curvature*

**Screen Height:**
  * any height *or* leave blank (if using *curvature* in width)

## Examples:

Clone into a directory, navigate to that directory from a command prompt, and then run the script. Some examples are shown below:

  ```python pi_shader_configs.py mame2003 crtpi 1920 1080```  

  ```python pi_shader_configs.py mame2003 crtpi curvature```  

  ```python pi_shader_configs.py 2003plus zfast 1280 720```  

  ```python pi_shader_configs.py 2003plus zfast curvature```  

This will create a folder with the resolution, i.e., *1920x1080* (or *curvature*). Beneath that folder will be another subfolder with the core name, i.e., *MAME 2003 (0.78)*. The individual cfg files are stored in the core subfolder. When the script completes it will print the path where you should transfer the files within RetroPie.

There's also a bat file (pi_shader_configs.bat) you may use to generate the cfg files. It will generate the cfg and zip files containing the same information in the root. You may modify the bat file to fit you needs for different cores, shaders and resolutions. Take a look at the bat file for examples, it's fairly self-explanatory.

For information and an explanation on how the cfg files improve shaders see the official RetroPie forum thread located [here.](https://retropie.org.uk/forum/topic/4046/crt-pi-shader-users-reduce-scaling-artifacts-with-these-configs-in-lr-mame2003-lr-fbalpha-lr-nestopia-and-more-to-come) You can also view additional information from the RetroPie documentation on "Shaders and Smoothing" [here.](https://retropie.org.uk/docs/Shaders-and-Smoothing/)

## Additional Information:

### Resolution Databases:
Due to core updates or errors during the creation process there may be certain games with missing or incorrect information from the resolution db files (located in the *resolution_db* folder). These are comma delimited text files that are very easy to modify or add new entries. One game entry per line. If you prefer to just leave a message with the correct information I'll update the database files in the repo.

Below is an example from a resolution db file for the game ```1942```. The fields in order:

*ROM Name, screenResX, screenResY, Type (raster or vector), Orientation (horizontal or vertical), aspectRatioX, aspectRatioY*

  ```1942,256,224,raster,vertical,3,4```

If the information looks incorrect I usually check the DAT first (if it contains complete XML info), followed by the core drivers and if all else fails search the Arcade Database - ArcadeItalia located [here](http://adb.arcadeitalia.net/) for the good information.

Also worth noting, I removed all entries with the *\<isbios\>*, *\<isdevice\>* or *\<ismechanical\>* tags. There are some other miscellaneous drivers/entries in the newer DAT's that aren't arcade machine related and will be removed in time.

### Game Type:
Just a quick note on the *Type* field in the resolution databases.

Vector games (i.e., ```asteroids``` or ```tempest```) are included in some of the database files but typically are not used in conjunction with shaders. The *Type* field is used to identify and disable them.

### Scale Factor:
Inside the cfg files you'll find the calculated scale factor (nonapplicable for curvature shaders). Typically if the scale factor is less than 3 the shaders won't look very pleasant and are disabled in the cfg files. You're more than welcome to enable them for a particular game to decide for yourself. A few examples of this are ```rampage``` and ```popeye``` that both have scale factors below 3.

## Miscellaneous:

### crt-pi Shader:
For additional information relating to the crt-pi shader see this post [here](https://retropie.org.uk/forum/topic/897/updated-crt-pi-shader) or for additional tweaks for video smoothing see the post [here.](https://retropie.org.uk/forum/topic/2592/video-smoothing-yay-or-nay/25) The RetroPie forums located [here](https://retropie.org.uk/forum/) contain a lot of good information about shaders.

### zfast Shader:
For additional information relating to the zfast shader see this post [here.](https://retropie.org.uk/forum/topic/13356/new-crt-lcd-shaders-for-rpi3-they-run-at-60fps-at-higher-resolutions-and-are-configurable)  The RetroPie forums located [here](https://retropie.org.uk/forum/) contain a lot of good information about shaders.

## Other:

### Requirements:
You need Pythong 2.7 (possibly older versions) to run the script. You'll also need to be running RetroPie 4.x or newer.

NOTE: For the lr-nestopia configs, you must set the lr-nestopia emulator as your default NES emulator. lr-fceumm (the default) causes lag with the shader, even for an overclocked pi3.

### Thanks:
Thanks to dankcushions for creating the original script, Andrew-H2O for refining the algorithms and UDb23 for the DB files.

A special thanks to davej for creating the crt-pi shader and ghogan42 for creating zfast.

Also a special thanks to the [Libretro](https://github.com/libretro) development team and others who make their work publicly available and share their knowledge. Without them this project wouldn't have been possible.
