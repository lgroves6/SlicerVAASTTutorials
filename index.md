
<div class="generic-content">

<h3 style="background-color: white;">INTRODUCTION</h3>
<div style="background-color: #D7E3ED;background-size: contain; color: black;  ">
<!-- <h4 style= "padding-right:2%; padding-left:2%; padding-top:1%; text-align-last: left;"> -->
<p style ="padding-right: 2%; padding-left: 2%; padding-top: 1%; text-align-last: left;" >
This blog provides an overview of the 3D Slicer architecture and module development with a focus on image-guided therapy (IGT) scripted modules. There are two main components required to develop an IGT module, which are explained in detail in this blog: (1) a platform for data capture and broadcasting (commonly using the Plus library, <a href = "https://plustoolkit.github.io/"> PlusServer </a>), (2) the 3D SlicerIGT Extension to receive the broadcasted data in Slicer for further processing and visualization. Sample code is also provided for reference and to facilitate implementation of these modules.

</p>

<p style= "padding-right:2%; padding-left:2%; text-align-last: left;"> <strong>How to navigate the blog:</strong></p> 
<p style= "padding-right:2%; padding-left:2%; text-align-last: left;"> The main page of this blog is fully interactive. A description of each component in the charts below appears when the cursor is placed over it, and detailed and detailed explanations can be accessed by clicking on the components. </p>

<p style= "padding-right:2%; padding-left:2%; text-align-last: left;"> <strong>Common Acronyms:</strong></p> 
<p style= "padding-right:2%; padding-left:2%; text-align-last: left;">IGT: Image-guided therapy <br> MRML: medical reality modeling language <br>GUI: graphic user interface</br></p>

&nbsp;
</div>
<h4 style="padding-top:2%;"> </h4>

<h3 class="headline headline--medium t-center" style="background-color: white;"><a href="<?php echo site_url('/slicer-roadmap') ?>">3D SLICER ARCHITECTURE</a></h3>

<div style="background-color: #D7E3ED;background-size:auto;overflow-x:scroll; color: black; padding-top:1%; "> 
  <!--  #D7E3ED -->

<p style= "padding-right:2%; padding-left:2%; padding-top:1%; text-align-last: left;">
Model, view, controller (MVC) is a software architecture pattern, which promotes software maintenance and re-usability. Each component is responsible for a specific aspect of the application development. The 3D Slicer platform follows this architectural pattern. In 3D Slicer, 'model', or sometimes 'data model', is referred to as 'MRML'; 'view' is the user interface, which can be command line or graphical interface made up of Qt widgets; and 'controller' is referred to as logic (VTK logic). Following best practices, module development in 3D Slicer should follow this architectural pattern. 
 </p>

<div class = 'tree' style = "padding-right:2%; padding-left:2%; padding-top:1%; ">

  <ul>
    <li>
      <div class = "tooltip"><a href= 'https://en.wikipedia.org/wiki/Model–view–controller'>Model</a>
        <span class="tooltiptext tooltip-model">Manages data and its attributes. </span>
      </div>
      <ul>
        <li>
          <div class = "tooltip"><a href = "https://www.slicer.org/wiki/Documentation/Nightly/Developers/MRML">MRML Overview</a>
            <span class="tooltiptext tooltip-mrmloverview"> The central data representation for managing 3D Slicer data types, such as volumes, models, tranforms, fiducials, cameras etc annd their visualization</span>
          </div>
       <ul>
        <li>
          <div class = "tooltip"><a href = "https://www.slicer.org/wiki/Documentation/Nightly/Developers/MRML">MRML Scene</a>
            <span class="tooltiptext tooltip-mrmlscene"> A collection of MRML nodes</span>
          </div>
        <ul>
        <li>
          <div class = "tooltip"><a href = "https://www.slicer.org/wiki/Documentation/Nightly/Developers/MRML">MRML Node</a>
            <span class="tooltiptext tooltip-mrmlnode"> A component of the data structure that is capable of storing: raw data, visualization and storage parameters.</span>
          </div>
          <ul>
        <li>
          <div class = "tooltip"><a href = "https://www.slicer.org/wiki/Documentation/Nightly/Developers/MRML">Attributes</a>
            <span class="tooltiptext tooltip-refandob">Analogous to variables assoicated with a MRML node. </span>
          </div>
        </li>
        <li>
           <div class = "tooltip"><a href ="https://www.slicer.org/wiki/Documentation/Nightly/Developers/MRML">References <br>and observers</br></a>
            <span class="tooltiptext tooltip-attributes">The method to access a MRML node, either through refercing a specific nodes ID or observing when changes to a node occur.</span>
          </div>
        </li>
      </ul>
      </ul>
    </ul>
  </ul>
      <li>
      <div class = "tooltip"><a href = "https://en.wikipedia.org/wiki/Model–view–controller">View</a>
        <span class="tooltiptext tooltip-view">The visual representation of information, that defines what the user sees and interacts with. </span>
      </div>
      <ul>
        <li>
          <div class = "tooltip"><a>Graphic User Interface</a>
            <span class="tooltiptext tooltip-gui">The portion of a Slicer module that the user interacts with.</span>
          </div>
       <ul>
        <li>
          <div class = "tooltip"><a href = "http://doc.qt.io/archives/qt-4.8/widgets-and-layouts.html">Widget</a>
            <span class="tooltiptext tooltip-widget">One component of the GUI, for example one specific button that the user can push to trigger an event.</span>
          </div>
        </li>
      </ul>
    </ul>
      <li>
      <div class = "tooltip"><a href = "https://en.wikipedia.org/wiki/Model–view–controller">Controller</a>
        <span class="tooltiptext tooltip-controller">Interacts with both the model and the view and controls their functionalities.</span>
      </div>
      <ul>
        <li>
          <div class = "tooltip"><a >Logic</a>
            <span class="tooltiptext tooltip-logic">The portion of the code that performs most of the tasks required by an algorithm.</span>
          </div>
       <ul>
        <li>
          <div class = "tooltip"><a>VTK logic</a>
            <span class="tooltiptext tooltip-functions">Specific portion of the logic that is written and called on to complete one task.</span>
          </div>
        </li>
      </ul>
    </ul>
    </li>
  </ul>

</div>
</div>

<h4 style="padding-top:2%;"> </h4>

<h3 class="headline headline--medium t-center" style="background-color: white;"><a href="<?php echo site_url('/igt-module/') ?>">IGT MODULE DEVELOPMENT</a></h3>
<div style="background-color: #D7E3ED;background-size: contain; color: black;  padding-top:1%; padding-bottom:2%;overflow-x:scroll;">
<p style= "padding-right:2%; padding-left:2%; padding-top:1%; text-align-last: left;">
This image represents how streaming medical images such as ultrasound and tracking information is accessed in 3D Slicer. The examples provided throughout this tutorial focus on ultrasound-guided interventions.
</p>
  <a href= "<?php echo site_url('/igt-module/') ?>"> <img style = "width: 80%; height:95%; align-content: center; padding-left: 10%;" src= <?php echo get_theme_file_uri('/images/plusSlicer.png') ?> /> </a>
  
<h1>  </h1>
</div>

<h4 style="padding-top:2%;"> </h4>

<h3 class="headline headline--medium t-center" style="background-color: white;">EXAMPLES AND DEMONSTRATIONS</h3>
<div style="background-color: #D7E3ED;  background-size:auto; overflow-x:scroll;">


  <div id="wrapper"><span class="label" style = "margin-top: -3%"> Module development <br> examples and<br>required components</span>
    <div class="branch lv1">
      <div class="entry"><span class="label"><a href="<?php echo site_url('/igt-demo') ?>">1. PlusServer configuration files</a></span></div>
      <div class="entry"><span class="label"><a href="<?php echo site_url('/igt-demo') ?>">2. Calibration of ultrasound and tools</a></span></div>
      <div class="entry"><span class="label"><a href="<?php echo site_url('/igt-demo') ?>">3. Displaying a tracked calibrated needle</a></span> </div>
    </div>
  </div>
&nbsp;

</div>



<h4 style="padding-top:2%;"> </h4>

  <h3 class="headline headline--medium t-center" style="background-color: white;"><a href = "<?php echo site_url('/create-module') ?>">DEVELOPE YOUR OWN MODULE</a></h3>
   <div style="background-color: #D7E3ED;background-size:auto;overflow-x:scroll">
  <h1 class="headline headline--medium t-center" style="background-color: white;"></h1>

<div id="wrapper"><span class="label">Process</span>
  <div class="branch lv1">
    <div class="entry"><span class="label"><a href = "<?php echo site_url('/create-module') ?>">Development Modes</a></span>
      <div class="branch lv2">
        <div class="entry"><span class="label">Scripted module <br> (i.e.Python)</span>
        </div>
        <div class="entry"><span class="label">Loadable module <br> (i.e.C++)</span>
      </div>
    </div>
  </div>
    <div class="entry"><span class="label"><a href = "<?php echo site_url('/create-module') ?>">Create a module</a></span></div>
    <div class="entry"><span class="label"><a href = "<?php echo site_url('/create-module') ?>">Add module to an extension</a></span></div>
</div>

&nbsp;
</div>

</div>
</div>
<!-- </article> -->
</section>


# SlicerVASST Tutorials
Prior to using any of these tutorials please review SlicerIGT.org and PlusToolkit.org to learn how to connect to the PlusServer to stream image and tracking data into Slicer. 

## Co-registration between HTC VIVE and spatial tracking systems 
This tutorial requires tracking a stylus with a X mm ball tip and a 3D printed calibration apparatus using the following stl. A sensor must be fixed to the apparatus in order to track it properly. The transforms associated with the sensors fixed to the tools will be streamed into Slicer using the following configuration file and the PlusServer. 

### PlusServer configuration file for sytlus and calibration apparatus 

<img src="/Media/PlusServer.PNG" alt="hi" class="inline"/>

### Co-registration Process 

[Hyperlink to co-calibration video demo](https://www.youtube.com/watch?v=gdwchohlMjI)
