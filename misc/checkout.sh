mkdir $WORK_ROOT/ixpe
cd $WORK_ROOT/ixpe
git clone git@bitbucket.org:ixpesw/gpdext.git
git clone git@bitbucket.org:ixpesw/gpdsw.git
git clone git@bitbucket.org:ixpesw/ixpeobssim.git
git clone git@bitbucket.org:ixpesw/gpdworkbook.git

mkdir $WORK_ROOT/gpd
cd $WORK_ROOT/gpd
git clone git@bitbucket.org:infn-gpd/gpdsuite_externals.git
git clone git@bitbucket.org:infn-gpd/gpdsuite.git

mkdir $WORK_ROOT/teaching
cd $WORK_ROOT/teaching
git clone git@bitbucket.org:lbaldini/statnotes.git

cd $WORK_ROOT
git clone git@bitbucket.org:lbaldini/baldaquin.git
git clone git@github.com:lucabaldini/webpage.git
