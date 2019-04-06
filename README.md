## File Transfer Protocol

### A P2P protocol for inter-system communication written ini python

#### Instructions

- "FileUpload [filename]" to send the file the server side.
- "FileDownload [filename]" to download the file from the server side.
- "show_client_files" to list all files in this directory of the client side.
- "show_server_files" to list all files in the server side.
- "IndexGet shortlist <starttimestamp> <endtimestamp>" to list the files modified in mentioned timestamp.
- "IndexGet shortlist <starttimestamp> <endtimestamp> .extension" to list the files modified in mentioned timestamp of a particular extension.
- "IndexGet longlist" similar to shortlist but with complete file listing.
- "IndexGet longlist .extension" similar to shortlist but with complete file listing. 
- "FileHash verify <filename>" checksum and lastmodified timestamp of the input file.
- "history" to see command history.
- "q" or "Q" to exit

------

### To run the code

To run client use command ```python client.py```, and to run server use command ```python server.py```.  

#### Inter-system communication

Keep the `HOST='0.0.0.0' `in server.py unmodified.  
Make the `HOST='IP'` where `IP='IP address of the host'` inside the ```client.py```.  

#### Intra-system communication

make `HOST='localhost'` in both `server.py` and `client.py`,

Results are present in Report.pdf