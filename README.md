# RetroPie Shader Config Files

This script creates cfg files for optimum shader appearence for use with RetroPie Libretro cores. Works with the following cores:

  **mame2000-libretro** *(based on MAME 0.37b5)*<br>
  **mame2003-libretro** *(based on MAME 0.78)*<br>
  **mame2003-plus-libretro** *(based on MAME 0.78 + additions)*<br>
  **mame2010-libretro** *(based on MAME 0.139)*<br>
  **mame2015-libretro** *(based on MAME 0.160)*<br>
  **mame2016-libretro** *(based on MAME 0.174)*<br>
  **fbalpha2012** *(based on FB Alpha 0.2.97.30)*<br>
  **fbneo** *(based on FinalBurn Neo)*<br>
  **consoles** *(currently only Nestopia/NES)*<br>

### Usage:

python retropie_shader_configs.py \<*core*\> -s \<*shader*\> -c \<*curvature*\> -x \<*screen width*\> -y \<*screen height*\> -o \<*orientation*\>

or

python retropie_shader_configs.py -h

## Parameters:
  * \<*core*\>
  * -s \<*shader*\>
  * -c \<*curvature*\>
  * -x \<*screen width*\>
  * -y \<*screen height*\>
  * -o \<*orientation*\>
  * -h (*show help information*)

### Core (required):
  Select core for shader.
  * mame2000
  * mame2003
  * 2003plus
  * mame2010
  * mame2015
  * mame2016
  * fba2012
  * fbneo
  * consoles

### Shader (optional):
  Select shader to apply.
  * crtpi (*default*)
  * zfast

### Curvature (optional):
  Use curvature shader (true) or standard shader (false).
  * true
  * false (*default*)

### Screen Width (optional):
  Uneeded/ignored if curvature is true.
  * any width (*default=1920*)

### Screen Height (optional):
  Uneeded/ignored if curvature is true.
  * any height (*default=1080*)

### Orientation (optional):
  Select game orientation--i.e., horizontal games only, vertical games only or all games
  * horizontal
  * vertical
  * all (*default*)

### Help (optional):
  Use seperately to show basic help information.
  * -h

## Examples:

Clone into a directory, navigate to that directory from a command prompt, and then run the script. Some examples are shown below:

  ```python retropie_shader_configs.py mame2003 -s crtpi -x 1920 -y 1080```  

  ```python retropie_shader_configs.py mame2003 -s crtpi -c true -o horizontal```  

  ```python retropie_shader_configs.py 2003plus -s zfast -x 1280 -y 720 -o vertical```  

  ```python retropie_shader_configs.py 2003plus -s zfast -c true```  

  ```python retropie_shader_configs.py fbneo -s crtpi -c false -x 1920 -y 1080 -o all```  

  ```python retropie_shader_configs.py fbneo```  

This will create a folder with the resolution, i.e., *1920x1080* (or *curvature*). Beneath that folder will be another subfolder with the core name, i.e., *MAME 2003 (0.78)*. The individual cfg files are stored in the core subfolder. When the script completes it will print the path where you should transfer the files within RetroPie.

There's also a bat file (retropie_shader_configs.bat) you may use to generate the cfg files. It will generate the cfg and zip files containing the same information in the root. You may modify the bat file to fit you needs for different cores, shaders and resolutions. Take a look at the bat file for examples, it's fairly self-explanatory.

For information and an explanation on how the cfg files improve shaders see the official RetroPie forum thread located [here.](https://retropie.org.uk/forum/topic/4046/crt-pi-shader-users-reduce-scaling-artifacts-with-these-configs-in-lr-mame2003-lr-fbalpha-lr-nestopia-and-more-to-come) You can also view additional information from the RetroPie documentation on "Shaders and Smoothing" [here.](https://retropie.org.uk/docs/Shaders-and-Smoothing/)

## Additional Information:

### Resolution Databases:
Due to updates there may be certain cores with missing, incorrect or extraneous information in the resolution db files (located in the *resolution_db* folder). They are comma delimited text files that are very easy to modify. You can update, delete or add new entries but keep only one game entry per line. You're more than welcome to submit a PR with any corrections or if you prefer to just leave a message, open an issue with the correct information and I'll update the DB files. Whatever you're more comfortable with works.

Below is an example from a resolution db file for the game ```1942```. The fields in order:

*ROM Name, screenResX, screenResY, Type (raster or vector), Orientation (horizontal or vertical), aspectRatioX, aspectRatioY*

  ```1942,256,224,raster,vertical,3,4```

If the information looks incorrect I usually check the DAT first (if it contains complete XML info), followed by the core drivers and if all else fails search the Arcade Database - ArcadeItalia located [here](http://adb.arcadeitalia.net/) for the good information.

Also worth noting, I removed all entries with the *\<isbios\>*, *\<isdevice\>* or *\<ismechanical\>* tags. There are some other miscellaneous drivers/entries in the newer DAT's that aren't arcade machine related and will be removed in time.

### Game Type:
Just a quick note on the *Type* field in the resolution databases.

Vector games (i.e., ```asteroids``` or ```tempest```) are included in some of the database files but typically are not used in conjunction with shaders. The *Type* field is used to identify and disable them.

### Scale Factor:
Inside the cfg files you'll find the calculated scale factor (nonapplicable for curvature shaders). Typically if the scale factor is less than 3 the shaders won't look very pleasant and are disabled in the cfg files. See the .csv log file, located in the script folder, to see which games have a scale factor less than 3.

You're more than welcome to enable them for a particular game to decide for yourself. A few examples of this are ```rampage``` and ```popeye``` that both have scale factors below 3.

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

Also a special thanks to the [RetroPie](https://retropie.org.uk) and [Libretro](https://github.com/libretro) development teams and others who make their work publicly available and share their knowledge. Without them this project wouldn't have been possible.
