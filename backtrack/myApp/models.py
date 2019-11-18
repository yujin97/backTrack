from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser, BaseUserManager
)
from django.db.models import Q

# Create your models here.
class Project(models.Model):
    title = models.CharField(max_length=200)
    sprint = models.DecimalField(max_digits=5, default = 1, blank = True, decimal_places = 0)
    sprintEffort = models.DecimalField(max_digits=5, decimal_places=1, default = 0, blank = True)
    started = models.BooleanField(blank = True, default = False)

    def __str__(self):
        return self.title

class UserManager(BaseUserManager):
    def create_user(self, username, email, password=None, is_acitve = True, is_staff=False, is_admin=False):
        if not username:
            raise ValueError("User must have an username!")
        if not email:
            raise ValueError("User must have an email address!")
        if not password:
            raise ValueError("User must have a password!")
        user_obj = self.model(
                email = self.normalize_email(email)
            )
        user_obj.username=username
        user_obj.staff = is_staff
        user_obj.admin = is_admin
        user_obj.active = is_acitve
        user_obj.set_password(password)
        user_obj.save(using=self._db)
        return user_obj

    def create_staffuser(self, username, email, password=None):
        user = self.create_user(
            username,
            email,
            password = password,
            is_staff = True
        )
        return user

    def create_superuser(self, username, email, password=None):
        user = self.create_user(
            username,
            email,
            password = password,
            is_staff = True,
            is_admin = True
        )
        return user

class User(AbstractBaseUser):
    username = models.CharField(max_length=255, default = 'newUser', unique = True)
    email = models.EmailField(max_length=255, unique = True, default = 'abc@gmail.com')
    active = models.BooleanField(default=False)
    staff = models.BooleanField(default=False)
    admin = models.BooleanField(default=False)
    developer = models.BooleanField(default=False)
    manager = models.BooleanField(default=False)
    scrumMaster = models.BooleanField(default=False)
    productOwner = models.BooleanField(default=False)
    devTeam = models.BooleanField(default=False)
    project = models.ManyToManyField(Project, blank=True)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']
    objects = UserManager()

    def __str__(self):
        return self.username

    def get_full_name(self):
        return self.username

    def get_short_name(self):
        return self.username

    def has_perm(self, perm, obj=None):
     return True

    def has_module_perms(self, app_label):
        return True

    def get_username(self):
        return self.username

    def get_email(self):
        return self.email

    @property
    def is_staff(self):
        return self.staff

    @property
    def is_active(self):
        return self.active

    def is_admin(self):
        return self.admin

    @property
    def is_developer(self):
        return self.developer

    @property
    def is_manager(self):
        return self.manager

    @property
    def is_scrumMaster(self):
        return self.scrumMaster

    @property
    def is_productOwner(self):
        return self.productOwner

    @property
    def is_devTeam(self):
        return self.devTeam

# class Developer(models.Model):
#     name = models.CharField(max_length=200)

#     def __str__(self):
#         return self.name

# class Participation(models.Model):
#     ROLES = (
#         (1, 'Product Owner'),
#         (2, 'Developer Team'),
#     )
#     project = models.ForeignKey(Project, on_delete=models.CASCADE)
#     developer = models.OneToOneField(Developer, on_delete=models.CASCADE)
#     role = models.PositiveSmallIntegerField(
#         choices=ROLES,
#         default=2,
#     )


def get_default_project():
    if PBI.objects.order_by('-priority').first():
        return Project.objects.all().first().pk
    else:
        return None

def get_max_priority():
    if PBI.objects.filter(priority=1):
        return PBI.objects.order_by('-priority').first().priority + 1 
    else:
        return 1

class PBI(models.Model):
    STATUS = (
        (1, 'Not Yet Started'),
        (2, 'In Progress'),
        (3, 'Done'),
        (4, 'Not Completed')
    )
    name = models.CharField(max_length=200, blank=True)
    estimate = models.DecimalField(max_digits=5, decimal_places=1)
    Description = models.CharField(max_length=400)
    status = models.PositiveSmallIntegerField(
        choices=STATUS,
        default=1,
    )
    priority = models.IntegerField(default = None, null=True, blank=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    sprintNo = models.DecimalField(max_digits=5, decimal_places=0, null=True, blank = True, default = None)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if self.pk == None:
            if PBI.objects.filter(Q(priority=1) & Q(project = self.project)):
                self.priority = PBI.objects.order_by('-priority').filter(project = self.project).first().priority+1
                super(PBI, self).save(*args, **kwargs)
            else:
                self.priority = 1
                super(PBI, self).save(*args, **kwargs)
        else:
            super(PBI, self).save(*args, **kwargs)


class PickedPBI(models.Model):
    pbi = models.OneToOneField(PBI, on_delete=models.CASCADE)
    taskNum = models.DecimalField(max_digits=5, decimal_places=0, default = 0, blank = True)
    notYetStarted = models.DecimalField(max_digits=5, decimal_places=0, default = 0, blank = True)
    inProgress = models.DecimalField(max_digits=5, decimal_places=0, default = 0, blank = True)
    done = models.DecimalField(max_digits=5, decimal_places=0, default = 0, blank = True)
    def __str__(self):
        return self.pbi.name

class Task(models.Model):
    STATUS = (
        (1, 'Not Yet Started'),
        (2, 'In Progress'),
        (3, 'Done'),
    )
    name = models.CharField(max_length=200, blank=True)
    estimate = models.DecimalField(max_digits=5, decimal_places=1)
    complete = models.DecimalField(max_digits=5, decimal_places=1, default = 0)
    Description = models.CharField(max_length=400)
    status = models.PositiveSmallIntegerField(
        choices=STATUS,
        default=1,
    )
    pbiPicked = models.ForeignKey(PickedPBI, on_delete=models.CASCADE)
    pic = models.ForeignKey(User, null=True, blank=True, default = None, on_delete=models.SET_NULL)
    def __str__(self):
        return self.name

# class done(models.Model):

#     name = models.CharField(max_length=200, blank=True)
#     estimate = models.DecimalField(max_digits=5, decimal_places=1)
#     Description = models.CharField(max_length=400)
#     sprint_id = models.IntegerField(default = 1)
#     project_linkage = models.ForeignKey(Product_Backlog, on_delete=models.CASCADE, default = get_default_project)
#     sprint_linkage = models.ForeignKey(Sprints, on_delete=models.CASCADE)

#     def __str__(self):
#         return self.name


# class Users(models.Model):
#     ROLES = (
#         (1, 'Product Owner'),
#         (2, 'Scrum Master'),
#         (3, 'Developer'),
#     )
#     name = models.CharField(max_length=200)
#     role = models.PositiveSmallIntegerField(
#         choices=ROLES,
#         default=3,
#     )
#     project_id = models.IntegerField(blank=True, null=True)
#     proj = models.OneToOneField(Project, on_delete=models.CASCADE)

#     def __str__(self):
#         return self.name
