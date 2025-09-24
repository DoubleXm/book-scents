# book-scents

项目分为三个部分，

- webfront：前端项目，基于 Vue3 + ElementPlus 实现
- backend: Flask 实现
- auto-test：自动测试，基于 pytest 实现

前端项目启动

```bash
cd webfront
pnpm install
pnpm run dev
```

后端项目启动（基于 docker）因为依赖数据库

```bash
cd backend
docker-compose up -d --build
```
