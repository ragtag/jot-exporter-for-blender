# "jot" Exporter for Blender

Jot is a very cool standalone WYSIWYG interactive stylized renderer, developed at Princeton University around 2002-03. It has some unique features that make it very interesting even now, more than 10 years later.

<img src="https://ragnarb.com/blog/wp-content/uploads/2013/04/david.gif" alt="Model of David by gabrielmda" />
Model of David by <a href="http://www.blendswap.com/blends/view/65345" target="_blank" rel="noopener">gabrielmda</a> rendered in Jot


Jot can render stylized silhouettes of animated 3D models with temporal coherence, which means the lines don't jiggle or flicker as the model moves. How the outline is rendered is defined by drawing a sample line, and applying the same style to the whole model. In addition, Jot has support for hatching and drawing in details at different levels of detail, plus some basic surface shading.

Jot works in real-time using OpenGL, so the artist can instantly see what she is doing. This means that rendering is extremely fast, as it's simply a question of stepping through the frames, and writing out images.

Unfortunately Jot hasn't been actively developed for years, and there has been no easy way to get your models and animation into Jot for years, until now. That where my Jot Exporter for Blender comes in. It let's you export your models and animation from Blender 2.6x to Jot. It's still very much in beta, but as far as I know everything works (see limitations below). My hope is that this exporter will bring renewed interest in Jot, and maybe one day we'll see it [brought back to life][1].

<a href="https://www.youtube.com/watch?v=gT9qU_fJNuw" target="_blank">Here</a> is a video from Siggraph 2002, that demonstrates some of the features of Jot.


# Installation

You can get Jot for Windows from <a title="Jot - official home page at Princeton" href="http://jot.cs.princeton.edu/" target="_blank" rel="noopener">here</a> (it can run under Wine, see below) and the source code for it <a title="jot-lib Google code project" href="https://github.com/QuLogic/jot-lib" target="_blank" rel="noopener">here</a>. It includes some documentation, tutorials and sample files to get you started.

  1. Download the <a title="Download Jot Exporter for Blender" href="https://github.com/ragtag/jot-exporter-for-blender/releases" target="_blank" rel="noopener">Jot exporter here</a> and extract it.
  2. Copy the io\_export\_jot folder to your blender addons folder (blender/2.82/scripts/addons).
  3. Hit F8 to reload addons in Blender and go to Edit>Preferences, and look for "Export to Jot stylized render" under the Addons tab and activate it.
  4. Now you should have a new entry for exporting to Jot in you File>Export menu.

# Exporting Your Models and Animation to Jot

Exporting you models to Jot is pretty straight forward.

  1. Select the models you want to export. You don't need to select the camera, as the active camera gets exported automatically. Only select geometry, as selecting armatures, lattices and other objects, will likely break the export.
  2. Choose File>Export>Jot Stylized Renderer (.jot)
  3. If you want to export animation, check the Export Animation checkbox on the left hand side, and choose a frame range. Also make sure to create a folder for the exported animation, as the exporter creates several files for each frame of animation, often resulting in literally hundreds of files.
  4. Give your export a name, and hit Export JOT. For long animations, or lots of polygons, this can take a short while.

The size of the viewport in Jot, depends on the render resolution you set in Blender.

# Running Jot on Windows

Even though jot was written back around 2003, it still runs fine one Windows XP, 7 and 8 (I haven't tested it on 10), and on 64-bit systems. I've tested it with Intel, ATI/AMD and Nvidia graphics card, and all work, though on the old integrated Intel card in my laptop it's really slow. Read the instructions in the README.txt file that comes with Jot on how to run it.

**Note!** If you have an Nvidia card with Optimus technology (most recent mobile Nvidia cards have this), you need to right click "jot-cmd" and choose "Run with Nvidia Graphics". Thanks to David Kolb for pointing this out.

# Running Jot on Linux

If you happen to be a skilled C++ developer, I'm sure you can figure out how to compile it from source. It was originally written to support both Linux and OSX, but I've yet to get it to compile on my 64-bit Linux.

Luckily, Jot can run under [Wine][2]. To simplify running Jot on Linux I've written a little shell script that helps launch it. You can download it from [here][3]. I've tested it on Ubuntu 12.04, but it should work on other distros.

You need Wine installed with working OpenGL, and a copy of  <a title="You can download it from Princeton" href="http://jot.cs.princeton.edu/" target="_blank" rel="noopener">Jot</a>. The script assumes the Jot unpacked in your home folder. If you've placed Jot somewhere else, just open the script in a text editor and follow the instructions there. Next place the script somewhere in PATH, such as /usr/local/bin/. Now you can run jot directly from the terminal, by simply typing &#8216;jot YOUR_FILE.jot'.

It's also possible to run Jot manually, though the process is a little bit more convoluted.

  1. Download the Windows version of jot, and place it where you prefer (~/.wine/drive_c/jot for instance).
  2. Edit jot/batch/config, so the line that says "set JOT\_ROOT=C:\rkalnins\jot-distrib-test\jot" points to where you placed you jot folder (e.g. "set JOT\_ROOT=C:\jot" if you placed it in ~/.wine/drive_c/jot)
  3. Start a command prompt (cmd.exe) in wine. One Ubuntu 12.04 this would be  
    &#8211; wine /usr/lib/i386-linux-gnu/wine/fakedlls/cmd.exe
  4. You now have a windows command prompt. Use it to got into the batch folder, and run the jot-config.bat  
    &#8211; C:  
    &#8211; cd C:\jot\batch  
    &#8211; jot-config.bat
  5. Go a folder you've exported your models or animation to in cmd.exe, and run:  
    &#8211; jotq yourfile.jot

This should open up your file in Jot. While it does work, it outputs a lot of errors to the terminal. You can improve the frame rate a little by hiding the terminal.

This was tested on Ubuntu 18.04, 64-bit, using Wine 3.0.

# Updating Your Animation

When you save changes in Jot (hit 's' on the keyboad), it writes out a .npr file. This file stores all the annotation information you've added in Jot. The exporter does not create this file, which means that you can modify your animation in Blender, and re-export, and the drawing you've done in Jot will remain intact. Note that Jot uses the file and the model names to know which annotation to apply to which model, so if you rename your file or models, this will not work correctly.

# Rendering Your Animation

First hit 'a' in the viewport to turn on anti-aliasing.

Then to render out a still image, simply hit 'g' in the Jot viewport. This should write out a png image in the folder you started jot from.

To render out animation, you need to do the following.

  1. Hit 'X' (capital X), to engage animation mode.
  2. Hit '-' (dash), to engage time sync.
  3. Hit '*' (asterix), to set it to render to file.
  4. Hit '/' to play back the animation, which will write a png file to disk for each frame.

If you would rather just render out the outlines, and use Cycles or Eevee for the surface, you can do this by making the basecoat transparent:

  1. Use Next Mode button to get to the Basecoat Editor.
  2. Select your model by clicking on it.
  3. In the Basecoat Editor hit the 'Add' button to add a Normal material.
  4. Un-check the 'Transparency to Background' check box.
  5. Slide the Alpha slider to zero.

# Known Limitations

If you find any bugs, please feel free to comment below.

  * Output resolution in Jot seems to be limited to the size of the viewport, which means that you can't easily render anything above your screen's resolution.
  * Exporting crease info does not work correctly on subdiv models. The only workaround is to Apply the subdiv modifiers, and add creases to the subdivided mesh afterwards. Creases show up as lines in Jot, so can be quite useful.
  * Not tested on OSX, but should work.

# Reference

  * You will find the Jot user manual in the folder alongside Jot itself.
  * JOT File Format Description 
      * <a href="http://jot.cs.princeton.edu/jot-file-format.txt" target="_blank" rel="noopener">http://jot.cs.princeton.edu/jot-file-format.txt</a>
  * Coherent Stylized Silhouettes 
      * [https://gfx.cs.princeton.edu/pubs/Kalnins\_2003\_CSS/index.php][4]
  * WYSIWYG NPR: Drawing Strokes Directly on 3D Models 
      * <a href="http://gfx.cs.princeton.edu/pubs/Kalnins_2002_WND/wnpr-final.pdf" target="_blank" rel="noopener">http://gfx.cs.princeton.edu/pubs/Kalnins_2002_WND/wnpr-final.pdf</a>
  * WYSIWYG NPR: Interactive Stylization for Stroke-Based Rendering of 3D Animation 
      * <a href="http://gfx.cs.princeton.edu/pubs/_2004_WNI/" target="_blank" rel="noopener">http://gfx.cs.princeton.edu/pubs/_2004_WNI/</a>

 [1]: https://ragnarb.com/resurrecting-jot/ "Resurrecting Jot"
 [2]: http://www.winehq.org/
 [3]: https://ragnarb.com/downloads/jot.tar.gz "Jot Launcher for Linux"
 [4]: https://gfx.cs.princeton.edu/pubs/Kalnins_2003_CSS/index.php
