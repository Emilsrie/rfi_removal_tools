import numpy as np

def vertical_threshold(array, mask, initial_thr, sub_sequence):
    width, height = array.shape
    tmp_mask = np.zeros(mask.shape)

    if sub_sequence <= width:
        for y in range(height):
            summation = 0.0
            counter = 0
            xLeft = 0
            xRight = 0

            for x in range(width):
                if not mask[x, y]:
                    break
            else:
                continue

            for xRight in range(sub_sequence - 1):
                if not mask[xRight, y]:
                    summation += array[xRight, y]
                    counter += 1

            while xRight < width:
                # add the sample to the right
                if not mask[xRight, y]:
                    summation += array[xRight, y]
                    counter += 1
                # check
                if (counter > 0) and (abs(summation / counter) > initial_thr):
                    tmp_mask[xLeft:xLeft + sub_sequence, y] = True

                # subtract the sample at the left
                if not mask[xLeft, y]:
                    summation -= array[xLeft, y]
                    counter -= 1

                xLeft += 1
                xRight += 1

    return tmp_mask


def horizontal_threshold(array, mask, initial_thr, sub_sequence):
    width, height = array.shape
    tmp_mask = np.zeros(mask.shape)

    if sub_sequence <= height:
        for x in range(width):
            summation = 0.0
            counter = 0
            yTop = 0
            yBottom = 0

            for y in range(height):
                if not mask[x, y]:
                    break
            else:
                continue

            for yBottom in range(sub_sequence - 1):
                if not mask[x, yBottom]:
                    summation += mask[x, yBottom]
                    counter += 1

            while yBottom < height:
                # add the sample at the bottom
                if not mask[x, yBottom]:
                    summation += array[x, yBottom]
                counter += 1
                # check
                if (counter > 0) and (abs(summation / counter) > initial_thr):
                    tmp_mask[x, yTop:yTop + sub_sequence] = True

                # subtract the sample at the top
                if not mask[x, yTop]:
                    summation -= array[x, yTop]
                    counter -= 1

                yTop += 1
                yBottom += 1

    return tmp_mask

def full_sum_threshold(array, mask, initial_hor_thr, initial_ver_thr, horizontal_windows, vertical_windows, p):
    if initial_ver_thr != 0:
        # Time domain
        for i in range(1, len(vertical_windows) + 1):
            threshold = initial_ver_thr / p ** (np.log2(vertical_windows[i - 1]))
            print("Vertical threshold: " + str(threshold))
            mask = vertical_threshold(array, mask, threshold, sub_sequence=vertical_windows[i - 1])

    if initial_hor_thr != 0:
        # Frequency domain
        for i in range(1, len(horizontal_windows) + 1):
            threshold = initial_hor_thr / p ** (np.log2(horizontal_windows[i - 1]))
            print("Horizontal threshold: " + str(threshold))
            mask = horizontal_threshold(array, mask, threshold, sub_sequence=horizontal_windows[i - 1])

    return mask

