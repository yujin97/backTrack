from django.db import models


# Create your models here.
class Project(models.Model):
    title = models.CharField(max_length=200)
    # owner_id = models.IntegerField()

    def __str__(self):
        return self.title

class Developer(models.Model):
    name = models.CharField(max_length=200)

class Manager(models.Model):
    name = models.CharField(max_length=200)
    project = models.OneToOneField(Project, on_delete=models.CASCADE, null=True, blank=True)

class Participation(models.Model):
    ROLES = (
        (1, 'Product Owner'),
        (2, 'Developer Team'),
    )
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    developer = models.OneToOneField(Developer, on_delete=models.CASCADE)
    role = models.PositiveSmallIntegerField(
        choices=ROLES,
        default=2,
    )


def get_max_priority():
    if PBI.objects.order_by('-priority').first():
        return PBI.objects.order_by('-priority').first().priority + 1 
    else:
        return 1

def get_default_project():
    if PBI.objects.order_by('-priority').first():
        return Project.objects.all().first().pk
    else:
        return None


class PBI(models.Model):
    STATUS = (
        (1, 'Not Yet Started'),
        (2, 'In Progress'),
        (3, 'Done'),
    )
    name = models.CharField(max_length=200, blank=True)
    estimate = models.DecimalField(max_digits=5, decimal_places=1)
    Description = models.CharField(max_length=400)
    status = models.PositiveSmallIntegerField(
        choices=STATUS,
        default=1,
    )
    priority = models.IntegerField(unique=True, default = None, null=True, blank=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.name

class PickedPBI(models.Model):
    pbi = models.OneToOneField(PBI, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)

class Task(models.Model):
    STATUS = (
        (1, 'Not Yet Started'),
        (2, 'In Progress'),
        (3, 'Done'),
    )
    name = models.CharField(max_length=200, blank=True)
    estimate = models.DecimalField(max_digits=5, decimal_places=1)
    Description = models.CharField(max_length=400)
    status = models.PositiveSmallIntegerField(
        choices=STATUS,
        default=1,
    )
    pbiPicked = models.ForeignKey(PickedPBI, on_delete=models.CASCADE)

