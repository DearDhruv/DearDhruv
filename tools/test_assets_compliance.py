#!/usr/bin/env python3
"""
Deep verification test for Google Play Developer Console profile assets.
Tests strict compliance with Google Play Developer Console technical & policy specifications.
"""
import os
import struct
import subprocess
import sys

def test_png_compliance(path, expected_w, expected_h, max_bytes=1048576):
    assert os.path.exists(path), f"File missing: {path}"
    file_size = os.path.getsize(path)
    
    with open(path, 'rb') as f:
        sig = f.read(8)
        assert sig == b'\x89PNG\r\n\x1a\n', f"{path} is not a valid PNG"
        
        # Read IHDR chunk
        chunk_len = struct.unpack('>I', f.read(4))[0]
        chunk_type = f.read(4)
        assert chunk_type == b'IHDR', f"{path} first chunk is not IHDR"
        ihdr_data = f.read(chunk_len)
        f.read(4) # CRC
        
        w, h, bit_depth, color_type, comp, filt, inter = struct.unpack('>IIBBBBB', ihdr_data)
        
        # Assertions
        assert w == expected_w, f"Width {w} != {expected_w}"
        assert h == expected_h, f"Height {h} != {expected_h}"
        assert bit_depth == 8, f"Bit depth {bit_depth} != 8"
        # Color type 2 = Truecolor RGB (24-bit, NO alpha channel)
        # Color type 6 = RGBA (disallowed by console)
        assert color_type == 2, f"Color type {color_type} != 2 (must be non-transparent 24-bit RGB)"
        assert comp == 0, "Compression must be 0"
        assert filt == 0, "Filter method must be 0"
        assert file_size <= max_bytes, f"File size {file_size} exceeds {max_bytes} (1 MB)"
        
    print(f" PASS: {os.path.basename(path)} -> {w}x{h} px, 24-bit RGB (color_type={color_type}), {file_size:,} bytes ({file_size/1024:.1f} KB) <= 1 MB")

def test_jpeg_compliance(path, expected_w, expected_h, max_bytes=1048576):
    assert os.path.exists(path), f"File missing: {path}"
    file_size = os.path.getsize(path)
    
    out = subprocess.run(['sips', '-g', 'pixelWidth', '-g', 'pixelHeight', '-g', 'hasAlpha', path], capture_output=True, text=True).stdout
    assert f"pixelWidth: {expected_w}" in out, f"Width mismatch: {out}"
    assert f"pixelHeight: {expected_h}" in out, f"Height mismatch: {out}"
    assert "hasAlpha: no" in out, "JPEG has unexpected alpha"
    assert file_size <= max_bytes, f"File size {file_size} exceeds {max_bytes} (1 MB)"
    
    print(f" PASS: {os.path.basename(path)} -> {expected_w}x{expected_h} px, JPEG (no alpha), {file_size:,} bytes ({file_size/1024:.1f} KB) <= 1 MB")

def test_promotional_text_compliance():
    promo_texts = {
        "Default English": "Android Artist crafting high-performance native apps, on-device AI runtimes & adaptive experiences across Mobile, Foldables and Android TV.",
        "Option B": "Android Artist: 15 years of craft architecting fluid Kotlin Multiplatform apps, on-device AI runtimes & adaptive UI across Mobile and TV.",
        "Option C": "Android Artist crafting fluid native apps, on-device AI runtimes, and adaptive experiences across Mobile, Foldables & Android TV.",
        "Option D": "Lead Android Engineer & Android Artist. Crafting high-performance native apps, on-device AI & arcade experiences across Mobile and TV.",
        "Spanish": "Android Artist creando apps nativas de alto rendimiento, IA en dispositivo y diseño adaptativo para Móviles, Plegables y Android TV.",
        "French": "Android Artist créant des apps natives fluides, de l'IA sur l'appareil et des interfaces adaptatives pour Mobiles, Pliables & TV.",
        "German": "Android Artist: Hochwertige native Apps, On-Device-KI und adaptive UIs für Smartphones, Foldables und Android TV aus einer Hand.",
        "Japanese": "Android Artist：スマホ、折りたたみ端末、Android TV向けに高性能ネイティブアプリやオンデバイスAI体験を開発。",
        "Hindi": "Android Artist: मोबाइल, फोल्डेबल्स और Android TV के लिए हाई-परफॉरमेंस ऐप्स और ऑन-डिवाइस AI अनुभव तैयार करते हुए。"
    }
    
    for label, text in promo_texts.items():
        length = len(text)
        assert length <= 140, f"Promo text '{label}' length {length} > 140!"
        print(f" PASS: Promo copy '{label}': {length}/140 chars")

def test_svg_policy_compliance():
    with open('assets/play-console/header-image-4096x2304.svg', 'r') as f:
        header_svg = f.read()
    
    # Assert no forbidden phrases or competitor branding in Google Play header banner
    assert "★ LIVE ON PLAY" not in header_svg, "Found forbidden '★ LIVE ON PLAY' badge"
    assert "LIVE ON PLAY" not in header_svg, "Found forbidden 'LIVE ON PLAY' badge"
    assert ">iOS<" not in header_svg, "Found competitor 'iOS' badge"
    assert "Android, iOS" not in header_svg, "Found competitor 'iOS' mention in description"
    print(" PASS: header-image-4096x2304.svg free of competitor references & policy-restricted badges")

def main():
    root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    assets_dir = os.path.join(root, 'assets', 'play-console')
    
    print("\n--- Running Google Play Console Asset Compliance Tests ---\n")
    test_png_compliance(os.path.join(assets_dir, 'developer-icon-512x512.png'), 512, 512)
    test_jpeg_compliance(os.path.join(assets_dir, 'developer-icon-512x512.jpg'), 512, 512)
    test_png_compliance(os.path.join(assets_dir, 'header-image-4096x2304.png'), 4096, 2304)
    test_jpeg_compliance(os.path.join(assets_dir, 'header-image-4096x2304.jpg'), 4096, 2304)
    
    print("\n--- Running Promotional Copy Length Tests ---\n")
    test_promotional_text_compliance()
    
    print("\n--- Running Policy Compliance Tests ---\n")
    test_svg_policy_compliance()
    
    print("\n ALL VERIFICATION TESTS PASSED SUCCESSFULLY! \n")

if __name__ == '__main__':
    main()
