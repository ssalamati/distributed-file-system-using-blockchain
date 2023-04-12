import hashlib
import json

# Chunk size 1MB
chunk_size = 1024 * 1024
SOURCE_DIR = "source/"
PART_DIR = "parts/"
DEST_DIR = "dest/"


class FileHandler:
    def __init__(self, file_path):
        self.file_path = file_path

    def write_meta(self, hash, parts, chunk_count):
        details = {
            "file_hash": hash,
            "chunk_count": chunk_count,
            "parts": parts
        }
        with open(PART_DIR + self.file_path + ".meta", 'w') as meta_file:
            meta_file.write(json.dumps(details))

    def split_file(self):

        # Open the file for reading
        hash_object = hashlib.sha256()
        with open(SOURCE_DIR + self.file_path, 'rb') as f:
            file = f.read(chunk_size)
            hash_object.update(file)
            file_hash = hash_object.hexdigest()
        with open(SOURCE_DIR + self.file_path, 'rb') as f:
            chunk_data = f.read(chunk_size)
            chunk_count = 0
            # Split the file into chunks and write them to disk
            parts = {}
            while chunk_data:
                hash_object.update(chunk_data)
                hash = hash_object.hexdigest()
                with open(PART_DIR + hash, 'wb') as chunk_file:
                    chunk_file.write(chunk_data)
                chunk_data = f.read(chunk_size)
                parts[chunk_count] = hash
                chunk_count += 1
            self.write_meta(file_hash, parts, chunk_count)
            print(f'Successfully split file {self.file_path} into {chunk_count} parts.')

    def hash_file(self):
        # Create a SHA256 hash object
        hash_object = hashlib.sha256()

        # Open the file for reading and hash each chunk
        with open(self.file_path, 'rb') as f:
            chunk_data = f.read(chunk_size)
            while chunk_data:
                hash_object.update(chunk_data)
                chunk_data = f.read(chunk_size)

        print(f'SHA256 hash of file {self.file_path}: {hash_object.hexdigest()}')

    def read_meta(self):
        with open(PART_DIR+self.file_path+".meta") as file:
            data = json.load(file)
            return data

    def join_files(self):
        meta_data = self.read_meta()
        chunk_count = meta_data["chunk_count"]
        parts = meta_data["parts"]
        # Open the output file for writing
        with open(DEST_DIR+self.file_path, 'wb') as output_file:
            # Iterate over the chunks and write them to the output file
            for i in range(0, chunk_count):
                hash = parts[str(i)]
                chunk_file_path = PART_DIR+hash
                with open(chunk_file_path, 'rb') as chunk_file:
                    output_file.write(chunk_file.read())

            print(f'Successfully joined {chunk_count} file parts into {self.file_path}.')


if __name__ == '__main__':
    fh = FileHandler('test.txt')
    fh.split_file()

    fh.join_files()
