# em_scripts
(potentially) useful python scripts for working with EM datasets developed
by members of the Davis lab at MIT.

__VERSION__ = 0.0.2

Directories provide overall structure and include the following:
--analyze--
* Provides tools to analyze metafiles (.cs or .star) or to view .mrc files
** analyze_2Dclassification.ipynb - jupyter notebook to inspect cryosparc 2D classification results.
** analyze_3Dhetrefine.ipynb - jupyter notebook to inpsect cryopsarc 3D heterogeneous refinement results.
** view_stack.py - python script to view first 9 images of a .mrc file stack

--bsh--
* Provides bash scripts to automate some common tasks
** relion_stats.sh - script to check on progress of a Relion job.

--create--
* Provides tools to simulate particle images
** parse_csparc_pose.py - python script to extract poses from a cryosparc refinement job file (.cs) and put them into a cryodrgn .pkl
** parse_csparc_ctf.py - python script to extract ctf params from a cryosparc refiment job file (.cs) and put them into a cryodrgn .pkl
** project3d.py - python script to generate noiseless (and no CTF) 2D projections from a 3D .mrc volume. Optionally can use poses provided as a .pkl file generated by parse_csparc_pose.py, or can simply generate random rotations. Requires cryodrgn.
** add_ctf_noise.py - python script to add structural noise, apply a CTF, and add shot noise to a stack of images. Optionally uses a cryodrgn ctf .pkl file or a cryodrgn defocus .pkl file. Applies noise according to Baxter et al with user defined levels of structural and shot noise.

--edit--
* Provides tools to edit metafiles or .mrc files (cropping, adding scale bars/etc).
** crop_real.py - a python script using EMAN's e2proc2d.py to crop .mrc files (or .mrcs stacks) in real space.
** edit_cs.py - a python script to edit cryosparc .cs files.
** edit_star.py - a python script to edit relion .star files.
** edit_star_interactive.ipynb - a jupyter notebook to interactively edit star files
** add_scale_bar.ipynb - a jupyter notebook to add scale bars to 2D .mrc images.
** add_scale.py - a python script to add a scale bar to 2D .mrc images.

--move--
* Provides scripts for managing/moving/linking data
** convert_mrc.py - a Python wrapper for e2proc2d to convert .mrc files to .png or .tiff
** create_symlink.py - a python wrapper to create symlinks to raw .mrc data using a cryosparc .cs file (often the output of curate micrographs job).
** get_images.py - a python wrapper to put all of the images within a nested directory into a single directory

--test--
* Testing data for various tools
