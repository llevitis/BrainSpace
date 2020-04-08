import glob
from jinja2 import Environment, FileSystemLoader

import nilearn.plotting as plotting
import numpy as np

def _create_static_fig(grad_object, atlas_filename, save_fig=False, output_dir=None):
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
        grad_object = [grad_object]
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

def _create_interactive_fig(grad_object, atlas_filename, output_dir): 
    dim = grad_obj.shape
    atlas = nib.load(atlas_filename)
    img_slice = [6, -18, 14]
    x_len = 10 
    y_len = 3 
    if dim == 3:
        grad_object = [grad_obj]
    for i in range(0, len(grad_object)):
        grad_img = nib.Nifti1Image(grad_object[i], atlas.affine, atlas.header)
        html_view = plotting.view_img(grad_img, colorbar=True, draw_cross=False, 
                                      cmap="viridis_r")
        html_view.save_as_html(os.path.join(os.path.join(output_dir, "gradient_" + str(i) + ".html")))


def _create_qc_report(grad_object, output_dir): 
    """
    Takes 3D gradient object or 4D stacked gradient object and creates 
    an HTML report with interactive images displayed
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
    
    gradient_images = sorted(glob.glob("gradient_*.html"))
    content = []
    for i, img in enumerate(gradient_images):
        curr_dict = {}
        curr_dict['name'] = "Gradient {0}".format(i+1)
        curr_dict['img'] = img
        content.append(dict)

    file_loader = FileSystemLoader('templates')
    env = Environment(loader=file_loader)

    template = env.get_template('gradients_qc_template.html')

    output_html = template.render(title="BrainSpace Gradients",
                                  content=content)

    file = os.path.join(output_dir, "gradients_qc.html")
    with open(file, "w") as f: 
        f.write(output_html)