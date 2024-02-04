from DCT.DCT_commun import *


def apply_dct_modify_coefficients(blocks, message):
    binary_message = message_to_binary(message)
    message_index = 0
    message_length = len(binary_message)

    modified_blocks = []

    for block in blocks:
        # Apply 2D DCT
        dct_block = dct(dct(block.T, norm='ortho').T, norm='ortho')

        # Iterate over high-frequency positions to modify coefficients
        for i in range(4, 8):
            for j in range(4, 8):
                if message_index < message_length:
                    # Modify the last bit of the coefficient with the message bit in one action
                    coef = dct_block[i, j]
                    # Clear the last bit and add the message bit directly
                    coef = (coef - coef % 2) + int(binary_message[message_index])
                    # Update the coefficient in the DCT block
                    dct_block[i, j] = coef
                    message_index += 1
                else:
                    break  # Exit loops if the entire message is encoded
            if message_index >= message_length:
                break

        # Apply the inverse DCT
        block_modified = idct(idct(dct_block.T, norm='ortho').T, norm='ortho')
        modified_blocks.append(block_modified)

    return modified_blocks