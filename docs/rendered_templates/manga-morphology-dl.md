
# Data model: MaNGA Deep Learning DR15 Morphology catalogue



#### General Description
<p>This catalogue contains Deep Learning (DL) based morphological classifications
    corresponding to 4672 PLATE-IFU entries in the MaNGA DR15 sample.
     Some PLATE-IFU entries are re-observations of the same galaxy
     (see DUPL_GR, DUPL_N and DUPL_ID), so the number of distinct
      galaxies in this catalogue is 4599.  The methodology for training and testing
      the DL models is described in <a href="http://adsabs.harvard.edu/doi/10.1093/mnras/sty338">Domínguez Sánchez et al. 2018</a>,
      where classifications for about 670,000 objects from the SDSS DR7
      Main Galaxy Sample are provided. Since about 20% of the MaNGA DR15
      galaxies were not included in that analysis, the present catalogue
    provides a homogenous morphological catalogue for all 4599 MaNGA DR15 galaxies.
        All the classifications have been eye-balled for additional reliability
        (see <a href="https://arxiv.org/abs/1811.02580">Fischer et al. 2018</a> for details).</p>
<p> This catalogue complements the
  <a href="https://data.sdss.org/datamodel/files/MANGA_MORPHOLOGY/GALAXY_ZOO/">Galaxy Zoo</a>
  MaNGA catalogue by providing a T-Type and a finer separation between S0s and pure ellipticals.
  For the parameters in common with the Galaxy Zoo (P_edge_on, P_bar, P_bulge, P_cigar),
  the DL-output probability distributions are more bimodal, reducing the fraction of
  galaxies with an uncertain classification
  (see <a href="http://adsabs.harvard.edu/doi/10.1093/mnras/sty338">Domínguez Sánchez et al. 2018</a>). </p>
<p> A companion catalogue, <a href="https://data.sdss.org/datamodel/files/MANGA_PHOTO/pymorph/PYMORPH_VER/manga-pymorph.html">MaNGA PyMorph DR15 photometric catalogue</a>,
     provides photometric parameters obtained from Sersic and Sersic+Exponential
     fits to the 2D surface brightness profiles for the same set of galaxies
    (see also <a href="https://arxiv.org/abs/1811.02580">Fischer et al. 2018</a>).<p>
</p></p>


#### Naming Convention
<code>manga-morphology-dl-DR15.fits</code>


#### Approximate Size
4672 galaxies, 19 columns; 670 KB


#### File Type
FITS


#### Written by
Helena Domínguez Sánchez, Mariangela Bernardi and Johanna-Laina Fischer.


#### Files
<p> The morphological catalogue is provided as one single .fits file:</p>
<ul>
<li><a href="#manga-morphology-dl-DR15.fits"></a>manga-morphology-dl-DR15</li>
</ul>


