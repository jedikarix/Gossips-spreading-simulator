import os
import requests
import zipfile

import nltk


def download_file(url, destination, compressed):
    print(f'Downloading {url} to {destination}')

    if not os.path.exists(os.path.dirname(destination)):
        os.makedirs(os.path.dirname(destination))

    if os.path.isfile(destination):
        print('File exists, skipping')
    else:
        downloaded = 0
        fname = f'{destination}.zip' if compressed else destination

        with requests.Session() as session:
            response = session.get(url, stream=True)
            google_warning_cookies = [v.value for v in response.cookies if v.name.startswith('download_warning')]
            if google_warning_cookies:
                response = session.get(f'{url}&confirm={google_warning_cookies[0]}', stream=True)

            size = int(response.headers['content-length']) // 1024 if 'content-length' in response.headers else '???'

            with open(fname, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        downloaded += len(chunk)
                        f.write(chunk)
                        print('\r{} kB /{} kB'.format(downloaded // 1024, size), end='')
        print()

        if compressed:
            print('Unzipping...')
            with zipfile.ZipFile(fname) as z:
                z.extractall(os.path.dirname(destination))
            print('Removing archive...')
            os.remove(fname)

        print('Done')
        print()


nltk.download('punkt')

download_file(
    'https://genseniclr2018.blob.core.windows.net/models/nli_large.model',
    os.path.join(os.path.dirname(__file__), 'GenSen', 'data', 'models', 'nli_large.model'),
    compressed=False
)

download_file(
    'https://genseniclr2018.blob.core.windows.net/models/nli_large_vocab.pkl',
    os.path.join(os.path.dirname(__file__), 'GenSen', 'data', 'models', 'nli_large_vocab.pkl'),
    compressed=False
)

download_file(
    'https://drive.google.com/uc?export=download&id=1lp927MxN6Rl7fZZvHffN2jW-0zK86jfV',
    os.path.join(os.path.dirname(__file__), 'GenSen', 'data', 'models', 'senteval.pickle'),
    compressed=False
)

download_file(
    'https://drive.google.com/uc?export=download&id=1AhX5E-w5GkvwPn9n3nDxLTHQ9rwN26hn',
    os.path.join(os.path.dirname(__file__), 'GenSen', 'data', 'embedding', 'glove.840B.300d.h5'),
    compressed=True
)
