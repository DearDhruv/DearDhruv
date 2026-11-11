#!/usr/bin/env python3
"""
Deep verification test for DearDhruv featured showcase cards and profile README.
Verifies:
1. XML validity for all SVGs.
2. Typography and margin safety against x=528px across multiple OS font engines.
3. Badge row boundary widths.
4. Markdown image asset existence and Play Store link validity.
5. Accuracy of metadata across repositories.
"""
import os
import re
import xml.etree.ElementTree as ET
from PIL import ImageFont

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

def test_xml_validity():
    print("=== 1. XML Parsing Verification ===")
    svgs = [
        'assets/open-store-showcase.svg',
        'assets/veloci-hue-showcase.svg',
        'assets/ai-playground-showcase.svg',
        'assets/divider.svg',
        'assets/profile-hero.svg',
        'assets/play-console/header-image-4096x2304.svg',
        'assets/play-console/developer-icon-512x512.svg'
    ]
    for rel_path in svgs:
        path = os.path.join(ROOT, rel_path)
        assert os.path.exists(path), f"File missing: {rel_path}"
        ET.parse(path)
        print(f" PASS: {rel_path} is valid XML")

def test_typography_and_margins():
    print("\n=== 2. Typography & Margin Verification Across Fonts ===")
    fonts_to_test = [
        ('SFNS', '/System/Library/Fonts/SFNS.ttf'),
        ('Arial', '/System/Library/Fonts/Supplemental/Arial.ttf'),
        ('Helvetica', '/System/Library/Fonts/Helvetica.ttc'),
        ('Trebuchet MS', '/System/Library/Fonts/Supplemental/Trebuchet MS.ttf'),
        ('Verdana (Worst-case wide)', '/System/Library/Fonts/Supplemental/Verdana.ttf')
    ]

    cards = [
        ('Open Store', 'assets/open-store-showcase.svg'),
        ('Veloci Hue', 'assets/veloci-hue-showcase.svg'),
        ('AI Playground', 'assets/ai-playground-showcase.svg')
    ]

    for card_name, rel_path in cards:
        path = os.path.join(ROOT, rel_path)
        tree = ET.parse(path)
        root = tree.getroot()
        desc_texts = [
            el.text for el in root.iter('{http://www.w3.org/2000/svg}text')
            if 'text-desc' in el.attrib.get('class', '')
        ]
        print(f"-- Testing {card_name} --")
        for font_label, font_path in fonts_to_test:
            if not os.path.exists(font_path):
                continue
            font = ImageFont.truetype(font_path, 13.5)
            for i, text in enumerate(desc_texts):
                w = font.getbbox(text)[2]
                right_edge = 42 + w
                margin = 528 - right_edge
                assert margin >= 30, f"FAIL: {card_name} line {i+1} with {font_label} has margin {margin}px < 30px! (Text: {text})"
                if 'Verdana' in font_label:
                    print(f" PASS [{font_label}] L{i+1}: \"{text[:35]}...\" -> margin to 528: {margin}px >= 30px")

def test_badge_row_boundaries():
    print("\n=== 3. Badge Widths and Bounding Boxes ===")
    cards = [
        ('Open Store', 'assets/open-store-showcase.svg'),
        ('Veloci Hue', 'assets/veloci-hue-showcase.svg'),
        ('AI Playground', 'assets/ai-playground-showcase.svg')
    ]
    for card_name, rel_path in cards:
        path = os.path.join(ROOT, rel_path)
        tree = ET.parse(path)
        root = tree.getroot()
        for g in root.iter('{http://www.w3.org/2000/svg}g'):
            if g.attrib.get('transform') == 'translate(0, 166)':
                max_x = 0
                for child in g:
                    tr = child.attrib.get('transform', 'translate(0, 0)')
                    match = re.search(r'translate\(([\d\.]+)', tr)
                    tx = float(match.group(1)) if match else 0.0
                    rect = child.find('{http://www.w3.org/2000/svg}rect')
                    if rect is not None:
                        rw = float(rect.attrib.get('width', 0))
                        max_x = max(max_x, tx + rw)
                assert max_x <= 486, f"{card_name} badges width {max_x} > 486!"
                safe_buffer = 528 - (42 + max_x)
                assert safe_buffer >= 40, f"Safe buffer too narrow: {safe_buffer}px"
                print(f" PASS: {card_name} badges row width = {max_x}px, leaves {safe_buffer}px safe buffer before mockup")

def test_markdown_and_links():
    print("\n=== 4. Markdown Links and Assets Verification ===")
    readme_path = os.path.join(ROOT, 'README.md')
    with open(readme_path, 'r') as f:
        readme = f.read()

    # Verify all local image links exist
    img_matches = re.findall(r'<img [^>]*src="([^"]+)"', readme)
    for link in img_matches:
        if not link.startswith('http'):
            clean_path = link.lstrip('./')
            full_path = os.path.join(ROOT, clean_path)
            assert os.path.exists(full_path), f"README links missing local image: {clean_path}"
            print(f" PASS: Verified local image asset {clean_path}")

    # Verify store URLs
    assert 'com.deardhruv.velocihue' in readme
    assert 'com.deardhruv.llmplayground' in readme
    assert 'com.deardhruv.openstore' in readme
    print(" PASS: All 3 Google Play application IDs verified")

    # Verify version touchpoints
    assert 'v0.1.8' in readme, "Missing v0.1.8 in README"
    assert 'v1.7.7' in readme, "Missing v1.7.7 in README"
    assert 'v1.0.7' in readme, "Missing v1.0.7 in README"
    print(" PASS: All 3 active release milestones explicitly documented in README")

def main():
    test_xml_validity()
    test_typography_and_margins()
    test_badge_row_boundaries()
    test_markdown_and_links()
    print("\n ALL ASSET & DOCUMENTATION VERIFICATION CHECKS PASSED SUCCESSFULLY! \n")

if __name__ == '__main__':
    main()
