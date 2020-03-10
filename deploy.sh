#!/usr/bin/env bash
set -ex
docker tag kerman_jt kermanjt/kerman_jt:latest
docker push kermanjt/kerman_jt:latest
rsync -avz --delete static/ --include='cards/' --include='css/' --include='js/' --include='images/' \
    --include='iconfont/' --include="robots.txt" --include='dist/' --exclude='/*' \
    kerman@kermanjt.com:/home/kerman/kermanjt.com/static
rsync -avz nginx/ kerman@kermanjt.com:/home/kerman/kermanjt.com/nginx
rsync -avz ./docker-compose.yml kerman@kermanjt.com:/home/kerman/kermanjt.com/
ssh kerman@kermanjt.com bash -s << EOF
cd /home/kerman/kermanjt.com
docker pull kermanjt/kerman_jt:latest
docker-compose down
docker-compose up -d
EOF

