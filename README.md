# EARIA2016-hackathon

[EARIA autumn school 2016](http://www.asso-aria.org/index.php?option=com_content&view=article&id=134&Itemid=531) : demonstration made by the team "bon appetit"

## Requirements
* python 2.7
* python libraries : web.py , sklearn, etc.

## Verify the availability of the ports (linux examples):
* sudo service --status-all
* sudo netstat -nlp
* sudo service NAME_OF_SERVICE stop

## Install Xampp (ubuntu examples taken from [here](https://doc.ubuntu-fr.org/xampp) )
1. [Get the installation file](http://www.apachefriends.org/fr/download.html)
2. sudo chmod 755 xampp-linux-*-installer.run
3. sudo ./xampp-linux-*-installer.run

## Copy the "gp1" directory into /opt/lampp/htdocs

## Start the application
1. Start xampp. in terminal type : sudo /opt/lampp/xampp start
2. Start the webservice. in terminal type : sudo python clustering_webservice.py
3. In your browser, go to [localhost:8888/gp1/](localhost:8888/gp1/) to see the interface