#!/usr/bin/env python3
"""
Build and validate Google Play Console Developer Profile assets.
Converts SVGs to 24-bit non-transparent PNGs and JPEGs meeting Play Console specs.
"""
import os
import subprocess
import struct
import zlib
import sys

def render_svg_to_png(svg_path, out_png_path):
    subprocess.run(['sips', '-s', 'format', 'png', svg_path, '--out', out_png_path], check=True)

def render_svg_to_jpeg(svg_path, out_jpg_path, quality="90"):
    subprocess.run(['sips', '-s', 'format', 'jpeg', '-s', 'formatOptions', quality, svg_path, '--out', out_jpg_path], check=True)

def unfilter_rgba(raw, w, h):
    stride = 1 + w * 4
    out = bytearray(w * h * 4)
    prev = bytearray(w * 4)
    for y in range(h):
        row_raw = raw[y * stride : (y + 1) * stride]
        filter_type = row_raw[0]
        cur = bytearray(w * 4)
        for i in range(w * 4):
            x = row_raw[1 + i]
            a = cur[i - 4] if i >= 4 else 0
            b = prev[i]
            c = prev[i - 4] if i >= 4 else 0
            if filter_type == 0: val = x
            elif filter_type == 1: val = (x + a) & 0xff
            elif filter_type == 2: val = (x + b) & 0xff
            elif filter_type == 3: val = (x + (a + b) // 2) & 0xff
            elif filter_type == 4:
                p = a + b - c; pa = abs(p - a); pb = abs(p - b); pc = abs(p - c)
                if pa <= pb and pa <= pc: pr = a
                elif pb <= pc: pr = b
                else: pr = c
                val = (x + pr) & 0xff
            cur[i] = val
        out[y * w * 4 : (y + 1) * w * 4] = cur
        prev = cur
    return out

def convert_rgba_to_rgb24_png(in_rgba_png, out_rgb_png, mask=0xff):
    with open(in_rgba_png, 'rb') as f:
        sig = f.read(8)
        assert sig == b'\x89PNG\r\n\x1a\n'
        chunks = []
        while True:
            lb = f.read(4)
            if not lb: break
            l = struct.unpack('>I', lb)[0]
            t = f.read(4)
            d = f.read(l)
            c = f.read(4)
            chunks.append((t, d))
            if t == b'IEND': break

    ihdr = [c[1] for c in chunks if c[0] == b'IHDR'][0]
    w, h, bit_depth, color_type = struct.unpack('>IIBB', ihdr[:10])
    
    idat_data = b''.join([c[1] for c in chunks if c[0] == b'IDAT'])
    decomp = zlib.decompress(idat_data)
    
    if color_type == 6:
        raw_rgba = unfilter_rgba(decomp, w, h)
        bpp = 3
        out_scanlines = []
        prev = bytearray(w * bpp)
        for y in range(h):
            rgba_row = raw_rgba[y * w * 4 : (y + 1) * w * 4]
            cur = bytearray(w * bpp)
            for x in range(w):
                cur[x*3] = rgba_row[x*4] & mask
                cur[x*3+1] = rgba_row[x*4+1] & mask
                cur[x*3+2] = rgba_row[x*4+2] & mask
            
            # Adaptive Sub vs Up heuristic
            sub = bytearray(w * bpp)
            sum_sub = 0
            for i in range(w * bpp):
                diff = (cur[i] - (cur[i - bpp] if i >= bpp else 0)) & 0xff
                sub[i] = diff
                sum_sub += diff if diff < 128 else 256 - diff
            
            up = bytearray(w * bpp)
            sum_up = 0
            for i in range(w * bpp):
                diff = (cur[i] - prev[i]) & 0xff
                up[i] = diff
                sum_up += diff if diff < 128 else 256 - diff
            
            if sum_sub <= sum_up:
                out_scanlines.append(b'\x01' + sub)
            else:
                out_scanlines.append(b'\x02' + up)
            prev = cur
        
        filtered_raw = b''.join(out_scanlines)
        new_idat = zlib.compress(filtered_raw, level=9)
        new_ihdr = struct.pack('>IIBBBBB', w, h, 8, 2, 0, 0, 0)
        
        def make_chunk(ctype, data):
            crc = zlib.crc32(ctype + data) & 0xffffffff
            return struct.pack('>I', len(data)) + ctype + data + struct.pack('>I', crc)
        
        with open(out_rgb_png, 'wb') as out_f:
            out_f.write(b'\x89PNG\r\n\x1a\n')
            out_f.write(make_chunk(b'IHDR', new_ihdr))
            out_f.write(make_chunk(b'IDAT', new_idat))
            out_f.write(make_chunk(b'IEND', b''))
    else:
        # Already RGB
        with open(out_rgb_png, 'wb') as out_f:
            with open(in_rgba_png, 'rb') as in_f:
                out_f.write(in_f.read())

def validate_png(path, expected_w, expected_h, max_bytes=1048576):
    size = os.path.getsize(path)
    with open(path, 'rb') as f:
        sig = f.read(8)
        assert sig == b'\x89PNG\r\n\x1a\n', f"{path} invalid PNG signature"
        l = struct.unpack('>I', f.read(4))[0]
        t = f.read(4)
        assert t == b'IHDR', f"{path} missing IHDR"
        w, h, bit_depth, color_type = struct.unpack('>IIBB', f.read(10))
    
    assert w == expected_w, f"{path} width {w} != {expected_w}"
    assert h == expected_h, f"{path} height {h} != {expected_h}"
    assert bit_depth == 8, f"{path} bit_depth {bit_depth} != 8"
    assert color_type == 2, f"{path} color_type {color_type} != 2 (not 24-bit RGB non-transparent)"
    assert size <= max_bytes, f"{path} size {size} > {max_bytes} (1 MB)"
    print(f"✓ {path}: {w}x{h}, 24-bit RGB (color_type={color_type}), {size} bytes ({size/1024:.1f} KB) <= 1 MB")

def validate_jpeg(path, expected_w, expected_h, max_bytes=1048576):
    size = os.path.getsize(path)
    # Check JPEG dimensions via sips
    out = subprocess.run(['sips', '-g', 'pixelWidth', '-g', 'pixelHeight', '-g', 'hasAlpha', path], capture_output=True, text=True).stdout
    assert f"pixelWidth: {expected_w}" in out, f"{path} width mismatch: {out}"
    assert f"pixelHeight: {expected_h}" in out, f"{path} height mismatch: {out}"
    assert "hasAlpha: no" in out, f"{path} has alpha"
    assert size <= max_bytes, f"{path} size {size} > {max_bytes}"
    print(f"✓ {path}: {expected_w}x{expected_h}, JPEG (no alpha), {size} bytes ({size/1024:.1f} KB) <= 1 MB")

def main():
    root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    assets_dir = os.path.join(root, 'assets', 'play-console')
    
    icon_svg = os.path.join(assets_dir, 'developer-icon-512x512.svg')
    icon_png = os.path.join(assets_dir, 'developer-icon-512x512.png')
    icon_jpg = os.path.join(assets_dir, 'developer-icon-512x512.jpg')
    
    header_svg = os.path.join(assets_dir, 'header-image-4096x2304.svg')
    header_png = os.path.join(assets_dir, 'header-image-4096x2304.png')
    header_jpg = os.path.join(assets_dir, 'header-image-4096x2304.jpg')
    
    tmp_icon_png = '/tmp/raw_icon_render.png'
    tmp_header_png = '/tmp/raw_header_render.png'
    
    print("Rendering developer icon...")
    render_svg_to_png(icon_svg, tmp_icon_png)
    convert_rgba_to_rgb24_png(tmp_icon_png, icon_png, mask=0xff)
    render_svg_to_jpeg(icon_svg, icon_jpg)
    
    print("Rendering header image banner (4096x2304)...")
    render_svg_to_png(header_svg, tmp_header_png)
    convert_rgba_to_rgb24_png(tmp_header_png, header_png, mask=0xf8)
    render_svg_to_jpeg(header_svg, header_jpg)
    
    print("\nValidating generated assets against Google Play Console specs:")
    validate_png(icon_png, 512, 512)
    validate_jpeg(icon_jpg, 512, 512)
    validate_png(header_png, 4096, 2304)
    validate_jpeg(header_jpg, 4096, 2304)
    
    # Cleanup
    if os.path.exists(tmp_icon_png): os.remove(tmp_icon_png)
    if os.path.exists(tmp_header_png): os.remove(tmp_header_png)
    print("\nAll assets built and verified successfully!")

if __name__ == '__main__':
    main()
