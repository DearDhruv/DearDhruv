# Google Play Developer Profile Assets · `@DearDhruv`

This directory contains the production-ready branding assets and promotional copy for the **DearDhruv** Google Play Developer Profile, crafted in accordance with the official [Google Play Console specifications](https://support.google.com/googleplay/android-developer/answer/9866130).

---

## 🎨 Asset Files Summary

| Asset | Format | Resolution | Color Depth | File Size | Console Limit | Status |
|---|---|---|---|---|---|---|
| **Developer Icon** | `PNG` | `512 × 512 px` | 24-bit RGB (no alpha) | **167.4 KB** (171,417 B) | Up to 1 MB | **Ready for upload** |
| **Developer Icon** | `JPEG` | `512 × 512 px` | 24-bit RGB | **41.7 KB** (42,658 B) | Up to 1 MB | **Alternative upload** |
| **Header Image** | `PNG` | `4096 × 2304 px` | 24-bit RGB (no alpha) | **844.9 KB** (865,136 B) | Up to 1 MB | **Ready for upload** |
| **Header Image** | `JPEG` | `4096 × 2304 px` | 24-bit RGB | **665.5 KB** (681,489 B) | Up to 1 MB | **Alternative upload** |
| **Developer Icon Source** | `SVG` | Vector (`512 × 512`) | Vector definitions | **7.0 KB** | Source | Editable |
| **Header Image Source** | `SVG` | Vector (`4096 × 2304`) | Vector definitions | **20.9 KB** | Source | Editable |

All raster files are strictly non-transparent, 24-bit RGB (PNG `IHDR` color type `2` / 8 bits per channel), strictly below Google Play Console's 1 MB cap.

---

## 📝 Promotional Text (Max 140 Characters)

### Recommended English (Default)
> `Android Artist crafting high-performance native apps, on-device AI runtimes & adaptive experiences across Mobile, Foldables and Android TV.`
- **Character count:** **139 / 140 characters** (Strictly verified)

### Alternative Options
- **Option B (Focus on Craft & Architecture - 137 chars):**  
  `Android Artist: 15 years of craft architecting fluid Kotlin Multiplatform apps, on-device AI runtimes & adaptive UI across Mobile and TV.`
- **Option C (Punchy & Direct - 129 chars):**  
  `Android Artist crafting fluid native apps, on-device AI runtimes, and adaptive experiences across Mobile, Foldables & Android TV.`
- **Option D (Lead & Games - 134 chars):**  
  `Lead Android Engineer & Android Artist. Crafting high-performance native apps, on-device AI & arcade experiences across Mobile and TV.`

---

## 🌐 Localized Promotional Text (Optional Translations)

Google Play Console allows you to add translations for your promotional text to show localized content to users around the world:

### Spanish (`es-419` / `es-ES`)
> `Android Artist creando apps nativas de alto rendimiento, IA en dispositivo y diseño adaptativo para Móviles, Plegables y Android TV.`  
*(132 characters · <= 140)*

### French (`fr-FR`)
> `Android Artist créant des apps natives fluides, de l'IA sur l'appareil et des interfaces adaptatives pour Mobiles, Pliables & TV.`  
*(129 characters · <= 140)*

### German (`de-DE`)
> `Android Artist: Hochwertige native Apps, On-Device-KI und adaptive UIs für Smartphones, Foldables und Android TV aus einer Hand.`  
*(128 characters · <= 140)*

### Japanese (`ja-JP`)
> `Android Artist：スマホ、折りたたみ端末、Android TV向けに高性能ネイティブアプリやオンデバイスAI体験を開発。`  
*(66 characters · <= 140)*

### Hindi (`hi-IN`)
> `Android Artist: मोबाइल, फोल्डेबल्स और Android TV के लिए हाई-परफॉरमेंस ऐप्स और ऑन-डिवाइस AI अनुभव तैयार करते हुए।`  
*(112 characters · <= 140)*

---

## 📐 Design & Safe Zone Architecture

### 1. Developer Icon (`512 × 512 px`)
- **Visual Motif:** Modern geometric interlocking **"DD"** monogram with neon lighting in Kotlin Violet (`#7F52FF`) and Compose Cyan/Emerald (`#00E5FF` to `#00E676`), accented with dual glowing Android antenna nodes and a central spark diamond.
- **Circular Safe Zone:** Google Play displays developer icons inside a circular mask. All visual elements, squircle corners, and the `DEARDHRUV` status pill are centered and fit comfortably within the circular radius ($r \approx 216\text{ px}$), ensuring zero clipping.
- **Background:** Solid deep space slate (`#070B14`), 100% opaque without alpha channel.

### 2. Header Image (`4096 × 2304 px`, 16:9)
- **Visual Story:** Showcases the DearDhruv brand and the three live Google Play apps:
  1. **Veloci Hue:** KMP × Compose Multiplatform arcade game.
  2. **AI Playground:** On-device neural LLM & diffusion image synthesis.
  3. **Open Store:** Lightweight Android TV Leanback launcher.
- **Safe Zone Alignment:**
  - **Lower 25% Safe Zone:** The lower portion contains atmospheric space and subtle baseline guides, preventing overlap from the circular developer icon and name overlaid by the Play Console UI.
  - **Upper 12% Safe Zone:** Leaves breathing room for system status bars and navigation affordances on mobile devices.
  - **Central 70% Horizontal Zone:** Ensures the three showcase cards and hero typography remain fully centered and legible across narrow mobile screens, tablets, and wide 4K displays.

---

## 🚀 How to Upload to Google Play Console

1. Log into your [Google Play Console](https://play.google.com/console).
2. On the left navigation menu, expand **Developer page** (under *Account* or *Store presence*).
3. Under **Developer icon**:
   - Upload [developer-icon-512x512.png](file:///Users/deardhruv/Dhruv/work/dhruv/dhruv-git/DearDhruv/assets/play-console/developer-icon-512x512.png) (or `.jpg`).
4. Under **Header image**:
   - Upload [header-image-4096x2304.png](file:///Users/deardhruv/Dhruv/work/dhruv/dhruv-git/DearDhruv/assets/play-console/header-image-4096x2304.png) (or `.jpg`).
5. Under **Promotional text**:
   - Paste the recommended copy:
     ```text
     Android Artist crafting high-performance native apps, on-device AI runtimes & adaptive experiences across Mobile, Foldables and Android TV.
     ```
   - (Optional) Click **Manage translations** and add localized text.
6. Click **Save** in the bottom-right corner.
