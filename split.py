import os
import sys

HEADER_MAGIC = b"MC"
HEADER_SIZE = 8

def split_mc(input_file, output_dir):
    with open(input_file, "rb") as f:
        data = f.read()

    os.makedirs(output_dir, exist_ok=True)
    pre_mc = data.find(HEADER_MAGIC)
    if pre_mc == -1:
        raise ValueError("No MC header found in file!")

    header_data = data[:pre_mc]
    header_path = os.path.join(output_dir, "header.dat")
    with open(header_path, "wb") as f:
        f.write(header_data)

    print(f"Header saved to {header_path} ({len(header_data)} bytes)")

    offset = pre_mc
    chunk_count = 0

    while offset < len(data):
        start = data.find(HEADER_MAGIC, offset)
        if start == -1:
            break

        if start + HEADER_SIZE > len(data):
            break

        header = data[start:start + HEADER_SIZE]
        width_px = header[6] * 8   
        height_px = header[7]
        image_bytes = (width_px * height_px) // 2  # 4bpp
        chunk_size = HEADER_SIZE + image_bytes
        end = start + chunk_size

        if end > len(data):
            print(f"Truncated image at offset {start:X}, stopping.")
            break
        chunk = data[start:end]
        output_filename = os.path.join(output_dir, f"{chunk_count:04}.csr")
        with open(output_filename, "wb") as out:
            out.write(chunk)

        print(
            f"Extracted {output_filename} | "
            f"Offset {start:X} | "
            f"{width_px}x{height_px} | "
            f"{chunk_size} bytes"
        )

        chunk_count += 1
        offset = end

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage:")
        print(" python split.py input_file.csr output_directory")
        sys.exit(1)

    inp_file, out_dir = sys.argv[1:]
    split_mc(inp_file, out_dir)