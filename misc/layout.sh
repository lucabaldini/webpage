#Create the main /data directory.
sudo mkdir /data; chmod 775 /data

#Create the basic subfolders in /data
mkdir /data/install
mkdir /data/personal
mkdir /data/work

#Setup the environment
mkdir ~/.bashrc.d
cd ~/.bashrc.d; wget https://osiris.df.unipi.it/~baldini/misc/env.bashrc
