import sys

from PlotNeuralNet.PyCore.TikzGen import (
    ToBegin,
    ToConnection,
    ToConv,
    ToCor,
    ToEnd,
    ToGenerate,
    ToHead,
    ToPool,
    ToSoftMax,
    ToSum,
)

# defined your arch
arch = [
    ToHead(".."),
    ToCor(),
    ToBegin(),
    ToConv(
        "conv1", 512, 64, offset="(0,0,0)", to="(0,0,0)", height=64, depth=64, width=2
    ),
    ToPool("pool1", offset="(0,0,0)", to="(conv1-east)"),
    ToConv(
        "conv2",
        128,
        64,
        offset="(1,0,0)",
        to="(pool1-east)",
        height=32,
        depth=32,
        width=2,
    ),
    ToConnection("pool1", "conv2"),
    ToPool("pool2", offset="(0,0,0)", to="(conv2-east)", height=28, depth=28, width=1),
    ToSoftMax("soft1", 10, "(3,0,0)", "(pool1-east)", caption="SOFT"),
    ToConnection("pool2", "soft1"),
    ToSum("sum1", offset="(1.5,0,0)", to="(soft1-east)", radius=2.5, opacity=0.6),
    ToConnection("soft1", "sum1"),
    ToEnd(),
]


def Main():
    """
    Generate the LaTeX file for a simple neural network diagram.

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
