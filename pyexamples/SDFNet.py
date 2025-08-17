# -*- coding: utf-8 -*-
# SDFNet (HashGrid + GeoNet + ColorNet, single region, no Router)
# 用 PlotNeuralNet 畫圖
import sys
sys.path.append('../')
from pycore.tikzeng import *
from pycore.blocks import *

arch = [
    to_head('..'),
    to_cor(),
    to_begin(),

    # ===== Input =====
    to_input('../SDFNet/dtu_65_47.png', to='(-6,0,0)', width=12, height=8),
    to_input('../SDFNet/dtu65_desired_pcd.png', to='(-3,0,0)', width=9, height=6),

    # ===== Encoder (HashGrid Encoding) =====
    to_ConvConvRelu(
        name='encoder', s_filer=1, n_filer=(32,32),
        offset="(0,0,0)", to="(0,0,0)",
        width=(2,2), height=25, depth=25,
        caption="HashGrid Encoder"
    ),

    # ===== GeoNet =====
    to_ConvConvRelu(
        name='geo', s_filer=1, n_filer=(64,64),
        offset="(3,2,0)", to="(encoder-east)",
        width=(2,2), height=15, depth=15,
        caption="GeoNet"
    ),
    to_connection("encoder", "geo"),

    to_Conv(
        name='sdf', s_filer=1, n_filer=1,
        offset="(3,0,0)", to="(geo-east)",
        width=1, height=10, depth=10,
        caption="SDF(x)"
    ),
    to_connection("geo", "sdf"),

    # ===== ColorNet =====
    to_ConvConvRelu(
        name='color', s_filer=1, n_filer=(64,64),
        offset="(3,-3,0)", to="(encoder-east)",
        width=(2,2), height=15, depth=15,
        caption="ColorNet"
    ),
    to_connection("encoder", "color"),

    to_Conv(
        name='rgb', s_filer=3, n_filer=1,
        offset="(3,0,0)", to="(color-east)",
        width=1, height=10, depth=10,
        caption="RGB(x)"
    ),
    to_connection("color", "rgb"),

    # # ===== Final Outputs =====
    # to_Conv(
    #     name="SDF_final", s_filer=1, n_filer=1,
    #     offset="(2,0,0)", to="(geo-east)",
    #     width=1, height=12, depth=12,
    #     caption="SDF(x)"
    # ),
    # to_connection("geo", "SDF_final"),

    # to_Conv(
    #     name="RGB_final", s_filer=3, n_filer=1,
    #     offset="(2,0,0)", to="(color-east)",
    #     width=1, height=12, depth=12,
    #     caption="RGB(x)"
    # ),
    # to_connection("color", "RGB_final"),

    to_end()
]

def main():
    namefile = str(sys.argv[0]).split('.')[0]
    to_generate(arch, namefile + '.tex')

if __name__ == '__main__':
    main()
