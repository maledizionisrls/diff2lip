from cog import BasePredictor, Input, Path
import subprocess
import os

class Predictor(BasePredictor):
    def setup(self):
        """Carica i modelli e prepara l'ambiente."""
        # Questo comando scarica i modelli pre-addestrati di Diff2Lip
        # Potrebbe essere necessario adattarlo in base a dove il repo li salva
        if not os.path.exists("checkpoints"):
            # Qui andrebbe il comando per scaricare i checkpoints, se necessario
            # Per ora, assumiamo che siano già nel repo o scaricati al build
            pass

    def predict(
        self,
        video: Path = Input(description="Video con il volto da sincronizzare"),
        audio: Path = Input(description="Audio da usare per la sincronizzazione"),
    ) -> Path:
        """Esegue la predizione di lip-sync."""

        # Definisce i percorsi per i file di output
        output_path = "/tmp/output.mp4"

        # Comando per eseguire lo script di inferenza originale di Diff2Lip
        # Assicurati che il percorso dello script sia corretto
        command = [
            "python", "generate.py",
            "--video_path", str(video),
            "--audio_path", str(audio),
            "--out_path", output_path,
            "--is_voxceleb2=False" # Importante per video generici
        ]

        # Esegue il comando
        try:
            subprocess.run(command, check=True, capture_output=True, text=True)
        except subprocess.CalledProcessError as e:
            # Se c'è un errore, lo mostra per il debug
            raise Exception(f"Errore durante l'inferenza: {e.stderr}")

        return Path(output_path)
