import os

# Garante que cada imagem tenha um label correspondente
image_files = []
for f in os.listdir("dataset\\images"):
    if f.endswith(('.jpg', '.png')):
        label_path = os.path.join("dataset\\labels", os.path.splitext(f)[0] + '.txt')
        if os.path.exists(label_path):
            image_files.append(f"dataset\\images\\{f}")

# 80% treino, 20% validação
split_idx = int(0.8 * len(image_files))
with open("dataset\\train.txt", "w") as f:
    f.write("\n".join(image_files[:split_idx]))
with open("dataset\\val.txt", "w") as f:
    f.write("\n".join(image_files[split_idx:]))