Challenge:
IXC Center Needs a way to integrate the booking system with the VMS and IXC ISE internet access 
because they are three separate systems now that don't have any links.

The solution is divided into two phases;
Phase one starts with using REST API's to get all the reservation from ixc.cisco.com
Then, it filters out the reservations that match the date two days from today.
If it matches, it will get the briefing document for the processed reservations.
Then, it will proceed to create visits for the visitors mentioned in the documents.
after that, each visitor will receive an email with the IXC ISE credentials for easier login

Phase two, when the visitor arrives at IXC and they check in at the WPR tablet,
The host will receive an email notifying him that the visitor has arrived.
Finally, the visit will be activated on the VMS.

Code Description:
Python file that can be installed on any VM or container that has reachability with the booking system, 
VMS and IXC ISE (might be required for phase 2)

This script:
1. Should be always on (you might use nohup command to let it run in the background
after closing terminal)
2. Will call the booking system daily at 10 PM
3. Should work on startup in case the VM or container got restarted through following
 the instructions in this link: 
 https://stackoverflow.com/questions/24518522/run-python-script-at-startup-in-ubuntu
