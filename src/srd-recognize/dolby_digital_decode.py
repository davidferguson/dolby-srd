import cv2 as cv
import click
from srd_fixel_frame import SRDFixelFrame

@click.command()
@click.option('--grid', is_flag=True, help='shows the grid used during recognition')
@click.argument('file', type=click.Path(exists=True))
def main(grid, file):
    """Reads in FILE and recognizes the SR•D fixels."""
    img = cv.imread(file)
    frame = SRDFixelFrame(img)
    frame.detect_corner_scale()
    frame.find_corners()
    frame.apply_thresholding()
    cv.imshow('', frame.thresholded)
    frame.reframe()
    cv.imshow('', frame.reframed)

    if grid:
        frame.draw_grid()
    
    frame.decode()
    frame.check_known_patterns()
    frame.print_ascii()

    cv.imshow("pattern", frame.colour_img)
    print('Showing recognized pattern, press any key to continue')
    cv.waitKey(0)


if __name__ == '__main__':
    main()
