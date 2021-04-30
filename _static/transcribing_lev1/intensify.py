import sys
from PIL import Image, ImageChops
import random
import argparse
import os


argument_parser = argparse.ArgumentParser(description="Intensifies gifs poorly")
argument_parser.add_argument("--file", "-f", action='store',
                             help="file path", required=True)
argument_parser.add_argument("--scale", "-s", action='store',
                             help="factor to scale frame duration (default 1)", default=1, required=False)
argument_parser.add_argument("--loops", "-l", action='store',
                             help="Number of times to loop (default 1)", default=1, required=False)
argument_parser.add_argument("--duplicate", "-d", action='store',
                             help="Number of times to duplicate intensify frames (default 1), useful when the source file is very slow.  ", default=1, required=False)
argument_parser.add_argument("--shift", action='store',
                             help="Max distance to shift (default 3)", default=3, required=False)


def main(parsed_args):
    im = Image.open(parsed_args.file)
    is_animated = hasattr(im, 'is_animated') and im.is_animated
    frames = 1
    time_scale = float(parsed_args.scale)
    shift_amount = int(parsed_args.shift)
    animation_loops = int(parsed_args.loops)
    if is_animated:
        frames = im.n_frames
        frame_duration = get_time_per_frame(im) * time_scale
    else:
        frame_duration = 40 * time_scale
        animation_loops = animation_loops if animation_loops > 2 else 10
    shift_range = range(shift_amount * -1, shift_amount)

    print(frame_duration)
    out_frames = []
    for loop in range(0, animation_loops):
        for frame in range(0, frames):
            im.seek(frame)
            for d in range(0, int(parsed_args.duplicate)):
                x = random.choice(shift_range)
                y = random.choice(shift_range)
                zoomed = ImageChops.offset(im, x, y)
                out_frames.append(zoomed)

    out = os.path.splitext(parsed_args.file)[0] + "-intensifies.gif"
    print(out)
    out_frames[-1].save(out, format='GIF', append_images=out_frames[0:-1], save_all=True,
                        duration=frame_duration, transparency=1, loop=0)


def get_time_per_frame(PIL_Image_object):
    """ Returns the average framerate of a PIL Image object """
    PIL_Image_object.seek(0)
    frame_count = duration = 0
    for f in range(0, PIL_Image_object.n_frames):
        try:
            frame_count += 1
            duration +=  PIL_Image_object.info['duration'] if 'duration' in PIL_Image_object.info else 1
            PIL_Image_object.seek(PIL_Image_object.tell() + 1)
        except EOFError:
            try:
                return duration / frame_count
            except:
                return 1
    return 1


if __name__ == '__main__':
    if len(sys.argv) < 2:
        argument_parser.print_help()
        exit(0)

    main(argument_parser.parse_args(sys.argv[1:]))
