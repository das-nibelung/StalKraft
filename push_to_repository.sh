#!/bin/bash

set -e

REGISTRY="127.0.0.1:5500"
IMAGES=(
  "nginx:1.24"
  "python:3.12"
  "node:20-alpine"
  "postgres:15"
  "alpine:latest"
)

# Проверка: доступен ли реестр
curl -s "http://$REGISTRY/v2/" > /dev/null || {
  echo "❌ Registry $REGISTRY недоступен. Убедись, что он запущен."
  exit 1
}

for image in "${IMAGES[@]}"; do
  echo "-----------------------------"
  echo "📦 Обработка: $image"
  name=$(echo "$image" | cut -d':' -f1)
  tag=$(echo "$image" | cut -d':' -f2)
  remote_tag="$REGISTRY/$name:$tag"

  # Проверка: есть ли такой образ в реестре
  repo_url="http://$REGISTRY/v2/$name/tags/list"
  exists=$(curl -s "$repo_url" | jq -r ".tags[]?" | grep -Fx "$tag" || true)

  if [ "$exists" == "$tag" ]; then
    echo "✅ Уже существует в registry: $remote_tag — пропускаем push"
    continue
  fi

  echo "📥 Скачиваем $image"
  docker pull "$image"

  echo "🔁 Тегируем как $remote_tag"
  docker tag "$image" "$remote_tag"

  echo "📤 Пушим $remote_tag"
  docker push "$remote_tag"

  echo "🧹 Удаляем временный тег"
  docker rmi "$remote_tag"
done

echo "✅ Готово. Все образы обработаны."

