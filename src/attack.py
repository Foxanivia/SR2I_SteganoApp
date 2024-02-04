
import sys
from multiprocessing.pool import ThreadPool

from scipy import ndimage, misc
from cmath import sqrt
import imageio

def spa(imam):

    seuil = 0.05 # Pour des images plus grandes essayer plus petit
    channel_map = {0: 'R', 1: 'G', 2: 'B'}

    I3d = imageio.imread(imam)
    width, height, channels = I3d.shape

    iii=0
    for ch in range(3):


        I = I3d[:, :, ch]

        x = 0
        y = 0
        k = 0
        for j in range(height):
            for i in range(width - 1):
                r = I[i, j]
                s = I[i + 1, j]
                if (s % 2 == 0 and r < s) or (s % 2 == 1 and r > s):
                    x += 1
                if (s % 2 == 0 and r > s) or (s % 2 == 1 and r < s):
                    y += 1
                if round(s / 2) == round(r / 2):
                    k += 1

        if k == 0:
            print("ERROR")
            sys.exit(0)

        a = 2 * k
        b = 2 * (2 * x - width * (height - 1))
        c = y - x

        bp = (-b + sqrt(b ** 2 - 4 * a * c)) / (2 * a)
        bm = (-b - sqrt(b ** 2 - 4 * a * c)) / (2 * a)
        beta = min(bp.real, bm.real)
        print(channel_map[ch] + ": stego", beta)
        if beta > seuil:
            print(channel_map[ch] + ": stego", beta)
        else:
            print(channel_map[ch] + ": cover")


def bruteforce_steghide():
    if not os.path.isfile(password_file):
        print("ERROR: File not found -", password_file)
        sys.exit(0)

    aletheialib.utils.check_bin("steghide")
    command = f"steghide extract -sf {path} -xf output.txt -p <PASSWORD> -f"

    if not os.path.isfile(password_file):
        print("ERROR: File not found -", password_file)
        sys.exit(0)

    with open(password_file, "rU") as f:
        passwords = f.readlines()

    params = [(passwd.replace("\n", ""),
               command,
               use_filetype,
               continue_searching,
               success_output_string) for passwd in passwords]

    n_proc = cpu_count()
    print("Using", n_proc, "processes")
    pool = ThreadPool(n_proc)

    # Process thread pool in batches
    batch = 100
    for i in range(0, len(params), batch):
        perc = round(100 * float(i) / len(passwords), 2)
        sys.stderr.write("Completed: " + str(perc) + '%    \r')
        pool = ThreadPool(n_proc)
        results = pool.map(check_password, params[i:i + batch])
        pool.close()
        pool.terminate()
        pool.join()
        if any(results):
            break



