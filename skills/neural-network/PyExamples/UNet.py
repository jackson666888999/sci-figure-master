import sys

from PlotNeuralNet.PyCore.Blocks import Block2ConvPool, BlockRes, BlockUnconv
from PlotNeuralNet.PyCore.TikzGen import (
    ToBegin,
    ToConnection,
    ToConvConvRelu,
    ToConvSoftMax,
    ToCor,
    ToEnd,
    ToGenerate,
    ToHead,
    ToInput,
    ToPool,
    ToSkip,
)

arch = [
    ToHead(".."),
    ToCor(),
    ToBegin(),
    # input
    ToInput("../Examples/FCN8s/Cats.jpg"),
    # block-001
    ToConvConvRelu(
        name="ccr_b1",
        sFilter=500,
        nFilter=(64, 64),
        offset="(0,0,0)",
        to="(0,0,0)",
        width=(2, 2),
        height=40,
        depth=40,
    ),
    ToPool(
        name="pool_b1",
        offset="(0,0,0)",
        to="(ccr_b1-east)",
        width=1,
        height=32,
        depth=32,
        opacity=0.5,
    ),
    *Block2ConvPool(
        name="b2",
        botton="pool_b1",
        top="pool_b2",
        sFilter=256,
        nFilter=128,
        offset="(1,0,0)",
        size=(32, 32, 3.5),
        opacity=0.5,
    ),
    *Block2ConvPool(
        name="b3",
        botton="pool_b2",
        top="pool_b3",
        sFilter=128,
        nFilter=256,
        offset="(1,0,0)",
        size=(25, 25, 4.5),
        opacity=0.5,
    ),
    *Block2ConvPool(
        name="b4",
        botton="pool_b3",
        top="pool_b4",
        sFilter=64,
        nFilter=512,
        offset="(1,0,0)",
        size=(16, 16, 5.5),
        opacity=0.5,
    ),
    # Bottleneck
    # block-005
    ToConvConvRelu(
        name="ccr_b5",
        sFilter=32,
        nFilter=(1024, 1024),
        offset="(2,0,0)",
        to="(pool_b4-east)",
        width=(8, 8),
        height=8,
        depth=8,
        caption="Bottleneck",
    ),
    ToConnection("pool_b4", "ccr_b5"),
    # Decoder
    *BlockUnconv(
        name="b6",
        botton="ccr_b5",
        top="end_b6",
        sFilter=64,
        nFilter=512,
        offset="(2.1,0,0)",
        size=(16, 16, 5.0),
        opacity=0.5,
    ),
    ToSkip(of="ccr_b4", to="ccr_res_b6", pos=1.25),
    *BlockUnconv(
        name="b7",
        botton="end_b6",
        top="end_b7",
        sFilter=128,
        nFilter=256,
        offset="(2.1,0,0)",
        size=(25, 25, 4.5),
        opacity=0.5,
    ),
    ToSkip(of="ccr_b3", to="ccr_res_b7", pos=1.25),
    *BlockUnconv(
        name="b8",
        botton="end_b7",
        top="end_b8",
        sFilter=256,
        nFilter=128,
        offset="(2.1,0,0)",
        size=(32, 32, 3.5),
        opacity=0.5,
    ),
    ToSkip(of="ccr_b2", to="ccr_res_b8", pos=1.25),
    *BlockUnconv(
        name="b9",
        botton="end_b8",
        top="end_b9",
        sFilter=512,
        nFilter=64,
        offset="(2.1,0,0)",
        size=(40, 40, 2.5),
        opacity=0.5,
    ),
    ToSkip(of="ccr_b1", to="ccr_res_b9", pos=1.25),
    ToConvSoftMax(
        name="soft1",
        sFilter=512,
        offset="(0.75,0,0)",
        to="(end_b9-east)",
        width=1,
        height=40,
        depth=40,
        caption="SOFT",
    ),
    ToConnection("end_b9", "soft1"),
    ToEnd(),
]


def Main():
    """
    Generate the LaTeX file for the U-Net architecture diagram.

    Parameters
    ----------
    None

    Returns
    -------
    None
    """
    nameFile = str(sys.argv[0]).split(".")[0]
    ToGenerate(arch, nameFile + ".tex")


if __name__ == "__main__":

    Main()
