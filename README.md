# Hermes Agent — Polza AI Image Generation Plugin

Плагин для генерации изображений через [Polza AI](https://polza.ai/?referral=2tzD86OTsh) в Hermes Agent. Поддерживает **17 моделей** различных категорий.

> 🔗 **Зарегистрироваться в Polza AI:** https://polza.ai/?referral=2tzD86OTsh

## Примеры генерации

> Все примеры — реальные генерации из плагина. [Все 23 изображения →](./examples/)

| Модель | Цена | Пример |
|--------|------|--------|
| **Seedream 4.5** ✅ | 5 ₽ | <img src="./examples/seedream-4-5_gen_2173421577241366529.jpg" width="160"> |
| **FLUX 2 Pro** | 5 ₽ | <img src="./examples/flux-2-pro_gen_2173421025269387265.jpg" width="160"> |
| **GPT Image 1.5** | 3 ₽ | <img src="./examples/gpt-image-1-5_gen_2173421160654049281.jpg" width="160"> |
| **GPT-5.4 Image 2** | 4 ₽ | <img src="./examples/gpt-5-4-image-2_gen_2173431095651602433.jpg" width="160"> |
| **Nano Banana 2** | 4.80 ₽ | <img src="./examples/gemini-3-1-flash-image-preview_gen_2173431019725393921.jpg" width="160"> |
| **Z-Image** 💸 | 1.40 ₽ | <img src="./examples/z-image_gen_2173430767643529217.jpg" width="160"> |
| **Grok Imagine** | 2.50 ₽ | <img src="./examples/grok-imagine-image_gen_2173430933789216769.jpg" width="160"> |
| **Seedream 5 Lite** | 4 ₽ | <img src="./examples/seedream-5-lite_gen_2173431273658519553.jpg" width="160"> |

## Категории моделей

### 🖼️ Text-to-Image (чистая генерация с нуля)
| Модель | Цена (₽) | Особенности |
|--------|----------|-------------|
| **Seedream 3.0** | 2.50 ₽ | Seed, Guidance scale, 5 ratios |
| **Yandex Art** | 2.91 ₽ | Seed, художественные стили, 7 ratios |
| **Z-Image (Tongyi)** | **1.40 ₽** 💸 | Самая дешёвая, 5 ratios |

### 🎨 Text-to-Image + Image Reference
| Модель | Цена (₽) | Особенности |
|--------|----------|-------------|
| **FLUX 2 Pro** | 5 / 7 ₽ (2K) | Фотореализм, до 8 реф. |
| **FLUX 2 Flex** | 14 / 24 ₽ (2K) | Быстрый, но дорогой |
| **Seedream 4.5** ✅ *default* | 5 ₽ | Quality (2K/4K), 8 ratios, до 14 реф. |
| **Seedream 4** | 3 ₽ | Seed, 1K/2K/4K, до 10 реф. |
| **Seedream 5 Lite** | 4 ₽ | Quality (2K/3K), до 10 реф. |
| **GPT Image 1.5** | 3 / 16.50 ₽ (high) | Quality tiers, до 16 реф. |
| **Qwen Image 2** | 4 ₽ | LLM-based, до 3 реф. |
| **Grok Imagine** | 2.50 ₽ | Быстрый, 3 ratios |

### 🎛️ Image-to-Image (с контролем влияния)
| Модель | Цена (₽) | Особенности |
|--------|----------|-------------|
| **Qwen Image** | 2.25–3 ₽ | Strength + Guidance scale |

### 🖌️ Multimodal + Inpainting
| Модель | Цена (₽) | Особенности |
|--------|----------|-------------|
| **GPT-5 Image** | 4.50 ₽ | Mask/inpaint, Enhance, до 5 реф. |

### 🌐 Multimodal text+image (вход и выход)
| Модель | Цена (₽) | Особенности |
|--------|----------|-------------|
| **GPT-5.4 Image 2** | 4 / 7 / 11 ₽ (4K) | 1K/2K/4K, до 16 реф. |
| **Nano Banana (Gemini 2.5 Flash)** | 2.90 ₽ | 10 ratios, быстрый |
| **Nano Banana 2 (Gemini 3.1 Flash)** | 4.80 / 7.20 / 10.80 ₽ (4K) | 11 ratios, типографика |
| **Nano Banana Pro (Gemini 3 Pro)** | 13.50 / 18 ₽ (4K) 🏆 | Топ-качество |

## Установка

```bash
# 1. Скопировать плагин
mkdir -p ~/.hermes/plugins/image_gen/polza/
# (положить сюда __init__.py и plugin.yaml)

# 2. Добавить API ключ в ~/.hermes/.env
echo "POLZA_API_KEY=*** >> ~/.hermes/.env

# 3. Включить плагин в ~/.hermes/config.yaml
cat >> ~/.hermes/config.yaml << 'EOF'
plugins:
  enabled:
    - image_gen/polza
EOF

# 4. Перезапустить Hermes
# В CLI: exit и заново
# В gateway: /restart

# 5. Выбрать модель через hermes tools
hermes tools
```

## Получение API ключа

1. Зарегистрироваться: **https://polza.ai/?referral=2tzD86OTsh**
2. Перейти в настройки → API ключи

## Лицензия

MIT
