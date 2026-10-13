from django.db import models
from django.contrib.auth.models import AbstractUser
from dietlense_app.utility_funcs import calculate_bmr

# Create your models here.


class CustomUser(AbstractUser):
    phone=models.CharField(max_length=15,unique=True)


class Userprofile(models.Model):
    age=models.IntegerField()
    height=models.PositiveIntegerField()
    weight=models.FloatField()
    GENDER_OPTIONS=(
        ('male','male'),
        ('female','female')
    )
    gender=models.CharField(max_length=20,choices=GENDER_OPTIONS,default="male")

    ACTIVITY_OPTIONS=(
        ("1.2","Sedentary (little/no excercise)"),
        ("1.375","Lightly Active (excercise 1-3 days/week)"),
        ("1.55","Moderately Active (excercise 3-5 days/week)"),
        ("1.725","Very Active (excercise 6-7 days/week)"),
        ("1.9","Extra Active (Very intense Activity)")
    )
    activity_level=models.CharField(max_length=200,choices=ACTIVITY_OPTIONS,default="1.2")
    bmr=models.FloatField(null=True)
    owner=models.OneToOneField(CustomUser,on_delete=models.CASCADE,related_name="profile")

    def save(self, *args,**kwargs):
        self.bmr=calculate_bmr(self.age,self.height,self.weight,self.gender,float(self.activity_level))
        return super().save(*args,**kwargs)


class FoodLog(models.Model):
        name=models.CharField(max_length=100)

        MEAL_TYPE_OPTIONS=(
            ('breakfast',"Breakfast"),
            ('lunch',"Lunch"),
            ('dinner',"Dinner"),
            ('snack',"Snack")
        )

        meal_type=models.CharField(max_length=100,choices=MEAL_TYPE_OPTIONS,null=True)

        calories=models.PositiveIntegerField(null=True)

        serving_size=models.CharField(max_length=100,null=True)

        notes=models.TextField(null=True)

        picture=models.ImageField(upload_to="foodlogs",null=True)

        owner=models.ForeignKey(CustomUser,on_delete=models.CASCADE,related_name="foodentries")

        created_at=models.DateTimeField(auto_now_add=True)


