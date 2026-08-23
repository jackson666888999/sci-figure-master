from .TikzGen import *


# define new block
def Block2ConvPool(
    name,
    botton,
    top,
    sFiler=256,
    nFiler=64,
    offset="(1,0,0)",
    size=(32, 32, 3.5),
    opacity=0.5,
):
    """
    Create a block with two convolutional layers followed by a pooling layer.

    Parameters
    ----------
    name : str
        Base name for the layers in the block.
    botton : str
        The node from which the block starts.
    top : str
        The node where the block ends.
    sFiler : int, optional
        Size of the filter, by default 256.
    nFiler : int, optional
        Number of filters, by default 64.
    offset : str, optional
        Position offset, by default "(1,0,0)".
    size : tuple of int, optional
        Size dimensions (height, depth, width), by default (32, 32, 3.5).
    opacity : float, optional
        Opacity for the pooling layer, by default 0.5.

    Returns
    -------
    list of str
        LaTeX code for the convolutional and pooling layers.
    """
    return [
        ToConvConvRelu(
            name=f"ccr_{name}",
            sFiler=str(sFiler),
            nFiler=(nFiler, nFiler),
            offset=offset,
            to=f"({botton}-east)",
            width=(size[2], size[2]),
            height=size[0],
            depth=size[1],
        ),
        ToPool(
            name=f"{top}",
            offset="(0,0,0)",
            to=f"(ccr_{name}-east)",
            width=1,
            height=size[0] - int(size[0] / 4),
            depth=size[1] - int(size[0] / 4),
            opacity=opacity,
        ),
        ToConnection(f"{botton}", f"ccr_{name}"),
    ]


def BlockUnconv(
    name,
    botton,
    top,
    sFiler=256,
    nFiler=64,
    offset="(1,0,0)",
    size=(32, 32, 3.5),
    opacity=0.5,
):
    """
    Create a block with an unpooling layer and convolutional layers.

    Parameters
    ----------
    name : str
        Base name for the layers in the block.
    botton : str
        The node from which the block starts.
    top : str
        The node where the block ends.
    sFiler : int, optional
        Size of the filter, by default 256.
    nFiler : int, optional
        Number of filters, by default 64.
    offset : str, optional
        Position offset, by default "(1,0,0)".
    size : tuple of int, optional
        Size dimensions (height, depth, width), by default (32, 32, 3.5).
    opacity : float, optional
        Opacity for the layers, by default 0.5.

    Returns
    -------
    list of str
        LaTeX code for the unpooling and convolutional layers.
    """
    return [
        ToUnPool(
            name=f"unpool_{name}",
            offset=offset,
            to=f"({botton}-east)",
            width=1,
            height=size[0],
            depth=size[1],
            opacity=opacity,
        ),
        ToConvRes(
            name=f"ccr_res_{name}",
            offset="(0,0,0)",
            to=f"(unpool_{name}-east)",
            sFiler=str(sFiler),
            nFiler=str(nFiler),
            width=size[2],
            height=size[0],
            depth=size[1],
            opacity=opacity,
        ),
        ToConv(
            name=f"ccr_{name}",
            offset="(0,0,0)",
            to=f"(ccr_res_{name}-east)",
            sFiler=str(sFiler),
            nFiler=str(nFiler),
            width=size[2],
            height=size[0],
            depth=size[1],
        ),
        ToConvRes(
            name=f"ccr_res_c_{name}",
            offset="(0,0,0)",
            to=f"(ccr_{name}-east)",
            sFiler=str(sFiler),
            nFiler=str(nFiler),
            width=size[2],
            height=size[0],
            depth=size[1],
            opacity=opacity,
        ),
        ToConv(
            name=f"{top}",
            offset="(0,0,0)",
            to=f"(ccr_res_c_{name}-east)",
            sFiler=str(sFiler),
            nFiler=str(nFiler),
            width=size[2],
            height=size[0],
            depth=size[1],
        ),
        ToConnection(f"{botton}", f"unpool_{name}"),
    ]


def BlockRes(
    num,
    name,
    botton,
    top,
    sFiler=256,
    nFiler=64,
    offset="(0,0,0)",
    size=(32, 32, 3.5),
    opacity=0.5,
):
    """
    Create a residual block with multiple convolutional layers and a skip connection.

    Parameters
    ----------
    num : int
        Number of convolutional layers in the block.
    name : str
        Base name for the layers in the block.
    botton : str
        The node from which the block starts.
    top : str
        The node where the block ends.
    sFiler : int, optional
        Size of the filter, by default 256.
    nFiler : int, optional
        Number of filters, by default 64.
    offset : str, optional
        Position offset, by default "(0,0,0)".
    size : tuple of int, optional
        Size dimensions (height, depth, width), by default (32, 32, 3.5).
    opacity : float, optional
        Opacity for the skip connection, by default 0.5.

    Returns
    -------
    list of str
        LaTeX code for the residual block.
    """
    lys = []
    layers = [f"{name}_{i}" for i in range(num - 1)] + [top]
    for layerName in layers:
        ly = [
            ToConv(
                name=f"{layerName}",
                offset=offset,
                to=f"({botton}-east)",
                sFiler=str(sFiler),
                nFiler=str(nFiler),
                width=size[2],
                height=size[0],
                depth=size[1],
            ),
            ToConnection(f"{botton}", f"{layerName}"),
        ]
        botton = layerName
        lys += ly

    lys += [
        ToSkip(of=layers[1], to=layers[-2], pos=1.25),
    ]
    return lys
