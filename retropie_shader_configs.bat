@echo off

python retropie_shader_configs.py 2003plus crtpi 1920 1080
python retropie_shader_configs.py mame2003 crtpi 1920 1080
python retropie_shader_configs.py consoles crtpi 1920 1080
python -c "import retropie_shader_configs; retropie_shader_configs.createZip('crtpi',False,1920,1080)"

python retropie_shader_configs.py 2003plus crtpi 1280 720
python retropie_shader_configs.py mame2003 crtpi 1280 720
python retropie_shader_configs.py consoles crtpi 1280 720
python -c "import retropie_shader_configs; retropie_shader_configs.createZip('crtpi',False,1280,720)"

python retropie_shader_configs.py 2003plus crtpi curvature
python retropie_shader_configs.py mame2003 crtpi curvature
python -c "import retropie_shader_configs; retropie_shader_configs.createZip('crtpi',True)"

python retropie_shader_configs.py 2003plus zfast 1920 1080
python retropie_shader_configs.py mame2003 zfast 1920 1080
python retropie_shader_configs.py consoles zfast 1920 1080
python -c "import retropie_shader_configs; retropie_shader_configs.createZip('zfast',False,1920,1080)"

python retropie_shader_configs.py 2003plus zfast 1280 720
python retropie_shader_configs.py mame2003 zfast 1280 720
python retropie_shader_configs.py consoles zfast 1280 720
python -c "import retropie_shader_configs; retropie_shader_configs.createZip('zfast',False,1280,720)"

python retropie_shader_configs.py 2003plus zfast curvature
python retropie_shader_configs.py mame2003 zfast curvature
python -c "import retropie_shader_configs; retropie_shader_configs.createZip('zfast',True)"

pause
