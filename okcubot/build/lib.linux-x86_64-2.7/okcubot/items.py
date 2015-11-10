# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field

class UserItem(Item):
    # Details
    d_username = Field()
    d_age = Field()
    d_gender = Field()
    d_city = Field()
    d_country = Field()
    d_orientation = Field()
    d_ethnicity = Field()
    d_bodytype = Field()
    d_diet_manner = Field()
    d_diet_type = Field()
    d_smokes = Field()
    d_drinks = Field()
    d_drugs = Field()
    # Fiction section
    d_religion_type = Field()
    d_religion_seriosity = Field()
    d_astrology_sign = Field()
    d_astrology_seriosity = Field()
    d_education_phase = Field()
    d_education_type = Field()
    d_job = Field()
    d_income = Field()
    d_relationship = Field()
    d_relationship_manner = Field()
    d_relationship_type = Field()
    d_offspring_current = Field()
    d_offspring_desires = Field()
    d_pets_dogs = Field()
    d_pets_cats = Field()
    d_languages = Field()
    # Looking for
    lf_want = Field()
    lf_min_age = Field()
    lf_max_age = Field()
    lf_location = Field()
    lf_single = Field()
    lf_for = Field()
    # Personality scale
    p_explove = Field() # Experienced in Love
    p_adven = Field() # Adventurous
    p_indie = Field() # Indie
    p_spon = Field() # Spontaneous
    p_scien = Field() # Scientific
    p_inde = Field() # Independent
    p_conf = Field() # Confident
    p_math = Field() # Mathematical
    p_logic = Field() # Logical
    p_organ = Field() # Organized
    p_oldfash = Field() # Old-Fashioned
    p_lit = Field() # Literary
    p_opti = Field() # Optimistic
    p_roman = Field() # Romantic
    p_comp = Field() # Compassionate
    p_lovedri = Field() # Love-driven
    p_sprit = Field() # Spiritual
    p_kinky = Field() # Kinky
    p_artsy = Field() # Artsy
    p_thrift = Field() # Thrifty
    p_drug = Field() # Drug-friendly
    p_arro = Field() # Arrogant
    p_sloppy = Field() # Sloppy
    p_extro = Field() # Extroverted
    p_geeky = Field() # Geeky
    p_aggre = Field() # Aggressive
    p_expsex = Field() # Experienced in sex
    p_capi = Field() # Capitalistic
    p_exer = Field() # Into Exercise
    p_kind = Field() # Kind
    p_pure = Field() # Pure
    p_convenmoral = Field() # Conventionally Moral
    p_manners = Field() # Mannered
    p_ambi = Field() # Ambitious
    p_polit = Field() # Political
    p_greed = Field() # Greedy
    p_sexdrive = Field() # Sex-driven
    p_energetic = Field() # Energetic
    p_cool = Field() # Cool
    p_introvert = Field() # Introverted
    p_trusting = Field() # Trusting
    p_dominant = Field() # Dominant
    p_laidback = Field() # Laid-back
    p_submissive = Field() # Submissive
    p_explife = Field() # Experienced in life
    p_friendstrangers = Field() # Fiendly to strangers
    p_honest = Field() # Honest
    p_giving = Field() # Giving 
    p_passion = Field() # Passion-driven
    p_progress = Field() # Progressive
    # Misc
    m_photocount = Field()

class QuestionItem(Item):
    id = Field()
    text = Field()
    # The text of the options
    option_1 = Field()
    option_2 = Field()
    option_3 = Field()
    option_4 = Field()

class AnswerItem(Item):
    # User who answered
    author = Field()
    # Question ID
    question = Field()
    # Value between 1-4
    answer = Field()
    # Answer text (if any)
    answer_text = Field()
