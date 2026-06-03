# Hermes Agent — Polza AI Image Generation Plugin

Плагин для генерации изображений через [Polza AI](https://polza.ai) в Hermes Agent.

## Модели

| Модель | Скорость | Особенности |
|--------|----------|-------------|
| `bytedance/seedream-4.5` ✅ *default* | ~10s | Высокое качество, широкий выбор соотношений сторон |
| `bytedance/seedream-4` | ~8s | Хорошее качество |
| `black-forest-labs/flux.2-pro` | ~6s | Студийный фотореализм |
| `black-forest-labs/flux.2-flex` | ~4s | Быстрый, гибкий |
| `openai/gpt-image-1.5` | ~15s | Сильное следование промпту |
| `qwen/image-2` | ~12s | LLM-based, сложные сцены |
| `yandex/yandex-art` | ~10s | Художественные стили |

## Установка

```bash
# 1. Скопировать плагин
mkdir -p ~/.hermes/plugins/image_gen/polza/
# (положить сюда __init__.py и plugin.yaml)

# 2. Добавить API ключ в ~/.hermes/.env
echo "POLZA_API_KEY=your_key_here" >> ~/.hermes/.env

# 3. Включить плагин в ~/.hermes/config.yaml
cat >> ~/.hermes/config.yaml << 'EOF'
plugins:
  enabled:
    - image_gen/polza
EOF

# 4. Перезапустить Hermes
# В CLI: exit и заново
# В gateway: /restart
```

## API ключ

Получить: https://polza.ai → API ключи

## Лицензия

MIT
