This is a very basic script to collect blade information from an HP C7000 enclosure. 
Script will login to OA and excecute multiple commands and process the result to show the details in a tabular format.
So far tested on ws460 Gen6/Gen8/Gen9 blades.
Please read the script and make sure you understand the working.

Notes : 
# Script will exclude iSCSI/HBA interface
# Blade loop are detected by the keywords, if you noticed not working, please check the keywords.

In case you find any bugs, please contact net.gini@gmail.com
