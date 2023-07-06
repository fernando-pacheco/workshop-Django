from django.db import models


class Categoria(models.Model):
    categoria = models.CharField(max_length=50)
    essencial = models.BooleanField(default=False)
    valor_planejamento = models.FloatField(default=0)

    def __str__(self):
        return self.categoria
    

class Conta(models.Model):
    bank_choices = (
        ('NU', 'Nubank'),
        ('CE', 'Caixa Econômica'),
        ('ITU', 'Itaú Unibanco'),
        ('C6', 'C6 Bank'),
        ('INT', 'Banco Inter'),
        ('BR', 'Bradesco'),
        ('BB', 'Bando do Brasil'),
    )

    tipo_choices = (    
        ('PJ', 'Pessoa Jurídica'),
        ('PF', 'Pessoa Física'),
    )

    apelido = models.CharField(max_length=50)
    bank = models.CharField(max_length=3,choices=bank_choices)
    tipo = models.CharField(max_length=2, choices=tipo_choices)
    valor = models.FloatField()
    icon = models.ImageField(upload_to='icones')

    def __str__(self):
        return self.apelido
    
