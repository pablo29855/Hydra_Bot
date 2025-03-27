# 🎵 HYDRA - Bot de Música para Discord  

HYDRA es un bot de música para Discord que te permite reproducir tus canciones favoritas de YouTube con comandos sencillos.  

## 🚀 Características  
✅ Reproduce música desde YouTube.  
✅ Controla la reproducción con comandos de pausa, reanudación y stop.  
✅ Soporte para cola de reproducción.  
✅ Usa comandos slash (`/`) para una experiencia más intuitiva.  

## 📌 Comandos disponibles  
| Comando       | Descripción |
|--------------|------------|
| **/play** `<nombre o URL>` | Reproduce una canción en tu canal de voz. |
| **/pause** | Pausa la música actual. |
| **/resume** | Reanuda la reproducción. |
| **/stop** | Detiene la música y desconecta el bot. |
| **/skip** | Salta la canción actual. |
| **/queue_list** | Muestra la lista de reproducción. |

## 🛠️ Instalación  
1️⃣ Clona el repositorio:  
```bash
git clone https://github.com/pablo29855/Hydra_Bot.git
cd Hydra_Bot
```
2️⃣ Instala las dependencias:  
```bash
pip install -r requirements.txt
```
3️⃣ Crea un archivo `.env` y agrega tu token de bot de Discord:  
```
DISCORD_TOKEN=tu_token_aquí
GUILD_ID=tu_id_del_servidor
```
4️⃣ Ejecuta el bot:  
```bash
python Hydra.py
```

