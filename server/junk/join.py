import hashlib
import json
import sys
# Chunk size 1MB
chunk_size = 1024 * 1024
DEST_DIR = "dest/"
PART_DIR = "parts/"
def read_meta(file_path):
    with open(PART_DIR+file_path+".meta") as file:
        data = json.load(file)
        return data

def join_files(file_path):
    meta_data = read_meta(file_path)
    chunk_count = meta_data["chunk_count"]
    parts = meta_data["parts"]
    # Open the output file for writing
    with open(DEST_DIR+file_path, 'wb') as output_file:
        # Iterate over the chunks and write them to the output file
        for i in range(0, chunk_count):
        #for hash in parts:
            #chunk_file_path = file_path + f'.part{i:03d}'
            hash = parts[str(i)]
            chunk_file_path = PART_DIR+hash
            with open(chunk_file_path, 'rb') as chunk_file:
                output_file.write(chunk_file.read())

        print(f'Successfully joined {chunk_count} file parts into {file_path}.')

if __name__ == '__main__':
    file_path = sys.argv[1]
    chunk_size = 1024 * 1024

    join_files(file_path)

