from django.db import models

# Create your models here.

class NFe(models.Model):

    class Meta:
        db_table = 'notafiscaleletronica'

    codigo = models.AutoField(primary_key=True)
    numero = models.CharField(null=False, max_length=255, unique=True)
    descricao = models.CharField(null=False, max_length=255)
    data_captura = models.DateTimeField(auto_now_add=True)
    bool_example = models.BooleanField(default=True)


    def __str__(self):
        return f'{self.codigo}, {self.numero} {self.descricao}, {self.data_captura}, ' \
               f'{self.bool_example}'

    def __repr__(self):
        return f'{self.codigo}, {self.numero} {self.descricao}, {self.data_captura}, ' \
               f'{self.bool_example}'
    pass