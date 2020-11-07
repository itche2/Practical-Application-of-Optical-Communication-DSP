# FYP
##  Dependencies
### 64-bit version Python 3.5 and above
Python 3.7 or later should be used as it is entirely compatible with all the python dependencies enlisted. It is recommended that the version of Python should be earlier than Python 3.5 as it is the earliest version QAMpy has been tested on. The 64-bit version Python should be installed due to the demand on memory to run computationally heavy instructions. To download the latest version of Python, go to: https://www.python.org/downloads/ 
QAMpy dependencies
QAMpy rely on multiple python libraries to build and run. These include numpy, scipy, cython, bitarray, numba, matplotlib and hdf5 libraries. To install the libraries, open the command line interpreter application and enter the following command.
$pip install numpy scipy cython bitarray numba matplotlib h5py

### QAMpy
QAMpy is a library found on the github repository that provide digital signal processing functions used in optical signal communications. To download the QAMpy library, go to: 
https://github.com/ChalmersPhotonicsLab/QAMpy
After downloading QAMpy, use the command line interpreter to navigate to the directory in QAMpy containing the setup.py file and run the following commands.
$cd C:\Users\Visitor\Downloads\QAMpy-master
$pip install setup.py
$pip install build.py
 
### Using the QAMpy framework
For the QAMpy framework to work with LabLAN, download the framework from: https://github.com/itche2/Practical-Application-of-Optical-Communication-DSP 
And LabLAN from: https://github.com/Jarred27/LabLAN 
Then relocate the script file from the QAMpy framework to “…\LabLAN-master\LabLAN-master\client\simpleUploadAndCapture”. This will enable LabLAN to use the signal files generated through QAMpy.
The main file to run is the runTest.py file where the framework is established while the accompanying script files provide the functionalities to the runTest.py file
