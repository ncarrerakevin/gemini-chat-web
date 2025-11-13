# 🚀 Deployment en Vercel

## Pasos para hacer deploy

### 1. Preparar el repositorio

Asegúrate de que tu proyecto esté en un repositorio Git (GitHub, GitLab, o Bitbucket).

```bash
# Si no has inicializado git
git init
git add .
git commit -m "Preparar para deployment en Vercel"

# Crear repositorio en GitHub y subir
git remote add origin <URL_DE_TU_REPO>
git push -u origin main
```

### 2. Instalar Vercel CLI (opcional)

```bash
npm install -g vercel
```

### 3. Deploy desde CLI

```bash
# Login en Vercel
vercel login

# Deploy
vercel
```

### 4. Deploy desde Dashboard de Vercel

1. Ve a [vercel.com](https://vercel.com)
2. Haz clic en "Import Project"
3. Conecta tu repositorio de GitHub/GitLab/Bitbucket
4. Selecciona tu repositorio
5. Vercel detectará automáticamente la configuración

### 5. Configurar Variables de Entorno

**MUY IMPORTANTE**: Debes configurar la API key en Vercel:

1. Ve a tu proyecto en Vercel Dashboard
2. Settings → Environment Variables
3. Agrega las siguientes variables:

```
GEMINI_API_KEY=AIzaSyC3dZUBCne6YPLpwv775RTchJ9bdvgdmIM
GEMINI_FLASH_MODEL=gemini-2.5-flash
```

### 6. Redeploy

Si ya desplegaste pero olvidaste las variables de entorno:

```bash
vercel --prod
```

O desde el dashboard: Deployments → Redeploy

## 📁 Estructura del Proyecto

```
.
├── api/
│   └── index.py          # Endpoint serverless
├── templates/
│   └── chat.html         # Interfaz web
├── vercel.json           # Configuración de Vercel
├── requirements.txt      # Dependencias Python
└── .vercelignore        # Archivos a ignorar
```

## ⚠️ Limitaciones de Vercel

- **Sesiones en memoria**: Las sesiones de chat se almacenan en memoria y se pierden entre requests. Para producción considera usar Redis o una base de datos.
- **Timeout**: Las funciones serverless tienen un límite de tiempo de ejecución (10s en plan gratuito).
- **Cold starts**: La primera request puede ser lenta debido a cold starts.

## 🔧 Troubleshooting

### Error: "API key no configurada"
- Verifica que agregaste `GEMINI_API_KEY` en las variables de entorno de Vercel

### Error 404
- Verifica que `vercel.json` esté en la raíz del proyecto
- Asegúrate de que la carpeta `api/` exista

### Streaming no funciona
- Vercel tiene limitaciones con Server-Sent Events (SSE)
- Considera usar polling o WebSockets como alternativa

## 🌐 URL de tu aplicación

Después del deployment, Vercel te dará una URL como:
```
https://tu-proyecto.vercel.app
```

## 🔒 Seguridad

- **NUNCA** commitees el archivo `.env` al repositorio
- Usa variables de entorno de Vercel para secretos
- Considera agregar autenticación si la app es pública
