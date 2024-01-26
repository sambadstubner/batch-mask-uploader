from pathlib import Path

import click

from utils.img_processing import Masker
import utils.img_processing as ip


@click.group
def cli():
    pass

@cli.command
@click.argument('design_path', type=click.File('rb'))
@click.argument('mask_path', type=click.File('rb'))
@click.argument('destination_path', type=click.File('wb'))
def mask_single(design_path, mask_path, destination_path):
    masker = Masker(design_path.name, mask_path.name, destination_path.name)
    masker.run()



@cli.command
@click.argument('design_path', type=click.File('rb'))
@click.argument('mask_folder', type=click.Path(exists=True, dir_okay=True))
@click.argument('destination_folder', type=click.Path(dir_okay=True))
def mask_dir(design_path, mask_folder, destination_folder):
    pathlist = Path(mask_folder).glob('**/*')
    # Create and export a mask for every mask in the mask folder
    for mask_path in pathlist:
        destination_path = f"{destination_folder}/{Path(design_path.name).stem}_{mask_path.stem}.png"
        Masker(design_path.name, str(mask_path), destination_path).run()


@cli.command
@click.argument('img_path', type=click.File('rb'))
def invert_img(img_path):
    ip.invert_img(img_path.name)

if __name__ == '__main__':
    cli()