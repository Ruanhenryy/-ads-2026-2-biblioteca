turma = {
    "Ana": [8.0, 9.5],
    "Bruno": [6.0, 5.5],
    "Carla": [4.0, 3.5]
}

medias = []

for nome, notas in turma.items():
    media = sum(notas) / len(notas)
    
    if media >= 7:
        situacao = "Aprovado"
    elif media >= 5:
        situacao = "Recuperação"
    else:
        situacao = "Reprovado"
    
    medias.append(media)
    
    print(f"{nome:<10} Média: {media:.1f}  Situação: {situacao}")

media_turma = sum(medias) / len(medias)

print(f"\nMédia da turma: {media_turma:.2f}")

print("\nRanking:")
ranking = sorted(turma.items(), key=lambda aluno: sum(aluno[1]) / len(aluno[1]), reverse=True)

for nome, notas in ranking:
    media = sum(notas) / len(notas)
    print(f"{nome:<10} {media:.1f}")