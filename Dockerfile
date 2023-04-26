FROM arm64v8/nginx:bullseye

COPY src/ /usr/share/nginx/html
