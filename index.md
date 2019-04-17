
# SlicerVASST Tutorials
Prior to using any of these tutorials please review SlicerIGT.org and PlusToolkit.org to learn how to connect to the PlusServer to stream image and tracking data into Slicer. 

<img src="/Media/PlusServer.PNG" class="inline"/>

## Co-registration between HTC VIVE and spatial tracking systems 
This tutorial requires tracking a stylus with a X mm ball tip and a 3D printed calibration apparatus using the following stl. A sensor must be fixed to the apparatus in order to track it properly. The transforms associated with the sensors fixed to the tools will be streamed into Slicer using the following configuration file and the PlusServer. 

### PlusServer configuration file for sytlus and calibration apparatus 

The configuration file required to steam the correct data into 3D Slicer can be found [here.](https://github.com/lgroves6/SlicerVAASTTutorials/blob/master/Co-calibration.xml)
### Co-registration Process 

<source src= "/Media/co-cal.mp4" type = "video/mp4"> </video>
