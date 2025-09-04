import pandas as pd
from django.core.management.base import BaseCommand
from django.db import transaction
from api.models import Autor

# Define a classe do comando customizado, herdando de BaseCommand
class Command(BaseCommand):
	# Aqui definimos os argumentos que o comando vai aceitar
    def add_arguments(self, parser):
		# Argumento opcional --arquivo, com valor padrão "population/autores.csv"
        parser.add_argument("--arquivo", default="population/autores.csv")
	    # Flag --truncate (True se for passado, False se não for)
        parser.add_argument("--truncate", action="store_true")
        # Flag --update (True se for passado, False se não for)
        parser.add_argument("--update", action="store_true")
        
	# O decorator garante que todas as operações dentro de handle sejam atômicas
    # (se der erro, nada é gravado no banco)
    @transaction.atomic
    def handle(self, *a, **o):
		# Lê o arquivo CSV especificado no argumento --arquivo (ou usa o padrão)
        df = pd.read_csv(o["arquivo"], encoding="utf-8-sig")
        # Normaliza os nomes das colunas:- strip() remove espaços em excesso - lower() converte para minúsculas- lstrip("\ufeff") remove o caractere BOM invisível
        df.columns = [c.strip().lower().lstrip("\ufeff")for c in df.columns]

        # Se a flag --truncate foi passada, apaga todos os registros da tabela Autor
        if o["truncate"]: Autor.objects.all().delete()

        # Garante que as colunas estejam em formato texto e remove espaços extras no começo/fim das strings
        df['autor'] = df['autor'].astype(str).str.strip()

        df['s_autor'] = df['s_autor'].astype(str).str.strip()

        # Padroniza e converte os dados em data 
        df['nasc'] = pd.to_datetime(df['nasc'], errors="coerce", format="%Y-%m-%d").dt.date

        # Substitui as linhas em branco/vazias por "None"
        df['nacio'] = df.get('nacio', "").astype(str).str.strip().str.capitalize().replace({"": None})

        # Mantém apenas linhas onde 'autor' e 's_autor' não estão vazias
        df = df.query("autor != '' and s_autor != '' ")

        if o["update"]:
            criados = atualizados = 0
            for r in df.itertuples(index=False):
                _, created = Autor.objects.update_or_create(
                 autor = r.autor, s_autor = r.s_autor , nasc = r.nasc , 
                 defaults={'nacio' : r.nacio}  
                )

                criados += int(created)
                atualizados += int(not created)
            self.stdout.write(self.style.SUCCESS(f'Criados: {criados} | Atualizados {atualizados}'))
        else:
            objs = [Autor(
                autor = r.autor, s_autor = r.s_autor , nasc = r.nasc , nacio = r.nacio
            ) for r in df.itertuples(index=False)
            ]

        Autor.objects.bulk_create(objs, ignore_conflicts=True)

        self.stdout.write(self.style.SUCCESS(f'Criados: {len(objs)}'))