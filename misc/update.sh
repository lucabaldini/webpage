#Start off with a general update.
sudo dnf update

#Now all the Python packages that we need.
sudo dnf install \
  thunderbird \
  gedit emacs \
  python3-scipy python3-matplotlib python3-pylint \
  zlib-devel ncurses-devel libcurl-devel libXt-devel readline-devel gcc gcc-c++ \
  gcc gcc-gfortran perl-devel perl-ExtUtils-MakeMaker python3-devel make \
  cmake expat-devel hdf5-devel libX11-devel libXmu-devel mesa-libGLU-devel \
  swig

#Install atom.
sudo rpm --import https://packagecloud.io/AtomEditor/atom/gpgkey
sudo sh -c 'echo -e "[Atom]\nname=Atom Editor\nbaseurl=https://packagecloud.io/AtomEditor/atom/el/7/\$basearch\nenabled=1\ngpgcheck=0\nrepo_gpgcheck=1\ngpgkey=https://packagecloud.io/AtomEditor/atom/gpgkey" > /etc/yum.repos.d/atom.repo'
sudo dnf install atom

#Install all the video codecs.
sudo dnf install https://mirrors.rpmfusion.org/free/fedora/rpmfusion-free-release-$(rpm -E %fedora).noarch.rpm https://mirrors.rpmfusion.org/nonfree/fedora/rpmfusion-nonfree-release-$(rpm -E %fedora).noarch.rpm
sudo dnf groupupdate multimedia --setop="install_weak_deps=False" --exclude=PackageKit-gstreamer-plugin

#And a few python packages to be installed via pip.
pip install --user regions skyfield mido loguru pydata_sphinx_theme
