from base64 import b64encode
from os.path import getsize
from mimetypes import guess_type
from django.core.files import File
def iter_file_content(file_path, chunk_size=File.DEFAULT_CHUNK_SIZE):
    file_size = getsize(file_path)
    with open(file_path, 'rb') as f:
        while f.tell() != file_size:
            data = f.read(chunk_size)
            yield data
def iter_file_to_blob_src(uploaded):
    content_type = guess_type(uploaded.name)[0]
    yield f'data:{content_type};base64,'
    for chunk in uploaded.chunks():
        yield str(b64encode(chunk), encoding='utf8')

