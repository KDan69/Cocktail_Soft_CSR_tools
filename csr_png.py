import sys
from PIL import Image

def make_csr_header(width, height):  
    if width % 8 != 0:
        raise ValueError("Width must be a multiple of 8 pixels!")

    return (
        b"MC" +
        b"\x00\x4F" +
        b"\x00\x00" +
        bytes([width // 8, height])
    )

def parse_csr_header(data):
    if len(data) < 8 or data[:2] != b"MC":
        raise ValueError("Invalid CSR file!")

    width = data[6] * 8
    height = data[7]
    return width, height

def png_to_csr(png_path, csr_path):
    img = Image.open(png_path).convert("P")
    width, height = img.size

    if width % 8 != 0:
        raise ValueError("Image width must be a multiple of 8")

    pixels = list(img.getdata())
    plane_size = (width * height) // 8
    planes = [bytearray(plane_size) for _ in range(4)]

    for i, px in enumerate(pixels):
        for bit in range(4):
            if px & (1 << bit):
                planes[bit][i // 8] |= (1 << (7 - (i % 8)))

    with open(csr_path, "wb") as f:
        f.write(make_csr_header(width, height))
        for plane in planes:
            f.write(plane)

    print(f"CSR written: {csr_path} ({width}x{height})")

def csr_to_png(csr_path, png_path):
    with open(csr_path, "rb") as f:
        data = f.read()

    width, height = parse_csr_header(data)
    plane_size = (width * height) // 8
    offset = 8

    planes = [
        data[offset + i * plane_size : offset + (i + 1) * plane_size]
        for i in range(4)
    ]

    pixels = []
    for i in range(width * height):
        value = 0
        for bit in range(4):
            if planes[bit][i // 8] & (1 << (7 - (i % 8))):
                value |= (1 << bit)
        pixels.append(value)

    img = Image.new("P", (width, height))
    img.putdata(pixels)

    # default 16-color grayscale palette
    palette = []
    for i in range(16):
        g = int(i * 255 / 15)
        palette.extend([g, g, g])
    img.putpalette(palette + [0] * (768 - len(palette)))

    img.save(png_path)
    print(f"PNG written: {png_path} ({width}x{height})")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage:")
        print("  python csr_png.py input_file output_file")
        sys.exit(1)

    input_file, output_file = sys.argv[1:]
    in_ext = input_file.lower().rsplit(".", 1)[-1]
    out_ext = output_file.lower().rsplit(".", 1)[-1]

    if in_ext == "png" and out_ext == "csr":
        png_to_csr(input_file, output_file)
    elif in_ext == "csr" and out_ext == "png":
        csr_to_png(input_file, output_file)
    else:
        print("Error: What the hell are you trying to convert here?")
        print("Expected:")
        print("  PNG -> CSR  or  CSR -> PNG")
        sys.exit(1)