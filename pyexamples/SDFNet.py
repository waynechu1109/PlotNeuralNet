import sys
sys.path.append('../')
from pycore.tikzeng import *
from pycore.blocks import *

arch = [
    to_head('..'),
    to_cor(),
    to_begin(),

    # input image
    to_input('../SDFNet/dtu_65_47.png', to='(-12,0,0)', width=12, height=8),

    # image block (create a tiny block to show the arrow)
    to_Conv(
        name='img_in', s_filer="", n_filer="",
        offset="(0,0,0)", to="(-10,0,0)",
        width=1e-4, height=1e-4, depth=1e-4,
        caption=''
    ),

    # pcd preprocess
    to_Pool(
        name='preprocess',
        offset="(0,0,0)", to="(-8,0,0)",
        width=10, height=10, depth=10,
        opacity=0.5,
        caption='Preprocess (VGGT or DUSt3R)'
    ),
    to_connection('img_in', 'preprocess'),

    # pcd front block (create a tiny block to show the arrow)
    to_Conv(
        name='pcd_node_front', s_filer="", n_filer="",
        offset="(0,0,0)", to="(-4,0,0)",
        width=1e-4, height=1e-4, depth=1e-4,
        caption=""
    ),
    to_connection('preprocess', 'pcd_node_front'),

    # pcd image
    to_input('../SDFNet/dtu65_desired_pcd.png', to='(-3,0,0)', width=9, height=6),

    # pcd back block (create a tiny block to show the arrow)
    to_Conv(
        name='pcd_node_back', s_filer="", n_filer="",
        offset="(0,0,0)", to="(-2,0,0)",
        width=1e-4, height=1e-4, depth=1e-4,
        caption=""
    ),
    # to_connection('preprocess', 'pcd_node_front')

    # ===== Encoder (HashGrid Encoding) =====
    to_HashEnc(
        name='encoder', s_filer=1, n_filer=(32,32),
        offset="(0.8,0,0)", to="(0,0,0)",
        width=(2,2), height=25, depth=25,
        caption="Hash Encoder"
    ),
    to_connection('pcd_node_back', 'encoder'),

    # ===== GeoNet =====
    to_ConvConvRelu(
        name='geo', s_filer=1, n_filer=(64,64),
        offset="(3,3,0)", to="(encoder-east)",
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

    # to_end 應該保持在最後
    to_end()
]

def main():
    namefile = str(sys.argv[0]).split('.')[0]
    to_generate(arch, namefile + '.tex')

if __name__ == '__main__':
    main()
