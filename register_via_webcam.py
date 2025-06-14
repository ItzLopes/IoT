import cv2
import requests

def capture_and_register(name: str, server_url: str = "http://localhost:5000/register"):
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Erro ao acessar a webcam.")
        return
    
    print("Pressione [ESPAÇO] para capturar a imagem.")

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Falha ao capturar imagem.")
            break

        cv2.imshow("Captura - Pressione [ESPAÇO] para capturar", frame)

        key = cv2.waitKey(1)
        if key == 32:
            _, img_encoded = cv2.imencode(".jpg", frame)
            response = requests.post(
                f"{server_url}?name={name}",
                data = img_encoded.tobytes()
            )
            print("Resposta do servidor:", response.json())
            break
        elif key == 27:
            print("Cancelado.")
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    nome = input("Digite o nome da pessoa: ")
    capture_and_register(nome)