import numpy as np

# root mean square error calculation
def rmse_calc(cleaned_data, original_data):
    n = original_data.shape[0]
    m = original_data.shape[1]
    nm = n*m

    data = (cleaned_data - original_data)**2
    summation = np.sum(data)

    if nm != 0:
        return round(np.sqrt(summation/nm), 6)
    else:
        return 0.0


# peak signal-to-noise calculation
def psnr_calc(cleaned_data, original_data):
    rmse = rmse_calc(cleaned_data, original_data)
    max_val = np.max(cleaned_data)

    if rmse != 0 and max_val != 0:
        return round(10 * np.log10((max_val / rmse)**2), 6)
    else:
        return 0.0
