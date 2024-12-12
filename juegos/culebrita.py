import pygame
import random
from Recursos.recursos import actualizar_lista_procesos, procesos_activos  # Asegúrate de tener esta función importada

def iniciar_culebrita():
    # Inicializar pygame
    pygame.init()


    nombre_proceso = "Culebrita"
    procesos_activos.append(nombre_proceso)
    actualizar_lista_procesos()  # Actualizar la interfaz
    
    # Dimensiones de la ventana
    ANCHO, ALTO = 800, 600
    TAMANIO_CUADRO = 20

    # Colores
    NEGRO = (0, 0, 0)
    BLANCO = (255, 255, 255)
    VERDE = (0, 255, 0)
    ROJO = (255, 0, 0)

    # Configuración de la ventana
    ventana = pygame.display.set_mode((ANCHO, ALTO))
    pygame.display.set_caption("Culebrita")

    # Reloj para controlar la velocidad del juego
    reloj = pygame.time.Clock()

    # Función para dibujar la serpiente
    def dibujar_serpiente(ventana, serpiente):
        for segmento in serpiente:
            pygame.draw.rect(ventana, VERDE, pygame.Rect(segmento[0], segmento[1], TAMANIO_CUADRO, TAMANIO_CUADRO))

    # Función para generar una posición aleatoria para la comida
    def generar_comida():
        x = random.randint(0, (ANCHO // TAMANIO_CUADRO) - 1) * TAMANIO_CUADRO
        y = random.randint(0, (ALTO // TAMANIO_CUADRO) - 1) * TAMANIO_CUADRO
        return x, y

    # Pantalla de Game Over
    def mostrar_game_over(puntuacion):
        fuente = pygame.font.Font(None, 48)
        texto = fuente.render("Game Over", True, ROJO)
        texto_reiniciar = pygame.font.Font(None, 36).render("Presiona R para reiniciar o Q para salir", True, BLANCO)
        puntuacion_texto = fuente.render(f"Puntuación: {puntuacion}", True, BLANCO)

        ventana.fill(NEGRO)
        ventana.blit(texto, (ANCHO // 2 - texto.get_width() // 2, ALTO // 3))
        ventana.blit(puntuacion_texto, (ANCHO // 2 - puntuacion_texto.get_width() // 2, ALTO // 2))
        ventana.blit(texto_reiniciar, (ANCHO // 2 - texto_reiniciar.get_width() // 2, ALTO // 1.5))
        pygame.display.flip()

        while True:
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    pygame.quit()
                if evento.type == pygame.KEYDOWN:
                    if evento.key == pygame.K_r:  # Reiniciar
                        return True
                    elif evento.key == pygame.K_q:  # Salir
                        pygame.quit()

    # Juego principal
    def main():
        # Inicializar variables del juego
        serpiente = [[100, 100]]  # Lista de segmentos de la serpiente
        direccion = "DERECHA"  # Dirección inicial
        comida = generar_comida()
        puntuacion = 0

        # Bucle principal del juego
        while True:
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    pygame.quit()

                # Cambiar la dirección de la serpiente
                if evento.type == pygame.KEYDOWN:
                    if evento.key == pygame.K_UP and direccion != "ABAJO":
                        direccion = "ARRIBA"
                    elif evento.key == pygame.K_DOWN and direccion != "ARRIBA":
                        direccion = "ABAJO"
                    elif evento.key == pygame.K_LEFT and direccion != "DERECHA":
                        direccion = "IZQUIERDA"
                    elif evento.key == pygame.K_RIGHT and direccion != "IZQUIERDA":
                        direccion = "DERECHA"

            # Mover la serpiente
            cabeza = serpiente[0][:]
            if direccion == "ARRIBA":
                cabeza[1] -= TAMANIO_CUADRO
            elif direccion == "ABAJO":
                cabeza[1] += TAMANIO_CUADRO
            elif direccion == "IZQUIERDA":
                cabeza[0] -= TAMANIO_CUADRO
            elif direccion == "DERECHA":
                cabeza[0] += TAMANIO_CUADRO

            # Agregar la nueva posición de la cabeza
            serpiente.insert(0, cabeza)

            # Verificar si la serpiente come la comida
            if cabeza == list(comida):
                comida = generar_comida()
                puntuacion += 1
            else:
                serpiente.pop()  # Eliminar el último segmento para mantener el tamaño

            # Verificar colisiones con las paredes
            if (cabeza[0] < 0 or cabeza[0] >= ANCHO or cabeza[1] < 0 or cabeza[1] >= ALTO):
                if mostrar_game_over(puntuacion):
                    main()
                return

            # Verificar colisiones con sí misma
            if cabeza in serpiente[1:]:
                if mostrar_game_over(puntuacion):
                    main()
                return

            # Dibujar todo en la ventana
            ventana.fill(NEGRO)
            dibujar_serpiente(ventana, serpiente)
            pygame.draw.rect(ventana, ROJO, pygame.Rect(comida[0], comida[1], TAMANIO_CUADRO, TAMANIO_CUADRO))

            # Mostrar la puntuación
            fuente = pygame.font.Font(None, 36)
            texto = fuente.render(f"Puntuación: {puntuacion}", True, BLANCO)
            ventana.blit(texto, (10, 10))

            # Actualizar la pantalla
            pygame.display.flip()

            # Controlar la velocidad del juego
            reloj.tick(10 + puntuacion // 5)  # Incrementa la velocidad a medida que aumenta la puntuación

    main()  # Llamar al bucle principal del juego
