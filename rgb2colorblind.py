#!/usr/bin/env python

import webcolors
import numpy as np
import os
import sys
from texttable import Texttable


class ColorBlindConverter(object):
    def __init__(self):
        (
            self.Normal,
            self.Protanopia,
            self.Deuteranopia,
            self.Tritanopia,
            self.Protanomaly,
            self.Deuteranomaly,
            self.Tritanomaly,
            self.Monochromacy
        )   = range(8)

        self.powGammaLookup = np.power(np.linspace(0, 256, 256) / 256, 2.2)
        self.conversion_coeffs = [
            {'cpu': 0.735, 'cpv':  0.265, 'am': 1.273463, 'ayi': -0.073894},
            {'cpu': 1.140, 'cpv': -0.140, 'am': 0.968437, 'ayi':  0.003331},
            {'cpu': 0.171, 'cpv': -0.003, 'am': 0.062921, 'ayi':  0.292119}]

    def _inversePow(self, x):
        return int(255.0 * float(0 if x <= 0 else (1 if x >= 1 else np.power(x, 1/2.2))))

    def convert(self, rgb, cb_type):
        self.rgb = rgb
        self.cb_type = cb_type
        
        if self.cb_type == 0:
            self.converted_rgb = self._convert_normal()
        elif self.cb_type in range(1, 4):
            self.converted_rgb = self._convert_colorblind()
        elif self.cb_type in range(4, 7):
            self.converted_rgb = self._convert_anomylize(self._convert_colorblind())
        elif self.cb_type == 7:
            self.converted_rgb = self._convert_monochrome()
        return

    def _convert_normal(self):
        return self.rgb

    def _convert_colorblind(self):
        
        wx = 0.312713;
        wy = 0.329016;
        wz = 0.358271;

        cpu, cpv, am, ayi = self.conversion_coeffs[{
            1: 0, 4: 0,
            2: 1, 5: 1,
            3: 2, 6: 2,
        }[self.cb_type]].values()

        r, g, b = self.rgb

        cr = self.powGammaLookup[r]
        cg = self.powGammaLookup[g]
        cb = self.powGammaLookup[b]

        # rgb -> xyz
        cx = (0.430574 * cr + 0.341550 * cg + 0.178325 * cb)
        cy = (0.222015 * cr + 0.706655 * cg + 0.071330 * cb)
        cz = (0.020183 * cr + 0.129553 * cg + 0.939180 * cb)

        sum_xyz = cx + cy + cz
        cu = 0
        cv = 0

        if(sum_xyz != 0):
            cu = cx / sum_xyz
            cv = cy / sum_xyz

        nx = wx * cy / wy
        nz = wz * cy / wy
        clm = 0
        dy = 0

        clm = (cpv - cv) / (cpu - cu) if (cu < cpu) else (cv - cpv) / (cu - cpu)
        clyi = cv - cu * clm
        du = (ayi - clyi) / (clm - am)
        dv = (clm * du) + clyi

        sx = du * cy / dv
        sy = cy
        sz = (1 - (du + dv)) * cy / dv

        # xyz->rgb
        sr =  (3.063218 * sx - 1.393325 * sy - 0.475802 * sz)
        sg = (-0.969243 * sx + 1.875966 * sy + 0.041555 * sz)
        sb =  (0.067871 * sx - 0.228834 * sy + 1.069251 * sz)

        dx = nx - sx
        dz = nz - sz

        # xyz->rgb

        dr =  (3.063218 * dx - 1.393325 * dy - 0.475802 * dz)
        dg = (-0.969243 * dx + 1.875966 * dy + 0.041555 * dz)
        db =  (0.067871 * dx - 0.228834 * dy + 1.069251 * dz)

        adjr = ((0 if sr < 0 else 1) - sr) / dr if dr > 0 else 0
        adjg = ((0 if sg < 0 else 1) - sg) / dg if dg > 0 else 0
        adjb = ((0 if sb < 0 else 1) - sb) / db if db > 0 else 0

        adjust = max([
            0 if (adjr > 1 or adjr < 0) else adjr,
            0 if (adjg > 1 or adjg < 0) else adjg,
            0 if (adjb > 1 or adjb < 0) else adjb])

        sr = sr + (adjust * dr)
        sg = sg + (adjust * dg)
        sb = sb + (adjust * db)

        return [self._inversePow(sr), self._inversePow(sg), self._inversePow(sb)]

    def _convert_anomylize(self, p_cb):
        v = 1.75
        d = v + 1
        
        r_orig, g_orig, b_orig = self.rgb
        r_cb, g_cb, b_cb = p_cb

        r_new = (v * r_cb + r_orig) / d
        g_new = (v * g_cb + g_orig) / d
        b_new = (v * b_cb + b_orig) / d

        return [int(r_new), int(g_new), int(b_new)]


    def _convert_monochrome(self):
        r_old, g_old, b_old = self.rgb
        g_new = (r_old * 0.299) + (g_old * 0.587) + (b_old * 0.114)
        return [int(g_new)]*3


def closest_color(requested_colour):
    min_colours = {}
    for key, name in webcolors.css3_hex_to_names.items():
        r_c, g_c, b_c = webcolors.hex_to_rgb(key)
        rd = (r_c - requested_colour[0]) ** 2
        gd = (g_c - requested_colour[1]) ** 2
        bd = (b_c - requested_colour[2]) ** 2
        min_colours[(rd + gd + bd)] = name
    return min_colours[min(min_colours.keys())].title()



if __name__ == '__main__':

    ############################################################
    # Command line parsing.
    ############################################################

    import argparse
    import os
    import textwrap

    cb_types = {
        'Normal':        '(normal vision)',
        'Protanopia':    '(red-blind)',
        'Deuteranopia':  '(green-blind)',
        'Tritanopia':    '(blue-blind)',
        'Protanomaly':   '(red-weak)',
        'Deuteranomaly': '(green-weak)',
        'Tritanomaly':   '(blue-weak)',
        'Monochromacy':  '(totally colorblind)'
    }
    description = textwrap.dedent(
    """
    This script is used to convert "normally" colored RGB/Hex values to colorblind RGB/Hex values.

    """ + '    '.join(['* {:} {:}\n'.format(k,v) for k,v in cb_types.items()]) +

    """
    with the default action to convert to 'All' types of colorblindness (and to
    a normal vision version).  Converting to only a select type of
    colorblindness can be accomplished with the CB parameter described below.

    The conversion processes and coefficients herein are used with permission
    from Colblindor [http://www.color-blindness.com/] and were therein used with
    permission of Matthew Wickline and the Human-Computer Interaction Resource
    Network [http://www.hcirn.com/] for non-commercial purposes.  As such, this
    code may only be used for non-commercial purposes.
    """)

    epilog = textwrap.dedent(
    """
    Typical command line calls might look like:

    > python """ + os.path.basename(__file__) + """ <r> <g> <b> --type <type>
    > python """ + os.path.basename(__file__) + """ <hex>       --type <type>
    """)

    if len(sys.argv) == 1:
        sys.argv.append('-h')

    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description=description, epilog=epilog)


    if len(sys.argv[1]) <= 3:   # rgb
        # Add optional, named, arguments.
        parser.add_argument('r', type = int, help = 'R to convert')
        parser.add_argument('g', type = int, help = 'G to convert')
        parser.add_argument('b', type = int, help = 'B to convert')
        use_rgb = True
    else:                   # hex
        parser.add_argument('hex', type = str, help = 'Hex to convert')
        use_rgb = False

    parser.add_argument('--type', '-t', '--no', '-n', type=str, default='All', help='type of colorblindness to convert to (default: All)')
    parser.add_argument('--pause', action='store_true', help='type of colorblindness to convert to (default: All)')

    args = parser.parse_args()

    rgb = [args.r, args.g, args.b] if use_rgb else list(webcolors.hex_to_rgb('#'+args.hex.lstrip('#')))
    cb = list(cb_types)[int(args.type)] if args.type.isnumeric() else args.type.title()


    ############################################################
    # Program execution.
    ############################################################


    cbconv = ColorBlindConverter()
    rows = [['NO', 'TYPE', 'RGB', 'HEX', 'NAME']]

    for cb_type, cb_type_name in enumerate(list(cb_types)):
        if cb_type_name.startswith(cb) or cb == 'All':
            cbconv.convert(rgb, cb_type)

            rows.append([
                cb_type,
                cb_type_name,
                str(tuple(cbconv.converted_rgb)),
                webcolors.rgb_to_hex(cbconv.converted_rgb),
                closest_color(cbconv.converted_rgb),
            ])

    table = Texttable()
    table.set_deco(Texttable.HEADER | Texttable.VLINES)
    table.add_rows(rows)
    print(table.draw())

    if args.pause:
        os.system('pause')
