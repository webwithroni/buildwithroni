#!/bin/bash
MSG="${1:-update}"
git add .
git commit -m "$MSG"
git push origin main
echo "✅ Pushed to GitHub: $MSG"
