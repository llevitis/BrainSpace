from nilearn import datasets
from nilearn.input_data import NiftiLabelsMasker
from nilearn.connectome import ConnectivityMeasure


def fmrivol2conn(funtional, atlas_filename, confounds_fn=""):
    """
    Takes 4D fmri volume and extracts the connectivity matrix
    Parameters
    ----------
    functional: path
        Fullpath to functional image in nifti
    altas_filename: path
        Fullpath to the parcellation to create the FC matrix.
        Must be in the same space than functional 
    confounds_fn (optional): path
        Path to a csv type file with the confound regressors.
    Returns
    -------
    FC_matrix: matrix
       Functional connectivy matrix of the image. 
    """
    masker = NiftiLabelsMasker(labels_img=atlas_filename, standardize=True)
    connectome_measure = ConnectivityMeasure(kind='correlation')
    if confounds_fn == "":
        timeseries = masker.fit_transform(funtional)
    else:
        timeseries = masker.fit_transform(funtional, confounds=confounds_fn)
    # call fit_transform from ConnectivityMeasure object
    FC_matrix = connectome_measure.fit_transform([timeseries])[0]
    # saving each subject correlation to correlations
    return FC_matrix