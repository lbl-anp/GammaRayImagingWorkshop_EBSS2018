# Welcome

Welcome to the high-resolution gamma-ray imaging workshop of the 
[Exotic Beam Summer School, 2018](https://sites.google.com/lbl.gov/ebss2018/home?authuser=0)
hosted by Lawrence Berkeley National Lab.
This workshop provides a basic introduction to Compton imaging, a 
collimator-less, kinematic imaging technique used for imaging
gamma-rays.
This repository comprises the workshop, with hands-on activities divided
into three lessons in the form of 
[jupyter notebooks](http://jupyter.org/).
It is assumed that the students for this workshop are familiar with 
python for scientific data analysis.
If this is not the case (or you'd like to brush up in preparation for the 
workshop), there are many great tutorials on the subject, such as the 
[Scipy Lecture Notes](https://www.scipy-lectures.org/).

## Preparation

All that is required to participate in this workshop is a computer with
python installed, along with some of the most common scientific data analysis
packages such as [numpy](http://www.numpy.org/),
[matplotlib](https://matplotlib.org/), and
[pytables](https://www.pytables.org/).

The LBNL computers that will be used for the workshop have all of the 
necessary installed and pre-configured on them.
In addition, there are several options for being able to participate in the 
workshop remotely or after the specified dates:

### Virtual Machine

We are providing a virtual machine running Ubuntu 16.04 that has all of the
software required for this workshop pre-installed and configured.
The VM can be downloaded 
[here](https://www.dropbox.com/sh/sl1ycp1d5i8vafu/AABWXPO1z07EC3wNVAEpVXo8a?dl=0) 
(N.B. The VM may be up to 17 GB in size, so the download may take a while.)

**It is not required to download this on your personal machine prior to the
workshop** - the provided computers will have all the necessary software.

### Python Package Managers

For users who already have python installed on their systems, a pip
`requirements.txt` file is provided containing all of the packages needed for
the data analysis covered in this workshop.
Popular python package managers such as `pip` or `conda` can be used to 
install the necessary packages on your system, for example:
```python
pip install -r requirements.txt
```
**NOTE**: Be careful if you're using your native system python... the above 
command can over-ride packages that are already installed.
Consider using 
[virtualenv](http://docs.python-guide.org/en/latest/dev/virtualenvs/) to avoid
this issue.

## Data

The data used for the hands-on portion of this workshop was generated via
simulation using the excellent [Geant4](https://geant4.web.cern.ch/) simulation
toolkit.
For more information about the setup of the simulation and the format of the
data, please see lesson 1.

The data can be downloaded 
[here](https://www.dropbox.com/s/ojq4i9fyz8f7205/hits.h5?dl=0).
The following command can be used to download the data with the appropriate
naming convention:

```bash
wget -L -O hits.h5 https://www.dropbox.com/s/ojq4i9fyz8f7205/hits.h5?dl=0
```
Make sure that the resultant `hits.h5` file is stored in the top-level 
directory of this project (i.e. the same directory that this `README.md` file
is in).
Once the data have been downloaded, you can test that your system is configured
properly with:

```bash
python compton_imaging.py
```

This should produce a Compton image created with 1000 cones from the simulated
dataset.
If the above command yields any errors, please notify the instructors (or
create an issue on the GitHub page if working remotely).

## License

The code associated with this tutorial is licenses under
[BSD3](https://opensource.org/licenses/BSD-3-Clause).
You are welcome to use and modify this code to your heart's content, as long as
proper attribution is maintained.
