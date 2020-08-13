from sentinel2 import *

# Get notebookname
notebookbasename = os.path.basename(notebook_path())
notebookname = os.path.splitext(notebookbasename)[0]
print("JupyterNotebook name : ", notebookname)


# FONT preparation setting. This font will be printed on each image
# 1. Download the font file from https://osdn.net/dl/mplus-fonts/mplus-TESTFLIGHT-063a.tar.xz
# 2. Execute thise command on your environment: wget https://osdn.net/dl/mplus-fonts/mplus-TESTFLIGHT-063a.tar.xz
# 3. Check the downloaded file: ls -l mplus-TESTFLIGHT-063a.tar.xz
# 4. -rw-r--r-- 1 jovyan users 10371708 Apr 23  2019 mplus-TESTFLIGHT-063a.tar.xz
# 5. Put the downloaded file to the same directory as your JupyterNotebook file

cwd = os.getcwd()
suffix = '.ttf'
base_filename = 'mplus-1c-bold'
fontfile = os.path.join(cwd,'mplus-TESTFLIGHT-063a',base_filename + suffix)

# Extract the font file. You may skip the process if it already there
if os.path.isfile(fontfile):
    print("Font file exist : " + fontfile)
else: 
    print("Extracting font file...")
    
    if os.path.isfile("mplus-TESTFLIGHT-063a.tar.xz"):
        !xz -dc mplus-TESTFLIGHT-*.tar.xz | tar xf -
    else:
        print("Font file extraction failed!")
        
    print("Font file extracted")
    if os.path.isfile(fontfile):
        print(fontfile)
