import numpy, imageio
from PIL import Image

path = input()
image_name = path.split('/')[-1] + '.png'

im = imageio.imread(path + '/' + image_name)
piece_dict = {0:'black_bishop', 
              1:'black_king',
              2:'black_queen',
              3:'black_knight',
              4:'black_pawn',
              5:'black_rook',
              6:'white_bishop',
              7:'white_king',
              8:'white_queen',
              9:'white_knight',
              10:'white_pawn',
              11:'white_rook'}

board = numpy.array(im)
board_top = numpy.nonzero(board)[0][0]
board_left = numpy.nonzero(board)[1][0]

print(board_top, board_left, sep=',')

board_bottom = numpy.nonzero(board)[0][-1] + 1 
board_right = numpy.nonzero(board)[1][-1] + 1 
board_dims = (board_bottom - board_top, board_right - board_left)
field_dims = (int(board_dims[0] / 8), int(board_dims[1] / 8))

black = numpy.array(Image.fromarray(imageio.imread(path + '/tiles/black.png', pilmode="RGB")).resize((field_dims[0], field_dims[1])))
white = numpy.array(Image.fromarray(imageio.imread(path + '/tiles/white.png', pilmode="RGB")).resize((field_dims[0], field_dims[1])))

pieces = numpy.ndarray((12, field_dims[0], field_dims[1], 4), dtype=numpy.uint8)
pieces[0] = numpy.array(Image.fromarray(imageio.imread(path + '/pieces/black/bishop.png')).resize((field_dims[0], field_dims[1])))
pieces[1] = numpy.array(Image.fromarray(imageio.imread(path + '/pieces/black/king.png')).resize((field_dims[0], field_dims[1])))
pieces[2] = numpy.array(Image.fromarray(imageio.imread(path + '/pieces/black/queen.png')).resize((field_dims[0], field_dims[1])))
pieces[3] = numpy.array(Image.fromarray(imageio.imread(path + '/pieces/black/knight.png')).resize((field_dims[0], field_dims[1])))
pieces[4] = numpy.array(Image.fromarray(imageio.imread(path + '/pieces/black/pawn.png')).resize((field_dims[0], field_dims[1])))
pieces[5] = numpy.array(Image.fromarray(imageio.imread(path + '/pieces/black/rook.png')).resize((field_dims[0], field_dims[1])))
pieces[6] = numpy.array(Image.fromarray(imageio.imread(path + '/pieces/white/bishop.png')).resize((field_dims[0], field_dims[1])))
pieces[7] = numpy.array(Image.fromarray(imageio.imread(path + '/pieces/white/king.png')).resize((field_dims[0], field_dims[1])))
pieces[8] = numpy.array(Image.fromarray(imageio.imread(path + '/pieces/white/queen.png')).resize((field_dims[0], field_dims[1])))
pieces[9] = numpy.array(Image.fromarray(imageio.imread(path + '/pieces/white/knight.png')).resize((field_dims[0], field_dims[1])))
pieces[10] = numpy.array(Image.fromarray(imageio.imread(path + '/pieces/white/pawn.png')).resize((field_dims[0], field_dims[1])))
pieces[11] = numpy.array(Image.fromarray(imageio.imread(path + '/pieces/white/rook.png')).resize((field_dims[0], field_dims[1])))

def populated_spaces(board, top, left, f_dims):
    pop_spaces = []
    for i in range(0, 8):
        for j in range(0, 8):
            space = board[top+i*f_dims[0]:top+(i+1)*f_dims[0], left+j*f_dims[1]:left+(j+1)*f_dims[1], :]
            if (numpy.mean(space) == numpy.mean(white)) or (numpy.mean(space) == numpy.mean(black)):
                continue
            else:
                pop_spaces.append((i, j))
    return pop_spaces

def determine_piece(place, board, top, left, f_dims, pieces):
    if sum(place) % 2 == 0:
        tile = Image.fromarray(imageio.imread(path + '/tiles/white.png')).resize((f_dims[0], f_dims[1]))
    else: 
        tile = Image.fromarray(imageio.imread(path + '/tiles/black.png')).resize((f_dims[0], f_dims[1]))
    space = board[top+place[0]*f_dims[0]:top+(place[0]+1)*f_dims[0], left+place[1]*f_dims[1]:left+(place[1]+1)*f_dims[1], :]
    for i in range(0, 12):
        pie = Image.fromarray(pieces[i, :, :, :])
        holder = tile.copy()
        holder.paste(pie, (0, 0), pie)
        supposed_space = numpy.array(holder)
        comparison = space == supposed_space[:, :, :3]
        if comparison.all():
            return i

pop = populated_spaces(board, board_top, board_left, field_dims)
sim_board = numpy.zeros((8, 8))

for p in pop:
    sim_board[p[0], p[1]] = determine_piece(p, board, board_top, board_left, field_dims, pieces)
