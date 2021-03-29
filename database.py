#from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from marshmallow import fields
#from marshmallow_sqlalchemy.fields import Nested

db = SQLAlchemy()
ma = Marshmallow()


def create_app(app):
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://db/brew_project'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)
    ma.init_app(app)


class Malt(db.Model):
    malt_id = db.Column(db.Integer, primary_key=True)
    malt_name = db.Column(db.String(45), nullable=False)
    malt_origin = db.Column(db.String(16), nullable=True)
    malt_category = db.Column(db.String(16), nullable=True)
    malt_type = db.Column(db.String(16), nullable=False)
    malt_lovibond = db.Column(db.Integer, nullable=False)
    malt_ppg = db.Column(db.Float, nullable=False)

    malt_ingredients = db.relationship('MaltIngredient', backref=db.backref('malt', lazy=True))

    def __init__(self, malt_name, malt_origin, malt_category, malt_type, malt_lovibond, malt_ppg):
        self.malt_name = malt_name
        self.malt_origin = malt_origin
        self.malt_category = malt_category
        self.malt_type = malt_type
        self.malt_lovibond = malt_lovibond
        self.malt_ppg = malt_ppg

    def __str__(self):
        return self.malt_name


class Hops(db.Model):
    hops_id = db.Column(db.Integer, primary_key=True)
    hops_variety = db.Column(db.String(45), nullable=False)
    hops_type = db.Column(db.String(10), nullable=False)
    hops_aa = db.Column(db.Float, nullable=False)
    hops_use = db.Column(db.String(10), nullable=True)

    hops_ingredients = db.relationship('HopsIngredient', backref=db.backref('hops', lazy=True))

    def __init__(self, hops_variety, hops_type, hops_aa, hops_use):
        self.hops_variety = hops_variety
        self.hops_type = hops_type
        self.hops_aa = hops_aa
        self.hops_use = hops_use


class Yeast(db.Model):
    yeast_id = db.Column(db.Integer, primary_key=True)
    yeast_strain = db.Column(db.String(45), nullable=False)
    yeast_lab = db.Column(db.String(16), nullable=False)
    yeast_code = db.Column(db.String(16), nullable=True)
    yeast_type = db.Column(db.String(16), nullable=False)
    yeast_floc = db.Column(db.String(16), nullable=False)
    yeast_atten = db.Column(db.Float, nullable=False)
    yeast_min_temp = db.Column(db.Float, nullable=False)
    yeast_max_temp = db.Column(db.Float, nullable=False)

    yeast_ingredients = db.relationship('YeastIngredient', backref=db.backref('yeast', lazy=True))

    def __init__(self, yeast_strain, yeast_lab, yeast_code, yeast_type, yeast_floc, yeast_atten, yeast_min_temp,
                 yeast_max_temp):
        self.yeast_strain = yeast_strain
        self.yeast_lab = yeast_lab
        self.yeast_code = yeast_code
        self.yeast_type = yeast_type
        self.yeast_floc = yeast_floc
        self.yeast_atten = yeast_atten
        self.yeast_min_temp = yeast_min_temp
        self.yeast_max_temp = yeast_max_temp


class Other(db.Model):
    other_id = db.Column(db.Integer, primary_key=True)
    other_name = db.Column(db.String(45), nullable=False)
    other_type = db.Column(db.String(10), nullable=False)
    other_use = db.Column(db.String(10), nullable=False)

    other_ingredients = db.relationship('OtherIngredient', backref=db.backref('other', lazy=True))

    def __init__(self, other_name, other_type, other_use):
        self.other_name = other_name
        self.other_type = other_type
        self.other_use = other_use


class MaltIngredient(db.Model):
    malt_ingred_id = db.Column(db.Integer, primary_key=True)
    malt_ingred_qty = db.Column(db.Integer, nullable=False)
    malt_id = db.Column(db.Integer, db.ForeignKey('malt.malt_id'), nullable=False)
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipe.recipe_id'), nullable=False)
    db.ForeignKeyConstraint(['malt_id', 'recipe_id'], ['malt.malt_id', 'recipe.recipe_id'])

    def __init__(self, malt_ingred_qty, malt_id, recipe_id):
        self.malt_id = malt_id
        self.recipe_id = recipe_id
        self.malt_ingred_qty = malt_ingred_qty


class HopsIngredient(db.Model):
    hops_ingred_id = db.Column(db.Integer, primary_key=True)
    hops_ingred_qty = db.Column(db.Integer, nullable=False)
    hops_time = db.Column(db.Integer, nullable=False)
    hops_id = db.Column(db.Integer, db.ForeignKey('hops.hops_id'), nullable=False)
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipe.recipe_id'), nullable=False)
    db.ForeignKeyConstraint(['hops_id', 'recipe_id'], ['hops.hops_id', 'recipe.recipe_id'])

    def __init__(self, hops_ingred_qty, hops_time, hops_id, recipe_id):
        self.hops_ingred_qty = hops_ingred_qty
        self.hops_time = hops_time
        self.hops_id = hops_id
        self.recipe_id = recipe_id


class YeastIngredient(db.Model):
    yeast_ingred_id = db.Column(db.Integer, primary_key=True)
    yeast_ingred_qty = db.Column(db.Integer, nullable=False)
    yeast_ingred_starter = db.Column(db.String(10), nullable=False)
    yeast_id = db.Column(db.Integer, db.ForeignKey('yeast.yeast_id'), nullable=False)
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipe.recipe_id'), nullable=False)
    db.ForeignKeyConstraint(['yeast_id', 'recipe_id'], ['yeast.yeast_id', 'recipe.recipe_id'])

    def __init__(self, yeast_ingred_qty, yeast_ingred_starter, yeast_id, recipe_id):
        self.yeast_ingred_qty = yeast_ingred_qty
        self.yeast_ingred_starter = yeast_ingred_starter
        self.yeast_id = yeast_id
        self.recipe_id = recipe_id


class OtherIngredient(db.Model):
    other_ingred_id = db.Column(db.Integer, primary_key=True)
    other_ingred_qty = db.Column(db.Integer, nullable=False)
    other_id = db.Column(db.Integer, db.ForeignKey('other.other_id'), nullable=False)
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipe.recipe_id'), nullable=False)
    db.ForeignKeyConstraint(['other_id', 'recipe_id'], ['other.other_id', 'recipe.recipe_id'])

    def __init__(self, other_ingred_qty, other_id, recipe_id):
        self.other_ingred_qty = other_ingred_qty
        self.other_id = other_id
        self.recipe_id = recipe_id


class Image(db.Model):
    image_id = db.Column(db.Integer, primary_key=True)
    image_description = db.Column(db.String(45), nullable=False)
    image_url = db.Column(db.String(10), nullable=False)

    styles = db.relationship('Style', backref=db.backref('image', lazy=True))
    recipes = db.relationship('Recipe', backref=db.backref('image', lazy=True))

    def __init__(self, image_id, image_description, image_url):
        self.image_id = image_id
        self.image_description = image_description
        self.image_url = image_url


class Style(db.Model):
    style_id = db.Column(db.Integer, primary_key=True)
    style_name = db.Column(db.String(45), nullable=False)
    style_category = db.Column(db.String(45), nullable=False)
    style_bjcp = db.Column(db.String(5), nullable=True)
    style_min_ibu = db.Column(db.Integer, nullable=False)
    style_max_ibu = db.Column(db.Integer, nullable=False)
    style_min_abv = db.Column(db.Integer, nullable=False)
    style_max_abv = db.Column(db.Integer, nullable=False)
    style_min_fg = db.Column(db.Float, nullable=False)
    style_max_fg = db.Column(db.Float, nullable=False)
    style_min_co2_vol = db.Column(db.Float, nullable=False)
    style_max_co2_vol = db.Column(db.Float, nullable=False)
    style_lovibond = db.Column(db.Float, nullable=False)

    image_id = db.Column(db.Integer, db.ForeignKey('image.image_id'), nullable=False)

    recipes = db.relationship('Recipe', backref=db.backref('style', lazy=True))

    def __init__(self, style_name, style_category, style_bjcp, style_min_ibu, style_max_ibu, style_min_abv,
                 style_max_abv, style_min_fg, style_max_fg, style_min_co2_vol, style_max_co2_vol, style_lovibond,
                 image_id):
        self.style_name = style_name
        self.style_category = style_category
        self.style_bjcp = style_bjcp
        self.style_min_ibu = style_min_ibu
        self.style_max_ibu = style_max_ibu
        self.style_min_abv = style_min_abv
        self.style_max_abv = style_max_abv
        self.style_min_fg = style_min_fg
        self.style_max_fg = style_max_fg
        self.style_min_co2_vol = style_min_co2_vol
        self.style_max_co2_vol = style_max_co2_vol
        self.style_lovibond = style_lovibond
        self.image_id = image_id


class Notes(db.Model):
    notes_id = db.Column(db.Integer, primary_key=True)
    notes_body = db.Column(db.String(45), nullable=False)
    notes_created = db.Column(db.DateTime, server_default=db.func.now())

    recipes = db.relationship('Recipe', backref=db.backref('note', lazy=True))

    def __init__(self, notes_id, notes_body):
        self.notes_id = notes_id
        self.notes_body = notes_body


class Recipe(db.Model):
    recipe_id = db.Column(db.Integer, primary_key=True)
    recipe_name = db.Column(db.String(45), nullable=False)
    recipe_method = db.Column(db.String(16), nullable=False)
    recipe_batch_size = db.Column(db.Integer, nullable=False)
    recipe_rating = db.Column(db.Integer, nullable=False)
    recipe_created = db.Column(db.DateTime, server_default=db.func.now())
    recipe_description = db.Column(db.String(255), nullable=False)
    style_id = db.Column(db.Integer, db.ForeignKey('style.style_id'), nullable=False)
    image_id = db.Column(db.Integer, db.ForeignKey('image.image_id'), nullable=False)
    notes_id = db.Column(db.Integer, db.ForeignKey('notes.notes_id'), nullable=False)

    malt_ingredients = db.relationship('MaltIngredient', backref=db.backref('recipe', uselist=False, lazy=True))
    hops_ingredients = db.relationship('HopsIngredient', backref=db.backref('recipe', uselist=False, lazy=True))
    yeast_ingredients = db.relationship('YeastIngredient', backref=db.backref('recipe', uselist=False, lazy=True))
    other_ingredients = db.relationship('OtherIngredient', backref=db.backref('recipe', uselist=False, lazy=True))
    sessions = db.relationship('Session', backref=db.backref('recipe', lazy=True))
    steps = db.relationship('Step', backref=db.backref('recipe', lazy=True))
    db.ForeignKeyConstraint(['style_id', 'image_id', 'notes_id'], ['style.style_id', 'image.image_id', 'notes.notes_id'])

    def __init__(self, recipe_name, recipe_method, recipe_srm, recipe_batch_size, recipe_rating,
                 recipe_description, style_id, image_id):
        self.recipe_name = recipe_name
        self.recipe_method = recipe_method
        self.recipe_srm = recipe_srm
        self.recipe_batch_size = recipe_batch_size
        self.recipe_rating = recipe_rating
        self.recipe_description = recipe_description
        self.style_id = style_id
        self.image_id = image_id


class Session(db.Model):
    session_id = db.Column(db.Integer, primary_key=True)
    session_name = db.Column(db.String(45), nullable=True)
    session_start = db.Column(db.DateTime, nullable=True)
    session_end = db.Column(db.DateTime, nullable=True)
    session_created = db.Column(db.DateTime, server_default=db.func.now())
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipe.recipe_id'), nullable=True)
    session_step_id = db.Column(db.Integer, db.ForeignKey('session_step.session_step_id'), nullable=True)
    db.ForeignKeyConstraint(['recipe_id', 'session_step_id'], ['recipe.recipe_id', 'session_step.session_step_id'])

    def __init__(self, session_id, session_step, session_start, session_end, recipe_id=None, session_step_id=None):
        self.session_id = session_id
        self.session_step = session_step
        self.session_start = session_start
        self.session_end = session_end
        self.recipe_id = recipe_id
        self.session_step_id = session_step_id


class Temps(db.Model):
    temp_id = db.Column(db.Integer, primary_key=True)
    temp_hlt = db.Column(db.Float, nullable=False)
    temp_mlt = db.Column(db.Float, nullable=False)
    temp_bk = db.Column(db.Float, nullable=False)
    temp_created = db.Column(db.DateTime, server_default=db.func.now())
    session_id = db.Column(db.Integer, db.ForeignKey('session.session_id'), nullable=False)

    def __init__(self, temp_hlt, temp_mlt, temp_bk, session_id):
        self.temp_hlt = temp_hlt
        self.temp_mlt = temp_mlt
        self.temp_bk = temp_bk
        self.session_id = session_id


class Step(db.Model):
    step_id = db.Column(db.Integer, primary_key=True)
    step_name = db.Column(db.String(45), nullable=True)
    step_kettle = db.Column(db.String(45), nullable=True)
    step_action = db.Column(db.String(45), nullable=True)
    step_temp = db.Column(db.Float, nullable=False)
    step_timer = db.Column(db.Integer, nullable=False)
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipe.recipe_id'), nullable=False)

    def __init__(self, step_name, step_kettle, step_temp, step_timer, recipe_id):
        self.step_name = step_name
        self.step_kettle = step_kettle
        self.step_temp = step_temp
        self.step_timer = step_timer
        self.recipe_id = recipe_id


class SessionStep(db.Model):
    session_step_id = db.Column(db.Integer, primary_key=True)
    session_step_start = db.Column(db.DateTime, nullable=False)
    session_step_end = db.Column(db.DateTime, nullable=False)
    step_id = db.Column(db.Integer, db.ForeignKey('step.step_id'), nullable=False)
    session_id = db.Column(db.Integer, db.ForeignKey('session.session_id'), nullable=False)
    db.ForeignKeyConstraint(['step_id', 'session_id'], ['step.step_id', 'session.session_id'])

    def __init__(self, session_step_start, session_step_end, step_id, session_id):
        self.step_id = step_id
        self.session_id = session_id
        self.session_step_start = session_step_start
        self.session_step_end = session_step_end


# Marshmallow Schemas
class MaltSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Malt


class HopsSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Hops


class YeastSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Yeast


class OtherSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Other


class MaltIngredientSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = MaltIngredient
    malt = Nested(MaltSchema)


class HopsIngredientSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = HopsIngredient
    hops = Nested(HopsSchema)


class YeastIngredientSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = YeastIngredient
    yeast = Nested(YeastSchema)


class OtherIngredientSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = OtherIngredient
    other = Nested(OtherSchema)


class StyleSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Style
        include_fk = True


class ImageSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Image


class NotesSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Notes


class TempsSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Temps


class StepSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Step


class SessionStepSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = SessionStep


class SessionSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Session
    sessions_steps = fields.List(Nested(SessionStepSchema))


class RecipeSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Recipe
    malt_ingredients = fields.List(Nested(MaltIngredientSchema))
    hops_ingredients = fields.List(Nested(HopsIngredientSchema))
    yeast_ingredients = fields.List(Nested(YeastIngredientSchema))
    other_ingredients = fields.List(Nested(OtherIngredientSchema))
    sessions = fields.List(Nested(SessionSchema))
    steps = fields.List(Nested(StepSchema))
