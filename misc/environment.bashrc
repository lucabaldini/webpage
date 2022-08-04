alias rm="rm -i"

export INSTALL_ROOT=/data/install
export PATH=$INSTALL_ROOT:$PATH

export TEXLIVE_VERSION=2022
export PATH=$INSTALL_ROOT/texlive/$TEXLIVE_VERSION/bin/x86_64-linux/:$PATH

export HEASOFT_VERSION=6.30.1
export HEASOFT_LIBC_VERSION=2.35
export HEADAS=$INSTALL_ROOT/heasoft-$HEASOFT_VERSION/x86_64-pc-linux-gnu-libc$HEASOFT_LIBC_VERSION/
. $HEADAS/headas-init.sh
