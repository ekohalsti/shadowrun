from django.db import models

class Books(models.Model):
    VERSION_CHOICES = (
        ('SR1', 'First edition'),
        ('SR2', 'Second edition'),
        ('SR3', 'Third edition'),
        ('SR4', 'Fourth edition'),
        ('SR5', 'Fifth edition'),
    )
    version = models.CharField(max_length=3, choices=VERSION_CHOICES, default='SR5')
    name = models.CharField(max_length=254)
    code = models.CharField(max_length=10)


class BaseModel(models.Model):
    VERSION_CHOICES = (
        ('SR1', 'First edition'),
        ('SR2', 'Second edition'),
        ('SR3', 'Third edition'),
        ('SR4', 'Fourth edition'),
        ('SR5', 'Fifth edition'),
    )
    version = models.CharField(max_length=3, choices=VERSION_CHOICES, default='SR5')
    source = models.ForeignKey(Books)
    page = models.CharField(max_length=254)


class ComplexForm(BaseModel):
    TARGET_CHOICES = (
        ('D','Device'),
        ('P','Persona'),
        ('F','File'),
        ('S','Self'),
        ('R','Sprite'),
        ('H','Host'),
        ('I', 'IC')
    )
    name = models.CharField(max_length=254)
    target = models.CharField()

#All attributes in the SR universe
class Attribute(BaseModel):
    attribute = models.CharField(max_length=255)
    description = models.TextField()

    def __unicode__(self):
        return self.attribute + " " + self.version

class Category(models.Model):
    TYPE_CHOICES = (
        ('A', 'Active'),
        ('K', 'Knowledge')
    )
    name = models.CharField(max_length=254)
    type = models.CharField(max_length=2, choices=TYPE_CHOICES)

#All skills in the SR universe
class Skill(BaseModel):
    SKILLGROUP_CHOICES = (
        ('AC', 'Acting'),
        ('AT', 'Athletics'),
        ('BI', 'Biotech'),
        ('CC', 'Close Combat'),
        ('CO', 'Conjuring'),
        ('CR', 'Cracking'),
        ('EL', 'Electronics'),
        ('EN', 'Enchanting'),
        ('FI', 'Firearms'),
        ('IN', 'Influence'),
        ('EG', 'Engineering'),
        ('OU', 'Outdoors'),
        ('SO', 'Sorcery'),
        ('ST', 'Stealth'),
        ('TA', 'Tasking')
    )

    name = models.CharField(max_length=255)
    attribute = models.ForeignKey(Attribute)
    category = models.ForeignKey(Category)
    default = models.BooleanField(default=False)
    skillgroup = models.CharField(max_length=3, choices=SKILLGROUP_CHOICES)
    specs = models.ForeignKey(Skill_specialization)

    def __unicode__(self):
        return self.name + " " + self.version

#All specializations gain +2 to skill
class Skill_specialization(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()

    def __unicode__(self):
        return self.name + " " + self.version

#class Skillgroup(models.Model):
class Skill_cost(models.Model):
    rank = models.IntegerField()
    cost = models.IntegerField()

class License(models.Model):
    name = models.CharField(max_length=255)
    cost = models.IntegerField() #nuyen

class ID(models.Model):
    rank = models.IntegerField()
    cost = models.IntegerField()

#work in progress
class Lifestyle(models.Model):
    name = models.CharField(max_length=255)
    nuyen = models.IntegerField()
    licenses = models.ManyToManyField(License)
    ids = models.ManyToManyField(ID)


class QualityBonus(models.Model):
    category = models.CharField(max_length=254)
    amount = models.CharField(max_length=254)


#TODO
class QualityForbidden(models.Model):
    name = models.CharField(max_length=254)

#work in progress
class Quality(BaseModel):
    QUALITY_TYPES = (
        ('POSITIVE', 'Positive'),
        ('NEGATIVE', 'Negative'),
    )
    name = models.CharField(max_length=255)
    category = models.CharField(max_length=255, choices=QUALITY_TYPES) #either positive or negative
    karma = models.IntegerField() #karma cost
    limit = models.IntegerField(null=True)
    bonus = models.ManyToManyField(QualityBonus)
    forbidden = models.ManyToManyField(QualityForbidden)

    def __unicode__(self):
        return self.name + " " + self.version

#work in progress
class Contact(models.Model):
    name = models.TextField()
    connection = models.IntegerField()
    loyalty = models.IntegerField()
    quote = models.CharField(max_length=255)
    skill = models.ForeignKey(Skill)
    visible_globally = models.BooleanField(default=True)
    description = models.TextField()
    cost = models.IntegerField() #cost in karma

    def __unicode__(self):
        return self.name + " " + self.version

#work in progress
class Ranged_weapon(models.Model):
    MODE_CHOICES = (
        ('SS', 'single shot'),
        ('FA', 'full automatic'),
        ('BF', 'burst fire'),
        ('SA', 'semi-automatic'),
    )
    name = models.CharField(max_length=255)
    dam = models.CharField(max_length=255)
    accuracy = models.IntegerField()
    ap = models.IntegerField()
    mode = models.CharField(blank=True, max_length=255)
    recoil = models.IntegerField(blank=True, null=True)
    cost = models.DecimalField(max_digits=7, decimal_places=2) #cost in nuyen

    def __unicode__(self):
        return self.name

class Melee_weapon(models.Model):
    name = models.CharField(blank=True, max_length=100)
    reach = models.IntegerField(blank=True, null=True)
    damage = models.CharField(blank=True, max_length=100)
    accuracy = models.IntegerField(blank=True, null=True)
    ap = models.IntegerField(blank=True, null=True)
    cost = models.DecimalField(max_digits=7, decimal_places=2) #cost in nuyen

    def __unicode__(self):
        return self.name

class Ammunition_cost(models.Model):
    cost = models.DecimalField(max_digits=7, decimal_places=2) #cost in nuyen

#work in progress
class Ammunition(models.Model):
    name = models.CharField(blank=True, max_length=100)
    cost = models.IntegerField(blank=True, null=True)

    def __unicode__(self):
        return self.name

#work in progress
class Armor(BaseModel):
    CATEGORY_CHOICES = (
        ('AR', 'Armor'),
        ('CL', 'Clothes'),
        ('CO', 'Cloaks'),
        ('HF', 'High-Fashoin Armor Clothing'),
        ('SA', 'Specialty Armor')
    )
    name = models.CharField(blank=True, max_length=254)
    category = models.CharField(max_length=3, choices=CATEGORY_CHOICES)
    rating = models.IntegerField(blank=True, null=True)
    capacity = models.IntegerField(blank=True, null=True)
    availability =  models.CharField(max_length=254, blank=True)
    cost = models.CharField(max_length=254)
    notes = models.CharField(blank=True, max_length=100)
    description = models.TextField(blank=True)

    def __unicode__(self):
        return self.name

class Bioware_grade(models.Model):
    name = models.CharField(max_length=254)
    essence = models.DecimalField(max_digits=4, decimal_places=2)
    cost = models.DecimalField(max_digits=4, decimal_places=2)
    availability = models.CharField(max_length=254)


class Bioware(BaseModel):
    CATEGORY_CHOICES = (
        ('BA', 'Basic'),
        ('OR', 'Orthoskin Upgrades'),
        ('CU', 'Cultured'),
        ('SY', 'Symbionts'),
        ('GE', 'Genemods'),
        ('BI', 'Biosculpting'),
        ('CO', 'Cosmetic Bioware'),
        ('BW', 'Bio-Weapons')
    )

    name = models.CharField(max_length=254),
    category = models.CharField(max_length=3, choices=CATEGORY_CHOICES)
    rating = models.IntegerField(null=True)
    essence = models.CharField(max_length=254)
    capacity = models.IntegerField(max_length=2, default=0)
    avail = models.CharField(max_length=254)
    cost = models.CharField(max_length=254)

class Cyberware(BaseModel):
    CYBERWARE_CATEGORIES = (
        ('BW', 'Bodyware'),
        ('CE', 'Cosmetic Enhancement'),
        ('CL', 'Cyberlimb'),
        ('CA', 'Cyberlimb Accessory'),
        ('CE', 'Cyberlimb Enhancement'),
        ('EW', 'Earware'),
        ('EY', 'Eyeware'),
        ('HN', 'Hard Nanoware'),
        ('HW', 'Headware'),
        ('NC', 'Nanocybernetics')
    )
    name = models.CharField(max_length=254),
    category = models.CharField(max_length=3, choices=CYBERWARE_CATEGORIES)
    rating = models.IntegerField(null=True)
    essence = models.CharField(max_length=254)
    capacity = models.IntegerField()
    availability = models.CharField()
    cost = models.CharField()
    bonus = models.CharField()


class GearWeaponBonus(models.Model):
    damage = models.IntegerField(null=True)
    armor_piercing = models.IntegerField(null=True)
    damage_type = models.CharField(max_length=254, null=True)

#What about ammo? Gear-classes?
class Gear(BaseModel):
    CATEGORY_CHOICES = (
        ('Ammunition'),
        ('Armor Enhancements'),
        ('Audio Devices'),
        ('Audio Enhancements'),
        ('Biotech'),
        ('Breaking and Entering Gear'),
        ('BTLs'),
        ('Chemicals'),
        ('Commlinks'),
        ('Commlink Accessories'),
        ('Common Programs'),
        ('Communications and Countermeasures'),
        ('Custom'),
        ('Cyberdeck Modules'),
        ('Cyberdecks'),
        ('Disguises'),
        ('DocWagon Contract'),
        ('Drugs'),
        ('Electronics Accessories'),
        ('Electronic Modification'),
        ('Electronic Parts'),
        ('Entertainment'),
        ('Explosives'),
        ('Extraction Devices'),
        ('Foci'),
        ('Food'),
        ('Formulae'),
        ('Grapple Gun'),
        ('Hacking Programs'),
        ('Housewares'),
        ('ID / Credsticks'),
        ('Magical Compounds'),
        ('Magical Supplies'),
        ('Miscellany'),
        ('Nanogear'),
        ('PI - Tac'),
        ('RFID Tags'),
        ('Rigger Command Consoles'),
        ('Security Devices'),
        ('Sensors'),
        ('Sensor Functions'),
        ('Sensor Housings'),
        ('Services'),
        ('Software'),
        ('Skillsofts'),
        ('Survival Gear'),
        ('Tools'),
        ('Tools of the Trade'),
        ('Toxins'),
        ('Vision Devices'),
        ('Vision Enhancements')
    )

    name = models.CharField(blank=True, max_length=100)
    category = models.CharField(max_length=254, choices=CATEGORY_CHOICES)
    rating = models.IntegerField(blank=True, null=True)
    availability = models.CharField(max_length=254)
    addweapon = models.CharField(max_length=254, null=True)
    weapon_bonus = models.ForeignKey(GearWeaponBonus)
    bonus = models.CharField(max_length=254, null=True)
    costfor = models.CharField(max_length=254, null=True)
    cost = models.CharField(max_length=254)
    description = models.TextField(blank=True, null=True)

    def __unicode__(self):
        return self.name

# Create your models here.
class Character_attribute(models.Model):
    name = models.ForeignKey(Attribute)
    rank = models.IntegerField()

class Character_skill(models.Model):
    skill = models.ForeignKey(Skill)
    rank = models.IntegerField()

class Personal_Data(models.Model):
    name = models.CharField(max_length=255)
    primary_alias = models.CharField(max_length=255)
    metatype = models.CharField(max_length=255)
    ethnicity = models.CharField(max_length=255)
    age = models.IntegerField()
    sex = models.CharField(max_length=255)
    height = models.IntegerField() #cm
    weight = models.IntegerField() #kg
    #street_cred =
    #notoriety
    #public_awareness
    karma = models.IntegerField()
    total_karma = models.IntegerField()
    miscellaneous = models.TextField()

    def __unicode__(self):
        return self.name

class Character(models.Model):
    personal_data = models.ForeignKey(Personal_Data)
    attributes = models.ManyToManyField(Character_attribute)
    skills = models.ManyToManyField(Character_skill)


#class Archetypes(models.Model):
