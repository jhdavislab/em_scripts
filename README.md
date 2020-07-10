# em_scripts
(potentially) useful python scripts for working with EM datasets

* get_images.py
  * an executable python script to grab all image files from a nested directory and put them into a single directory. Run get_images.py --help for details on usage.

* create_symlink.py
  * an executable python script to parse a cryosparc .cs file and create symlinks for the subset of .mrc files in that cryosparc file. Most useful if you have curated micrographs in cryosparc and then want to just take that subset for processing in a different tool. Run create_symlink.py --help for details on usage.

* relion_stats.sh
  * bash tool to check on the progress of a relion Refine3D job.

* crop_real.py
  * a python script using eman's e2proc2d.py to crop .mrc files (or .mrcs stacks) in real space
  
* edit_cs.py
  * a python script to edit cryosparc .cs files

* edit_star.py
  * a python script to edit relion .star files

* convert_py.star
  * a python script using emans e2proc2d.py to convert .mrc files to the file type of your choice.
