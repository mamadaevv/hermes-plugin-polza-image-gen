# Hermes Agent — Polza AI Image Generation Plugin

Плагин для генерации изображений через [Polza AI](https://polza.ai/?referral=2tzD86OTsh) в Hermes Agent. Поддерживает **17 моделей** различных категорий.

> 🔗 **Зарегистрироваться в Polza AI:** https://polza.ai/?referral=2tzD86OTsh

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
