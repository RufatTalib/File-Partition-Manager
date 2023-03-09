# Python-File-Partition
Dividing big sized file to smaller blocks, and re-mix

<h3>Supports</h3>
<ul>
  <li>Images ( like png, jpg/jpeg, ... )</li>
  <li>Videos ( mp4, avi, ...)</li>
  <li>Document files ( docx, pdf, ...)</li>
  <li>Executable programs ( .exe, .out, ... )</li>
  <li>Files has no extention ( all type of files )</li>  
  
</ul>

<h3>Usage</h3>

<p>Partition</p>
<code>partition = Partition("exampledrive:\\examplepath\\examplefilename.examplefileformat", examplePartitionSize)</code><br>
<code>partition.Generate()</code><br>
<br>
<p>Building</p>
<code>builder = Builder()</code><br>
<code>builder.Build("Partitions_For_examplefilename", "examplefilename_backed.examplefileformat")</code>

<h4>
  Partition size stands for block size. Prefering high partition size is good for big files.
</h4>
