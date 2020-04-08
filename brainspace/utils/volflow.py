from nilearn import datasets
from nilearn.input_data import NiftiLabelsMasker
from nilearn.connectome import ConnectivityMeasure
import nilearn.plotting as plotting
import numpy as np


def fmrivols2conn(fmri_filenames, atlas_filename, confounds_fn="", measure='correlation'):
    """
    Takes 4D fmri volumes from different and extracts the connectivity matrix
    Parameters
    ----------
    fmri_filenames: lists of paths  or path
        List Fullpath to functional images in nifti
    altas_filename: path
        Fullpath to the parcellation to create the FC matrix.
        Must be in the same space than functional 
    confounds_fn (optional): path
        Paths to a csv type files with the confound regressors for each dataset.
    measure: str
        {"correlation", "partial correlation", "tangent", "covariance", "precision"}, optional
    Returns
    -------
    FC_matrix: matrix
       Functional connectivy matrix of the image. 
    """
    # if user is only inputing one module adapt input so is accepted by the function
    if isinstance(fmri_filenames,str):
        fmri_filenames = [fmri_filenames]
        confounds_fn = [confounds_fn]
    # Create masker to extract the timeseries
    masker = NiftiLabelsMasker(labels_img=atlas_filename, standardize=True)
    # define the connectome measure
    connectome_measure = ConnectivityMeasure(kind=measure)
    timeseries = []
    # loop that extracts the timeseries for each volume
    for i,volume in enumerate(fmri_filenames):
        if confounds_fn[0] == "":
            timeseries.append(masker.fit_transform(volume).T)
        else:
            timeseries.append(masker.fit_transform(volume, confounds=confounds_fn[i]).T)
    timeseries = np.array(timeseries)
    mean_ts = np.mean(timeseries,axis=0)
    # call fit_transform from ConnectivityMeasure object
    FC_matrix = connectome_measure.fit_transform([mean_ts.T])[0]
    # saving each subject correlation to correlations
    return FC_matrix

def grad2fig(grad_object, atlas_filename, save_fig=False, output_dir=None):
    """
    Takes 3D gradient object or 4D stacked gradient object and creates 
    figure depicting slices from each gradient 
    Parameters
    ----------
    grad_object: 3D or 4D np array
    altas_filename: path
        Fullpath to the parcellation used to create the FC matrix.
    save_fig: boolean
        Should the figure be saved
    output_dir (optional): path
        Path to directory where figure should be saved 
    Returns
    -------
    Figure depicting the gradients 
    """
    dim = grad_obj.shape
    atlas = nib.load(atlas_filename)
    img_slice = [6, -18, 14]
    x_len = 10 
    y_len = 3 
    if dim == 3:
        grad_img = nib.Nifti1Image(grad_object, atlas.affine, atlas.header)
        fig = plt.figure(figsize=(x_len,y_len))
        plotting.plot_stat_map(grad_img, colorbar=True, 
                               draw_cross=False, cut_coords=img_slice, 
                               cmap="viridis_r", title="Gradient 1", 
                               symmetric_cbar=False)
    elif dim == 4:
        grad_img_list = []
        num_grads = len(grad_obj)
        for i in range(0, num_grads):
            grad_img = nib.Nifti1Image(grad_obj[i], atlas.affine, atlas.header)
            grad_img_list.append(grad_img)
        fig = plt.figure(figsize=(x_len, num_grads*3))
        for i, grad_img in enumerate(img_list):
            idx = i + 1
            ax = plt.subplot(num_grads, 1, idx)
            title = "Gradient {0}".format(idx)
            plotting.plot_stat_map(grad_img, colorbar=True, 
                                   draw_cross=False, cut_coords=img_slice, 
                                   cmap="viridis_r", title=title, 
                                   symmetric_cbar=False, axes=ax)
        if save_fig == True & output_dir != None:
            plt.save_fig(os.path.join(output_dir, "brainspace_gradients.png"))
        