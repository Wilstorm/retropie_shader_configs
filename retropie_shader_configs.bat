@echo off

python retropie_shader_configs.py mame2000 -s crtpi -c false -x 1920 -y 1080 -o all
python retropie_shader_configs.py mame2003 -s crtpi -c false -x 1920 -y 1080 -o all
python retropie_shader_configs.py 2003plus -s crtpi -c false -x 1920 -y 1080 -o all
python retropie_shader_configs.py mame2010 -s crtpi -c false -x 1920 -y 1080 -o all
python retropie_shader_configs.py mame2015 -s crtpi -c false -x 1920 -y 1080 -o all
python retropie_shader_configs.py mame2016 -s crtpi -c false -x 1920 -y 1080 -o all
python retropie_shader_configs.py fba2012 -s crtpi -c false -x 1920 -y 1080 -o all
python retropie_shader_configs.py fbneo -s crtpi -c false -x 1920 -y 1080 -o all
python retropie_shader_configs.py consoles -s crtpi -c false -x 1920 -y 1080 -o all
python -c "import retropie_shader_configs; retropie_shader_configs.createZip('crtpi',False,1920,1080)"

python retropie_shader_configs.py mame2000 -s crtpi -c false -x 1280 -y 720 -o all
python retropie_shader_configs.py mame2003 -s crtpi -c false -x 1280 -y 720 -o all
python retropie_shader_configs.py 2003plus -s crtpi -c false -x 1280 -y 720 -o all
python retropie_shader_configs.py mame2010 -s crtpi -c false -x 1280 -y 720 -o all
python retropie_shader_configs.py mame2015 -s crtpi -c false -x 1280 -y 720 -o all
python retropie_shader_configs.py mame2016 -s crtpi -c false -x 1280 -y 720 -o all
python retropie_shader_configs.py fba2012 -s crtpi -c false -x 1280 -y 720 -o all
python retropie_shader_configs.py fbneo crtpi -s crtpi -c false -x 1280 -y 720 -o all
python retropie_shader_configs.py consoles crtpi -s crtpi -c false -x 1280 -y 720 -o all
python -c "import retropie_shader_configs; retropie_shader_configs.createZip('crtpi',False,1280,720)"

python retropie_shader_configs.py mame2000 -s crtpi -c true -o all
python retropie_shader_configs.py mame2003 -s crtpi -c true -o all
python retropie_shader_configs.py 2003plus -s crtpi -c true -o all
python retropie_shader_configs.py mame2010 -s crtpi -c true -o all
python retropie_shader_configs.py mame2015 -s crtpi -c true -o all
python retropie_shader_configs.py mame2016 -s crtpi -c true -o all
python retropie_shader_configs.py fba2012 -s crtpi -c true -o all
python retropie_shader_configs.py fbneo -s crtpi -c true -o all
python -c "import retropie_shader_configs; retropie_shader_configs.createZip('crtpi',True)"

python retropie_shader_configs.py mame2000 -s zfast -c false -x 1920 -y 1080 -o all
python retropie_shader_configs.py mame2003 -s zfast -c false -x 1920 -y 1080 -o all
python retropie_shader_configs.py 2003plus -s zfast -c false -x 1920 -y 1080 -o all
python retropie_shader_configs.py mame2010 -s zfast -c false -x 1920 -y 1080 -o all
python retropie_shader_configs.py mame2015 -s zfast -c false -x 1920 -y 1080 -o all
python retropie_shader_configs.py mame2016 -s zfast -c false -x 1920 -y 1080 -o all
python retropie_shader_configs.py fba2012 -s zfast -c false -x 1920 -y 1080 -o all
python retropie_shader_configs.py fbneo -s zfast -c false -x 1920 -y 1080 -o all
python retropie_shader_configs.py consoles -s zfast -c false -x 1920 -y 1080 -o all
python -c "import retropie_shader_configs; retropie_shader_configs.createZip('zfast',False,1920,1080)"

python retropie_shader_configs.py mame2000 -s zfast -c false -x 1280 -y 720 -o all
python retropie_shader_configs.py mame2003 -s zfast -c false -x 1280 -y 720 -o all
python retropie_shader_configs.py 2003plus -s zfast -c false -x 1280 -y 720 -o all
python retropie_shader_configs.py mame2010 -s zfast -c false -x 1280 -y 720 -o all
python retropie_shader_configs.py mame2015 -s zfast -c false -x 1280 -y 720 -o all
python retropie_shader_configs.py mame2016 -s zfast -c false -x 1280 -y 720 -o all
python retropie_shader_configs.py fba2012 -s zfast -c false -x 1280 -y 720 -o all
python retropie_shader_configs.py fbneo -s zfast -c false -x 1280 -y 720 -o all
python retropie_shader_configs.py consoles -s zfast -c false -x 1280 -y 720 -o all
python -c "import retropie_shader_configs; retropie_shader_configs.createZip('zfast',False,1280,720)"

python retropie_shader_configs.py mame2000 -s zfast -c true -o all
python retropie_shader_configs.py mame2003 -s zfast -c true -o all
python retropie_shader_configs.py 2003plus -s zfast -c true -o all
python retropie_shader_configs.py mame2010 -s zfast -c true -o all
python retropie_shader_configs.py mame2015 -s zfast -c true -o all
python retropie_shader_configs.py mame2016 -s zfast -c true -o all
python retropie_shader_configs.py fba2012 -s zfast -c true -o all
python retropie_shader_configs.py fbneo -s zfast -c true -o all
python -c "import retropie_shader_configs; retropie_shader_configs.createZip('zfast',True)"

pause
