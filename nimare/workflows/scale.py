import click
import numpy as np

from ..dataset import Database
from ..due import due, Doi
from ..dataset.extract import convert_sleuth_to_database
from ..meta.cbma.ale import SCALE

from nimare.dataset.extract import convert_sleuth_to_database
from nimare.meta.cbma.ale import SCALE
from nimare.meta.cbma.kernel import ALEKernel
from nimare.dataset import Database
from nimare.due import due, Doi

n_iters_default = 10000

@click.command(name='scale', short_help='permutation-based, modified MACM approach '
                                        'that takes activation frequency bias into '
                                        'account',
               help='Method for performing Specific CoActivation Likelihood Estimation (SCALE),'
                    'a modified meta-analytic coactivation modeling (MACM) that takes activation'
                    'frequency bias into account, for delineating distinct core networks of '
                    'coactivation, using a permutation based approach with Family Wise Error '
                    'multiple comparison correction.')
                    
@click.argument('database', required=True, type=click.Path(exists=True, readable=True))
@click.option('--output_dir', required=True, type=click.Path(), help='Directory into which clustering results will be written.')
@click.option('--output_prefix', type=str, help='Common prefix for output SCALE results.')
@click.option('--n_iters', default=n_iters_default, show_default=True, type=int, help='Number of iterations for SCALE to perform in the likelihood estimation.')
@click.option('--base_img', type=click.Path(exists=True, readable=True), help='Voxelwise baseline activation rates.')

@due.dcite(Doi('10.1016/j.neuroimage.2014.06.007'),
           description='Introduces Specific CoActivation Likelihood Estimation (SCALE) for meta-analytic coactivation modeling.')

def scale_workflow(database, output_dir, output_prefix, n_iters, base_img):
    #db = Database(database)
    #dset = db.get_dataset()
    #dataset from sleuth for now
    if database.endswith('.json'):
        db = Database(database)
    if database.endswith('.txt'):
        db = convert_sleuth_to_database(database)
    dset = db.get_dataset()
    ijk = np.vstack(np.where(dset.mask.get_data())).T
    #ijk = np.loadtxt(base_img)
    estimator = SCALE(dset, ijk=ijk, kernel_estimator=ALEKernel, n_iters=n_iters)
    estimator.fit(dset.ids, voxel_thresh=0.001, n_iters=10000, n_cores=4)
    estimator.save_results(output_dir=output_dir, prefix=output_prefix, prefix_sep='_')
    print('Done! :)')
