import s3fs
import tempfile
import os
import re

def validate_s3_path(s3_path: str) -> bool:
    """
    S3 경로가 올바른지 간단히 체크하는 함수
    올바른 형식: s3://버킷명/키
    """
    pattern = r"^s3://[a-z0-9\-\.]{3,63}/.+"
    return bool(re.match(pattern, s3_path.strip()))

def download_s3_to_tempfile(s3_path: str) -> str:
    fs = s3fs.S3FileSystem(anon=False)  # 동기 모드
    with fs.open(s3_path, 'rb') as s3file:
        suffix = '.' + s3_path.split('.')[-1]
        with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmpfile:
            tmpfile.write(s3file.read())
            return tmpfile.name

def cleanup_tempfiles(file_paths):
    for path in file_paths:
        try:
            os.remove(path)
        except Exception:
            pass
