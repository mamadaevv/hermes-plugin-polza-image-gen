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

## Установка

### Быстрая (через hermes plugins install)

```bash
# 1. Установить плагин одной командой
hermes plugins install mamadaevv/hermes-plugin-polza-image-gen --enable

# 2. Добавить API ключ в .env
echo "POLZA_API_KEY=*** >> ~/.hermes/.env

# 3. Готово! Следующая генерация пойдёт через Polza AI
```

### Ручная

```bash
# 1. Создать директорию
mkdir -p ~/.hermes/plugins/image_gen/polza/

# 2. Скачать файлы
curl -Lo ~/.hermes/plugins/image_gen/polza/__init__.py \
  https://raw.githubusercontent.com/mamadaevv/hermes-plugin-polza-image-gen/main/__init__.py
curl -Lo ~/.hermes/plugins/image_gen/polza/plugin.yaml \
  https://raw.githubusercontent.com/mamadaevv/hermes-plugin-polza-image-gen/main/plugin.yaml

# 3. Добавить API ключ
echo "POLZA_API_KEY=*** >> ~/.hermes/.env

# 4. Включить в конфиге
cat >> ~/.hermes/config.yaml << 'EOF'
plugins:
  enabled:
    - image_gen/polza
EOF
```

## Использование

После установки просто попроси сгенерировать изображение. По умолчанию используется **Seedream 4.5**.

### Выбор модели в разговоре

Можешь прямо в запросе указать какую модель использовать — агент сам переключится:

> «сгенерируй горный пейзаж в Nano Banana 2»
> «сделай фотореалистичного кота на FLUX 2 Pro»

Или попросить сменить дефолтную модель на время:

> «поставь Z-Image default, пока не отменю»

Модель переключается без рестарта. Приоритет выбора:

```
1. POLZA_IMAGE_MODEL (env var)     — временная смена через терминал
2. Модель в запросе                — ты сказал какую, я сделал
3. image_gen.polza.model (config)  — выбор через hermes tools
4. Seedream 4.5                    — встроенный дефолт
```

### Выбор модели через hermes tools

```bash
# Открыть меню выбора модели
hermes tools
# → Image Generation → Polza AI → выбрать модель

# Или напрямую в конфиг
hermes config set image_gen.polza.model tongyi-mai/z-image
```

### Список всех моделей

| Категория | Модели |
|-----------|--------|
| **🖼️ Text-to-Image** | Z-Image (1.40 ₽), Seedream 3.0 (2.50 ₽), Yandex Art (2.91 ₽) |
| **🎨 Text-to-Image + референсы** | FLUX 2 Pro (5 ₽), Seedream 4.5 (5 ₽), GPT Image 1.5 (3 ₽), Qwen Image 2 (4 ₽), Grok Imagine (2.50 ₽) |
| **🎛️ Image-to-Image** | Qwen Image (2.25–3 ₽) — strength + guidance |
| **🖌️ Inpainting** | GPT-5 Image (4.50 ₽) — маски, enhance |
| **🌐 Multimodal** | GPT-5.4 Image 2 (4 ₽), Nano Banana (2.90 ₽), Nano Banana 2 (4.80 ₽), Nano Banana Pro (13.50 ₽) |

## Категории моделей (полный список)

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

## Получение API ключа

1. Зарегистрироваться: **https://polza.ai/?referral=2tzD86OTsh**
2. Перейти в настройки → API ключи

## Лицензия

MIT
