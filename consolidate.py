import os
import sys

def consolidate_csr(input_dir, output_file):
    header_path = os.path.join(input_dir, "header.dat")

    file_list = [
        f for f in os.listdir(input_dir)
        if os.path.isfile(os.path.join(input_dir, f)) and f.endswith(".csr")
    ]
    file_list.sort()

    with open(output_file, 'wb') as outfile:
        # Write header first (no separator after)
        with open(header_path, 'rb') as header:
            outfile.write(header.read())

        # Write .csr files with separators between them
        for i, filename in enumerate(file_list):
            file_path = os.path.join(input_dir, filename)
            with open(file_path, 'rb') as infile:
                outfile.write(infile.read())
            if i < len(file_list) - 1:
                outfile.write(b'\x00\x00') #files needs to be separated by 00 00

    print(f"Header and {len(file_list)} CSR files processed.")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage:")
        print("  python consolidate.py input_folder output.csr")
        sys.exit(1)

    folder, output = sys.argv[1:]
    consolidate_csr(folder, output)