# em_scripts
(potentially) useful python scripts for working with EM datasets

* get_images.py
  * an executable python script to grab all image files from a nested directory and put them into a single directory. Run get_images.py --help for details on usage.

* create_symlink.py
  * an executable python script to parse a cryosparc .cs file and create symlinks for the subset of .mrc files in that cryosparc file. Most useful if you have curated micrographs in cryosparc and then want to just take that subset for processing in a different tool. Run create_symlink.py --help for details on usage.
