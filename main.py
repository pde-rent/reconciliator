import os
import shutil
import hashlib

def checksum(file_path, chunk_size=16*1024):
    # Initialize the hash object
    sha256_hash = hashlib.sha256()

    # Open the file in binary mode
    with open(file_path, "rb") as f:
        # Read the file chunk by chunk to avoid loading the entire file into memory
        for chunk in iter(lambda: f.read(chunk_size), b""):
            sha256_hash.update(chunk)

    # Get the hexadecimal digest of the hash
    return sha256_hash.hexdigest()

def same_file(f1, f2):
    checksum1 = checksum(f1)
    checksum2 = checksum(f2)
    return checksum1 == checksum2

def reconcile_folders(dst_folder, src_folder, rm_all_duplicates=True, simulate=False):

    mismatch_conflicts = []
    duplicates_to_remove = []
    duplicates = set()
    path_by_duplicates = {}

    def get_all_nested_files(root):
        files = []
        for dirpath, dirnames, filenames in os.walk(root):
            if len(filenames) > 0:
                for f in filenames:
                    files.append(os.path.join(dirpath, f))
            for d in dirnames:
                nested_files = get_all_nested_files(os.path.join(dirpath, d))
                if nested_files and len(nested_files) > 0:
                    files += nested_files
        return files

    files = get_all_nested_files(src_folder)
    # Walk through the nested folder recursively
    for src_file_path in files:
        f = src_file_path.split(src_folder)[1]
        dst_file_path = dst_folder + f

        # If the file exists in the root folder and is the same, delete it from the nested folder
        if os.path.exists(dst_file_path):
            if same_file(src_file_path, dst_file_path):
                if not simulate:
                    os.remove(src_file_path)
                print(f"Removed duplicate file {f} from {src_folder}")
            else:
                print(f"Conflict: {f} differs in dst folder. Please handle manually...")
                mismatch_conflicts.append(f)
        else:
            cs = checksum(src_file_path)
            if f in duplicates or cs in duplicates:
                prev_path = path_by_duplicates.get(f, path_by_duplicates[cs])
                print(f"{f} is a copy of {prev_path}")
                duplicates_to_remove.append(f)
                if rm_all_duplicates:
                    if not simulate:
                        os.remove(src_file_path)
                    print(f"Removed duplicate file {f} from {src_folder}")
                continue
            else:
                duplicates.add(f)
                duplicates.add(cs)
                path_by_duplicates[f] = src_file_path
                path_by_duplicates[cs] = src_file_path
            if not simulate:
                shutil.move(src_file_path, os.path.dirname(dst_file_path))
            print(f"Moved missing file {f} to dst {dst_file_path}")

    # After moving all files, remove the empty nested folder
    try:
        if len(mismatch_conflicts) > 0:
            print("Please resolve these mismatch conflicts:")
            for conflict in mismatch_conflicts:
                print(f"\t- {conflict}")

        if len(duplicates_to_remove) > 0:
            if rm_all_duplicates:
                print(f"{len(duplicates_to_remove)} duplicates removed:")
            else:
                print("Please remove these duplicates:")
            for duplicate in duplicates_to_remove:
                prev_path = path_by_duplicates.get(duplicate, None)
                print(f"\t- {duplicate}->{prev_path}")
        else:
            if not simulate:
                shutil.rmtree(src_folder)
            print(f"{src_folder} cleared removed")
    except OSError as e:
        print(f"Error: {src_folder} could not be removed {e}")

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Reconcile folders (partially copied, duplicates, version conflicts, etc.)")
    parser.add_argument("--dst", type=str, help="Destination folder (to be updated)", required=True)
    parser.add_argument("--src", type=str, help="Source folder (to be removed)", required=True)
    parser.add_argument("--rm-all-duplicates", action="store_true", help="Remove all duplicates", default=False)
    parser.add_argument("--simulate", action="store_true", help="Simulate the operation", default=False)
    args = parser.parse_args()
    reconcile_folders(
        dst_folder=args.dst,
        src_folder=args.src,
        rm_all_duplicates=args.rm_all_duplicates,
        simulate=args.simulate)
