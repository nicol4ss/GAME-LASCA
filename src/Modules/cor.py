def iluminar_escurecer_cor(cor, deslocamento=-15):
    """ escurece ou ilumina uma cor em hex, como #87c95f, por exemplo """

    rgb_hex = [cor[x:x+2] for x in [1, 3, 5]]
    novo_rgb = [int(valor_hex, 16) + deslocamento for valor_hex in rgb_hex]
    novo_rgb = [min([255, max([0, i])]) for i in novo_rgb]                  # garante que valores estejam entre 0 e 255

    return "#" + "".join([hex(i)[2:] for i in novo_rgb])