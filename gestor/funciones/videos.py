import yt_dlp as youtube_dl
def descargar_video(url):
    calidad = input("Elige la calidad (e.g., 1080, 720, 480 o 'best' para la mejor): ")

    ydl_opts = {
        'format': f'bestvideo[height<={calidad}]+bestaudio/best',

    # Corregido el uso del operador de asignación '='
        'outtmpl': '%(title)s.%(ext)s',  # Corregida la cadena y el uso de .s
    }
    
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
