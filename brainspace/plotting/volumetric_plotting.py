import os
import glob
from jinja2 import Environment, FileSystemLoader

import matplotlib.pyplot as plt
import numpy as np
import nibabel as nib
import nilearn.plotting as plotting

def _create_static_fig(grad_obj, atlas, save_fig=False, output_dir=None, output_file=None):
    """
    Takes 3D gradient object or 4D stacked gradient object and creates 
    figure depicting slices from each gradient 
    Parameters
    ----------
    grad_obj: 3D or 4D np array
    altas_filename: path or Nifti1Image
        Fullpath to the parcellation used to create the FC matrix or the loaded
        atlas.
    save_fig: boolean
        Should the figure be saved
    output_dir (optional): path
        Path to directory where figure should be saved
    output_file (optional): filename
        Name of output file with extension 
    Returns
    -------
    Figure depicting the gradients 
    """
    dim = grad_obj.shape
    if type(atlas) == str:
        atlas = nib.load(atlas)
    img_slice = [6, -18, 14]
    x_len = 10 
    y_len = 3 
    if dim == 3:
        grad_object = [grad_object]
    grad_img_list = []
    num_grads = len(grad_obj)
    for i in range(0, num_grads):
        grad_img = nib.Nifti1Image(grad_obj[i], atlas.affine, atlas.header)
        grad_img_list.append(grad_img)
    fig = plt.figure(figsize=(x_len, num_grads*3))
    for i, grad_img in enumerate(grad_img_list):
        idx = i + 1
        ax = plt.subplot(num_grads, 1, idx)
        title = "Gradient {0}".format(idx)
        plotting.plot_stat_map(grad_img, colorbar=True, 
                                draw_cross=False, cut_coords=img_slice, 
                                cmap="viridis_r", title=title, 
                                symmetric_cbar=False, axes=ax)
    if save_fig == True and output_dir != None:
        if output_file != None: 
            output_file = os.path.join(output_dir, output_file)
        else: 
            output_file = os.path.join(output_dir, "brainspace_gradients.png")
        plt.savefig(output_file)

def _create_interactive_fig(grad_obj, atlas, output_dir): 
    dim = grad_obj.shape
    if type(atlas) == str:
        atlas = nib.load(atlas)
    img_slice = [6, -18, 14]
    x_len = 10 
    y_len = 3 
    if dim == 3:
        grad_obj = [grad_obj]
    for i in range(0, len(grad_obj)):
        grad_img = nib.Nifti1Image(grad_obj[i], atlas.affine, atlas.header)
        html_view = plotting.view_img(grad_img, colorbar=True, draw_cross=False, 
                                      cmap="viridis_r")
        html_view.save_as_html(os.path.join(os.path.join(output_dir, "gradient_" + str(i) + ".html")))


def _create_qc_report(output_dir): 
    """
    Takes 3D gradient object or 4D stacked gradient object and creates 
    an HTML report with interactive images displayed
    Parameters
    ----------
    output_dir (optional): path
        Path to directory where HTML report should be saved 
    Returns
    -------
    Figure depicting the gradients 
    """
    
    gradient_images = sorted(glob.glob(os.path.join(output_dir,"gradient_*.html")))
    content = []
    for i, img in enumerate(gradient_images):
        curr_dict = {}
        curr_dict['name'] = "Gradient {0}".format(i+1)
        curr_dict['img'] = img
        content.append(curr_dict)

    template_path=os.path.join(os.path.dirname(__file__),'./templates')
    file_loader = FileSystemLoader(searchpath=template_path)
    env = Environment(loader=file_loader)

    template = env.get_template('gradients_qc_template.html')

    output_html = template.render(title="BrainSpace Gradients",
                                  content=content)

    file = os.path.join(output_dir, "gradients_qc.html")
    with open(file, "w") as f: 
        f.write(output_html)